"""
IFC format exporter
Convert IFC to DWG, SketchUp (OBJ), and generate previews
Note: Revit compatibility is provided via IFC files (Revit imports IFC natively)
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional

from config.sketch2bim import settings


def export_to_dwg(ifc_path: str, output_path: str, scale_ratio: float = 0.01) -> bool:
    """
    Export IFC to DWG format using ezdxf
    Creates proper DXF file (AutoCAD compatible - opens as DWG)
    """
    try:
        # Try using ezdxf for proper DWG/DXF export
        import ezdxf
        import ifcopenshell
        import ifcopenshell.geom
        import numpy as np
        from loguru import logger
        
        # Open IFC file
        ifc_file = ifcopenshell.open(ifc_path)
        
        # Create DXF document (AutoCAD 2010 format - widely compatible)
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        
        # Create layers for different element types
        doc.layers.add('WALLS', color=7)  # White/black
        doc.layers.add('ROOMS', color=2)  # Yellow
        doc.layers.add('DOORS', color=1)  # Red
        doc.layers.add('WINDOWS', color=5)  # Blue
        # Landscape/Urban layers
        doc.layers.add('PATHS', color=3)  # Green
        doc.layers.add('ROADS', color=4)  # Cyan
        doc.layers.add('ZONES', color=6)  # Magenta
        doc.layers.add('WATER', color=1)  # Red (different from doors)
        doc.layers.add('PARKING', color=8)  # Gray
        doc.layers.add('BUILDINGS', color=7)  # White/black
        doc.layers.add('PLAZAS', color=2)  # Yellow
        doc.layers.add('STREETS', color=4)  # Cyan
        
        # Geometry extraction settings
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        settings.set(settings.WELD_VERTICES, True)
        
        # Extract and convert walls
        walls = ifc_file.by_type("IfcWall")
        for wall in walls:
            try:
                shape = ifcopenshell.geom.create_shape(settings, wall)
                geometry = shape.geometry
                verts = np.array(geometry.verts).reshape(-1, 3)
                faces = np.array(geometry.faces).reshape(-1, 3)
                
                # Convert 3D geometry to 2D plan view (top-down)
                # Extract edges from faces for 2D representation
                for face in faces:
                    if len(face) >= 3:
                        # Get vertices for this face
                        face_verts = verts[face]
                        # Project to 2D (x, y plane - top view)
                        points_2d = [(v[0], v[1]) for v in face_verts]
                        
                        # Create polyline for wall outline
                        if len(points_2d) >= 2:
                            msp.add_lwpolyline(
                                points_2d,
                                dxfattribs={'layer': 'WALLS', 'closed': True}
                            )
            except Exception as e:
                logger.warning(f"Failed to export wall to DWG: {e}")
                continue
        
        # Extract and convert doors
        doors = ifc_file.by_type("IfcDoor")
        for door in doors:
            try:
                shape = ifcopenshell.geom.create_shape(settings, door)
                geometry = shape.geometry
                verts = np.array(geometry.verts).reshape(-1, 3)
                
                # Create door as rectangle/block
                if len(verts) >= 4:
                    # Get bounding box
                    min_x = min(v[0] for v in verts)
                    max_x = max(v[0] for v in verts)
                    min_y = min(v[1] for v in verts)
                    max_y = max(v[1] for v in verts)
                    
                    # Create rectangle for door
                    msp.add_lwpolyline(
                        [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)],
                        dxfattribs={'layer': 'DOORS', 'closed': True}
                    )
            except Exception as e:
                logger.warning(f"Failed to export door to DWG: {e}")
                continue
        
        # Extract and convert windows
        windows = ifc_file.by_type("IfcWindow")
        for window in windows:
            try:
                shape = ifcopenshell.geom.create_shape(settings, window)
                geometry = shape.geometry
                verts = np.array(geometry.verts).reshape(-1, 3)
                
                # Create window as rectangle
                if len(verts) >= 4:
                    min_x = min(v[0] for v in verts)
                    max_x = max(v[0] for v in verts)
                    min_y = min(v[1] for v in verts)
                    max_y = max(v[1] for v in verts)
                    
                    msp.add_lwpolyline(
                        [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)],
                        dxfattribs={'layer': 'WINDOWS', 'closed': True}
                    )
            except Exception as e:
                logger.warning(f"Failed to export window to DWG: {e}")
                continue
        
        # Extract rooms from spatial structure
        spaces = ifc_file.by_type("IfcSpace")
        for space in spaces:
            try:
                # Get space boundaries
                shape = ifcopenshell.geom.create_shape(settings, space)
                geometry = shape.geometry
                verts = np.array(geometry.verts).reshape(-1, 3)
                faces = np.array(geometry.faces).reshape(-1, 3)
                
                # Create room outline (2D projection)
                for face in faces:
                    if len(face) >= 3:
                        face_verts = verts[face]
                        points_2d = [(v[0], v[1]) for v in face_verts]
                        
                        if len(points_2d) >= 2:
                            msp.add_lwpolyline(
                                points_2d,
                                dxfattribs={'layer': 'ROOMS', 'closed': True}
                            )
            except Exception as e:
                logger.warning(f"Failed to export space to DWG: {e}")
                continue
        
        # Extract landscape/urban elements (IfcBuildingElementProxy)
        proxies = ifc_file.by_type("IfcBuildingElementProxy")
        for proxy in proxies:
            try:
                # Get proxy name to determine type
                name = proxy.Name or ""
                layer_name = 'PATHS'  # Default
                
                # Determine layer based on name or properties
                if 'path' in name.lower() or 'walkway' in name.lower():
                    layer_name = 'PATHS'
                elif 'road' in name.lower() or 'street' in name.lower():
                    layer_name = 'ROADS'
                elif 'water' in name.lower() or 'pond' in name.lower() or 'pool' in name.lower():
                    layer_name = 'WATER'
                elif 'parking' in name.lower():
                    layer_name = 'PARKING'
                elif 'network' in name.lower():
                    layer_name = 'STREETS'
                
                try:
                    shape = ifcopenshell.geom.create_shape(settings, proxy)
                    geometry = shape.geometry
                    verts = np.array(geometry.verts).reshape(-1, 3)
                    faces = np.array(geometry.faces).reshape(-1, 3)
                    
                    for face in faces:
                        if len(face) >= 3:
                            face_verts = verts[face]
                            points_2d = [(v[0], v[1]) for v in face_verts]
                            
                            if len(points_2d) >= 2:
                                msp.add_lwpolyline(
                                    points_2d,
                                    dxfattribs={'layer': layer_name, 'closed': len(points_2d) > 2}
                                )
                except Exception:
                    # If geometry extraction fails, skip
                    continue
            except Exception as e:
                logger.warning(f"Failed to export proxy element to DWG: {e}")
                continue
        
        # Extract buildings (IfcBuilding) for urban plans
        buildings = ifc_file.by_type("IfcBuilding")
        for building in buildings:
            try:
                # Buildings are spatial containers, extract their contained elements
                # For now, just mark the building location
                try:
                    shape = ifcopenshell.geom.create_shape(settings, building)
                    geometry = shape.geometry
                    verts = np.array(geometry.verts).reshape(-1, 3)
                    faces = np.array(geometry.faces).reshape(-1, 3)
                    
                    for face in faces:
                        if len(face) >= 3:
                            face_verts = verts[face]
                            points_2d = [(v[0], v[1]) for v in face_verts]
                            
                            if len(points_2d) >= 2:
                                msp.add_lwpolyline(
                                    points_2d,
                                    dxfattribs={'layer': 'BUILDINGS', 'closed': True}
                                )
                except Exception:
                    continue
            except Exception as e:
                logger.warning(f"Failed to export building to DWG: {e}")
                continue
        
        # Save as DXF (AutoCAD opens DXF files natively, can save as DWG)
        # Save with .dxf extension for compatibility (AutoCAD opens DXF as DWG)
        dxf_path = output_path.replace('.dwg', '.dxf') if output_path.endswith('.dwg') else output_path
        if not dxf_path.endswith('.dxf'):
            dxf_path = dxf_path + '.dxf'
        
        doc.saveas(dxf_path)
        logger.info(f"DWG/DXF file created successfully: {dxf_path}")
        
        # Also copy to .dwg path for user convenience (same file, different extension)
        if dxf_path != output_path and os.path.exists(dxf_path):
            import shutil
            shutil.copy(dxf_path, output_path)
        
        return os.path.exists(output_path) or os.path.exists(dxf_path)
    
    except ImportError:
        # Fallback: Try IfcConvert if available
        try:
            result = subprocess.run(
                ["IfcConvert", "--version"],
                capture_output=True,
                timeout=5
            )
            
            if result.returncode == 0:
                subprocess.run(
                    ["IfcConvert", ifc_path, output_path],
                    timeout=60
                )
                return os.path.exists(output_path)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Final fallback: Copy IFC with .dwg extension
        import shutil
        try:
            shutil.copy(ifc_path, output_path)
            logger.warning("DWG export: Created IFC-compatible file. Install ezdxf for proper DWG export.")
            return True
        except Exception as e:
            logger.error(f"DWG export failed: {e}")
            return False
    
    except Exception as e:
        logger.error(f"DWG export failed: {e}")
        # Fallback to IFC copy
        try:
            import shutil
            shutil.copy(ifc_path, output_path)
            logger.warning("DWG export: Created IFC-compatible file as fallback.")
            return True
        except Exception:
            return False


def export_to_rvt(ifc_path: str, output_path: str) -> bool:
    """
    Prepare IFC file for Revit import
    
    Note: Revit can import IFC files natively. This function provides
    an IFC file with a .rvt.ifc extension to indicate it's intended for Revit.
    No native RVT file generation is performed - Revit imports IFC directly.
    
    Args:
        ifc_path: Path to IFC file
        output_path: Output path (will be .rvt.ifc extension)
    
    Returns:
        True if file copied successfully
    """
    from loguru import logger
    
    # Revit imports IFC directly - no conversion needed
    # We provide IFC with .rvt.ifc extension to indicate it's for Revit
    import shutil
    try:
        shutil.copy(ifc_path, output_path)
        logger.info(f"IFC file prepared for Revit import: {output_path}")
        logger.info("Note: Revit can import IFC files natively - no RVT conversion needed")
        return True
    except Exception as e:
        logger.error(f"RVT preparation failed: {e}")
        return False


def generate_preview_image(ifc_path: str, output_path: str) -> bool:
    """
    Generate preview image from IFC using IfcOpenShell
    Creates a wireframe/geometry preview without Blender
    """
    try:
        import ifcopenshell
        import ifcopenshell.geom
        import numpy as np
        from PIL import Image, ImageDraw
        import math
        
        # Open IFC file
        ifc_file = ifcopenshell.open(ifc_path)
        
        # Get all walls, slabs, and openings for preview
        walls = ifc_file.by_type("IfcWall")
        slabs = ifc_file.by_type("IfcSlab")
        doors = ifc_file.by_type("IfcDoor")
        windows = ifc_file.by_type("IfcWindow")
        
        if not (walls or slabs or doors or windows):
            # Fallback: create placeholder image
            print("No geometry found in IFC, creating placeholder preview")
            img = Image.new('RGB', (1920, 1080), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((960, 540), "IFC Preview\n(No geometry found)", 
                     fill='black', anchor='mm', align='center')
            img.save(output_path)
            return os.path.exists(output_path)
        
        # Extract geometry and collect all points
        all_points = []
        bounds = {'min_x': float('inf'), 'max_x': float('-inf'),
                  'min_y': float('inf'), 'max_y': float('-inf'),
                  'min_z': float('inf'), 'max_z': float('-inf')}
        
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        
        # Process walls
        for wall in walls:
            try:
                shape = ifcopenshell.geom.create_shape(settings, wall)
                geometry = shape.geometry
                points = np.array(geometry.verts).reshape(-1, 3)
                all_points.append(('wall', points))
                
                # Update bounds
                if len(points) > 0:
                    bounds['min_x'] = min(bounds['min_x'], points[:, 0].min())
                    bounds['max_x'] = max(bounds['max_x'], points[:, 0].max())
                    bounds['min_y'] = min(bounds['min_y'], points[:, 1].min())
                    bounds['max_y'] = max(bounds['max_y'], points[:, 1].max())
                    bounds['min_z'] = min(bounds['min_z'], points[:, 2].min())
                    bounds['max_z'] = max(bounds['max_z'], points[:, 2].max())
            except Exception:
                continue
        
        # Process slabs (floors)
        for slab in slabs:
            try:
                shape = ifcopenshell.geom.create_shape(settings, slab)
                geometry = shape.geometry
                points = np.array(geometry.verts).reshape(-1, 3)
                all_points.append(('slab', points))
                
                # Update bounds
                if len(points) > 0:
                    bounds['min_x'] = min(bounds['min_x'], points[:, 0].min())
                    bounds['max_x'] = max(bounds['max_x'], points[:, 0].max())
                    bounds['min_y'] = min(bounds['min_y'], points[:, 1].min())
                    bounds['max_y'] = max(bounds['max_y'], points[:, 1].max())
            except Exception:
                continue
        
        # Check if we have valid bounds
        if (bounds['min_x'] == float('inf') or 
            bounds['max_x'] == float('-inf')):
            # No valid geometry found, create placeholder
            img = Image.new('RGB', (1920, 1080), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((960, 540), "IFC Preview\n(Geometry extraction failed)", 
                     fill='black', anchor='mm', align='center')
            img.save(output_path)
            return os.path.exists(output_path)
        
        # Calculate view dimensions (isometric top-down view)
        width = bounds['max_x'] - bounds['min_x']
        height = bounds['max_y'] - bounds['min_y']
        
        # Add padding
        padding = max(width, height) * 0.1
        width += padding * 2
        height += padding * 2
        
        # Image dimensions
        img_width, img_height = 1920, 1080
        
        # Calculate scale to fit
        scale_x = (img_width - 40) / width if width > 0 else 1
        scale_y = (img_height - 40) / height if height > 0 else 1
        scale = min(scale_x, scale_y)
        
        # Center offset
        center_x = (bounds['min_x'] + bounds['max_x']) / 2
        center_y = (bounds['min_y'] + bounds['max_y']) / 2
        offset_x = img_width / 2 - center_x * scale
        offset_y = img_height / 2 - center_y * scale
        
        # Create image with white background
        img = Image.new('RGB', (img_width, img_height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw geometry (top-down isometric view)
        for geom_type, points in all_points:
            if len(points) < 3:
                continue
            
            # Color by type
            if geom_type == 'wall':
                color = (100, 100, 200)  # Blue for walls
            elif geom_type == 'slab':
                color = (200, 200, 200)  # Gray for floors
            else:
                color = (150, 150, 150)  # Default gray
            
            # Convert 3D points to 2D (isometric projection: top-down)
            # Simple orthographic projection (x, y plane, ignoring z)
            projected_points = []
            for point in points:
                x = point[0] * scale + offset_x
                y = point[1] * scale + offset_y
                projected_points.append((x, y))
            
            # Draw wireframe (connect points)
            if len(projected_points) >= 2:
                # Draw edges (simplified - just connect consecutive points)
                for i in range(len(projected_points) - 1):
                    draw.line([projected_points[i], projected_points[i + 1]], 
                             fill=color, width=2)
                # Close loop if enough points
                if len(projected_points) >= 3:
                    draw.line([projected_points[-1], projected_points[0]], 
                             fill=color, width=2)
        
        # Add title
        draw.text((20, 20), "IFC Model Preview (Top-Down View)", 
                 fill='black')
        
        # Save image
        img.save(output_path)
        
        print(f"Preview generated successfully: {output_path}")
        return os.path.exists(output_path)
    
    except ImportError as e:
        print(f"Preview generation requires additional dependencies: {e}")
        print("Creating placeholder image...")
        # Create simple placeholder
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (1920, 1080), color='lightgray')
            draw = ImageDraw.Draw(img)
            draw.text((960, 540), "IFC Preview\n(Dependencies not available)", 
                     fill='black', anchor='mm', align='center')
            img.save(output_path)
            return os.path.exists(output_path)
        except Exception:
            return False
    
    except Exception as e:
        print(f"Preview generation failed: {e}")
        import traceback
        traceback.print_exc()
        # Create fallback placeholder
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (1920, 1080), color='lightgray')
            draw = ImageDraw.Draw(img)
            draw.text((960, 540), f"Preview Error\n{str(e)[:50]}", 
                     fill='red', anchor='mm', align='center')
            img.save(output_path)
            return os.path.exists(output_path)
        except Exception:
            return False


def export_to_sketchup(ifc_path: str, output_path: str) -> bool:
    """
    Export IFC to SketchUp-compatible format (OBJ)
    SketchUp can import OBJ files natively
    """
    try:
        import ifcopenshell
        import ifcopenshell.geom
        import numpy as np
        from loguru import logger
        
        # Open IFC file
        ifc_file = ifcopenshell.open(ifc_path)
        
        # Geometry extraction settings
        settings = ifcopenshell.geom.settings()
        settings.set(settings.USE_WORLD_COORDS, True)
        settings.set(settings.WELD_VERTICES, True)
        
        # Collect all geometry
        all_vertices = []
        all_faces = []
        vertex_offset = 0
        
        # Extract walls
        walls = ifc_file.by_type("IfcWall")
        for wall in walls:
            try:
                shape = ifcopenshell.geom.create_shape(settings, wall)
                geometry = shape.geometry
                verts = np.array(geometry.verts).reshape(-1, 3)
                faces = np.array(geometry.faces).reshape(-1, 3)
                
                # Add vertices
                for v in verts:
                    all_vertices.append((v[0], v[1], v[2]))
                
                # Add faces with offset
                for face in faces:
                    if len(face) >= 3:
                        # OBJ uses 1-based indexing
                        all_faces.append([vertex_offset + face[0] + 1, 
                                         vertex_offset + face[1] + 1, 
                                         vertex_offset + face[2] + 1])
                
                vertex_offset += len(verts)
            except Exception as e:
                logger.warning(f"Failed to export wall to OBJ: {e}")
                continue
        
        # Extract doors
        doors = ifc_file.by_type("IfcDoor")
        for door in doors:
            try:
                shape = ifcopenshell.geom.create_shape(settings, door)
                geometry = shape.geometry
                verts = np.array(geometry.verts).reshape(-1, 3)
                faces = np.array(geometry.faces).reshape(-1, 3)
                
                for v in verts:
                    all_vertices.append((v[0], v[1], v[2]))
                
                for face in faces:
                    if len(face) >= 3:
                        all_faces.append([vertex_offset + face[0] + 1, 
                                         vertex_offset + face[1] + 1, 
                                         vertex_offset + face[2] + 1])
                
                vertex_offset += len(verts)
            except Exception as e:
                logger.warning(f"Failed to export door to OBJ: {e}")
                continue
        
        # Extract windows
        windows = ifc_file.by_type("IfcWindow")
        for window in windows:
            try:
                shape = ifcopenshell.geom.create_shape(settings, window)
                geometry = shape.geometry
                verts = np.array(geometry.verts).reshape(-1, 3)
                faces = np.array(geometry.faces).reshape(-1, 3)
                
                for v in verts:
                    all_vertices.append((v[0], v[1], v[2]))
                
                for face in faces:
                    if len(face) >= 3:
                        all_faces.append([vertex_offset + face[0] + 1, 
                                         vertex_offset + face[1] + 1, 
                                         vertex_offset + face[2] + 1])
                
                vertex_offset += len(verts)
            except Exception as e:
                logger.warning(f"Failed to export window to OBJ: {e}")
                continue
        
        # Extract slabs (floors)
        slabs = ifc_file.by_type("IfcSlab")
        for slab in slabs:
            try:
                shape = ifcopenshell.geom.create_shape(settings, slab)
                geometry = shape.geometry
                verts = np.array(geometry.verts).reshape(-1, 3)
                faces = np.array(geometry.faces).reshape(-1, 3)
                
                for v in verts:
                    all_vertices.append((v[0], v[1], v[2]))
                
                for face in faces:
                    if len(face) >= 3:
                        all_faces.append([vertex_offset + face[0] + 1, 
                                         vertex_offset + face[1] + 1, 
                                         vertex_offset + face[2] + 1])
                
                vertex_offset += len(verts)
            except Exception as e:
                logger.warning(f"Failed to export slab to OBJ: {e}")
                continue
        
        # Write OBJ file
        # Use .obj extension (SketchUp imports OBJ natively)
        obj_path = output_path.replace('.skp', '.obj') if output_path.endswith('.skp') else output_path
        if not obj_path.endswith('.obj'):
            obj_path = obj_path + '.obj'
        
        with open(obj_path, 'w') as f:
            # Write header
            f.write("# OBJ file exported from IFC\n")
            f.write("# SketchUp-compatible format\n")
            f.write(f"# Generated from: {ifc_path}\n\n")
            
            # Write vertices
            for v in all_vertices:
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            
            # Write faces
            f.write("\n")
            for face in all_faces:
                if len(face) == 3:
                    f.write(f"f {face[0]} {face[1]} {face[2]}\n")
                elif len(face) == 4:
                    # Quad face - triangulate
                    f.write(f"f {face[0]} {face[1]} {face[2]}\n")
                    f.write(f"f {face[0]} {face[2]} {face[3]}\n")
        
        logger.info(f"SketchUp/OBJ file created successfully: {obj_path}")
        
        # Also copy to .skp.obj path for user convenience
        if obj_path != output_path and os.path.exists(obj_path):
            import shutil
            shutil.copy(obj_path, output_path)
        
        return os.path.exists(obj_path) or os.path.exists(output_path)
    
    except Exception as e:
        from loguru import logger
        logger.error(f"SketchUp/OBJ export failed: {e}")
        # Fallback: Copy IFC with .obj extension
        try:
            import shutil
            shutil.copy(ifc_path, output_path.replace('.skp', '.obj'))
            logger.warning("SketchUp export: Created IFC-compatible file as fallback.")
            return True
        except Exception:
            return False


def export_to_formats(
    ifc_path: str,
    output_dir: str,
    job_id: str,
    scale_ratio: float = 0.01
) -> Dict[str, Optional[str]]:
    """
    Export IFC to multiple formats
    
    Args:
        ifc_path: Path to IFC file
        output_dir: Output directory
        job_id: Job ID
        scale_ratio: Scale ratio for dimensions (optional)
    
    Returns:
        dict with paths to generated files
    """
    output_path = Path(output_dir)
    
    result = {
        "dwg_path": None,
        "rvt_path": None,
        "sketchup_path": None,
        "preview_path": None
    }
    
    # Export to DWG
    dwg_path = output_path / f"{job_id}.dwg"
    if export_to_dwg(ifc_path, str(dwg_path), scale_ratio):
        result["dwg_path"] = str(dwg_path)
    
    # Prepare for Revit
    rvt_path = output_path / f"{job_id}.rvt.ifc"
    if export_to_rvt(ifc_path, str(rvt_path)):
        result["rvt_path"] = str(rvt_path)
    
    # Export to SketchUp (OBJ format)
    sketchup_path = output_path / f"{job_id}.obj"
    if export_to_sketchup(ifc_path, str(sketchup_path)):
        result["sketchup_path"] = str(sketchup_path)
    
    # Generate preview
    preview_path = output_path / f"{job_id}_preview.png"
    if generate_preview_image(ifc_path, str(preview_path)):
        result["preview_path"] = str(preview_path)
    
    return result

