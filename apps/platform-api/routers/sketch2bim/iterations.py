"""
Iteration routes - IFC file versioning and editing
REST API for creating, listing, and managing IFC iterations
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
import uuid
from pathlib import Path
from loguru import logger

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from sketch2bim_database import get_db
from sketch2bim_auth import get_current_user
from sketch2bim_models import User, Job, Iteration
from sketch2bim_schemas import IterationCreate, IterationUpdate, IterationResponse
# Utils imported as needed
from sketch2bim_exceptions import NotFoundError, ValidationError

router = APIRouter(prefix="/iterations", tags=["iterations"])


@router.post("/jobs/{job_id}/iterations", response_model=IterationResponse)
async def create_iteration(
    job_id: str,
    iteration_data: IterationCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """
    Create a new iteration from an existing IFC file
    
    If parent_iteration_id is provided, creates iteration from that parent.
    Otherwise, uses the job's original IFC file.
    """
    # Verify job exists and belongs to user
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()
    if not job:
        raise NotFoundError(f"Job {job_id} not found")
    
    # Verify parent iteration if provided
    parent_iteration = None
    if iteration_data.parent_iteration_id:
        parent_iteration = db.query(Iteration).filter(
            Iteration.id == iteration_data.parent_iteration_id,
            Iteration.job_id == job_id,
            Iteration.user_id == user.id
        ).first()
        if not parent_iteration:
            raise NotFoundError(f"Parent iteration {iteration_data.parent_iteration_id} not found")
    
    # Determine source IFC URL
    source_ifc_url = None
    if parent_iteration:
        source_ifc_url = parent_iteration.ifc_url
    elif job.ifc_url:
        source_ifc_url = job.ifc_url
    else:
        raise ValidationError("No IFC file available to create iteration from")
    
    # Create iteration record
    iteration = Iteration(
        id=str(uuid.uuid4()),
        job_id=job_id,
        user_id=user.id,
        parent_iteration_id=iteration_data.parent_iteration_id,
        ifc_url=source_ifc_url,  # Initially same as source, will be updated after processing
        ifc_filename=job.sketch_filename.replace(
            Path(job.sketch_filename).suffix, ".ifc"
        ) if job.sketch_filename else f"{job_id}.ifc",
        changes_json=iteration_data.changes_json or {},
        change_summary=_generate_change_summary(iteration_data.changes_json),
        name=iteration_data.name or f"Iteration {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        notes=iteration_data.notes
    )
    
    db.add(iteration)
    db.commit()
    db.refresh(iteration)
    
    logger.info(f"Created iteration {iteration.id} for job {job_id}")
    
    return iteration


@router.get("/jobs/{job_id}/iterations", response_model=List[IterationResponse])
async def list_iterations(
    job_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all iterations for a job
    """
    # Verify job exists and belongs to user
    job = db.query(Job).filter(Job.id == job_id, Job.user_id == user.id).first()
    if not job:
        raise NotFoundError(f"Job {job_id} not found")
    
    # Get all iterations for this job
    iterations = db.query(Iteration).filter(
        Iteration.job_id == job_id,
        Iteration.user_id == user.id
    ).order_by(desc(Iteration.created_at)).all()
    
    return iterations


@router.get("/iterations/{iteration_id}", response_model=IterationResponse)
async def get_iteration(
    iteration_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific iteration
    """
    iteration = db.query(Iteration).filter(
        Iteration.id == iteration_id,
        Iteration.user_id == user.id
    ).first()
    
    if not iteration:
        raise NotFoundError(f"Iteration {iteration_id} not found")
    
    return iteration


@router.patch("/iterations/{iteration_id}", response_model=IterationResponse)
async def update_iteration(
    iteration_id: str,
    iteration_data: IterationUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update iteration metadata (name, notes, changes)
    """
    iteration = db.query(Iteration).filter(
        Iteration.id == iteration_id,
        Iteration.user_id == user.id
    ).first()
    
    if not iteration:
        raise NotFoundError(f"Iteration {iteration_id} not found")
    
    # Update fields
    if iteration_data.name is not None:
        iteration.name = iteration_data.name
    if iteration_data.notes is not None:
        iteration.notes = iteration_data.notes
    if iteration_data.changes_json is not None:
        iteration.changes_json = iteration_data.changes_json
        iteration.change_summary = _generate_change_summary(iteration_data.changes_json)
    
    db.commit()
    db.refresh(iteration)
    
    return iteration


@router.post("/iterations/{iteration_id}/regenerate")
async def regenerate_iteration(
    iteration_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """
    Regenerate IFC file for an iteration with applied changes
    
    This will:
    1. Load the parent IFC or original job IFC
    2. Apply changes from changes_json
    3. Generate new IFC file
    4. Upload to CDN
    5. Update iteration.ifc_url
    """
    iteration = db.query(Iteration).filter(
        Iteration.id == iteration_id,
        Iteration.user_id == user.id
    ).first()
    
    if not iteration:
        raise NotFoundError(f"Iteration {iteration_id} not found")
    
    # Get job
    job = db.query(Job).filter(Job.id == iteration.job_id).first()
    if not job:
        raise NotFoundError(f"Job {iteration.job_id} not found")
    
    # Check if job has plan_data
    if not job.plan_data:
        raise ValidationError("Job does not have plan data. Cannot regenerate IFC.")
    
    # Create output directory
    from pathlib import Path
    output_dir = Path("./outputs") / iteration_id
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load original plan_data and apply changes
    import copy
    plan_data = copy.deepcopy(job.plan_data)
    
    # Apply changes from changes_json if provided
    if iteration.changes_json:
        changes = iteration.changes_json
        applied_changes = 0
        
        # Apply moved elements (walls, doors, windows)
        if changes.get("moved_elements"):
            for move in changes["moved_elements"]:
                element_id = move.get("element_id")
                new_position = move.get("position")
                element_type = move.get("element_type", "wall")  # wall, door, window
                
                # Find and update element in plan_data
                if element_type == "wall" and "walls" in plan_data:
                    for wall in plan_data["walls"]:
                        if wall.get("id") == element_id:
                            if isinstance(new_position, dict):
                                wall["start"] = new_position.get("start", wall.get("start"))
                                wall["end"] = new_position.get("end", wall.get("end"))
                                applied_changes += 1
                            break
                elif element_type in ["door", "window"] and "openings" in plan_data:
                    for opening in plan_data["openings"]:
                        if opening.get("id") == element_id:
                            if isinstance(new_position, dict):
                                opening["position"] = new_position
                                applied_changes += 1
                            elif isinstance(new_position, list) and len(new_position) >= 2:
                                opening["position"] = new_position
                                applied_changes += 1
                            break
        
        # Apply resized rooms
        if changes.get("resized_rooms"):
            for resize in changes["resized_rooms"]:
                room_id = resize.get("room_id")
                new_size = resize.get("size")
                new_polygon = resize.get("polygon")
                
                # Find and update room in plan_data
                if "rooms" in plan_data:
                    for room in plan_data["rooms"]:
                        if room.get("id") == room_id:
                            change_applied = False
                            if new_polygon and isinstance(new_polygon, list):
                                room["polygon"] = new_polygon
                                # Recalculate area if polygon changed
                                if len(new_polygon) >= 3:
                                    # Simple area calculation (shoelace formula)
                                    area = 0
                                    for i in range(len(new_polygon)):
                                        j = (i + 1) % len(new_polygon)
                                        area += new_polygon[i][0] * new_polygon[j][1]
                                        area -= new_polygon[j][0] * new_polygon[i][1]
                                    room["area"] = abs(area) / 2
                                    change_applied = True
                            elif new_size and isinstance(new_size, (int, float)):
                                # Scale room polygon proportionally
                                if room.get("polygon") and len(room["polygon"]) > 0:
                                    current_area = room.get("area", 0)
                                    if current_area > 0:
                                        scale = (new_size / current_area) ** 0.5
                                        center_x = sum(p[0] for p in room["polygon"]) / len(room["polygon"])
                                        center_y = sum(p[1] for p in room["polygon"]) / len(room["polygon"])
                                        room["polygon"] = [
                                            [center_x + (p[0] - center_x) * scale, 
                                             center_y + (p[1] - center_y) * scale]
                                            for p in room["polygon"]
                                        ]
                                        room["area"] = new_size
                                        change_applied = True
                            
                            if change_applied:
                                applied_changes += 1
                            break
        
        # Apply added elements
        if changes.get("added_elements"):
            for add in changes["added_elements"]:
                element_type = add.get("element_type")
                element_data = add.get("element_data", {})
                
                if element_type == "room" and "rooms" in plan_data:
                    plan_data["rooms"].append(element_data)
                    applied_changes += 1
                elif element_type == "wall" and "walls" in plan_data:
                    plan_data["walls"].append(element_data)
                    applied_changes += 1
                elif element_type in ["door", "window"] and "openings" in plan_data:
                    plan_data["openings"].append(element_data)
                    applied_changes += 1
        
        # Apply removed elements
        if changes.get("removed_elements"):
            for remove in changes["removed_elements"]:
                element_id = remove.get("element_id")
                element_type = remove.get("element_type", "wall")
                
                if element_type == "room" and "rooms" in plan_data:
                    plan_data["rooms"] = [r for r in plan_data["rooms"] if r.get("id") != element_id]
                    applied_changes += 1
                elif element_type == "wall" and "walls" in plan_data:
                    plan_data["walls"] = [w for w in plan_data["walls"] if w.get("id") != element_id]
                    applied_changes += 1
                elif element_type in ["door", "window"] and "openings" in plan_data:
                    plan_data["openings"] = [o for o in plan_data["openings"] if o.get("id") != element_id]
                    applied_changes += 1
        
        # Apply modified properties
        if changes.get("modified_properties"):
            for prop_change in changes["modified_properties"]:
                element_id = prop_change.get("element_id")
                element_type = prop_change.get("element_type", "room")
                properties = prop_change.get("properties", {})
                
                # Find element and update properties
                if element_type == "room" and "rooms" in plan_data:
                    for room in plan_data["rooms"]:
                        if room.get("id") == element_id:
                            room.update(properties)
                            applied_changes += 1
                            break
                elif element_type == "wall" and "walls" in plan_data:
                    for wall in plan_data["walls"]:
                        if wall.get("id") == element_id:
                            wall.update(properties)
                            applied_changes += 1
                            break
        
        logger.info(f"Applied {applied_changes} changes to plan_data for iteration {iteration_id}")
    
    # Generate IFC from modified plan_data
    from ..ai.ifc_generator import generate_ifc_from_plan
    from ..utils import upload_to_bunny, create_signed_bunny_url, generate_remote_path, upload_checkpoint
    
    ifc_path = str(output_dir / f"{iteration_id}.ifc")
    
    try:
        success = generate_ifc_from_plan(plan_data, ifc_path)
        
        if not success:
            raise ValidationError("Failed to generate IFC file")
        
        # Upload IFC checkpoint immediately
        ifc_checkpoint_url = upload_checkpoint(ifc_path, iteration_id, "ifc")
        if ifc_checkpoint_url:
            logger.info(f"Iteration IFC checkpoint saved: {ifc_checkpoint_url}")
        
        # Upload to CDN (permanent storage)
        remote_path = generate_remote_path(iteration_id, f"{iteration_id}.ifc")
        ifc_url = upload_to_bunny(ifc_path, remote_path)
        iteration.ifc_url = create_signed_bunny_url(ifc_url)
        
        db.commit()
        
        logger.info(f"IFC regenerated for iteration {iteration_id}: {iteration.ifc_url}")
        
        return {
            "status": "completed",
            "message": "IFC file regenerated successfully",
            "iteration_id": iteration_id,
            "ifc_url": iteration.ifc_url
        }
    except Exception as e:
        logger.error(f"IFC regeneration failed for iteration {iteration_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"IFC regeneration failed: {str(e)}")
    finally:
        # Cleanup local file
        if Path(ifc_path).exists():
            try:
                Path(ifc_path).unlink()
            except:
                pass


@router.delete("/iterations/{iteration_id}")
async def delete_iteration(
    iteration_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete an iteration
    """
    iteration = db.query(Iteration).filter(
        Iteration.id == iteration_id,
        Iteration.user_id == user.id
    ).first()
    
    if not iteration:
        raise NotFoundError(f"Iteration {iteration_id} not found")
    
    # Check if it has children
    children = db.query(Iteration).filter(
        Iteration.parent_iteration_id == iteration_id
    ).count()
    
    if children > 0:
        raise ValidationError("Cannot delete iteration with child iterations")
    
    db.delete(iteration)
    db.commit()
    
    return {"status": "deleted", "iteration_id": iteration_id}


def _generate_change_summary(changes_json: dict) -> str:
    """
    Generate human-readable summary of changes
    """
    if not changes_json:
        return "No changes recorded"
    
    summary_parts = []
    
    if changes_json.get("moved_elements"):
        count = len(changes_json["moved_elements"])
        summary_parts.append(f"Moved {count} element(s)")
    
    if changes_json.get("resized_rooms"):
        count = len(changes_json["resized_rooms"])
        summary_parts.append(f"Resized {count} room(s)")
    
    if changes_json.get("added_elements"):
        count = len(changes_json["added_elements"])
        summary_parts.append(f"Added {count} element(s)")
    
    if changes_json.get("removed_elements"):
        count = len(changes_json["removed_elements"])
        summary_parts.append(f"Removed {count} element(s)")
    
    if changes_json.get("modified_properties"):
        count = len(changes_json["modified_properties"])
        summary_parts.append(f"Modified {count} propertie(s)")
    
    return "; ".join(summary_parts) if summary_parts else "Changes applied"

