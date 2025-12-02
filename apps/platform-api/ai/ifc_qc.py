"""
IFC Quality Control and Validation Module
Validates IFC files, auto-fixes common issues, and generates QC reports
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    import ifcopenshell
    import ifcopenshell.validate
    IFC_AVAILABLE = True
except ImportError:
    IFC_AVAILABLE = False
    print("Warning: ifcopenshell not available. IFC validation will be limited.")


@dataclass
class QCError:
    """Represents a QC error"""
    severity: str  # critical|warning|info
    category: str  # geometry|topology|units|standards
    message: str
    element_id: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class QCReport:
    """Quality control report - structured and categorized like Gates"""
    valid: bool
    confidence_score: float  # 0-100
    errors: List[QCError]
    warnings: List[QCError]
    info: List[QCError]
    file_size: int
    element_counts: Dict[str, int]
    validation_timestamp: str
    ifc_schema_version: Optional[str] = None
    # Enhanced structured fields
    categories: Optional[Dict[str, Any]] = None  # Categorized results by type
    overall_status: Optional[str] = None  # "passed", "failed", "warning"
    recommendations: Optional[List[str]] = None  # Actionable recommendations


class IFCValidator:
    """Validates IFC files for quality and compliance"""
    
    def __init__(self):
        self.min_wall_count = 1
        self.min_file_size = 1000  # bytes
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        
    def validate_ifc(self, ifc_path: str, project_type: str = "architecture") -> QCReport:
        """
        Comprehensive IFC validation
        
        Args:
            ifc_path: Path to IFC file
            project_type: Project type (architecture only)
            
        Returns:
            QCReport with validation results
        """
        errors = []
        warnings = []
        info = []
        
        # Basic file checks
        if not os.path.exists(ifc_path):
            errors.append(QCError(
                severity="critical",
                category="file",
                message="IFC file does not exist"
            ))
            return QCReport(
                valid=False,
                confidence_score=0.0,
                errors=errors,
                warnings=warnings,
                info=info,
                file_size=0,
                element_counts={},
                validation_timestamp=datetime.utcnow().isoformat()
            )
        
        # File size check
        file_size = os.path.getsize(ifc_path)
        if file_size < self.min_file_size:
            errors.append(QCError(
                severity="critical",
                category="file",
                message=f"IFC file too small ({file_size} bytes). Likely corrupted or empty."
            ))
        elif file_size > self.max_file_size:
            warnings.append(QCError(
                severity="warning",
                category="file",
                message=f"IFC file very large ({file_size / 1024 / 1024:.1f} MB). May cause performance issues."
            ))
        
        # Try to open and parse IFC
        ifc_file = None
        ifc_schema = None
        element_counts = {}
        
        if IFC_AVAILABLE:
            try:
                ifc_file = ifcopenshell.open(ifc_path)
                ifc_schema = ifc_file.schema
                
                # Count elements
                element_counts = self._count_elements(ifc_file, project_type)
                
                # Validate using ifcopenshell
                validation_errors = ifcopenshell.validate.validate(ifc_file)
                
                for error in validation_errors:
                    errors.append(QCError(
                        severity="critical",
                        category="standards",
                        message=str(error),
                        suggestion="Check IFC schema compliance"
                    ))
                
                # Geometry validation
                geom_errors, geom_warnings = self._validate_geometry(ifc_file, project_type)
                errors.extend(geom_errors)
                warnings.extend(geom_warnings)
                
                # Topology validation
                topo_errors, topo_warnings = self._validate_topology(ifc_file)
                errors.extend(topo_errors)
                warnings.extend(topo_warnings)
                
                # Units validation
                units_errors, units_warnings = self._validate_units(ifc_file)
                errors.extend(units_errors)
                warnings.extend(units_warnings)
                
            except Exception as e:
                errors.append(QCError(
                    severity="critical",
                    category="file",
                    message=f"Failed to parse IFC file: {str(e)}",
                    suggestion="File may be corrupted or invalid IFC format"
                ))
        else:
            warnings.append(QCError(
                severity="warning",
                category="system",
                message="ifcopenshell not available. Limited validation performed.",
                suggestion="Install ifcopenshell for full validation"
            ))
        
        # Calculate confidence score
        confidence = self._calculate_confidence(errors, warnings, element_counts, project_type)
        
        # Determine if valid
        critical_errors = [e for e in errors if e.severity == "critical"]
        valid = len(critical_errors) == 0
        
        return QCReport(
            valid=valid,
            confidence_score=confidence,
            errors=errors,
            warnings=warnings,
            info=info,
            file_size=file_size,
            element_counts=element_counts,
            validation_timestamp=datetime.utcnow().isoformat(),
            ifc_schema_version=ifc_schema
        )
    
    def _count_elements(self, ifc_file, project_type: str = "architecture") -> Dict[str, int]:
        """Count different element types in IFC"""
        counts = {}
        
        # Common element types for all projects
        element_types = [
            "IfcWall", "IfcWallStandardCase",
            "IfcSlab", "IfcRoof",
            "IfcDoor", "IfcWindow",
            "IfcSpace", "IfcZone",
            "IfcBuilding", "IfcBuildingStorey",
            "IfcColumn", "IfcBeam",
            "IfcSite", "IfcProject"
        ]
        
        # Architecture only - no landscape/urban elements
        
        for elem_type in element_types:
            try:
                elements = ifc_file.by_type(elem_type)
                counts[elem_type] = len(elements)
            except:
                counts[elem_type] = 0
        
        return counts
    
    def _validate_geometry(self, ifc_file, project_type: str = "architecture") -> tuple[List[QCError], List[QCError]]:
        """Validate geometry quality"""
        errors = []
        warnings = []
        
        if project_type == "architecture":
            # Architecture-specific validation (existing logic)
            # Check for walls
            walls = ifc_file.by_type("IfcWall") + ifc_file.by_type("IfcWallStandardCase")
            if len(walls) == 0:
                errors.append(QCError(
                    severity="critical",
                    category="geometry",
                    message="No walls found in IFC model",
                    suggestion="Ensure walls are properly created during generation"
                ))
            elif len(walls) < self.min_wall_count:
                warnings.append(QCError(
                    severity="warning",
                    category="geometry",
                    message=f"Very few walls detected ({len(walls)})",
                    suggestion="Verify sketch detection captured all walls"
                ))
            
            # Check for spaces/rooms
            spaces = ifc_file.by_type("IfcSpace")
            if len(spaces) == 0:
                warnings.append(QCError(
                    severity="warning",
                    category="geometry",
                    message="No spaces (rooms) defined in IFC",
                    suggestion="Consider adding IfcSpace elements for better BIM compatibility"
                ))
            
            # Check for building storeys
            storeys = ifc_file.by_type("IfcBuildingStorey")
            if len(storeys) == 0:
                warnings.append(QCError(
                    severity="warning",
                    category="geometry",
                    message="No building storeys defined",
                    suggestion="Add IfcBuildingStorey for proper building hierarchy"
                ))
        
        return errors, warnings
    
    def _validate_topology(self, ifc_file) -> tuple[List[QCError], List[QCError]]:
        """Validate topological relationships"""
        errors = []
        warnings = []
        
        # Check for orphaned elements (elements not connected to building)
        buildings = ifc_file.by_type("IfcBuilding")
        if len(buildings) == 0:
            warnings.append(QCError(
                severity="warning",
                category="topology",
                message="No IfcBuilding element found",
                suggestion="Add IfcBuilding as root element for proper structure"
            ))
        
        # Check for elements without proper containment
        walls = ifc_file.by_type("IfcWall") + ifc_file.by_type("IfcWallStandardCase")
        for wall in walls:
            # Check if wall has proper placement
            if not hasattr(wall, 'ObjectPlacement') or wall.ObjectPlacement is None:
                warnings.append(QCError(
                    severity="warning",
                    category="topology",
                    message=f"Wall {wall.id()} missing ObjectPlacement",
                    element_id=str(wall.id()),
                    suggestion="Ensure all elements have proper placement"
                ))
        
        return errors, warnings
    
    def _validate_units(self, ifc_file) -> tuple[List[QCError], List[QCError]]:
        """Validate units and measurements"""
        errors = []
        warnings = []
        
        # Check for unit assignment
        try:
            project = ifc_file.by_type("IfcProject")[0]
            if hasattr(project, 'UnitsInContext'):
                units = project.UnitsInContext
                if units is None:
                    warnings.append(QCError(
                        severity="warning",
                        category="units",
                        message="No units defined in project",
                        suggestion="Define length, area, and volume units"
                    ))
        except (IndexError, AttributeError):
            warnings.append(QCError(
                severity="warning",
                category="units",
                message="Could not verify units",
                suggestion="Ensure project has proper unit definitions"
            ))
        
        return errors, warnings
    
    def _calculate_confidence(self, errors: List[QCError], warnings: List[QCError], 
                             element_counts: Dict[str, int], project_type: str = "architecture") -> float:
        """Calculate confidence score 0-100"""
        score = 100.0
        
        # Deduct for critical errors
        critical_count = len([e for e in errors if e.severity == "critical"])
        score -= critical_count * 20
        
        # Deduct for warnings
        score -= len(warnings) * 5
        
        # Project-type-specific confidence calculations
        if project_type == "architecture":
            # Deduct for missing essential architectural elements
            if element_counts.get("IfcWall", 0) == 0:
                score -= 30
            if element_counts.get("IfcBuilding", 0) == 0:
                score -= 10
        
        
        # Bonus for having multiple element types
        element_type_count = sum(1 for v in element_counts.values() if v > 0)
        score += min(10, element_type_count * 2)
        
        return max(0.0, min(100.0, score))


class IFCAutoFixer:
    """Auto-fixes common IFC issues"""
    
    def auto_fix_ifc(self, ifc_path: str, output_path: Optional[str] = None) -> str:
        """
        Attempt to auto-fix common IFC issues
        
        Args:
            ifc_path: Path to input IFC file
            output_path: Path for fixed IFC (if None, creates new file)
            
        Returns:
            Path to fixed IFC file
        """
        if not IFC_AVAILABLE:
            raise Exception("ifcopenshell required for auto-fix")
        
        if output_path is None:
            output_path = ifc_path.replace(".ifc", "_fixed.ifc")
        
        try:
            # Open IFC
            ifc_file = ifcopenshell.open(ifc_path)
            
            # Fix: Ensure building exists
            buildings = ifc_file.by_type("IfcBuilding")
            if len(buildings) == 0:
                # Create a building (simplified - would need proper setup)
                pass  # Complex operation, skip for now
            
            # Fix: Ensure project has units
            projects = ifc_file.by_type("IfcProject")
            if projects:
                project = projects[0]
                # Add units if missing (simplified)
                pass  # Complex operation, skip for now
            
            # Save fixed file
            ifc_file.write(output_path)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Auto-fix failed: {str(e)}")


def validate_ifc(ifc_path: str, project_type: str = "architecture") -> QCReport:
    """
    Convenience function to validate IFC
    
    Args:
        ifc_path: Path to IFC file
        project_type: Project type (architecture only)
        
    Returns:
        QCReport
    """
    validator = IFCValidator()
    return validator.validate_ifc(ifc_path, project_type)


def auto_fix_ifc(ifc_path: str, output_path: Optional[str] = None) -> str:
    """
    Convenience function to auto-fix IFC
    
    Args:
        ifc_path: Path to input IFC
        output_path: Path for output (optional)
        
    Returns:
        Path to fixed IFC
    """
    fixer = IFCAutoFixer()
    return fixer.auto_fix_ifc(ifc_path, output_path)


def write_qc_report(job_id: str, report: QCReport, output_dir: str) -> str:
    """
    Write QC report to JSON and optionally PDF
    
    Args:
        job_id: Job identifier
        report: QCReport object
        output_dir: Directory to save report
        
    Returns:
        Path to report file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # JSON report
    json_path = output_path / f"{job_id}_qc_report.json"
    with open(json_path, 'w') as f:
        json.dump(asdict(report), f, indent=2)
    
    # Simple text report
    txt_path = output_path / f"{job_id}_qc_report.txt"
    with open(txt_path, 'w') as f:
        f.write(f"IFC Quality Control Report\n")
        f.write(f"{'=' * 50}\n\n")
        f.write(f"Job ID: {job_id}\n")
        f.write(f"Validation Time: {report.validation_timestamp}\n")
        f.write(f"IFC Schema: {report.ifc_schema_version or 'Unknown'}\n")
        f.write(f"File Size: {report.file_size:,} bytes\n")
        f.write(f"Valid: {'Yes' if report.valid else 'No'}\n")
        f.write(f"Confidence Score: {report.confidence_score:.1f}/100\n\n")
        
        f.write(f"Element Counts:\n")
        for elem_type, count in report.element_counts.items():
            f.write(f"  {elem_type}: {count}\n")
        f.write("\n")
        
        if report.errors:
            f.write(f"Errors ({len(report.errors)}):\n")
            for error in report.errors:
                f.write(f"  [{error.severity.upper()}] {error.category}: {error.message}\n")
                if error.suggestion:
                    f.write(f"    Suggestion: {error.suggestion}\n")
            f.write("\n")
        
        if report.warnings:
            f.write(f"Warnings ({len(report.warnings)}):\n")
            for warning in report.warnings:
                f.write(f"  [{warning.severity.upper()}] {warning.category}: {warning.message}\n")
                if warning.suggestion:
                    f.write(f"    Suggestion: {warning.suggestion}\n")
            f.write("\n")
    
    return str(json_path)

