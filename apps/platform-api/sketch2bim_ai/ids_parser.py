"""
Information Delivery Specification (IDS) Parser
Parses IDS XML files for BIM requirements validation
IDS is an open standard for defining BIM requirements and validating IFC models
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from xml.etree import ElementTree as ET
from datetime import datetime
import json

from loguru import logger


@dataclass
class IDSRequirement:
    """Represents a single requirement in an IDS file"""
    name: str
    ifc_class: str  # e.g., "IfcWall", "IfcDoor"
    applicable_entity: Optional[str] = None
    applicable_predefined_type: Optional[str] = None
    property_sets: List[Dict[str, Any]] = field(default_factory=list)
    properties: List[Dict[str, Any]] = field(default_factory=list)
    material: Optional[Dict[str, Any]] = None
    classification: Optional[Dict[str, Any]] = None


@dataclass
class IDSSpecification:
    """Represents a complete IDS specification"""
    name: str
    version: str
    description: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    requirements: List[IDSRequirement] = field(default_factory=list)


class IDSParser:
    """Parser for Information Delivery Specification (IDS) XML files"""
    
    def __init__(self):
        self.namespaces = {
            'ids': 'http://standards.buildingsmart.org/IDS'
        }
    
    def parse(self, ids_path: str) -> IDSSpecification:
        """
        Parse an IDS XML file
        
        Args:
            ids_path: Path to IDS XML file
            
        Returns:
            IDSSpecification object
        """
        if not Path(ids_path).exists():
            raise FileNotFoundError(f"IDS file not found: {ids_path}")
        
        tree = ET.parse(ids_path)
        root = tree.getroot()
        
        # Extract specification metadata
        spec = self._parse_specification(root)
        
        # Parse requirements
        spec.requirements = self._parse_requirements(root)
        
        logger.info(f"Parsed IDS specification: {spec.name} with {len(spec.requirements)} requirements")
        
        return spec
    
    def _parse_specification(self, root: ET.Element) -> IDSSpecification:
        """Parse specification metadata"""
        info_elem = root.find('.//ids:info', self.namespaces)
        
        name = ""
        version = "1.0"
        description = None
        author = None
        date = None
        
        if info_elem is not None:
            name_elem = info_elem.find('ids:name', self.namespaces)
            if name_elem is not None:
                name = name_elem.text or ""
            
            version_elem = info_elem.find('ids:version', self.namespaces)
            if version_elem is not None:
                version = version_elem.text or "1.0"
            
            description_elem = info_elem.find('ids:description', self.namespaces)
            if description_elem is not None:
                description = description_elem.text
            
            author_elem = info_elem.find('ids:author', self.namespaces)
            if author_elem is not None:
                author = author_elem.text
            
            date_elem = info_elem.find('ids:date', self.namespaces)
            if date_elem is not None:
                date = date_elem.text
        
        return IDSSpecification(
            name=name,
            version=version,
            description=description,
            author=author,
            date=date
        )
    
    def _parse_requirements(self, root: ET.Element) -> List[IDSRequirement]:
        """Parse all requirements from IDS file"""
        requirements = []
        
        # Find all specification elements (each represents a requirement)
        specs = root.findall('.//ids:specification', self.namespaces)
        
        for spec_elem in specs:
            try:
                req = self._parse_requirement(spec_elem)
                if req:
                    requirements.append(req)
            except Exception as e:
                logger.warning(f"Failed to parse requirement: {e}")
                continue
        
        return requirements
    
    def _parse_requirement(self, spec_elem: ET.Element) -> Optional[IDSRequirement]:
        """Parse a single requirement specification"""
        # Extract name
        name_elem = spec_elem.find('ids:name', self.namespaces)
        name = name_elem.text if name_elem is not None else "Unnamed Requirement"
        
        # Extract applicable entity (e.g., IfcWall)
        applicable_elem = spec_elem.find('.//ids:applicability/ids:entity', self.namespaces)
        ifc_class = applicable_elem.get('name') if applicable_elem is not None else ""
        
        if not ifc_class:
            logger.warning("Requirement missing applicable entity")
            return None
        
        # Extract predefined type if present
        predefined_type_elem = spec_elem.find('.//ids:applicability/ids:entity/ids:predefinedType', self.namespaces)
        applicable_predefined_type = predefined_type_elem.get('name') if predefined_type_elem is not None else None
        
        # Extract property sets and properties
        property_sets = self._parse_property_sets(spec_elem)
        properties = self._parse_properties(spec_elem)
        
        # Extract material requirements
        material = self._parse_material(spec_elem)
        
        # Extract classification requirements
        classification = self._parse_classification(spec_elem)
        
        return IDSRequirement(
            name=name,
            ifc_class=ifc_class,
            applicable_predefined_type=applicable_predefined_type,
            property_sets=property_sets,
            properties=properties,
            material=material,
            classification=classification
        )
    
    def _parse_property_sets(self, spec_elem: ET.Element) -> List[Dict[str, Any]]:
        """Parse property set requirements"""
        property_sets = []
        
        pset_elems = spec_elem.findall('.//ids:propertySet', self.namespaces)
        
        for pset_elem in pset_elems:
            name_elem = pset_elem.find('ids:name', self.namespaces)
            if name_elem is not None:
                property_sets.append({
                    'name': name_elem.text,
                    'required': pset_elem.get('required', 'true').lower() == 'true'
                })
        
        return property_sets
    
    def _parse_properties(self, spec_elem: ET.Element) -> List[Dict[str, Any]]:
        """Parse property requirements"""
        properties = []
        
        prop_elems = spec_elem.findall('.//ids:property', self.namespaces)
        
        for prop_elem in prop_elems:
            name_elem = prop_elem.find('ids:name', self.namespaces)
            value_elem = prop_elem.find('ids:value', self.namespaces)
            
            if name_elem is not None:
                prop_data = {
                    'name': name_elem.text,
                    'required': prop_elem.get('required', 'true').lower() == 'true'
                }
                
                if value_elem is not None:
                    # Extract value constraints
                    prop_data['value_type'] = value_elem.get('type')
                    prop_data['value'] = value_elem.text
                
                properties.append(prop_data)
        
        return properties
    
    def _parse_material(self, spec_elem: ET.Element) -> Optional[Dict[str, Any]]:
        """Parse material requirements"""
        material_elem = spec_elem.find('.//ids:material', self.namespaces)
        
        if material_elem is not None:
            return {
                'required': material_elem.get('required', 'true').lower() == 'true'
            }
        
        return None
    
    def _parse_classification(self, spec_elem: ET.Element) -> Optional[Dict[str, Any]]:
        """Parse classification requirements"""
        classification_elem = spec_elem.find('.//ids:classification', self.namespaces)
        
        if classification_elem is not None:
            return {
                'system': classification_elem.get('system'),
                'required': classification_elem.get('required', 'true').lower() == 'true'
            }
        
        return None


def load_ids_template(template_name: str) -> Optional[IDSSpecification]:
    """
    Load a predefined IDS template
    
    Args:
        template_name: Name of template (e.g., 'iso19650', 'residential', 'commercial')
        
    Returns:
        IDSSpecification or None if template not found
    """
    templates_dir = Path(__file__).parent / "ids_templates"
    
    if not templates_dir.exists():
        logger.warning(f"IDS templates directory not found: {templates_dir}")
        return None
    
    template_path = templates_dir / f"{template_name}.xml"
    
    if not template_path.exists():
        logger.warning(f"IDS template not found: {template_path}")
        return None
    
    parser = IDSParser()
    return parser.parse(str(template_path))

