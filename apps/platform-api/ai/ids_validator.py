"""
IDS (Information Delivery Specification) Validator
Validates IFC files against IDS specifications
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

try:
    import ifcopenshell
    IFC_AVAILABLE = True
except ImportError:
    IFC_AVAILABLE = False

from .ids_parser import IDSSpecification, IDSRequirement
from loguru import logger


@dataclass
class IDSValidationResult:
    """Result of IDS validation"""
    passed: bool
    requirement_name: str
    ifc_class: str
    element_id: Optional[str] = None
    element_type: Optional[str] = None
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IDSValidationReport:
    """Complete IDS validation report"""
    specification_name: str
    specification_version: str
    validation_timestamp: str
    total_requirements: int
    passed_requirements: int
    failed_requirements: int
    results: List[IDSValidationResult] = field(default_factory=list)
    
    @property
    def pass_rate(self) -> float:
        """Calculate pass rate as percentage"""
        if self.total_requirements == 0:
            return 0.0
        return (self.passed_requirements / self.total_requirements) * 100.0
    
    @property
    def all_passed(self) -> bool:
        """Check if all requirements passed"""
        return self.failed_requirements == 0


class IDSValidator:
    """Validates IFC files against IDS specifications"""
    
    def __init__(self):
        if not IFC_AVAILABLE:
            logger.warning("ifcopenshell not available. IDS validation will be limited.")
    
    def validate(self, ifc_path: str, ids_spec: IDSSpecification) -> IDSValidationReport:
        """
        Validate IFC file against IDS specification
        
        Args:
            ifc_path: Path to IFC file
            ids_spec: IDS specification to validate against
            
        Returns:
            IDSValidationReport with validation results
        """
        if not IFC_AVAILABLE:
            return IDSValidationReport(
                specification_name=ids_spec.name,
                specification_version=ids_spec.version,
                validation_timestamp=datetime.utcnow().isoformat(),
                total_requirements=len(ids_spec.requirements),
                passed_requirements=0,
                failed_requirements=0,
                results=[IDSValidationResult(
                    passed=False,
                    requirement_name="IFC Support",
                    ifc_class="",
                    message="ifcopenshell not available. Cannot validate IFC files."
                )]
            )
        
        if not Path(ifc_path).exists():
            return IDSValidationReport(
                specification_name=ids_spec.name,
                specification_version=ids_spec.version,
                validation_timestamp=datetime.utcnow().isoformat(),
                total_requirements=len(ids_spec.requirements),
                passed_requirements=0,
                failed_requirements=0,
                results=[IDSValidationResult(
                    passed=False,
                    requirement_name="File Access",
                    ifc_class="",
                    message=f"IFC file not found: {ifc_path}"
                )]
            )
        
        # Open IFC file
        try:
            ifc_file = ifcopenshell.open(ifc_path)
        except Exception as e:
            logger.error(f"Failed to open IFC file: {e}")
            return IDSValidationReport(
                specification_name=ids_spec.name,
                specification_version=ids_spec.version,
                validation_timestamp=datetime.utcnow().isoformat(),
                total_requirements=len(ids_spec.requirements),
                passed_requirements=0,
                failed_requirements=0,
                results=[IDSValidationResult(
                    passed=False,
                    requirement_name="IFC Parsing",
                    ifc_class="",
                    message=f"Failed to parse IFC file: {str(e)}"
                )]
            )
        
        # Validate each requirement
        results = []
        for requirement in ids_spec.requirements:
            req_results = self._validate_requirement(ifc_file, requirement)
            results.extend(req_results)
        
        # Count passed/failed
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        
        return IDSValidationReport(
            specification_name=ids_spec.name,
            specification_version=ids_spec.version,
            validation_timestamp=datetime.utcnow().isoformat(),
            total_requirements=len(results),
            passed_requirements=passed,
            failed_requirements=failed,
            results=results
        )
    
    def _validate_requirement(self, ifc_file, requirement: IDSRequirement) -> List[IDSValidationResult]:
        """Validate a single IDS requirement against IFC file"""
        results = []
        
        # Get all elements of the required IFC class
        try:
            elements = ifc_file.by_type(requirement.ifc_class)
        except Exception as e:
            logger.warning(f"Failed to get elements of type {requirement.ifc_class}: {e}")
            return [IDSValidationResult(
                passed=False,
                requirement_name=requirement.name,
                ifc_class=requirement.ifc_class,
                message=f"Invalid IFC class: {requirement.ifc_class}"
            )]
        
        if not elements:
            # No elements found - check if this is a failure
            return [IDSValidationResult(
                passed=False,
                requirement_name=requirement.name,
                ifc_class=requirement.ifc_class,
                message=f"No {requirement.ifc_class} elements found in IFC file"
            )]
        
        # Validate each element
        for element in elements:
            result = self._validate_element(element, requirement)
            results.append(result)
        
        return results
    
    def _validate_element(self, element, requirement: IDSRequirement) -> IDSValidationResult:
        """Validate a single IFC element against a requirement"""
        element_id = str(element.id())
        element_type = element.is_a()
        
        # Check predefined type if required
        if requirement.applicable_predefined_type:
            if hasattr(element, 'PredefinedType'):
                if element.PredefinedType != requirement.applicable_predefined_type:
                    return IDSValidationResult(
                        passed=False,
                        requirement_name=requirement.name,
                        ifc_class=requirement.ifc_class,
                        element_id=element_id,
                        element_type=element_type,
                        message=f"PredefinedType mismatch: expected {requirement.applicable_predefined_type}, got {element.PredefinedType}",
                        details={'expected_type': requirement.applicable_predefined_type, 'actual_type': element.PredefinedType}
                    )
        
        # Validate property sets
        property_validation = self._validate_property_sets(element, requirement)
        if not property_validation['passed']:
            return IDSValidationResult(
                passed=False,
                requirement_name=requirement.name,
                ifc_class=requirement.ifc_class,
                element_id=element_id,
                element_type=element_type,
                message=property_validation['message'],
                details=property_validation.get('details', {})
            )
        
        # Validate properties
        property_validation = self._validate_properties(element, requirement)
        if not property_validation['passed']:
            return IDSValidationResult(
                passed=False,
                requirement_name=requirement.name,
                ifc_class=requirement.ifc_class,
                element_id=element_id,
                element_type=element_type,
                message=property_validation['message'],
                details=property_validation.get('details', {})
            )
        
        # Validate material if required
        if requirement.material and requirement.material.get('required'):
            material_validation = self._validate_material(element)
            if not material_validation['passed']:
                return IDSValidationResult(
                    passed=False,
                    requirement_name=requirement.name,
                    ifc_class=requirement.ifc_class,
                    element_id=element_id,
                    element_type=element_type,
                    message=material_validation['message']
                )
        
        # All checks passed
        return IDSValidationResult(
            passed=True,
            requirement_name=requirement.name,
            ifc_class=requirement.ifc_class,
            element_id=element_id,
            element_type=element_type,
            message="Requirement satisfied"
        )
    
    def _validate_property_sets(self, element, requirement: IDSRequirement) -> Dict[str, Any]:
        """Validate property sets on element"""
        if not requirement.property_sets:
            return {'passed': True}
        
        # Get property sets from element
        try:
            if hasattr(element, 'IsDefinedBy'):
                element_psets = {}
                for rel in element.IsDefinedBy:
                    if rel.is_a('IfcRelDefinesByProperties'):
                        pset = rel.RelatingPropertyDefinition
                        if pset.is_a('IfcPropertySet'):
                            element_psets[pset.Name] = pset
            else:
                element_psets = {}
        except Exception as e:
            logger.warning(f"Failed to get property sets: {e}")
            element_psets = {}
        
        # Check required property sets
        for pset_req in requirement.property_sets:
            if pset_req['required'] and pset_req['name'] not in element_psets:
                return {
                    'passed': False,
                    'message': f"Required property set '{pset_req['name']}' not found",
                    'details': {'missing_pset': pset_req['name']}
                }
        
        return {'passed': True}
    
    def _validate_properties(self, element, requirement: IDSRequirement) -> Dict[str, Any]:
        """Validate properties on element"""
        if not requirement.properties:
            return {'passed': True}
        
        # Get all properties from element
        element_properties = {}
        try:
            if hasattr(element, 'IsDefinedBy'):
                for rel in element.IsDefinedBy:
                    if rel.is_a('IfcRelDefinesByProperties'):
                        pset = rel.RelatingPropertyDefinition
                        if pset.is_a('IfcPropertySet'):
                            for prop in pset.HasProperties:
                                element_properties[prop.Name] = prop
        except Exception as e:
            logger.warning(f"Failed to get properties: {e}")
            element_properties = {}
        
        # Check required properties
        for prop_req in requirement.properties:
            if prop_req['required']:
                if prop_req['name'] not in element_properties:
                    return {
                        'passed': False,
                        'message': f"Required property '{prop_req['name']}' not found",
                        'details': {'missing_property': prop_req['name']}
                    }
                
                # Validate property value if specified
                if 'value' in prop_req:
                    prop = element_properties[prop_req['name']]
                    prop_value = self._get_property_value(prop)
                    
                    if prop_value != prop_req['value']:
                        return {
                            'passed': False,
                            'message': f"Property '{prop_req['name']}' value mismatch: expected {prop_req['value']}, got {prop_value}",
                            'details': {
                                'property': prop_req['name'],
                                'expected': prop_req['value'],
                                'actual': prop_value
                            }
                        }
        
        return {'passed': True}
    
    def _get_property_value(self, prop) -> Any:
        """Extract property value from IFC property"""
        if hasattr(prop, 'NominalValue'):
            if prop.NominalValue:
                return prop.NominalValue.wrappedValue
        return None
    
    def _validate_material(self, element) -> Dict[str, Any]:
        """Validate material on element"""
        try:
            if hasattr(element, 'HasAssignments'):
                for assignment in element.HasAssignments:
                    if assignment.is_a('IfcRelAssociatesMaterial'):
                        return {'passed': True, 'message': 'Material found'}
        except Exception:
            pass
        
        return {'passed': False, 'message': 'Required material not found'}


def validate_ifc_against_ids(ifc_path: str, ids_spec: IDSSpecification) -> IDSValidationReport:
    """
    Convenience function to validate IFC against IDS
    
    Args:
        ifc_path: Path to IFC file
        ids_spec: IDS specification
        
    Returns:
        IDSValidationReport
    """
    validator = IDSValidator()
    return validator.validate(ifc_path, ids_spec)

