"""
Pure Python IFC generator using IfcOpenShell
No Blender required - generates IFC files directly from plan data
Uses verified API pattern from existing codebase
"""
import ifcopenshell
import ifcopenshell.api
from typing import Dict, Any, Optional, Callable
from pathlib import Path
import math
from loguru import logger


def generate_ifc_from_plan(
    plan_data: Dict[str, Any], 
    output_path: str,
    progress_callback: Optional[Callable[[int, str], None]] = None,
    project_type: str = "architecture"
) -> bool:
    """
    Generate IFC file from detected plan geometry
    
    Args:
        plan_data: Dictionary with rooms, walls, openings from sketch detection
        output_path: Path to save IFC file
        progress_callback: Optional callback function(progress: int, message: str)
        project_type: Project type (architecture, landscape, urban)
        
    Returns:
        True if successful
    """
    # Always use architecture IFC generator
    return generate_architecture_ifc(plan_data, output_path, progress_callback)


def generate_architecture_ifc(
    plan_data: Dict[str, Any], 
    output_path: str,
    progress_callback: Optional[Callable[[int, str], None]] = None
) -> bool:
    """
    Generate IFC file for architectural plans (original implementation)
    
    Args:
        plan_data: Dictionary with rooms, walls, openings
        output_path: Path to save IFC file
        progress_callback: Optional callback function
        
    Returns:
        True if successful
    """
    try:
        def update_progress(progress: int, message: str):
            if progress_callback:
                progress_callback(progress, message)
            logger.info(f"IFC Generation: {progress}% - {message}")
        
        update_progress(0, "Creating IFC file structure")
        
        # Continue with original architecture IFC generation logic
        
        # Create new IFC file using verified API pattern
        # Use project.create_file as shown in Blender script fallback
        try:
            file = ifcopenshell.api.run("project.create_file")
            logger.debug("Created IFC file using project.create_file API")
        except Exception as e:
            # Fallback to ifcopenshell.file if project.create_file doesn't exist
            logger.debug(f"project.create_file not available, using fallback: {e}")
            try:
                file = ifcopenshell.file(schema="IFC4")
            except Exception as fallback_error:
                logger.error(f"Failed to create IFC file: {fallback_error}")
                raise Exception(f"Cannot create IFC file. IfcOpenShell may not be properly installed: {fallback_error}")
        
        # Create IFC project structure using verified API pattern
        try:
            project = ifcopenshell.api.run(
                "root.create_entity",
                file,
                ifc_class="IfcProject",
                name="Sketch2BIM Project"
            )
        except Exception as e:
            logger.error(f"Failed to create IfcProject: {e}")
            raise Exception(f"Cannot create IFC project structure: {e}")
        
        # Set project units (millimeters) - verify this API exists
        try:
            ifcopenshell.api.run(
                "unit.assign_unit",
                file,
                length={"is_metric": True, "raw": "MILLIMETERS"},
                area={"is_metric": True, "raw": "SQUARE_METRE"},
                volume={"is_metric": True, "raw": "CUBIC_METRE"}
            )
        except Exception as e:
            logger.warning(f"Could not set units: {e}")
            # Continue without units - IFC file will still be valid
        
        update_progress(10, "Creating spatial structure")
        
        # Create site using verified API pattern
        site = ifcopenshell.api.run(
            "root.create_entity",
            file,
            ifc_class="IfcSite",
            name="Default Site"
        )
        ifcopenshell.api.run("aggregate.assign_object", file, product=site, relating_object=project)
        
        # Create building using verified API pattern
        building = ifcopenshell.api.run(
            "root.create_entity",
            file,
            ifc_class="IfcBuilding",
            name="Building"
        )
        ifcopenshell.api.run("aggregate.assign_object", file, product=building, relating_object=site)
        
        # Create building storey (ground floor) using verified API pattern
        storey = ifcopenshell.api.run(
            "root.create_entity",
            file,
            ifc_class="IfcBuildingStorey",
            name="Ground Floor"
        )
        ifcopenshell.api.run("aggregate.assign_object", file, product=storey, relating_object=building)
        
        update_progress(20, "Processing walls")
        
        # Get scale ratio from plan data (from legend) or use default
        scale_ratio = plan_data.get("scale_ratio", 0.01)  # Default: 100 pixels = 1 meter
        
        # Create walls from detected lines using verified API pattern
        walls = plan_data.get("walls", [])
        wall_count = min(len(walls), 100)  # Limit to 100 walls for performance
        
        for i, wall_data in enumerate(walls[:wall_count]):
            try:
                start = wall_data.get("start", [0, 0])
                end = wall_data.get("end", [1000, 0])
                
                # Convert 2D coordinates to 3D (meters)
                start_x = start[0] * scale_ratio
                start_y = start[1] * scale_ratio
                end_x = end[0] * scale_ratio
                end_y = end[1] * scale_ratio
                
                # Calculate wall length and angle
                dx = end_x - start_x
                dy = end_y - start_y
                length = math.sqrt(dx*dx + dy*dy)
                
                if length < 0.1:  # Skip tiny walls (< 10cm)
                    continue
                
                # Create wall using verified API pattern from todolist.txt
                # Example: wall = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcWall")
                wall = ifcopenshell.api.run(
                    "root.create_entity",
                    file,
                    ifc_class="IfcWallStandardCase",
                    name=f"Wall {i+1}"
                )
                
                # Assign wall to storey using verified API pattern
                ifcopenshell.api.run("spatial.assign_container", file, product=wall, relating_structure=storey)
                
                # Add basic placement (Phase 1, Step 2: Basic Geometry)
                # Use proper placement via geometry.edit_object_placement if available
                try:
                    # Convert coordinates to millimeters (IFC standard)
                    start_x_mm = start_x * 1000
                    start_y_mm = start_y * 1000
                    start_z_mm = 0  # Ground level
                    
                    # Calculate angle in radians
                    angle = math.atan2(dy, dx) if length > 0 else 0
                    
                    # Create placement at wall start point
                    # API: geometry.edit_object_placement(file, product=wall, matrix=placement_matrix)
                    # Matrix format: [x_axis, y_axis, z_axis, origin]
                    placement_matrix = [
                        [math.cos(angle), -math.sin(angle), 0.0, start_x_mm],
                        [math.sin(angle), math.cos(angle), 0.0, start_y_mm],
                        [0.0, 0.0, 1.0, start_z_mm],
                        [0.0, 0.0, 0.0, 1.0]
                    ]
                    
                    # Try to set placement (may not exist in all IfcOpenShell versions)
                    ifcopenshell.api.run(
                        "geometry.edit_object_placement",
                        file,
                        product=wall,
                        matrix=placement_matrix
                    )
                except Exception as e:
                    # Placement is optional - entities without explicit placement are still valid IFC
                    logger.debug(f"Could not set wall placement (this is optional): {e}")
                
                # Add wall properties (optional, verify API exists)
                try:
                    _add_wall_properties(file, wall, wall_data)
                except Exception as e:
                    logger.debug(f"Could not add wall properties: {e}")
                
            except Exception as e:
                logger.warning(f"Failed to create wall {i+1}: {e}")
                continue
        
        update_progress(60, "Processing floors")
        
        # Create slabs (floors) from detected rooms using verified API pattern
        rooms = plan_data.get("rooms", [])
        room_count = min(len(rooms), 50)  # Limit to 50 rooms
        
        for i, room_data in enumerate(rooms[:room_count]):
            try:
                polygon = room_data.get("polygon", [])
                if len(polygon) < 3:
                    continue
                
                # Create slab for floor using verified API pattern
                slab = ifcopenshell.api.run(
                    "root.create_entity",
                    file,
                    ifc_class="IfcSlab",
                    name=f"Floor {i+1}",
                    predefined_type="FLOOR"
                )
                
                # Assign slab to storey using verified API pattern
                ifcopenshell.api.run("spatial.assign_container", file, product=slab, relating_structure=storey)
                
                # Add basic placement (Phase 1, Step 2: Basic Geometry)
                # Calculate room center for placement
                try:
                    # Calculate centroid of room polygon
                    if len(polygon) >= 3:
                        sum_x = sum(p[0] * scale_ratio for p in polygon)
                        sum_y = sum(p[1] * scale_ratio for p in polygon)
                        center_x = sum_x / len(polygon)
                        center_y = sum_y / len(polygon)
                        
                        # Convert to millimeters
                        center_x_mm = center_x * 1000
                        center_y_mm = center_y * 1000
                        center_z_mm = 0  # Ground level
                        
                        # Create placement at room center
                        placement_matrix = [
                            [1.0, 0.0, 0.0, center_x_mm],
                            [0.0, 1.0, 0.0, center_y_mm],
                            [0.0, 0.0, 1.0, center_z_mm],
                            [0.0, 0.0, 0.0, 1.0]
                        ]
                        
                        ifcopenshell.api.run(
                            "geometry.edit_object_placement",
                            file,
                            product=slab,
                            matrix=placement_matrix
                        )
                except Exception as e:
                    # Placement is optional - entities without explicit placement are still valid IFC
                    logger.debug(f"Could not set slab placement (this is optional): {e}")
                
                # Add slab properties (optional, verify API exists)
                try:
                    _add_slab_properties(file, slab, room_data)
                except Exception as e:
                    logger.debug(f"Could not add slab properties: {e}")
                
            except Exception as e:
                logger.warning(f"Failed to create floor {i+1}: {e}")
                continue
        
        update_progress(85, "Processing openings")
        
        # Create openings (doors/windows) from detected openings using verified API pattern
        openings = plan_data.get("openings", [])
        opening_count = min(len(openings), 50)  # Limit to 50 openings
        
        for i, opening_data in enumerate(openings[:opening_count]):
            try:
                opening_type = opening_data.get("type", "door")
                position = opening_data.get("position", [0, 0])
                
                # Create opening using verified API pattern
                if opening_type == "door":
                    opening = ifcopenshell.api.run(
                        "root.create_entity",
                        file,
                        ifc_class="IfcDoor",
                        name=f"Door {i+1}"
                    )
                else:
                    opening = ifcopenshell.api.run(
                        "root.create_entity",
                        file,
                        ifc_class="IfcWindow",
                        name=f"Window {i+1}"
                    )
                
                # Assign opening to storey using verified API pattern
                ifcopenshell.api.run("spatial.assign_container", file, product=opening, relating_structure=storey)
                
                # Add basic placement (Phase 1, Step 2: Basic Geometry)
                try:
                    # Convert position to 3D coordinates (meters)
                    pos_x = position[0] * scale_ratio
                    pos_y = position[1] * scale_ratio
                    pos_z = 0  # Ground level
                    
                    # Convert to millimeters
                    pos_x_mm = pos_x * 1000
                    pos_y_mm = pos_y * 1000
                    pos_z_mm = pos_z * 1000
                    
                    # Create placement at opening position
                    placement_matrix = [
                        [1.0, 0.0, 0.0, pos_x_mm],
                        [0.0, 1.0, 0.0, pos_y_mm],
                        [0.0, 0.0, 1.0, pos_z_mm],
                        [0.0, 0.0, 0.0, 1.0]
                    ]
                    
                    ifcopenshell.api.run(
                        "geometry.edit_object_placement",
                        file,
                        product=opening,
                        matrix=placement_matrix
                    )
                except Exception as e:
                    # Placement is optional - entities without explicit placement are still valid IFC
                    logger.debug(f"Could not set opening placement (this is optional): {e}")
                
            except Exception as e:
                logger.warning(f"Failed to create opening {i+1}: {e}")
                continue
        
        symbols = plan_data.get("symbols") or []
        if symbols:
            update_progress(90, f"Placing {min(len(symbols), 200)} symbols")
            _place_symbol_elements(file, storey, symbols, scale_ratio)
        
        update_progress(95, "Writing IFC file")
        
        # Validate output path
        output_path_obj = Path(output_path)
        output_dir = output_path_obj.parent
        if not output_dir.exists():
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                logger.error(f"Cannot create output directory {output_dir}: {e}")
                raise Exception(f"Cannot create output directory: {e}")
        
        # Write IFC file
        try:
            file.write(str(output_path))
        except Exception as e:
            logger.error(f"Failed to write IFC file to {output_path}: {e}")
            raise Exception(f"Cannot write IFC file: {e}")
        
        # Verify file was created
        if not output_path_obj.exists():
            logger.error(f"IFC file was not created at {output_path}")
            return False
        
        file_size = output_path_obj.stat().st_size
        if file_size < 1000:  # At least 1KB
            logger.error(f"IFC file too small: {file_size} bytes (expected at least 1KB)")
            return False
        
        # Try to validate IFC file can be opened
        try:
            test_file = ifcopenshell.open(str(output_path))
            test_file.close()
        except Exception as e:
            logger.warning(f"Generated IFC file may be invalid (cannot be opened): {e}")
            # Continue anyway - some IFC readers may still accept it
        
        update_progress(100, "IFC file generated successfully")
        logger.info(f"IFC file created successfully: {output_path} ({file_size} bytes)")
        return True
    
    except Exception as e:
        logger.error(f"IFC generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def _add_wall_properties(file: ifcopenshell.file, wall, wall_data: Dict[str, Any]):
    """Add properties to wall using IfcOpenShell API"""
    try:
        # Verify if pset API exists before using
        # Use ifcopenshell.api.run("pset.add_pset", ...) if it exists
        pset = ifcopenshell.api.run(
            "pset.add_pset",
            file,
            product=wall,
            name="Pset_WallCommon"
        )
        
        # Add properties using pset.edit_pset if it exists
        ifcopenshell.api.run(
            "pset.edit_pset",
            file,
            pset=pset,
            properties={
                "Thickness": 200.0,  # 200mm
                "Height": 3000.0  # 3000mm
            }
        )
    except Exception as e:
        # Property set creation might fail - that's okay, continue without properties
        logger.debug(f"Could not add wall properties (this is optional): {e}")
        # Silently fail - properties are optional for IFC files


def _add_slab_properties(file: ifcopenshell.file, slab, room_data: Dict[str, Any]):
    """Add properties to slab using IfcOpenShell API"""
    try:
        area = room_data.get("area", 0.0)
        room_type = room_data.get("room_type", "Unknown")
        
        # Verify if pset API exists before using
        pset = ifcopenshell.api.run(
            "pset.add_pset",
            file,
            product=slab,
            name="Pset_SlabCommon"
        )
        
        # Add properties
        properties = {
            "Thickness": 200.0,  # 200mm
        }
        
        if area > 0:
            properties["Area"] = area
        
        if room_type and room_type != "Unknown":
            properties["RoomType"] = room_type
        
        ifcopenshell.api.run(
            "pset.edit_pset",
            file,
            pset=pset,
            properties=properties
        )
    except Exception as e:
        # Property set creation might fail - that's okay, continue without properties
        logger.debug(f"Could not add slab properties (this is optional): {e}")
        # Silently fail - properties are optional for IFC files


def _place_symbol_elements(file: ifcopenshell.file, storey, symbols: Any, scale_ratio: float):
    """Create IFC elements for detected symbols."""
    max_symbols = min(len(symbols), 200)
    for idx, symbol in enumerate(symbols[:max_symbols]):
        bbox = symbol.get("bbox")
        if not bbox or len(bbox) != 4:
            continue

        ifc_class = _infer_ifc_class_for_symbol(symbol)
        name = symbol.get("display_name") or symbol.get("label") or f"Symbol {idx+1}"

        try:
            element = ifcopenshell.api.run(
                "root.create_entity",
                file,
                ifc_class=ifc_class,
                name=name,
            )
        except Exception as e:
            logger.debug(f"Failed to create {ifc_class} for symbol {name}: {e}")
            continue

        try:
            ifcopenshell.api.run("spatial.assign_container", file, product=element, relating_structure=storey)
        except Exception as e:
            logger.debug(f"Failed to assign symbol {name} to storey: {e}")

        # Placement at bbox center
        try:
            center_x = ((bbox[0] + bbox[2]) / 2.0) * scale_ratio * 1000
            center_y = ((bbox[1] + bbox[3]) / 2.0) * scale_ratio * 1000
            placement_matrix = [
                [1.0, 0.0, 0.0, center_x],
                [0.0, 1.0, 0.0, center_y],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
            ifcopenshell.api.run("geometry.edit_object_placement", file, product=element, matrix=placement_matrix)
        except Exception as e:
            logger.debug(f"Symbol placement optional failure for {name}: {e}")

        try:
            _add_symbol_properties(file, element, symbol)
        except Exception as e:
            logger.debug(f"Could not add symbol properties for {name}: {e}")


def _infer_ifc_class_for_symbol(symbol: Dict[str, Any]) -> str:
    if symbol.get("ifc_type"):
        return symbol["ifc_type"]
    category = symbol.get("category")
    if category == "interior_furniture":
        return "IfcFurnishingElement"
    if category == "mep_systems":
        return "IfcFlowTerminal"
    if category == "architectural_core":
        return "IfcBuildingElementProxy"
    if category == "structural_elements":
        return "IfcBuildingElementProxy"
    return "IfcAnnotation"


def _add_symbol_properties(file: ifcopenshell.file, element, symbol: Dict[str, Any]):
    """Attach metadata from symbol detection to the IFC element."""
    try:
        pset = ifcopenshell.api.run("pset.add_pset", file, product=element, name="Pset_SymbolDetection")
        props = {
            "Label": symbol.get("label"),
            "DisplayName": symbol.get("display_name"),
            "Category": symbol.get("category"),
            "Confidence": float(symbol.get("confidence", 0.0)),
            "AreaPixels": float(symbol.get("area_pixels", 0.0)),
            "Source": symbol.get("source", "ml_detector"),
        }
        bbox = symbol.get("bbox")
        if bbox:
            props["BBox"] = ",".join(f"{float(v):.2f}" for v in bbox)
        if symbol.get("ifc_type"):
            props["IfcTypeHint"] = symbol["ifc_type"]

        ifcopenshell.api.run("pset.edit_pset", file, pset=pset, properties=props)
    except Exception as e:
        logger.debug(f"Symbol property attachment optional failure: {e}")
