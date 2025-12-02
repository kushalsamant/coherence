"""
Custom Rule Engine for Project-Specific Validation
Validates IFC models against custom rules (metadata, naming conventions, etc.)
Inspired by SortDesk Gates custom rule engine
"""
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json
import re

try:
    import ifcopenshell
    IFC_AVAILABLE = True
except ImportError:
    IFC_AVAILABLE = False

from loguru import logger


@dataclass
class ValidationRule:
    """Represents a validation rule"""
    name: str
    description: str
    rule_type: str  # metadata, naming, structure, property, custom
    enabled: bool = True
    severity: str = "warning"  # critical, warning, info
    config: Dict[str, Any] = field(default_factory=dict)
    validator: Optional[Callable] = None  # Custom validator function
    
    def __post_init__(self):
        """Initialize validator based on rule_type"""
        if self.validator is None:
            if self.rule_type == 'naming':
                self.validator = self._validate_naming_convention
            elif self.rule_type == 'metadata':
                self.validator = self._validate_metadata
            elif self.rule_type == 'property':
                self.validator = self._validate_property
            elif self.rule_type == 'structure':
                self.validator = self._validate_structure
    
    def _validate_naming_convention(self, element, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate naming convention"""
        if not hasattr(element, 'Name') or not element.Name:
            return {
                'passed': False,
                'message': f"Element {element.id()} missing Name property"
            }
        
        pattern = config.get('pattern', '.*')
        required_prefix = config.get('prefix')
        required_suffix = config.get('suffix')
        
        name = element.Name
        
        # Check pattern
        if not re.match(pattern, name):
            return {
                'passed': False,
                'message': f"Element name '{name}' does not match pattern '{pattern}'"
            }
        
        # Check prefix
        if required_prefix and not name.startswith(required_prefix):
            return {
                'passed': False,
                'message': f"Element name '{name}' should start with '{required_prefix}'"
            }
        
        # Check suffix
        if required_suffix and not name.endswith(required_suffix):
            return {
                'passed': False,
                'message': f"Element name '{name}' should end with '{required_suffix}'"
            }
        
        return {'passed': True}
    
    def _validate_metadata(self, element, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate metadata requirements"""
        required_properties = config.get('required_properties', [])
        required_psets = config.get('required_psets', [])
        
        missing_properties = []
        missing_psets = []
        
        # Check property sets
        element_psets = {}
        try:
            if hasattr(element, 'IsDefinedBy'):
                for rel in element.IsDefinedBy:
                    if rel.is_a('IfcRelDefinesByProperties'):
                        pset = rel.RelatingPropertyDefinition
                        if pset.is_a('IfcPropertySet'):
                            element_psets[pset.Name] = pset
        except Exception:
            pass
        
        for pset_name in required_psets:
            if pset_name not in element_psets:
                missing_psets.append(pset_name)
        
        # Check properties
        element_properties = {}
        for pset in element_psets.values():
            for prop in pset.HasProperties:
                element_properties[prop.Name] = prop
        
        for prop_name in required_properties:
            if prop_name not in element_properties:
                missing_properties.append(prop_name)
        
        if missing_psets or missing_properties:
            messages = []
            if missing_psets:
                messages.append(f"Missing property sets: {', '.join(missing_psets)}")
            if missing_properties:
                messages.append(f"Missing properties: {', '.join(missing_properties)}")
            
            return {
                'passed': False,
                'message': '; '.join(messages),
                'details': {
                    'missing_psets': missing_psets,
                    'missing_properties': missing_properties
                }
            }
        
        return {'passed': True}
    
    def _validate_property(self, element, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate property value"""
        property_name = config.get('property_name')
        property_set = config.get('property_set')
        expected_value = config.get('expected_value')
        value_type = config.get('value_type', 'any')
        
        if not property_name:
            return {'passed': True}  # Skip if no property specified
        
        # Get property value
        try:
            if hasattr(element, 'IsDefinedBy'):
                for rel in element.IsDefinedBy:
                    if rel.is_a('IfcRelDefinesByProperties'):
                        pset = rel.RelatingPropertyDefinition
                        if pset.is_a('IfcPropertySet'):
                            if not property_set or pset.Name == property_set:
                                for prop in pset.HasProperties:
                                    if prop.Name == property_name:
                                        prop_value = None
                                        if hasattr(prop, 'NominalValue') and prop.NominalValue:
                                            prop_value = prop.NominalValue.wrappedValue
                                        
                                        if prop_value is None:
                                            return {
                                                'passed': False,
                                                'message': f"Property '{property_name}' has no value"
                                            }
                                        
                                        # Check expected value
                                        if expected_value is not None:
                                            if prop_value != expected_value:
                                                return {
                                                    'passed': False,
                                                    'message': f"Property '{property_name}' value mismatch: expected {expected_value}, got {prop_value}"
                                                }
                                        
                                        return {'passed': True}
        except Exception as e:
            logger.warning(f"Failed to validate property: {e}")
        
        return {
            'passed': False,
            'message': f"Property '{property_name}' not found"
        }
    
    def _validate_structure(self, element, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate structural requirements"""
        required_relationships = config.get('required_relationships', [])
        required_containment = config.get('required_containment', False)
        
        issues = []
        
        # Check containment
        if required_containment:
            if not hasattr(element, 'ContainedInStructure') or not element.ContainedInStructure:
                issues.append("Element not contained in structure")
        
        # Check relationships
        for rel_type in required_relationships:
            found = False
            try:
                if hasattr(element, 'IsDefinedBy'):
                    for rel in element.IsDefinedBy:
                        if rel.is_a(rel_type):
                            found = True
                            break
            except Exception:
                pass
            
            if not found:
                issues.append(f"Missing relationship: {rel_type}")
        
        if issues:
            return {
                'passed': False,
                'message': '; '.join(issues)
            }
        
        return {'passed': True}


@dataclass
class RuleValidationResult:
    """Result of rule validation"""
    rule_name: str
    passed: bool
    element_id: Optional[str] = None
    element_type: Optional[str] = None
    message: str = ""
    severity: str = "warning"
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RuleValidationReport:
    """Complete rule validation report"""
    project_name: Optional[str] = None
    validation_timestamp: str = ""
    total_rules: int = 0
    enabled_rules: int = 0
    passed_rules: int = 0
    failed_rules: int = 0
    results: List[RuleValidationResult] = field(default_factory=list)
    
    @property
    def pass_rate(self) -> float:
        """Calculate pass rate"""
        if self.enabled_rules == 0:
            return 100.0
        return (self.passed_rules / self.enabled_rules) * 100.0


class RuleEngine:
    """Custom rule engine for IFC validation"""
    
    def __init__(self):
        self.rules: List[ValidationRule] = []
        self.rule_library: Dict[str, ValidationRule] = {}
        
        # Initialize built-in rules
        self._initialize_builtin_rules()
    
    def _initialize_builtin_rules(self):
        """Initialize built-in validation rules"""
        # Naming convention rules
        self.add_rule(ValidationRule(
            name="Wall Naming Convention",
            description="Walls should follow naming convention (e.g., WALL-###)",
            rule_type="naming",
            config={
                'ifc_class': 'IfcWall',
                'pattern': r'^[A-Z]+\d+.*',
                'prefix': None,
                'suffix': None
            }
        ))
        
        # Metadata rules
        self.add_rule(ValidationRule(
            name="Wall Metadata Required",
            description="Walls must have basic metadata (Pset_WallCommon)",
            rule_type="metadata",
            config={
                'ifc_class': 'IfcWall',
                'required_psets': ['Pset_WallCommon'],
                'required_properties': []
            }
        ))
        
        # Property rules
        self.add_rule(ValidationRule(
            name="Door Property Required",
            description="Doors should have FireRating property",
            rule_type="property",
            config={
                'ifc_class': 'IfcDoor',
                'property_set': 'Pset_DoorCommon',
                'property_name': 'FireRating',
                'value_type': 'string'
            },
            enabled=False  # Disabled by default
        ))
    
    def add_rule(self, rule: ValidationRule):
        """Add a validation rule"""
        self.rules.append(rule)
        self.rule_library[rule.name] = rule
    
    def remove_rule(self, rule_name: str):
        """Remove a validation rule"""
        self.rules = [r for r in self.rules if r.name != rule_name]
        self.rule_library.pop(rule_name, None)
    
    def load_rules_from_file(self, rules_path: str):
        """Load rules from JSON file"""
        if not Path(rules_path).exists():
            logger.warning(f"Rules file not found: {rules_path}")
            return
        
        with open(rules_path, 'r') as f:
            rules_data = json.load(f)
        
        for rule_data in rules_data.get('rules', []):
            rule = ValidationRule(**rule_data)
            self.add_rule(rule)
        
        logger.info(f"Loaded {len(rules_data.get('rules', []))} rules from {rules_path}")
    
    def save_rules_to_file(self, rules_path: str):
        """Save rules to JSON file"""
        rules_data = {
            'version': '1.0',
            'timestamp': datetime.utcnow().isoformat(),
            'rules': [
                {
                    'name': rule.name,
                    'description': rule.description,
                    'rule_type': rule.rule_type,
                    'enabled': rule.enabled,
                    'severity': rule.severity,
                    'config': rule.config
                }
                for rule in self.rules
            ]
        }
        
        with open(rules_path, 'w') as f:
            json.dump(rules_data, f, indent=2)
        
        logger.info(f"Saved {len(self.rules)} rules to {rules_path}")
    
    def validate_ifc(self, ifc_path: str, enabled_only: bool = True) -> RuleValidationReport:
        """
        Validate IFC file against all rules
        
        Args:
            ifc_path: Path to IFC file
            enabled_only: Only validate enabled rules
            
        Returns:
            RuleValidationReport
        """
        if not IFC_AVAILABLE:
            return RuleValidationReport(
                validation_timestamp=datetime.utcnow().isoformat(),
                results=[RuleValidationResult(
                    rule_name="IFC Support",
                    passed=False,
                    message="ifcopenshell not available. Cannot validate IFC files."
                )]
            )
        
        if not Path(ifc_path).exists():
            return RuleValidationReport(
                validation_timestamp=datetime.utcnow().isoformat(),
                results=[RuleValidationResult(
                    rule_name="File Access",
                    passed=False,
                    message=f"IFC file not found: {ifc_path}"
                )]
            )
        
        # Open IFC file
        try:
            ifc_file = ifcopenshell.open(ifc_path)
        except Exception as e:
            logger.error(f"Failed to open IFC file: {e}")
            return RuleValidationReport(
                validation_timestamp=datetime.utcnow().isoformat(),
                results=[RuleValidationResult(
                    rule_name="IFC Parsing",
                    passed=False,
                    message=f"Failed to parse IFC file: {str(e)}"
                )]
            )
        
        # Filter rules
        rules_to_check = [r for r in self.rules if r.enabled or not enabled_only]
        
        # Validate against each rule
        results = []
        for rule in rules_to_check:
            rule_results = self._validate_rule(ifc_file, rule)
            results.extend(rule_results)
        
        # Count passed/failed
        passed = sum(1 for r in results if r.passed)
        failed = len(results) - passed
        
        return RuleValidationReport(
            validation_timestamp=datetime.utcnow().isoformat(),
            total_rules=len(self.rules),
            enabled_rules=len(rules_to_check),
            passed_rules=passed,
            failed_rules=failed,
            results=results
        )
    
    def _validate_rule(self, ifc_file, rule: ValidationRule) -> List[RuleValidationResult]:
        """Validate a single rule against IFC file"""
        results = []
        
        # Get applicable IFC class from config
        ifc_class = rule.config.get('ifc_class')
        if not ifc_class:
            # Rule applies to all elements - validate against sample
            logger.warning(f"Rule '{rule.name}' has no ifc_class specified")
            return [RuleValidationResult(
                rule_name=rule.name,
                passed=False,
                message="Rule has no ifc_class specified"
            )]
        
        # Get elements of specified class
        try:
            elements = ifc_file.by_type(ifc_class)
        except Exception as e:
            logger.warning(f"Failed to get elements of type {ifc_class}: {e}")
            return [RuleValidationResult(
                rule_name=rule.name,
                passed=False,
                message=f"Invalid IFC class: {ifc_class}"
            )]
        
        if not elements:
            return [RuleValidationResult(
                rule_name=rule.name,
                passed=True,
                message=f"No {ifc_class} elements found (rule satisfied by absence)"
            )]
        
        # Validate each element
        for element in elements:
            if rule.validator:
                try:
                    validation_result = rule.validator(element, rule.config)
                except Exception as e:
                    logger.error(f"Error validating rule '{rule.name}': {e}")
                    validation_result = {
                        'passed': False,
                        'message': f"Validation error: {str(e)}"
                    }
                
                results.append(RuleValidationResult(
                    rule_name=rule.name,
                    passed=validation_result.get('passed', False),
                    element_id=str(element.id()),
                    element_type=element.is_a(),
                    message=validation_result.get('message', ''),
                    severity=rule.severity,
                    details=validation_result.get('details', {})
                ))
        
        return results


def create_rule_template(template_name: str, output_path: str):
    """
    Create a rule template file
    
    Args:
        template_name: Name of template (residential, commercial, custom)
        output_path: Path to save template
    """
    templates = {
        'residential': {
            'rules': [
                {
                    'name': 'Wall Naming - Residential',
                    'description': 'Walls should be named WALL-###',
                    'rule_type': 'naming',
                    'enabled': True,
                    'severity': 'warning',
                    'config': {
                        'ifc_class': 'IfcWall',
                        'pattern': r'^WALL-\d+.*',
                        'prefix': 'WALL-'
                    }
                },
                {
                    'name': 'Room Metadata - Residential',
                    'description': 'Spaces must have RoomType and Area',
                    'rule_type': 'metadata',
                    'enabled': True,
                    'severity': 'warning',
                    'config': {
                        'ifc_class': 'IfcSpace',
                        'required_properties': ['RoomType', 'Area']
                    }
                }
            ]
        },
        'commercial': {
            'rules': [
                {
                    'name': 'Fire Rating Required',
                    'description': 'Doors and walls must have fire rating',
                    'rule_type': 'property',
                    'enabled': True,
                    'severity': 'critical',
                    'config': {
                        'ifc_class': 'IfcDoor',
                        'property_set': 'Pset_DoorCommon',
                        'property_name': 'FireRating',
                        'value_type': 'string'
                    }
                }
            ]
        }
    }
    
    template = templates.get(template_name, {'rules': []})
    template['version'] = '1.0'
    template['timestamp'] = datetime.utcnow().isoformat()
    
    with open(output_path, 'w') as f:
        json.dump(template, f, indent=2)
    
    logger.info(f"Created rule template '{template_name}' at {output_path}")

