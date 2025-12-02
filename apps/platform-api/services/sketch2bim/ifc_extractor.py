"""
IFC Data Extractor
Extracts structured data from IFC models (COBie, property sets, etc.)
"""
from typing import Dict, List, Any, Optional
from pathlib import Path
import ifcopenshell
import ifcopenshell.util.element
from loguru import logger


class IFCExtractor:
    """
    Extracts structured data from IFC models
    Supports COBie format, custom property sets, and various export formats
    """
    
    def __init__(self):
        pass
    
    def extract_cobie_data(self, ifc_file_path: str) -> Dict[str, Any]:
        """
        Extract COBie (Construction Operations Building Information Exchange) data
        
        Args:
            ifc_file_path: Path to IFC file
            
        Returns:
            Dictionary with COBie data structure
        """
        try:
            ifc_file = ifcopenshell.open(ifc_file_path)
            
            cobie_data = {
                'facility': self._extract_facility(ifc_file),
                'floors': self._extract_floors(ifc_file),
                'spaces': self._extract_spaces(ifc_file),
                'zones': self._extract_zones(ifc_file),
                'types': self._extract_types(ifc_file),
                'components': self._extract_components(ifc_file),
                'systems': self._extract_systems(ifc_file),
                'attributes': self._extract_attributes(ifc_file),
            }
            
            logger.info("COBie data extraction complete")
            return cobie_data
            
        except Exception as e:
            logger.error(f"COBie extraction failed: {e}")
            raise
    
    def _extract_facility(self, ifc_file: ifcopenshell.file) -> Dict[str, Any]:
        """Extract facility information"""
        facility = {}
        
        # Get project
        projects = ifc_file.by_type("IfcProject")
        if projects:
            project = projects[0]
            facility['name'] = project.Name or 'Unnamed Project'
            facility['description'] = project.Description or ''
            facility['global_id'] = str(project.GlobalId) if hasattr(project, 'GlobalId') else None
        
        # Get site
        sites = ifc_file.by_type("IfcSite")
        if sites:
            site = sites[0]
            facility['site_name'] = site.Name or ''
            facility['site_description'] = site.Description or ''
        
        return facility
    
    def _extract_floors(self, ifc_file: ifcopenshell.file) -> List[Dict[str, Any]]:
        """Extract floor/storey information"""
        floors = []
        
        storeys = ifc_file.by_type("IfcBuildingStorey")
        for storey in storeys:
            floor_data = {
                'name': storey.Name or 'Unnamed Floor',
                'description': storey.Description or '',
                'elevation': float(storey.Elevation) if hasattr(storey, 'Elevation') and storey.Elevation else None,
                'global_id': str(storey.GlobalId) if hasattr(storey, 'GlobalId') else None,
            }
            floors.append(floor_data)
        
        return floors
    
    def _extract_spaces(self, ifc_file: ifcopenshell.file) -> List[Dict[str, Any]]:
        """Extract space information"""
        spaces = []
        
        ifc_spaces = ifc_file.by_type("IfcSpace")
        for space in ifc_spaces:
            space_data = {
                'name': space.Name or 'Unnamed Space',
                'description': space.Description or '',
                'long_name': space.LongName or '',
                'global_id': str(space.GlobalId) if hasattr(space, 'GlobalId') else None,
            }
            
            # Get property sets
            psets = ifcopenshell.util.element.get_psets(space)
            if psets:
                space_data['properties'] = psets
            
            spaces.append(space_data)
        
        return spaces
    
    def _extract_zones(self, ifc_file: ifcopenshell.file) -> List[Dict[str, Any]]:
        """Extract zone information"""
        zones = []
        
        ifc_zones = ifc_file.by_type("IfcZone")
        for zone in ifc_zones:
            zone_data = {
                'name': zone.Name or 'Unnamed Zone',
                'description': zone.Description or '',
                'global_id': str(zone.GlobalId) if hasattr(zone, 'GlobalId') else None,
            }
            zones.append(zone_data)
        
        return zones
    
    def _extract_types(self, ifc_file: ifcopenshell.file) -> List[Dict[str, Any]]:
        """Extract type/product information"""
        types = []
        
        # Get product types
        type_classes = [
            "IfcWallType",
            "IfcDoorType",
            "IfcWindowType",
            "IfcSlabType",
            "IfcBeamType",
            "IfcColumnType",
        ]
        
        for type_class in type_classes:
            ifc_types = ifc_file.by_type(type_class)
            for ifc_type in ifc_types:
                type_data = {
                    'name': ifc_type.Name or 'Unnamed Type',
                    'type': type_class,
                    'description': ifc_type.Description or '',
                    'global_id': str(ifc_type.GlobalId) if hasattr(ifc_type, 'GlobalId') else None,
                }
                
                # Get property sets
                psets = ifcopenshell.util.element.get_psets(ifc_type)
                if psets:
                    type_data['properties'] = psets
                
                types.append(type_data)
        
        return types
    
    def _extract_components(self, ifc_file: ifcopenshell.file) -> List[Dict[str, Any]]:
        """Extract component/product information"""
        components = []
        
        # Get products
        product_classes = [
            "IfcWall",
            "IfcDoor",
            "IfcWindow",
            "IfcSlab",
            "IfcBeam",
            "IfcColumn",
            "IfcRoof",
            "IfcStair",
        ]
        
        for product_class in product_classes:
            products = ifc_file.by_type(product_class)
            for product in products:
                component_data = {
                    'name': product.Name or 'Unnamed Component',
                    'type': product_class,
                    'description': product.Description or '',
                    'global_id': str(product.GlobalId) if hasattr(product, 'GlobalId') else None,
                }
                
                # Get property sets
                psets = ifcopenshell.util.element.get_psets(product)
                if psets:
                    component_data['properties'] = psets
                
                components.append(component_data)
        
        return components
    
    def _extract_systems(self, ifc_file: ifcopenshell.file) -> List[Dict[str, Any]]:
        """Extract system information (MEP systems)"""
        systems = []
        
        ifc_systems = ifc_file.by_type("IfcSystem")
        for system in ifc_systems:
            system_data = {
                'name': system.Name or 'Unnamed System',
                'description': system.Description or '',
                'global_id': str(system.GlobalId) if hasattr(system, 'GlobalId') else None,
            }
            systems.append(system_data)
        
        return systems
    
    def _extract_attributes(self, ifc_file: ifcopenshell.file) -> Dict[str, Any]:
        """Extract general attributes and metadata"""
        attributes = {
            'schema_version': ifc_file.schema,
            'file_name': ifc_file.wrapped_data.file_name if hasattr(ifc_file, 'wrapped_data') else None,
        }
        
        return attributes
    
    def extract_property_sets(
        self,
        ifc_file_path: str,
        pset_names: Optional[List[str]] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract specific property sets from IFC model
        
        Args:
            ifc_file_path: Path to IFC file
            pset_names: Optional list of property set names to extract
            
        Returns:
            Dictionary mapping property set names to lists of property data
        """
        try:
            ifc_file = ifcopenshell.open(ifc_file_path)
            result = {}
            
            # Get all products
            products = ifc_file.by_type("IfcProduct")
            
            for product in products:
                psets = ifcopenshell.util.element.get_psets(product)
                
                for pset_name, pset_props in psets.items():
                    if pset_names and pset_name not in pset_names:
                        continue
                    
                    if pset_name not in result:
                        result[pset_name] = []
                    
                    result[pset_name].append({
                        'element_name': product.Name or 'Unnamed',
                        'element_type': product.is_a(),
                        'element_id': product.id(),
                        'properties': pset_props,
                    })
            
            logger.info(f"Extracted {len(result)} property sets")
            return result
            
        except Exception as e:
            logger.error(f"Property set extraction failed: {e}")
            raise

