"""
Model generation orchestrator
Coordinates sketch reading and BIM model creation
"""
from pathlib import Path
from typing import Dict, Any, Optional
import tempfile
import os

from .sketch_reader import read_sketch
from .legend_parser import parse_legend_from_sketch
from .ifc_generator import generate_ifc_from_plan
from .exporter import export_to_formats
from .ifc_qc import validate_ifc, write_qc_report
from .processing_agent import ProcessingAgent
from ..config import settings
from ..utils import upload_checkpoint
from loguru import logger


class ModelGenerator:
    """
    Orchestrates the full sketch-to-BIM pipeline
    Uses pure Python IfcOpenShell (no Blender required)
    """
    
    def __init__(self):
        pass
    
    def generate_from_sketch(
        self,
        sketch_path: str,
        output_dir: str,
        job_id: str,
        project_type: str = "architecture",
        checkpoints: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Complete pipeline: sketch → plan data → IFC → other formats
        
        Args:
            sketch_path: Path to uploaded sketch
            output_dir: Directory for output files
            job_id: Unique job identifier
        
        Returns:
            dict with file paths and metadata
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        result = {
            "success": False,
            "plan_data": None,
            "confidence": 0.0,
            "legend_data": None,
            "ifc_path": None,
            "dwg_path": None,
            "rvt_path": None,
            "sketchup_path": None,
            "preview_path": None,
            "qc_report_path": None,
            "qc_report": None,
            "requires_review": False,
            "error": None
        }
        
        # Use provided checkpoints or empty dict
        checkpoints = checkpoints or {}
        
        try:
            # Step 0: Use Processing Agent for intelligent sketch processing
            logger.info("Initializing processing agent...")
            agent = ProcessingAgent()
            
            # Process sketch with agent (includes legend parsing and quality gates)
            processing_result = agent.process_sketch(sketch_path, legend_data=None, max_retries=settings.ML_AGENT_MAX_RETRIES, project_type=project_type)
            
            # Extract results
            plan_data = processing_result.plan_data
            
            # Get legend data from processing result (parsed in agent)
            legend_data = processing_result.quality_metrics.get("legend_data") or {}
            
            if not processing_result.success:
                result["error"] = processing_result.error or "Processing failed"
                result["recommendations"] = processing_result.recommendations
                logger.error(f"Processing agent failed: {result['error']}")
                return result
            
            # Store results
            result["legend_data"] = legend_data
            result["plan_data"] = plan_data
            result["confidence"] = processing_result.confidence
            result["quality_metrics"] = processing_result.quality_metrics
            result["gate_results"] = [gate.__dict__ for gate in processing_result.gate_results]
            
            if legend_data.get("scale"):
                logger.info(f"Legend detected: scale={legend_data['scale']}, confidence={legend_data.get('confidence', 0):.2f}")
            else:
                logger.info("No legend detected, using default scale")
            
            # Log detected elements (architecture only)
            logger.info(f"Detected: {len(plan_data.get('rooms', []))} rooms, "
                       f"{len(plan_data.get('walls', []))} walls, "
                       f"confidence: {result['confidence']:.1f}%")
            
            # Check if we should proceed to IFC generation
            should_proceed, reason = agent.should_proceed_to_ifc(plan_data, project_type)
            if not should_proceed:
                result["error"] = f"Cannot proceed to IFC generation: {reason}"
                result["recommendations"] = processing_result.recommendations
                return result
            
            # Add scale ratio to plan data for IFC generation
            if legend_data and legend_data.get("scale_ratio"):
                plan_data["scale_ratio"] = legend_data["scale_ratio"]
            else:
                # Default scale: 100 pixels = 1 meter
                plan_data["scale_ratio"] = 0.01
            
            # Step 2: Generate IFC file using pure Python IfcOpenShell
            ifc_filename = f"{job_id}.ifc"
            ifc_path = output_path / ifc_filename
            
            # Check if IFC checkpoint exists (resume)
            if "ifc" in checkpoints and Path(checkpoints["ifc"]).exists():
                logger.info(f"Using existing IFC checkpoint: {checkpoints['ifc']}")
                result["ifc_path"] = checkpoints["ifc"]
            else:
                logger.info("Generating IFC model using IfcOpenShell...")
                
                # Progress callback for job status updates
                def progress_callback(progress: int, message: str):
                    logger.info(f"IFC Generation Progress: {progress}% - {message}")
                
                success = generate_ifc_from_plan(
                    plan_data,
                    str(ifc_path),
                    progress_callback=progress_callback,
                    project_type=project_type
                )
                
                if not success:
                    result["error"] = "Failed to generate IFC model"
                    logger.error(f"IFC generation failed for job {job_id}")
                    return result
                
                result["ifc_path"] = str(ifc_path)
                logger.info(f"IFC file generated successfully: {ifc_path}")
                
                # Upload IFC checkpoint immediately
                ifc_checkpoint_url = upload_checkpoint(str(ifc_path), job_id, "ifc")
                if ifc_checkpoint_url:
                    result["ifc_checkpoint_url"] = ifc_checkpoint_url
                    logger.info(f"IFC checkpoint saved: {ifc_checkpoint_url}")
            
            # Step 2.5: Validate IFC and generate QC report
            logger.info("Validating IFC and generating QC report...")
            qc_report = validate_ifc(str(ifc_path), project_type)
            qc_report_path = write_qc_report(job_id, qc_report, str(output_path))
            result["qc_report_path"] = qc_report_path
            result["qc_report"] = qc_report
            
            # Step 2.6: IDS Validation (if IDS file provided)
            ids_validation_result = None
            if hasattr(settings, 'IDS_FILE_PATH') and settings.IDS_FILE_PATH:
                try:
                    from ..validation.ids_parser import IDSParser
                    from ..validation.ids_validator import IDSValidator
                    from ..validation.report_generator import ReportGenerator
                    
                    logger.info("Running IDS validation...")
                    parser = IDSParser()
                    ids_spec = parser.parse(settings.IDS_FILE_PATH)
                    
                    validator = IDSValidator()
                    ids_validation_result = validator.validate(str(ifc_path), ids_spec)
                    
                    # Generate IDS validation report
                    report_gen = ReportGenerator()
                    ids_report_path = str(output_path / f"{job_id}_ids_validation.json")
                    report_gen.generate_json_report(ids_validation_result, ids_report_path)
                    result["ids_validation_report"] = ids_report_path
                    result["ids_validation_passed"] = ids_validation_result.overall_passed
                    
                    logger.info(f"IDS validation complete: {'PASSED' if ids_validation_result.overall_passed else 'FAILED'}")
                except Exception as e:
                    logger.warning(f"IDS validation failed: {e}")
                    # Don't fail the job if IDS validation fails, just log it
            
            # Run post-IFC quality gate using agent
            post_ifc_gate = agent.quality_assessor.assess_ifc_quality(qc_report)
            if processing_result.gate_results:
                processing_result.gate_results.append(post_ifc_gate)
            
            # Check if review is needed
            if not qc_report.valid or qc_report.confidence_score < 50.0 or not post_ifc_gate.passed:
                result["requires_review"] = True
                logger.warning(f"QC check: Confidence {qc_report.confidence_score:.1f}%, requires review")
                if post_ifc_gate.recommendations:
                    result["recommendations"] = result.get("recommendations", []) + post_ifc_gate.recommendations
            
            # Step 3: Export to other formats (use checkpoints if available)
            logger.info("Exporting to additional formats...")
            scale_ratio = plan_data.get("scale_ratio", 0.01)
            
            # Check for existing checkpoints and use them, otherwise export
            exported = {}
            
            # Check DWG checkpoint
            if "dwg" in checkpoints and Path(checkpoints["dwg"]).exists():
                logger.info(f"Using existing DWG checkpoint: {checkpoints['dwg']}")
                exported["dwg_path"] = checkpoints["dwg"]
            else:
                # Export all formats
                exported_result = export_to_formats(
                    str(ifc_path),
                    str(output_path),
                    job_id,
                    scale_ratio=scale_ratio
                )
                exported = exported_result
            
            # Check other checkpoint types
            if "obj" in checkpoints and Path(checkpoints["obj"]).exists():
                logger.info(f"Using existing OBJ checkpoint: {checkpoints['obj']}")
                exported["sketchup_path"] = checkpoints["obj"]
            
            if "rvt" in checkpoints and Path(checkpoints["rvt"]).exists():
                logger.info(f"Using existing RVT checkpoint: {checkpoints['rvt']}")
                exported["rvt_path"] = checkpoints["rvt"]
            
            if "preview" in checkpoints and Path(checkpoints["preview"]).exists():
                logger.info(f"Using existing Preview checkpoint: {checkpoints['preview']}")
                exported["preview_path"] = checkpoints["preview"]
            
            result["dwg_path"] = exported.get("dwg_path")
            result["rvt_path"] = exported.get("rvt_path")
            result["sketchup_path"] = exported.get("sketchup_path")
            result["preview_path"] = exported.get("preview_path")
            
            # Upload checkpoints for all exported files (if not already checkpoints)
            if result.get("dwg_path") and Path(result["dwg_path"]).exists() and "dwg" not in checkpoints:
                dwg_checkpoint_url = upload_checkpoint(result["dwg_path"], job_id, "dwg")
                if dwg_checkpoint_url:
                    result["dwg_checkpoint_url"] = dwg_checkpoint_url
                    logger.info(f"DWG checkpoint saved: {dwg_checkpoint_url}")
            
            if result.get("sketchup_path") and Path(result["sketchup_path"]).exists() and "obj" not in checkpoints:
                obj_checkpoint_url = upload_checkpoint(result["sketchup_path"], job_id, "obj")
                if obj_checkpoint_url:
                    result["obj_checkpoint_url"] = obj_checkpoint_url
                    logger.info(f"OBJ checkpoint saved: {obj_checkpoint_url}")
            
            if result.get("rvt_path") and Path(result["rvt_path"]).exists() and "rvt" not in checkpoints:
                rvt_checkpoint_url = upload_checkpoint(result["rvt_path"], job_id, "rvt")
                if rvt_checkpoint_url:
                    result["rvt_checkpoint_url"] = rvt_checkpoint_url
                    logger.info(f"RVT checkpoint saved: {rvt_checkpoint_url}")
            
            if result.get("preview_path") and Path(result["preview_path"]).exists() and "preview" not in checkpoints:
                preview_checkpoint_url = upload_checkpoint(result["preview_path"], job_id, "preview")
                if preview_checkpoint_url:
                    result["preview_checkpoint_url"] = preview_checkpoint_url
                    logger.info(f"Preview checkpoint saved: {preview_checkpoint_url}")
            
            result["success"] = True
            logger.success(f"Model generation completed successfully for job {job_id}")
            
        except Exception as e:
            logger.error(f"Model generation error for job {job_id}: {e}", exc_info=True)
            result["error"] = str(e)
        
        return result
    
    def validate_output(self, ifc_path: str) -> bool:
        """
        Validate generated IFC file
        """
        if not os.path.exists(ifc_path):
            return False
        
        # Check file size
        size = os.path.getsize(ifc_path)
        if size < 1000:  # Too small to be valid
            return False
        
        # Try to parse IFC
        try:
            import ifcopenshell
            ifc_file = ifcopenshell.open(ifc_path)
            
            # Check for basic elements
            walls = ifc_file.by_type("IfcWall")
            slabs = ifc_file.by_type("IfcSlab")
            
            if len(walls) == 0:
                logger.warning("No walls found in IFC file")
            
            return True
        
        except Exception as e:
            logger.error(f"IFC validation failed: {e}", exc_info=True)
            return False


def generate_model(sketch_path: str, output_dir: str, job_id: str, project_type: str = "architecture", checkpoints: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Convenience function for model generation
    
    Args:
        sketch_path: Path to sketch file
        output_dir: Output directory
        job_id: Job ID
        project_type: Project type
        checkpoints: Optional dict of checkpoint_type -> local_path for resuming
    """
    generator = ModelGenerator()
    return generator.generate_from_sketch(sketch_path, output_dir, job_id, project_type=project_type, checkpoints=checkpoints)

