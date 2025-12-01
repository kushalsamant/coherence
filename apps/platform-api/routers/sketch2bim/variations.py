"""
Layout variation routes - Generate alternative room arrangements
REST API for creating and managing layout variations
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
import uuid
from loguru import logger

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from sketch2bim_database import get_db
from sketch2bim_auth import get_current_user, require_active_subscription
from sketch2bim_models import User, Job, LayoutVariation
from sketch2bim_schemas import VariationGenerateRequest, VariationResponse
from sketch2bim_exceptions import NotFoundError, ValidationError
from sketch2bim_ai.layout_generator import generate_layout_variations

router = APIRouter(prefix="/variations", tags=["variations"])


@router.post("/jobs/{job_id}/variations", response_model=List[VariationResponse])
async def generate_variations(
    job_id: str,
    request: VariationGenerateRequest,
    user: User = Depends(require_active_subscription()),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """
    Generate multiple layout variations from the same sketch
    
    Creates alternative room arrangements by:
    - Rearranging room positions
    - Adjusting room sizes
    - Changing adjacencies
    - Maintaining constraints (if provided)
    """
    # Verify job exists and belongs to user
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()
    if not job:
        raise NotFoundError(f"Job {job_id} not found")
    
    # Verify job is completed
    if job.status != "completed":
        raise ValidationError("Job must be completed before generating variations")
    
    # Verify plan_data exists
    if not job.plan_data:
        raise ValidationError("Job does not have plan data. Cannot generate variations.")
    
    # Generate variations in background
    logger.info(f"Generating {request.num_variations} variations for job {job_id}")
    
    # Create variation records (will be updated when processing completes)
    variations = []
    for i in range(request.num_variations):
        variation = LayoutVariation(
            id=str(uuid.uuid4()),
            job_id=job_id,
            user_id=user.id,
            variation_number=i + 1,
            plan_data=None,  # Will be set by generator
            confidence=0.0
        )
        db.add(variation)
        variations.append(variation)
    
    db.commit()
    
    # Process variations in background
    if background_tasks:
        background_tasks.add_task(
            _process_variations,
            job_id=job_id,
            variation_ids=[v.id for v in variations],
            original_plan_data=job.plan_data,
            num_variations=request.num_variations,
            constraints=request.constraints
        )
    else:
        # Synchronous processing (for testing)
        _process_variations(
            job_id=job_id,
            variation_ids=[v.id for v in variations],
            original_plan_data=job.plan_data,
            num_variations=request.num_variations,
            constraints=request.constraints
        )
    
    return variations


@router.get("/jobs/{job_id}/variations", response_model=List[VariationResponse])
async def list_variations(
    job_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all variations for a job
    """
    # Verify job exists and belongs to user
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()
    if not job:
        raise NotFoundError(f"Job {job_id} not found")
    
    # Get all variations for this job
    variations = db.query(LayoutVariation).filter(
        LayoutVariation.job_id == job_id,
        LayoutVariation.user_id == user.id
    ).order_by(LayoutVariation.variation_number).all()
    
    return variations


@router.get("/variations/{variation_id}", response_model=VariationResponse)
async def get_variation(
    variation_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific variation
    """
    variation = db.query(LayoutVariation).filter(
        LayoutVariation.id == variation_id,
        LayoutVariation.user_id == user.id
    ).first()
    
    if not variation:
        raise NotFoundError(f"Variation {variation_id} not found")
    
    return variation


@router.delete("/variations/{variation_id}")
async def delete_variation(
    variation_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a variation
    """
    variation = db.query(LayoutVariation).filter(
        LayoutVariation.id == variation_id,
        LayoutVariation.user_id == user.id
    ).first()
    
    if not variation:
        raise NotFoundError(f"Variation {variation_id} not found")
    
    db.delete(variation)
    db.commit()
    
    return {"status": "deleted", "variation_id": variation_id}


def _process_variations(
    job_id: str,
    variation_ids: List[str],
    original_plan_data: dict,
    num_variations: int,
    constraints: dict = None
):
    """
    Background task to process layout variations
    """
    from ..database import SessionLocal
    db = SessionLocal()
    
    try:
        # Generate variations using layout generator
        variations_data = generate_layout_variations(
            original_plan_data=original_plan_data,
            num_variations=num_variations,
            constraints=constraints
        )
        
        # Update variation records
        for i, variation_id in enumerate(variation_ids):
            variation = db.query(LayoutVariation).filter(
                LayoutVariation.id == variation_id
            ).first()
            
            if variation and i < len(variations_data):
                var_data = variations_data[i]
                variation.plan_data = var_data.get("plan_data")
                variation.confidence = var_data.get("confidence", 0.0)
                
                # Generate IFC for this variation
                if variation.plan_data:
                    from pathlib import Path
                    from ..ai.ifc_generator import generate_ifc_from_plan
                    from ..ai.exporter import export_to_formats
                    from ..utils import upload_to_bunny, create_signed_bunny_url, generate_remote_path, upload_checkpoint
                    
                    # Create output directory
                    output_dir = Path("./outputs") / variation.id
                    output_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Generate IFC
                    ifc_path = str(output_dir / f"{variation.id}.ifc")
                    success = generate_ifc_from_plan(variation.plan_data, ifc_path)
                    
                    if success and Path(ifc_path).exists():
                        # Upload IFC checkpoint immediately
                        ifc_checkpoint_url = upload_checkpoint(ifc_path, variation.id, "ifc")
                        if ifc_checkpoint_url:
                            logger.info(f"Variation IFC checkpoint saved: {ifc_checkpoint_url}")
                        
                        # Export to other formats (DWG, SketchUp)
                        exported = export_to_formats(
                            ifc_path,
                            str(output_dir),
                            variation.id,
                            scale_ratio=0.01  # Default scale
                        )
                        
                        # Upload checkpoints for exported files
                        if exported.get("dwg_path") and Path(exported["dwg_path"]).exists():
                            upload_checkpoint(exported["dwg_path"], variation.id, "dwg")
                        if exported.get("sketchup_path") and Path(exported["sketchup_path"]).exists():
                            upload_checkpoint(exported["sketchup_path"], variation.id, "obj")
                        if exported.get("preview_path") and Path(exported["preview_path"]).exists():
                            upload_checkpoint(exported["preview_path"], variation.id, "preview")
                        
                        # Upload IFC (permanent storage)
                        remote_path = generate_remote_path(variation.id, f"{variation.id}.ifc")
                        ifc_url = upload_to_bunny(ifc_path, remote_path)
                        variation.ifc_url = create_signed_bunny_url(ifc_url)
                        
                        # Upload preview if available
                        if exported.get("preview_path") and Path(exported["preview_path"]).exists():
                            preview_remote_path = generate_remote_path(variation.id, f"{variation.id}_preview.png")
                            preview_url = upload_to_bunny(exported["preview_path"], preview_remote_path)
                            variation.preview_image_url = preview_url
                        
                        logger.info(f"Variation {variation.id} IFC generated: {variation.ifc_url}")
                    else:
                        logger.warning(f"Failed to generate IFC for variation {variation.id}")
        
        db.commit()
        logger.info(f"Processed {len(variation_ids)} variations for job {job_id}")
        
    except Exception as e:
        logger.error(f"Error processing variations for job {job_id}: {e}", exc_info=True)
    finally:
        db.close()

