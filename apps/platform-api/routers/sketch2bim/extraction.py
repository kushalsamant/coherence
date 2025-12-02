"""
Data extraction and export routes
Extract IFC data and export to various formats
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from pathlib import Path
from loguru import logger

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database.sketch2bim import get_db
from auth.sketch2bim import get_current_user
from models.sketch2bim import Job
from utils.sketch2bim.exceptions import NotFoundError
from services.sketch2bim.ifc_extractor import IFCExtractor
from services.sketch2bim.exporter import DataExporter

router = APIRouter(prefix="/extraction", tags=["extraction"])


@router.post("/jobs/{job_id}/extract")
async def extract_job_data(
    job_id: str,
    format: str = Query("json", regex="^(json|csv|excel|xml)$"),
    include_cobie: bool = Query(True),
    property_sets: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Extract data from a completed job's IFC file
    
    Args:
        job_id: Job ID
        format: Export format (json, csv, excel, xml)
        include_cobie: Include COBie data extraction
        property_sets: Optional list of property set names to extract
        
    Returns:
        Download URL or data depending on format
    """
    # Get job
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundError(f"Job {job_id} not found")
    
    # Check permissions
    if user.id != job.user_id and not getattr(user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized to access this job")
    
    if job.status != "completed":
        raise HTTPException(status_code=400, detail="Job must be completed to extract data")
    
    if not job.ifc_url:
        raise HTTPException(status_code=400, detail="No IFC file available for this job")
    
    try:
        # Download IFC file temporarily
        import tempfile
        import requests
        
        response = requests.get(job.ifc_url, timeout=60)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.ifc', delete=False) as f:
            f.write(response.content)
            temp_ifc_path = f.name
        
        try:
            # Extract data
            extractor = IFCExtractor()
            exporter = DataExporter()
            
            data = {}
            
            if include_cobie:
                cobie_data = extractor.extract_cobie_data(temp_ifc_path)
                data['cobie'] = cobie_data
            
            if property_sets:
                pset_data = extractor.extract_property_sets(temp_ifc_path, property_sets)
                data['property_sets'] = pset_data
            
            # Export to requested format
            output_dir = Path("./extractions") / job_id
            output_dir.mkdir(parents=True, exist_ok=True)
            
            if format == "json":
                output_path = str(output_dir / f"{job_id}_extracted.json")
                result_path = exporter.export_to_json(data, output_path)
            elif format == "csv":
                # Export each category as separate CSV
                if 'cobie' in data:
                    result_paths = []
                    for category, items in data['cobie'].items():
                        if isinstance(items, list) and items:
                            csv_path = str(output_dir / f"{job_id}_{category}.csv")
                            exporter.export_to_csv(items, csv_path)
                            result_paths.append(csv_path)
                    result_path = result_paths[0] if result_paths else None
                else:
                    raise HTTPException(status_code=400, detail="No list data available for CSV export")
            elif format == "excel":
                # Export COBie data as multi-sheet Excel
                if 'cobie' in data:
                    excel_path = str(output_dir / f"{job_id}_extracted.xlsx")
                    result_path = exporter.export_to_excel(data['cobie'], excel_path)
                else:
                    raise HTTPException(status_code=400, detail="No COBie data available for Excel export")
            elif format == "xml":
                output_path = str(output_dir / f"{job_id}_extracted.xml")
                result_path = exporter.export_to_xml(data, output_path)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
            
            # Upload to CDN and return URL
            from ..utils import upload_to_bunny, create_signed_bunny_url, generate_remote_path
            
            remote_path = generate_remote_path(job_id, Path(result_path).name)
            file_url = upload_to_bunny(result_path, remote_path)
            signed_url = create_signed_bunny_url(file_url)
            
            logger.info(f"Data extraction complete for job {job_id}, format: {format}")
            
            return {
                "job_id": job_id,
                "format": format,
                "download_url": signed_url,
                "file_path": result_path,
            }
            
        finally:
            # Cleanup temp file
            if Path(temp_ifc_path).exists():
                Path(temp_ifc_path).unlink()
                
    except Exception as e:
        logger.error(f"Data extraction failed for job {job_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


@router.get("/jobs/{job_id}/property-sets")
async def get_job_property_sets(
    job_id: str,
    pset_names: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Get property sets from a job's IFC file
    
    Args:
        job_id: Job ID
        pset_names: Optional list of property set names to filter
        
    Returns:
        Dictionary mapping property set names to data
    """
    # Get job
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundError(f"Job {job_id} not found")
    
    # Check permissions
    if user.id != job.user_id and not getattr(user, 'is_admin', False):
        raise HTTPException(status_code=403, detail="Not authorized to access this job")
    
    if not job.ifc_url:
        raise HTTPException(status_code=400, detail="No IFC file available for this job")
    
    try:
        import tempfile
        import requests
        
        response = requests.get(job.ifc_url, timeout=60)
        response.raise_for_status()
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.ifc', delete=False) as f:
            f.write(response.content)
            temp_ifc_path = f.name
        
        try:
            extractor = IFCExtractor()
            pset_data = extractor.extract_property_sets(temp_ifc_path, pset_names)
            
            return {
                "job_id": job_id,
                "property_sets": pset_data,
            }
            
        finally:
            if Path(temp_ifc_path).exists():
                Path(temp_ifc_path).unlink()
                
    except Exception as e:
        logger.error(f"Property set extraction failed for job {job_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

