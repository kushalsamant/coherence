"""
Job generation routes
Upload sketches, check status, download results
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks, Request, Form
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from loguru import logger
import time

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database.sketch2bim import get_db
from auth.sketch2bim import get_current_user, require_active_subscription
from models.sketch2bim import User, Job
from models.sketch2bim_schemas import (
    UploadResponse,
    BatchUploadResponse,
    JobResponse,
    JobStatusResponse,
    BatchJobResponse,
    PlanData,
    SymbolSummary,
)
from utils.sketch2bim.exceptions import ValidationError, NotFoundError, RateLimitError, ProcessingError
from utils.sketch2bim import (
    generate_job_id, is_allowed_file, get_file_extension,
    check_rate_limit, log_job_event, sanitize_filename, validate_upload_file,
    upload_bytes_to_bunny, generate_temp_path, download_from_bunny,
    download_checkpoint, get_checkpoint_remote_path
)
from utils.sketch2bim.audit import log_audit_event
from services.sketch2bim.metrics import record_api_request
from config.sketch2bim import settings

router = APIRouter(prefix="/generate", tags=["generate"])


# Temporary upload directory
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Output directory
OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def _build_symbol_summary(plan_data: Optional[Dict[str, Any]]) -> Optional[SymbolSummary]:
    if not plan_data:
        return None
    symbols = plan_data.get("symbols") or []
    metadata = plan_data.get("symbol_metadata") or {}
    enabled = metadata.get("enabled", bool(symbols))
    if not symbols and not enabled:
        return None

    categories: Dict[str, int] = {}
    label_counts: Dict[str, int] = {}
    for symbol in symbols:
        category = symbol.get("category") or "uncategorized"
        categories[category] = categories.get(category, 0) + 1
        label = symbol.get("label") or symbol.get("display_name") or category
        label_counts[label] = label_counts.get(label, 0) + 1

    sample_labels = sorted(label_counts.keys(), key=lambda k: label_counts[k], reverse=True)[:5]

    return SymbolSummary(
        total_detected=len(symbols),
        categories=categories,
        sample_labels=sample_labels,
        enabled=bool(enabled),
        inference_ms=metadata.get("inference_ms"),
        model_path=metadata.get("model_path"),
    )


def _job_to_response(job: Job) -> JobResponse:
    response = JobResponse.from_orm(job)
    response.symbol_summary = _build_symbol_summary(job.plan_data)
    return response


def process_sketch_task(user_id: int, sketch_path: str, job_id: str, project_type: str = "architecture"):
    """
    Process uploaded sketch and generate IFC file
    This function runs in background using FastAPI BackgroundTasks
    
    Args:
        user_id: User ID
        sketch_path: Path to uploaded sketch
        job_id: Job ID
        project_type: Project type (architecture only)
    """
    # Create new database session for background task
    from database.sketch2bim import SessionLocal
    db = SessionLocal()
    
    try:
        # Get job
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            logger.error(f"Job {job_id} not found")
            return
        
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User {user_id} not found")
            job.status = "failed"
            job.error_message = "User not found"
            db.commit()
            return
        
        # Update job status
        job.status = "processing"
        job.started_at = datetime.utcnow()
        job.progress = 10
        db.commit()
        
        log_job_event(job_id, "processing_started", {})
        
        # Ensure sketch file is available locally (download from BunnyCDN if needed)
        sketch_path_obj = Path(sketch_path)
        if not sketch_path_obj.exists():
            # Local file doesn't exist, try to download from BunnyCDN
            if job.sketch_url:
                logger.info(f"Local sketch file not found, downloading from BunnyCDN: {job.sketch_url}")
                # Extract remote path from URL
                from urllib.parse import urlparse
                parsed_url = urlparse(job.sketch_url)
                remote_path = parsed_url.path.lstrip('/')  # Remove leading slash
                
                # Ensure local directory exists
                sketch_path_obj.parent.mkdir(parents=True, exist_ok=True)
                
                # Download from BunnyCDN
                if download_from_bunny(remote_path, str(sketch_path_obj)):
                    logger.info(f"Successfully downloaded sketch from BunnyCDN to {sketch_path}")
                else:
                    raise ProcessingError(
                        f"Failed to download sketch from BunnyCDN: {job.sketch_url}",
                        job_id=job_id
                    )
            else:
                raise ProcessingError(
                    f"Sketch file not found locally and no sketch_url available: {sketch_path}",
                    job_id=job_id
                )
        else:
            logger.info(f"Using local sketch file: {sketch_path}")
        
        # Create output directory
        output_dir = OUTPUT_DIR / job_id
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check for existing checkpoints (resume logic)
        checkpoints_available = {}
        if job.plan_data and isinstance(job.plan_data, dict):
            metadata = job.plan_data.get("_metadata", {})
            checkpoints = metadata.get("checkpoints", {})
            if checkpoints:
                logger.info(f"Found existing checkpoints for job {job_id}: {list(checkpoints.keys())}")
                # Download checkpoints to local output directory
                for checkpoint_type, checkpoint_url in checkpoints.items():
                    remote_path = get_checkpoint_remote_path(job_id, checkpoint_type)
                    if remote_path:
                        # Determine local path based on checkpoint type
                        checkpoint_filenames = {
                            "ifc": f"{job_id}.ifc",
                            "dwg": f"{job_id}.dwg",
                            "obj": f"{job_id}.obj",
                            "rvt": f"{job_id}.rvt.ifc",
                            "preview": f"{job_id}_preview.png"
                        }
                        local_filename = checkpoint_filenames.get(checkpoint_type)
                        if local_filename:
                            local_path = output_dir / local_filename
                            if download_checkpoint(job_id, checkpoint_type, str(local_path)):
                                checkpoints_available[checkpoint_type] = str(local_path)
                                logger.info(f"Downloaded checkpoint: {checkpoint_type} -> {local_path}")
        
        # Update progress
        job.progress = 20
        db.commit()
        
        # Import here to avoid circular imports
        from ai.model_generator import generate_model
        from utils.sketch2bim import (
            upload_to_bunny,
            create_signed_bunny_url,
            generate_remote_path
        )
        from utils.sketch2bim.costing import calculate_job_cost
        from services.sketch2bim.metrics import record_job
        
        # Get project_type from job
        project_type = job.project_type or "architecture"
        
        # Generate model (will use checkpoints if available to skip steps)
        logger.info(f"Generating model for job {job_id} (project_type: {project_type})")
        if checkpoints_available:
            logger.info(f"Resuming from checkpoints: {list(checkpoints_available.keys())}")
        log_job_event(job_id, "generating_model", {"project_type": project_type, "checkpoints": list(checkpoints_available.keys())})
        
        try:
        result = generate_model(str(sketch_path), str(output_dir), job_id, project_type=project_type, checkpoints=checkpoints_available)
        except Exception as e:
            logger.error(f"Model generation exception for job {job_id}: {e}", exc_info=True)
            raise ProcessingError(
                f"Model generation failed: {str(e)}",
                job_id=job_id,
                details={"error_type": type(e).__name__}
            )
        
        if not result["success"]:
            error_msg = result.get("error", "Model generation failed")
            raise ProcessingError(
                error_msg,
                job_id=job_id,
                details={"result": result}
            )
        
        # Store plan data
        plan_data_dict = result["plan_data"] if isinstance(result["plan_data"], dict) else {}
        
        # Store checkpoint URLs in plan_data metadata
        checkpoints = {}
        if result.get("ifc_checkpoint_url"):
            checkpoints["ifc"] = result["ifc_checkpoint_url"]
        if result.get("dwg_checkpoint_url"):
            checkpoints["dwg"] = result["dwg_checkpoint_url"]
        if result.get("obj_checkpoint_url"):
            checkpoints["obj"] = result["obj_checkpoint_url"]
        if result.get("rvt_checkpoint_url"):
            checkpoints["rvt"] = result["rvt_checkpoint_url"]
        if result.get("preview_checkpoint_url"):
            checkpoints["preview"] = result["preview_checkpoint_url"]
        
        if checkpoints:
            if "_metadata" not in plan_data_dict:
                plan_data_dict["_metadata"] = {}
            plan_data_dict["_metadata"]["checkpoints"] = checkpoints
        
        job.plan_data = plan_data_dict
        job.detection_confidence = result["confidence"]
        
        # Store legend data if available
        if result.get("legend_data"):
            job.legend_data = result["legend_data"]
            job.legend_detected = result["legend_data"].get("confidence", 0) > 0.3
        
        # Store QC report if available
        if result.get("qc_report_path"):
            job.qc_report_path = result["qc_report_path"]
        
        # Check if review is needed
        if result.get("requires_review") or result.get("confidence", 0) < 50.0:
            job.status = "review"
            job.requires_review = True
            log_job_event(job_id, "requires_review", {
                "confidence": result.get("confidence", 0),
                "qc_score": result.get("qc_report", {}).get("confidence_score", 0) if result.get("qc_report") else 0
            })
        else:
            job.requires_review = False
        
        job.progress = 60
        db.commit()  # Save checkpoints to database immediately
        
        # Upload files to CDN
        logger.info(f"Uploading files to CDN for job {job_id}")
        log_job_event(job_id, "uploading_files", {})
        
        # Upload IFC
        if result["ifc_path"] and Path(result["ifc_path"]).exists():
            remote_path = generate_remote_path(job_id, f"{job_id}.ifc")
            ifc_url = upload_to_bunny(result["ifc_path"], remote_path)
            job.ifc_url = create_signed_bunny_url(ifc_url)
            logger.info(f"IFC uploaded: {job.ifc_url}")
        
        job.progress = 70
        db.commit()
        
        # Upload DWG if available
        if result.get("dwg_path") and Path(result["dwg_path"]).exists():
            remote_path = generate_remote_path(job_id, f"{job_id}.dwg")
            dwg_url = upload_to_bunny(result["dwg_path"], remote_path)
            job.dwg_url = create_signed_bunny_url(dwg_url)
            logger.info(f"DWG uploaded: {job.dwg_url}")
        
        job.progress = 80
        db.commit()
        
        # Upload RVT if available
        if result.get("rvt_path") and Path(result["rvt_path"]).exists():
            remote_path = generate_remote_path(job_id, f"{job_id}.rvt.ifc")
            rvt_url = upload_to_bunny(result["rvt_path"], remote_path)
            job.rvt_url = create_signed_bunny_url(rvt_url)
            logger.info(f"RVT uploaded: {job.rvt_url}")
        
        # Upload SketchUp (OBJ) if available
        if result.get("sketchup_path") and Path(result["sketchup_path"]).exists():
            remote_path = generate_remote_path(job_id, f"{job_id}.obj")
            sketchup_url = upload_to_bunny(result["sketchup_path"], remote_path)
            job.sketchup_url = create_signed_bunny_url(sketchup_url)
            logger.info(f"SketchUp/OBJ uploaded: {job.sketchup_url}")
        
        # Upload preview if available
        if result.get("preview_path") and Path(result["preview_path"]).exists():
            remote_path = generate_remote_path(job_id, f"{job_id}_preview.png")
            preview_url = upload_to_bunny(result["preview_path"], remote_path)
            job.preview_image_url = preview_url
            logger.info(f"Preview uploaded: {job.preview_image_url}")
        
        job.progress = 90
        db.commit()
        
        # Calculate and store cost
        processing_duration = (datetime.utcnow() - job.started_at).total_seconds() if job.started_at else 0
        file_size = Path(result["ifc_path"]).stat().st_size if result.get("ifc_path") and Path(result["ifc_path"]).exists() else 0
        
        cost_breakdown = calculate_job_cost(
            processing_duration=processing_duration,
            file_size_bytes=file_size,
            gpu_type="cpu",  # Using CPU for pure Python processing
            storage_days=7
        )
        job.cost_usd = cost_breakdown["total"]
        
        # Set expiration
        job.expires_at = datetime.utcnow() + timedelta(days=7)
        
        # Mark as completed (unless it requires review)
        if job.status != "review":
            job.status = "completed"
        job.completed_at = datetime.utcnow()
        job.progress = 100
        db.commit()
        
        log_job_event(job_id, "completed", {
            "confidence": result["confidence"],
            "files_generated": [k for k, v in result.items() if v and k.endswith("_path")]
        })
        
        # Record metrics
        duration = (datetime.utcnow() - job.started_at).total_seconds() if job.started_at else 0
        record_job(
            status="completed",
            duration=duration,
            cost=job.cost_usd,
            user_tier=user.subscription_tier
        )
        
        # Users download files from dashboard (no email needed)
        
        # Cleanup local files and temp checkpoints from BunnyCDN
        cleanup_local_files(sketch_path, output_dir)
        cleanup_temp_checkpoints(job_id, job.plan_data)
        
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        # Handle failure
        error_msg = str(e)
        logger.error(f"Job {job_id} failed: {error_msg}", exc_info=True)
        log_job_event(job_id, "failed", {"error": error_msg})
        
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = "failed"
            job.error_message = error_msg
            job.completed_at = datetime.utcnow()
            
            db.commit()
            
            # Users can check dashboard for job status (no email needed)
            
            # Record metrics
            from ..monitoring.metrics import record_job
            duration = (datetime.utcnow() - job.started_at).total_seconds() if job.started_at else 0
            record_job(
                status="failed",
                duration=duration,
                cost=0.0,
                user_tier=user.subscription_tier if user else "unknown"
            )
    finally:
        db.close()


def cleanup_local_files(sketch_path: str, output_dir: Path):
    """Clean up temporary local files"""
    try:
        # Remove sketch
        if Path(sketch_path).exists():
            Path(sketch_path).unlink()
        
        # Remove output directory
        if output_dir.exists():
            shutil.rmtree(output_dir)
        
        logger.info(f"Cleaned up local files: {sketch_path}, {output_dir}")
    except Exception as e:
        logger.warning(f"Cleanup warning: {e}")


def cleanup_temp_checkpoints(job_id: str, plan_data: Optional[Dict[str, Any]]):
    """Clean up temporary checkpoint files from BunnyCDN after job completion"""
    from utils.sketch2bim import delete_from_bunny, get_checkpoint_remote_path
    
    if not plan_data or not isinstance(plan_data, dict):
        return
    
    metadata = plan_data.get("_metadata", {})
    checkpoints = metadata.get("checkpoints", {})
    
    if not checkpoints:
        return
    
    logger.info(f"Cleaning up temp checkpoints for job {job_id}: {list(checkpoints.keys())}")
    
    # Delete each checkpoint file from BunnyCDN
    checkpoint_types = ["ifc", "dwg", "obj", "rvt", "preview"]
    for checkpoint_type in checkpoint_types:
        if checkpoint_type in checkpoints:
            try:
                remote_path = get_checkpoint_remote_path(job_id, checkpoint_type)
                if remote_path:
                    if delete_from_bunny(remote_path):
                        logger.info(f"Deleted checkpoint: {checkpoint_type}")
                    else:
                        logger.warning(f"Failed to delete checkpoint: {checkpoint_type}")
            except Exception as e:
                logger.warning(f"Error deleting checkpoint {checkpoint_type}: {e}")


@router.post("/upload", response_model=UploadResponse)
async def upload_sketch(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    project_type: str = Form("architecture"),
    user: User = Depends(require_active_subscription()),
    db: Session = Depends(get_db)
):
    """
    Upload a sketch and queue BIM generation job
    """
    # Validate project_type (only architecture supported)
    if project_type != "architecture":
        project_type = "architecture"
    
    # Sanitize filename
    sanitized_filename = sanitize_filename(file.filename or "sketch")
    
    # Validate file extension
    if not is_allowed_file(sanitized_filename):
        raise ValidationError(
            f"File type not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}",
            field="file"
        )
    
    # Check file size from header
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset
    
    if file_size > settings.max_upload_size_bytes:
        raise ValidationError(
            f"File too large. Max: {settings.MAX_UPLOAD_SIZE_MB}MB",
            field="file",
            details={"file_size": file_size, "max_size": settings.max_upload_size_bytes}
        )
    
    # Check rate limit
    if not await check_rate_limit(user.id):
        raise RateLimitError()
    
    # Generate job ID
    job_id = generate_job_id()
    
    # Read file content
    file.file.seek(0)
    file_content = await file.read()
    
    # Upload sketch directly to BunnyCDN temp storage
    temp_remote_path = generate_temp_path(job_id, sanitized_filename)
    try:
        sketch_url = upload_bytes_to_bunny(file_content, temp_remote_path)
        logger.info(f"Uploaded sketch to BunnyCDN: {sketch_url}")
    except Exception as e:
        logger.error(f"Failed to upload sketch to BunnyCDN: {e}")
        raise ValidationError(
            f"Failed to upload file to storage: {str(e)}",
            field="file"
        )
    
    # Also save locally as fallback (for immediate processing)
    job_upload_dir = UPLOAD_DIR / job_id
    job_upload_dir.mkdir(exist_ok=True)
    sketch_path = job_upload_dir / sanitized_filename
    with open(sketch_path, "wb") as buffer:
        buffer.write(file_content)
    
    # Create job record with sketch_url pointing to BunnyCDN
    job = Job(
        id=job_id,
        user_id=user.id,
        status="queued",
        sketch_filename=sanitized_filename,
        sketch_format=get_file_extension(sanitized_filename),
        project_type=project_type,
        sketch_url=sketch_url  # Store BunnyCDN URL for resumability
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # Queue job for processing
    log_job_event(job_id, "job_created", {
        "user_id": user.id,
        "filename": file.filename
    })
    
    # Audit log
    client_ip = request.client.host if request.client else None
    log_audit_event(
        user_id=user.id,
        action="create",
        resource_type="job",
        resource_id=job_id,
        details={"filename": file.filename},
        ip_address=client_ip
    )
    
    # Record API metrics
    start_time = time.time()
    record_api_request(
        method="POST",
        endpoint="/generate/upload",
        status_code=200,
        duration=time.time() - start_time
    )
    
    # Queue job for async processing with BackgroundTasks
    background_tasks.add_task(
        process_sketch_task,
        user.id,
        str(sketch_path),
        job_id,
        project_type
    )
    
    return UploadResponse(
        job_id=job_id,
        message="Sketch uploaded successfully. Processing started."
    )


@router.post("/batch-upload", response_model=BatchUploadResponse)
async def batch_upload_sketches(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    project_type: str = Form("architecture"),
    user: User = Depends(require_active_subscription()),
    db: Session = Depends(get_db)
):
    """
    Upload multiple sketches for batch processing
    
    All files in the batch will use the same project_type.
    Each file is processed as a separate job.
    Processing happens asynchronously in the background.
    
    Limitations:
    - Maximum file size per file: 50MB
    - All files must be valid image/PDF formats
    - Processing time varies per file
    - Requires active subscription (trial or paid tier)
    """
    # Validate project_type (only architecture supported)
    if project_type != "architecture":
        project_type = "architecture"
    
    total_files = len(files)
    
    # Validate all files first
    for file in files:
        if not is_allowed_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed: {file.filename}"
            )
    
    # Generate batch ID
    batch_id = generate_job_id()
    job_ids = []
    failed_files = []
    
    # Process each file with error handling
    for file in files:
        job_id = None
        try:
            job_id = generate_job_id()
            
            # Check file size
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset
            
            if file_size > settings.max_upload_size_bytes:
                failed_files.append({
                    "filename": file.filename,
                    "error": f"File too large. Max: {settings.MAX_UPLOAD_SIZE_MB}MB"
                })
                continue
            
            # Read file content
            file.file.seek(0)
            file_content = await file.read()
            
            sanitized_filename = sanitize_filename(file.filename or "sketch")
            
            # Upload sketch directly to BunnyCDN temp storage
            temp_remote_path = generate_temp_path(job_id, sanitized_filename)
            try:
                sketch_url = upload_bytes_to_bunny(file_content, temp_remote_path)
                logger.info(f"Uploaded batch sketch to BunnyCDN: {sketch_url}")
            except Exception as e:
                logger.error(f"Failed to upload batch sketch to BunnyCDN: {e}")
                failed_files.append({
                    "filename": file.filename,
                    "error": f"Failed to upload to storage: {str(e)}"
                })
                continue
            
            # Also save locally as fallback (for immediate processing)
            job_upload_dir = UPLOAD_DIR / job_id
            job_upload_dir.mkdir(exist_ok=True)
            sketch_path = job_upload_dir / sanitized_filename
            try:
                with open(sketch_path, "wb") as buffer:
                    buffer.write(file_content)
            except Exception as e:
                logger.warning(f"Failed to save local file {file.filename}: {e}, will download from BunnyCDN")
            
            # Create job with sketch_url pointing to BunnyCDN
            job = Job(
                id=job_id,
                user_id=user.id,
                status="queued",
                sketch_filename=sanitized_filename,
                sketch_format=get_file_extension(file.filename),
                project_type=project_type,
                sketch_url=sketch_url,  # Store BunnyCDN URL for resumability
                batch_id=batch_id  # Store batch_id on job
            )
            
            db.add(job)
            job_ids.append(job_id)
            
            # Queue job for processing with BackgroundTasks
            background_tasks.add_task(
                process_sketch_task,
                user.id,
                str(sketch_path),
                job_id,
                project_type
            )
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename} in batch: {e}", exc_info=True)
            failed_files.append({
                "filename": file.filename,
                "error": f"Processing error: {str(e)}"
            })
            # Cleanup if job was created but failed
            if job_id:
                try:
                    job_upload_dir = UPLOAD_DIR / job_id
                    if job_upload_dir.exists():
                        shutil.rmtree(job_upload_dir)
                except:
                    pass
    
    # Commit all successful jobs
    try:
        db.commit()
    except Exception as e:
        logger.error(f"Failed to commit batch jobs: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create batch jobs: {str(e)}"
        )
    
    # Log batch creation (including failures)
    log_job_event(batch_id, "batch_created", {
        "user_id": user.id,
        "total_jobs": total_files,
        "successful_jobs": len(job_ids),
        "failed_jobs": len(failed_files),
        "job_ids": job_ids,
        "failed_files": failed_files
    })
    
    # If all files failed, return error
    if len(job_ids) == 0:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "All files in batch failed to process",
                "failed_files": failed_files
            }
        )
    
    # Return response with success and failure info
    response = BatchUploadResponse(
        batch_id=batch_id,
        job_ids=job_ids,
        total_jobs=total_files
    )
    
    # Log warning if some files failed
    if failed_files:
        logger.warning(f"Batch {batch_id}: {len(failed_files)} files failed out of {total_files}")
    
    return response


@router.get("/status/{job_id}", response_model=JobStatusResponse)
def get_job_status(
    job_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get job processing status
    """
    # Validate job ID format
    from utils.sketch2bim import validate_job_id
    if not validate_job_id(job_id):
        raise ValidationError("Invalid job ID format", field="job_id")
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == user.id
    ).first()
    
    if not job:
        raise NotFoundError("Job", job_id)
    
    message = None
    if job.status == "queued":
        message = "Job is queued for processing"
    elif job.status == "processing":
        message = f"Processing... {job.progress}% complete"
    elif job.status == "completed":
        message = "Job completed successfully"
    elif job.status == "failed":
        message = "Job failed"
    
    return JobStatusResponse(
        id=job.id,
        status=job.status,
        progress=job.progress,
        message=message,
        error=job.error_message
    )


@router.get("/jobs", response_model=List[JobResponse])
def list_jobs(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0
):
    """
    List user's jobs
    """
    jobs = db.query(Job).filter(
        Job.user_id == user.id
    ).order_by(Job.created_at.desc()).limit(limit).offset(offset).all()
    
    return [_job_to_response(job) for job in jobs]


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(
    job_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed job information
    """
    # Validate job ID format
    from utils.sketch2bim import validate_job_id
    if not validate_job_id(job_id):
        raise ValidationError("Invalid job ID format", field="job_id")
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == user.id
    ).first()
    
    if not job:
        raise NotFoundError("Job", job_id)
    
    return _job_to_response(job)


@router.get("/jobs/{job_id}/plan-data", response_model=PlanData)
def get_job_plan_data(
    job_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve raw plan data (rooms, walls, symbols) for QA tools.
    """
    from utils.sketch2bim import validate_job_id
    if not validate_job_id(job_id):
        raise ValidationError("Invalid job ID format", field="job_id")

    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == user.id
    ).first()

    if not job:
        raise NotFoundError("Job", job_id)

    if not job.plan_data:
        raise HTTPException(status_code=404, detail="Plan data not available yet")

    return job.plan_data


@router.post("/review/{job_id}")
async def review_job(
    job_id: str,
    action: str,  # approve|reject
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Approve or reject a job that requires review
    
    Args:
        job_id: Job ID
        action: 'approve' or 'reject'
    """
    # Check if user is admin or job owner
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Only allow review if job is in review status
    if job.status != "review":
        raise HTTPException(
            status_code=400,
            detail=f"Job is not in review status (current: {job.status})"
        )
    
    # Check permissions (admin or job owner)
    is_admin = user.email.endswith("@sketch2bim.com")  # Simple admin check
    is_owner = job.user_id == user.id
    
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized to review this job")
    
    if action == "approve":
        job.status = "completed"
        job.requires_review = False
        log_job_event(job_id, "review_approved", {"reviewed_by": user.id})
    elif action == "reject":
        job.status = "failed"
        job.error_message = "Job rejected after review"
        log_job_event(job_id, "review_rejected", {"reviewed_by": user.id})
    else:
        raise HTTPException(status_code=400, detail="Action must be 'approve' or 'reject'")
    
    db.commit()
    
    return {
        "message": f"Job {action}d successfully",
        "job_id": job_id,
        "status": job.status
    }


@router.delete("/jobs/{job_id}")
def delete_job(
    job_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a job and its associated files
    """
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == user.id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Delete from CDN if exists
    if job.ifc_url:
        from utils.sketch2bim import delete_from_bunny
        # Extract remote path from URL
        # This is simplified - implement proper path extraction
        pass
    
    # Delete job record
    db.delete(job)
    db.commit()
    
    log_job_event(job_id, "job_deleted", {"user_id": user.id})
    
    return {"message": "Job deleted successfully"}


@router.get("/batch/{batch_id}", response_model=BatchJobResponse)
def get_batch_status(
    batch_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get status of all jobs in a batch
    """
    # Query all jobs in batch for this user
    jobs = db.query(Job).filter(
        Job.batch_id == batch_id,
        Job.user_id == user.id
    ).all()
    
    if not jobs:
        raise HTTPException(
            status_code=404,
            detail=f"Batch {batch_id} not found"
        )
    
    # Calculate statistics
    total_jobs = len(jobs)
    completed = sum(1 for j in jobs if j.status == "completed")
    failed = sum(1 for j in jobs if j.status == "failed")
    processing = sum(1 for j in jobs if j.status == "processing")
    queued = sum(1 for j in jobs if j.status == "queued")
    review = sum(1 for j in jobs if j.status == "review")
    
    # Convert jobs to JobResponse
    job_responses = [
        JobResponse(
            id=job.id,
            status=job.status,
            progress=job.progress,
            sketch_filename=job.sketch_filename,
            created_at=job.created_at,
            completed_at=job.completed_at,
            ifc_url=job.ifc_url,
            dwg_url=job.dwg_url,
            rvt_url=job.rvt_url,
            preview_image_url=job.preview_image_url,
            error_message=job.error_message
        )
        for job in jobs
    ]
    
    return BatchJobResponse(
        batch_id=batch_id,
        total_jobs=total_jobs,
        completed=completed,
        failed=failed,
        processing=processing,
        queued=queued,
        review=review,
        jobs=job_responses
    )

