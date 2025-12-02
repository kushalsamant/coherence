"""
Layout variation generator
Generates alternative room arrangements from the same sketch
Uses simple algorithms to rearrange rooms while maintaining constraints
"""
from typing import Dict, Any, List, Optional
import random
import copy
from loguru import logger


def generate_layout_variations(
    original_plan_data: Dict[str, Any],
    num_variations: int = 3,
    constraints: Optional[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """
    Generate multiple layout variations from original plan data
    
    Args:
        original_plan_data: Original detected plan data with rooms, walls, openings
        num_variations: Number of variations to generate (1-10)
        constraints: Optional constraints (room sizes, adjacencies, etc.)
    
    Returns:
        List of variation dictionaries, each with plan_data and confidence
    """
    variations = []
    
    rooms = original_plan_data.get("rooms", [])
    walls = original_plan_data.get("walls", [])
    openings = original_plan_data.get("openings", [])
    
    if not rooms:
        logger.warning("No rooms found in plan data, cannot generate variations")
        return []
    
    for i in range(num_variations):
        try:
            # Create variation by rearranging rooms
            variation_plan = _create_variation(
                rooms=rooms,
                walls=walls,
                openings=openings,
                variation_number=i + 1,
                constraints=constraints
            )
            
            # Calculate confidence (simpler variations have higher confidence)
            confidence = _calculate_confidence(variation_plan, original_plan_data)
            
            variations.append({
                "plan_data": variation_plan,
                "confidence": confidence,
                "variation_number": i + 1
            })
            
        except Exception as e:
            logger.error(f"Error generating variation {i + 1}: {e}")
            continue
    
    logger.info(f"Generated {len(variations)} layout variations")
    return variations


def _create_variation(
    rooms: List[Dict[str, Any]],
    walls: List[Dict[str, Any]],
    openings: List[Dict[str, Any]],
    variation_number: int,
    constraints: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a single layout variation
    
    Strategy:
    1. Rearrange room positions (swap adjacent rooms)
    2. Adjust room sizes slightly (within constraints)
    3. Maintain wall connections
    4. Preserve openings where possible
    """
    # Deep copy to avoid modifying original
    variation_rooms = copy.deepcopy(rooms)
    variation_walls = copy.deepcopy(walls)
    variation_openings = copy.deepcopy(openings)
    
    # Strategy 1: Swap room positions (if multiple rooms)
    if len(variation_rooms) > 1:
        # Randomly select two rooms to swap
        idx1, idx2 = random.sample(range(len(variation_rooms)), 2)
        
        # Swap room polygons (positions)
        room1_polygon = variation_rooms[idx1].get("polygon", [])
        room2_polygon = variation_rooms[idx2].get("polygon", [])
        
        if room1_polygon and room2_polygon:
            # Calculate centers
            center1 = _calculate_polygon_center(room1_polygon)
            center2 = _calculate_polygon_center(room2_polygon)
            
            # Swap positions (translate rooms)
            variation_rooms[idx1]["polygon"] = _translate_polygon(
                room1_polygon, 
                center2[0] - center1[0], 
                center2[1] - center1[1]
            )
            variation_rooms[idx2]["polygon"] = _translate_polygon(
                room2_polygon,
                center1[0] - center2[0],
                center1[1] - center2[1]
            )
    
    # Strategy 2: Adjust room sizes (slightly expand/contract)
    if constraints and constraints.get("allow_size_adjustment", True):
        for room in variation_rooms:
            polygon = room.get("polygon", [])
            if polygon and len(polygon) >= 3:
                # Slight random scaling (0.9x to 1.1x)
                scale = random.uniform(0.9, 1.1)
                room["polygon"] = _scale_polygon(polygon, scale)
    
    # Strategy 3: Rearrange room order (for different adjacencies)
    # This is a simple approach - in production, would use more sophisticated algorithms
    
    return {
        "rooms": variation_rooms,
        "walls": variation_walls,  # Keep walls as-is for now
        "openings": variation_openings,  # Keep openings as-is for now
        "confidence": 0.7,  # Default confidence
        "variation_type": "room_rearrangement"
    }


def _calculate_polygon_center(polygon: List[List[float]]) -> tuple:
    """Calculate center point of polygon"""
    if not polygon:
        return (0, 0)
    
    x_sum = sum(point[0] for point in polygon)
    y_sum = sum(point[1] for point in polygon)
    count = len(polygon)
    
    return (x_sum / count, y_sum / count)


def _translate_polygon(polygon: List[List[float]], dx: float, dy: float) -> List[List[float]]:
    """Translate polygon by dx, dy"""
    return [[point[0] + dx, point[1] + dy] for point in polygon]


def _scale_polygon(polygon: List[List[float]], scale: float) -> List[List[float]]:
    """Scale polygon around its center"""
    if not polygon:
        return polygon
    
    center = _calculate_polygon_center(polygon)
    cx, cy = center
    
    scaled = []
    for point in polygon:
        # Translate to origin, scale, translate back
        px, py = point[0] - cx, point[1] - cy
        scaled.append([px * scale + cx, py * scale + cy])
    
    return scaled


def _calculate_confidence(variation_plan: Dict[str, Any], original_plan_data: Dict[str, Any]) -> float:
    """
    Calculate confidence score for a variation
    
    Higher confidence if:
    - Similar number of rooms
    - Similar total area
    - Valid geometry
    """
    original_rooms = original_plan_data.get("rooms", [])
    variation_rooms = variation_plan.get("rooms", [])
    
    if len(variation_rooms) != len(original_rooms):
        return 0.5  # Lower confidence if room count differs
    
    # Calculate area similarity
    original_area = sum(room.get("area", 0) for room in original_rooms)
    variation_area = sum(room.get("area", 0) for room in variation_rooms)
    
    if original_area > 0:
        area_ratio = min(variation_area, original_area) / max(variation_area, original_area)
    else:
        area_ratio = 0.8
    
    # Base confidence on area similarity
    confidence = 0.6 + (area_ratio * 0.3)  # 0.6-0.9 range
    
    return min(confidence, 0.95)  # Cap at 95%

