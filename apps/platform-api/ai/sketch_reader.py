"""
Sketch reading and geometry detection
Modular architecture supporting multiple detection methods
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple, Optional
import cv2
import numpy as np
from pathlib import Path
import json

from loguru import logger

from config.sketch2bim import settings

_SYMBOL_DETECTOR = None
_SYMBOL_DETECTOR_INITIALIZED = False


def get_symbol_detector():
    """
    Lazy-load and cache the symbol detector to avoid repeated torch initialization.
    """
    global _SYMBOL_DETECTOR, _SYMBOL_DETECTOR_INITIALIZED
    if _SYMBOL_DETECTOR_INITIALIZED:
        return _SYMBOL_DETECTOR

    _SYMBOL_DETECTOR_INITIALIZED = True
    if not getattr(settings, "SYMBOL_DETECTOR_ENABLED", False):
        logger.debug("Symbol detector disabled via settings.")
        return None

    try:
        from .symbol_detector import SymbolDetector

        _SYMBOL_DETECTOR = SymbolDetector(
            model_path=settings.SYMBOL_DETECTOR_MODEL_PATH,
            class_map_path=settings.SYMBOL_DETECTOR_CLASS_FILE,
            confidence_threshold=settings.SYMBOL_DETECTOR_CONFIDENCE,
            device_preference=getattr(settings, "SYMBOL_DETECTOR_DEVICE", "auto"),
            max_results=getattr(settings, "SYMBOL_DETECTOR_MAX_RESULTS", 200),
        )
        if not _SYMBOL_DETECTOR.available:
            logger.warning("Symbol detector failed to initialize; falling back to geometry-only output.")
            _SYMBOL_DETECTOR = None
    except Exception as exc:
        logger.warning(f"Symbol detector import failed: {exc}")
        _SYMBOL_DETECTOR = None

    return _SYMBOL_DETECTOR


class SketchReader(ABC):
    """Base class for sketch readers"""
    
    @abstractmethod
    def read_sketch(self, image_path: str, legend_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Read sketch and extract geometry
        
        Args:
            image_path: Path to sketch image
            legend_data: Optional parsed legend data (scale, room labels, etc.)
        
        Returns:
            dict with keys: rooms, walls, openings, confidence
        """
        pass
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image before detection
        - Auto-rotate and deskew
        - Adaptive thresholding
        - Morphological operations
        - Perspective correction
        - Enhance contrast
        """
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Step 1: Auto-deskew (detect and correct rotation)
        gray = self._deskew_image(gray)
        
        # Step 2: Enhance contrast using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Step 3: Denoise
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
        
        # Step 4: Apply morphological operations to clean up noise
        # Opening: removes small noise
        kernel_open = np.ones((2, 2), np.uint8)
        opened = cv2.morphologyEx(denoised, cv2.MORPH_OPEN, kernel_open, iterations=1)
        
        # Closing: connects broken lines
        kernel_close = np.ones((3, 3), np.uint8)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel_close, iterations=1)
        
        return closed
    
    def _deskew_image(self, image: np.ndarray) -> np.ndarray:
        """
        Auto-deskew image by detecting rotation angle and correcting it
        
        Args:
            image: Grayscale image
            
        Returns:
            Deskewed image
        """
        # Detect edges to find lines
        edges = cv2.Canny(image, 50, 150, apertureSize=3)
        
        # Use HoughLines to detect dominant line angles
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        
        if lines is None or len(lines) < 2:
            return image  # Not enough lines to determine skew
        
        # Calculate angles of detected lines
        angles = []
        for line in lines[:20]:  # Use first 20 lines
            rho, theta = line[0]
            # Convert to degrees, normalize to -45 to 45
            angle = np.degrees(theta) - 90
            if angle < -45:
                angle += 90
            angles.append(angle)
        
        if not angles:
            return image
        
        # Use median angle to avoid outliers
        median_angle = np.median(angles)
        
        # Only correct if angle is significant (> 0.5 degrees)
        if abs(median_angle) < 0.5:
            return image
        
        # Rotate image to correct skew
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, 
                                 borderMode=cv2.BORDER_REPLICATE)
        
        return rotated
    
    def _adaptive_canny(self, image: np.ndarray) -> np.ndarray:
        """
        Adaptive Canny edge detection using Otsu's threshold
        
        Args:
            image: Preprocessed grayscale image
            
        Returns:
            Edge-detected image
        """
        # Use Otsu's method to determine optimal thresholds
        # Otsu finds the threshold that minimizes intra-class variance
        threshold_value, _ = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Calculate Canny thresholds based on Otsu's threshold
        # Lower threshold: 50% of Otsu threshold
        # Upper threshold: 150% of Otsu threshold (standard ratio is 1:3, but we use 1:1.5 for better detection)
        lower_threshold = max(10, int(threshold_value * 0.5))
        upper_threshold = min(255, int(threshold_value * 1.5))
        
        # Multi-scale edge detection: detect at different scales and combine
        edges_list = []
        
        # Scale 1: Original resolution
        edges1 = cv2.Canny(image, lower_threshold, upper_threshold, apertureSize=3)
        edges_list.append(edges1)
        
        # Scale 2: Slightly blurred (better for detecting larger features)
        blurred = cv2.GaussianBlur(image, (5, 5), 1.0)
        edges2 = cv2.Canny(blurred, lower_threshold, upper_threshold, apertureSize=3)
        edges_list.append(edges2)
        
        # Scale 3: More blurred (for very large features)
        blurred2 = cv2.GaussianBlur(image, (7, 7), 1.5)
        edges3 = cv2.Canny(blurred2, lower_threshold, upper_threshold, apertureSize=3)
        edges_list.append(edges3)
        
        # Combine all scales (union of edges)
        combined = np.zeros_like(edges1)
        for edges in edges_list:
            combined = cv2.bitwise_or(combined, edges)
        
        return combined
    
    def _link_edges(self, edges: np.ndarray) -> np.ndarray:
        """
        Link broken edges using morphological operations
        
        Args:
            edges: Edge-detected image
            
        Returns:
            Image with better-connected edges
        """
        # Dilate to connect nearby edges
        kernel_dilate = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel_dilate, iterations=2)
        
        # Erode to restore original edge thickness
        kernel_erode = np.ones((2, 2), np.uint8)
        eroded = cv2.erode(dilated, kernel_erode, iterations=1)
        
        # Additional closing to connect gaps
        kernel_close = np.ones((3, 3), np.uint8)
        closed = cv2.morphologyEx(eroded, cv2.MORPH_CLOSE, kernel_close, iterations=1)
        
        return closed
    
    def _detect_walls(self, edges: np.ndarray, scale_ratio: float) -> List[Dict]:
        """
        Enhanced wall detection with line merging, angle alignment, and validation
        
        Args:
            edges: Edge-detected image
            scale_ratio: Scale ratio from legend (pixels to meters)
            
        Returns:
            List of wall dictionaries
        """
        # Detect lines using HoughLinesP
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=50,
            maxLineGap=10
        )
        
        if lines is None or len(lines) == 0:
            return []
        
        # Convert to list of line segments
        line_segments = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length_pixels = float(np.sqrt((x2-x1)**2 + (y2-y1)**2))
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            
            line_segments.append({
                "start": [float(x1), float(y1)],
                "end": [float(x2), float(y2)],
                "length_pixels": length_pixels,
                "angle": angle
            })
        
        # Merge nearby parallel lines (wall thickness detection)
        merged_lines = self._merge_line_segments(line_segments)
        
        # Align to common angles (0°, 45°, 90°, etc.)
        aligned_lines = self._align_to_common_angles(merged_lines)
        
        # Convert to wall format with real-world units
        walls = []
        for line in aligned_lines:
            length_meters = line["length_pixels"] * scale_ratio
            
            # Validate wall (filter out too short lines)
            if length_meters < 0.5:  # Minimum 0.5 meters
                continue
            
            walls.append({
                "start": line["start"],
                "end": line["end"],
                "length": length_meters,
                "length_pixels": line["length_pixels"]
            })
        
        return walls
    
    def _merge_line_segments(self, lines: List[Dict]) -> List[Dict]:
        """
        Merge nearby parallel lines into single walls (detects wall thickness)
        
        Args:
            lines: List of line segments
            
        Returns:
            Merged line segments
        """
        if not lines:
            return []
        
        merged = []
        used = set()
        
        for i, line1 in enumerate(lines):
            if i in used:
                continue
            
            # Find parallel lines nearby
            merged_line = line1.copy()
            merged_group = [line1]
            
            for j, line2 in enumerate(lines[i+1:], start=i+1):
                if j in used:
                    continue
                
                # Check if lines are parallel (within 5 degrees)
                angle_diff = abs(line1["angle"] - line2["angle"])
                angle_diff = min(angle_diff, 180 - angle_diff)  # Handle wrap-around
                
                if angle_diff > 5:
                    continue
                
                # Check if lines are close together (within 20 pixels)
                dist = self._distance_between_lines(line1, line2)
                if dist < 20:
                    # Merge lines
                    merged_group.append(line2)
                    used.add(j)
                    
                    # Extend merged line to cover both segments
                    merged_line = self._extend_line_segment(merged_line, line2)
            
            merged.append(merged_line)
            used.add(i)
        
        return merged
    
    def _distance_between_lines(self, line1: Dict, line2: Dict) -> float:
        """Calculate minimum distance between two line segments"""
        # Calculate distance from midpoint of line1 to line2
        mid1 = [(line1["start"][0] + line1["end"][0]) / 2,
                (line1["start"][1] + line1["end"][1]) / 2]
        
        # Distance from point to line segment
        p1 = np.array(line2["start"])
        p2 = np.array(line2["end"])
        p = np.array(mid1)
        
        # Vector from p1 to p2
        v = p2 - p1
        # Vector from p1 to p
        w = p - p1
        
        # Project w onto v
        if np.dot(v, v) == 0:
            return float(np.linalg.norm(p - p1))
        
        t = max(0, min(1, np.dot(w, v) / np.dot(v, v)))
        proj = p1 + t * v
        
        return float(np.linalg.norm(p - proj))
    
    def _extend_line_segment(self, line1: Dict, line2: Dict) -> Dict:
        """Extend line1 to include line2"""
        # Get all endpoints
        points = [line1["start"], line1["end"], line2["start"], line2["end"]]
        
        # Find the two points that are farthest apart
        max_dist = 0
        best_start = points[0]
        best_end = points[0]
        
        for i, p1 in enumerate(points):
            for j, p2 in enumerate(points[i+1:], start=i+1):
                dist = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                if dist > max_dist:
                    max_dist = dist
                    best_start = p1
                    best_end = p2
        
        # Recalculate angle and length
        angle = np.degrees(np.arctan2(best_end[1] - best_start[1], 
                                      best_end[0] - best_start[0]))
        length = float(max_dist)
        
        return {
            "start": best_start,
            "end": best_end,
            "length_pixels": length,
            "angle": angle
        }
    
    def _align_to_common_angles(self, lines: List[Dict]) -> List[Dict]:
        """
        Align lines to common architectural angles (0°, 45°, 90°, etc.)
        
        Args:
            lines: List of line segments
            
        Returns:
            Lines aligned to common angles
        """
        common_angles = [0, 45, 90, 135, -45, -90, -135]
        aligned = []
        
        for line in lines:
            angle = line["angle"]
            
            # Find closest common angle
            closest_angle = min(common_angles, key=lambda a: min(abs(angle - a), 
                                                                  abs(angle - a - 360),
                                                                  abs(angle - a + 360)))
            
            # Only align if close enough (within 10 degrees)
            angle_diff = min(abs(angle - closest_angle), 
                            abs(angle - closest_angle - 360),
                            abs(angle - closest_angle + 360))
            
            if angle_diff < 10:
                # Recalculate line with aligned angle
                length = line["length_pixels"]
                start = line["start"]
                
                # Calculate new end point
                rad = np.radians(closest_angle)
                end = [start[0] + length * np.cos(rad),
                      start[1] + length * np.sin(rad)]
                
                aligned.append({
                    "start": start,
                    "end": end,
                    "length_pixels": length,
                    "angle": closest_angle
                })
            else:
                # Keep original if not close to common angle
                aligned.append(line)
        
        return aligned
    
    def _detect_rooms(self, contours: List, hierarchy: Optional[np.ndarray], 
                     room_labels: Dict[str, str], scale_ratio: float) -> List[Dict]:
        """
        Enhanced room detection with contour hierarchy analysis and validation
        
        Args:
            contours: List of contours
            hierarchy: Contour hierarchy information
            room_labels: Optional room labels from legend
            scale_ratio: Scale ratio from legend (pixels to meters)
            
        Returns:
            List of room dictionaries
        """
        rooms = []
        
        # Process contours with hierarchy awareness
        for i, contour in enumerate(contours):
            # Filter by area
            area = cv2.contourArea(contour)
            if area < 1000:  # Ignore small contours
                continue
            
            # Better polygon simplification with adaptive epsilon
            epsilon = self._adaptive_epsilon(contour)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Validate room shape
            if not self._validate_room(approx, area):
                continue
            
            # Convert to list of points
            points = [[float(p[0][0]), float(p[0][1])] for p in approx]
            
            # Check if this is a nested room (room within a room)
            is_nested = False
            if hierarchy is not None and len(hierarchy) > 0:
                is_nested = self._is_nested_room(i, hierarchy)
            
            # Use legend data for room type if available
            room_type = self._guess_room_type(approx, room_labels)
            
            # Calculate area in real-world units using scale ratio
            area_pixels = float(area)
            area_meters = area_pixels * (scale_ratio ** 2)
            
            # Calculate aspect ratio for validation
            rect = cv2.minAreaRect(contour)
            width, height = rect[1]
            aspect_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else 1.0
            
            rooms.append({
                "id": i,
                "polygon": points,
                "room_type": room_type,
                "area": area_meters,
                "area_pixels": area_pixels,
                "is_nested": is_nested,
                "aspect_ratio": float(aspect_ratio)
            })
        
        return rooms
    
    def _adaptive_epsilon(self, contour: np.ndarray) -> float:
        """
        Calculate adaptive epsilon for polygon simplification
        Uses a percentage of perimeter, but adjusts based on contour complexity
        """
        perimeter = cv2.arcLength(contour, True)
        # Start with 2% of perimeter
        base_epsilon = 0.02 * perimeter
        
        # Adjust based on contour area (larger areas can tolerate more simplification)
        area = cv2.contourArea(contour)
        if area > 50000:  # Large rooms
            return base_epsilon * 1.5
        elif area < 5000:  # Small rooms (closets, bathrooms)
            return base_epsilon * 0.5
        else:
            return base_epsilon
    
    def _validate_room(self, approx: np.ndarray, area: float) -> bool:
        """
        Validate if a contour represents a valid room
        
        Args:
            approx: Approximated polygon
            area: Contour area
            
        Returns:
            True if valid room, False otherwise
        """
        # Must have at least 4 points (rectangle minimum)
        if len(approx) < 4:
            return False
        
        # Check minimum area (at least 5 square meters in real-world)
        # Assuming default scale, this is roughly 5000 pixels
        if area < 5000:
            return False
        
        # Check if shape is too irregular (convexity defects)
        hull = cv2.convexHull(approx)
        hull_area = cv2.contourArea(hull)
        
        if hull_area == 0:
            return False
        
        # Solidity: ratio of contour area to convex hull area
        # Valid rooms should have solidity > 0.7 (not too irregular)
        solidity = area / hull_area
        if solidity < 0.7:
            return False
        
        return True
    
    def _is_nested_room(self, contour_idx: int, hierarchy: np.ndarray) -> bool:
        """
        Check if a room is nested inside another room (e.g., closet in bedroom)
        
        Args:
            contour_idx: Index of contour to check
            hierarchy: Contour hierarchy array
            
        Returns:
            True if nested, False otherwise
        """
        if hierarchy is None or len(hierarchy) == 0:
            return False
        
        # Check if this contour has a parent (is inside another contour)
        # In RETR_TREE hierarchy: [Next, Previous, First_Child, Parent]
        if contour_idx < len(hierarchy[0]):
            parent_idx = hierarchy[0][contour_idx][3]
            return parent_idx >= 0  # -1 means no parent
        
        return False


class OpenCVReader(SketchReader):
    """
    OpenCV-based sketch reader
    Uses edge detection and contour finding
    """

    def __init__(self):
        self._symbol_detector = None
        self._symbol_detector_checked = False
    
    def read_sketch(self, image_path: str, legend_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Read sketch using OpenCV
        
        Args:
            image_path: Path to sketch image
            legend_data: Optional parsed legend data (scale, room labels, etc.)
        """
        # Preprocess
        img = self.preprocess_image(image_path)
        
        # Get scale ratio from legend data
        scale_ratio = 0.01  # Default: 100 pixels = 1 meter
        if legend_data and legend_data.get("scale_ratio"):
            scale_ratio = legend_data["scale_ratio"]
        
        # Get room labels from legend data
        room_labels = {}
        if legend_data and legend_data.get("room_labels"):
            room_labels = legend_data["room_labels"]
        
        # Edge detection with adaptive thresholds and multi-scale approach
        edges = self._adaptive_canny(img)
        
        # Better edge linking using morphological operations
        edges = self._link_edges(edges)
        
        # Find contours
        contours, hierarchy = cv2.findContours(
            edges,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # Enhanced room detection with hierarchy analysis
        rooms = self._detect_rooms(contours, hierarchy, room_labels, scale_ratio)
        
        # Detect lines for walls with improved detection
        walls = self._detect_walls(edges, scale_ratio)
        
        # Enhanced opening detection with gap-based detection and validation
        openings = self._detect_openings_enhanced(img, edges, walls, scale_ratio)

        symbols_result = self._detect_symbols(image_path)
        symbols = symbols_result.get("symbols", []) if symbols_result else []
        
        return {
            "rooms": rooms,
            "walls": walls[:100],  # Limit walls
            "openings": openings,
            "symbols": symbols,
            "symbol_metadata": {k: v for k, v in (symbols_result or {}).items() if k != "symbols"},
            "confidence": self._calculate_confidence(rooms, walls, legend_data, openings),
            "scale_ratio": scale_ratio  # Include scale ratio for IFC generation
        }
    
    def _guess_room_type(self, contour, room_labels: Dict[str, str] = None) -> str:
        """
        Guess room type based on shape and legend labels
        
        Args:
            contour: Contour of room
            room_labels: Optional room labels from legend
        """
        area = cv2.contourArea(contour)
        
        # If room labels available, try to match (simplified - would use OCR in full implementation)
        # For now, use heuristics
        
        # Simple heuristics
        if area < 5000:
            return "bathroom"
        elif area > 20000:
            return "living"
        else:
            return "bedroom"
    
    def _detect_openings_enhanced(self, img: np.ndarray, edges: np.ndarray, 
                                 walls: List[Dict], scale_ratio: float) -> List[Dict]:
        """
        Enhanced opening detection with gap-based detection and validation
        
        Args:
            img: Image array
            edges: Edge detection result
            walls: List of detected walls
            scale_ratio: Scale ratio from legend (pixels to meters)
            
        Returns:
            List of opening dictionaries
        """
        openings = []
        
        # Method 1: Detect gaps in walls (gaps indicate openings)
        gap_openings = self._detect_openings_from_gaps(edges, walls, scale_ratio)
        openings.extend(gap_openings)
        
        # Method 2: Detect small rectangular contours (traditional method)
        contour_openings = self._detect_openings_from_contours(edges, scale_ratio)
        openings.extend(contour_openings)
        
        # Validate and deduplicate openings
        validated = self._validate_openings(openings, walls, scale_ratio)
        
        return validated[:30]  # Limit openings

    def _detect_symbols(self, image_path: str) -> Dict[str, Any]:
        """
        Run ML-based symbol detection if configured.
        """
        if not self._symbol_detector_checked:
            self._symbol_detector = get_symbol_detector()
            self._symbol_detector_checked = True

        if not self._symbol_detector:
            return {"symbols": [], "enabled": False, "reason": "disabled"}

        try:
            return self._symbol_detector.detect(image_path)
        except Exception as exc:
            logger.warning(f"Symbol detection failed: {exc}")
            return {"symbols": [], "enabled": False, "reason": "error"}
    
    def _detect_openings_from_gaps(self, edges: np.ndarray, walls: List[Dict], 
                                   scale_ratio: float) -> List[Dict]:
        """
        Detect openings by finding gaps in wall lines
        
        Args:
            edges: Edge-detected image
            walls: List of detected walls
            scale_ratio: Scale ratio
            
        Returns:
            List of openings detected from gaps
        """
        openings = []
        
        # For each wall, check for gaps along the wall line
        for wall in walls:
            start = wall["start"]
            end = wall["end"]
            
            # Sample points along the wall
            num_samples = 20
            for i in range(num_samples):
                t = i / (num_samples - 1)
                x = int(start[0] + t * (end[0] - start[0]))
                y = int(start[1] + t * (end[1] - start[1]))
                
                # Check if there's a gap (no edge) near this point
                # Look in a small region perpendicular to the wall
                gap_size = 10  # pixels
                gap_found = False
                
                # Check perpendicular direction
                dx = end[0] - start[0]
                dy = end[1] - start[1]
                length = np.sqrt(dx**2 + dy**2)
                if length > 0:
                    # Perpendicular vector
                    perp_x = -dy / length
                    perp_y = dx / length
                    
                    # Check for gap in perpendicular direction
                    gap_pixels = 0
                    for offset in range(-gap_size, gap_size + 1):
                        check_x = int(x + offset * perp_x)
                        check_y = int(y + offset * perp_y)
                        
                        if (0 <= check_y < edges.shape[0] and 
                            0 <= check_x < edges.shape[1]):
                            if edges[check_y, check_x] == 0:
                                gap_pixels += 1
                    
                    # If significant gap found, it might be an opening
                    if gap_pixels > gap_size * 0.7:
                        gap_found = True
                
                if gap_found:
                    # Estimate opening width
                    width_pixels = gap_size * 2
                    width_meters = width_pixels * scale_ratio
                    
                    # Classify as door or window based on size
                    opening_type = "door" if width_meters < 1.2 else "window"
                    
                    openings.append({
                        "type": opening_type,
                        "position": [float(x), float(y)],
                        "width": width_meters,
                        "method": "gap"
                    })
        
        return openings
    
    def _detect_openings_from_contours(self, edges: np.ndarray, 
                                       scale_ratio: float) -> List[Dict]:
        """
        Detect openings from small rectangular contours
        
        Args:
            edges: Edge-detected image
            scale_ratio: Scale ratio
            
        Returns:
            List of openings detected from contours
        """
        openings = []
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Adjust size thresholds based on scale
            min_area = 100 / (scale_ratio ** 2) if scale_ratio > 0 else 100
            max_area = 2000 / (scale_ratio ** 2) if scale_ratio > 0 else 2000
            
            if min_area < area < max_area:
                # Check if contour is roughly rectangular
                rect = cv2.minAreaRect(contour)
                center = rect[0]
                width, height = rect[1]
                
                # Calculate aspect ratio
                aspect_ratio = max(width, height) / min(width, height) if min(width, height) > 0 else 1.0
                
                # Openings should be roughly rectangular (aspect ratio < 3)
                if aspect_ratio < 3:
                    # Estimate opening size in meters
                    width_meters = max(width, height) * scale_ratio
                    
                    # Classify based on size and aspect ratio
                    if width_meters < 1.2:
                        opening_type = "door"
                    elif width_meters < 2.0:
                        opening_type = "window"
                    else:
                        continue  # Too large, probably not an opening
                    
                    openings.append({
                        "type": opening_type,
                        "position": [float(center[0]), float(center[1])],
                        "width": width_meters,
                        "method": "contour"
                    })
        
        return openings
    
    def _validate_openings(self, openings: List[Dict], walls: List[Dict], 
                           scale_ratio: float) -> List[Dict]:
        """
        Validate openings: ensure they're on walls and have reasonable dimensions
        
        Args:
            openings: List of detected openings
            walls: List of detected walls
            scale_ratio: Scale ratio
            
        Returns:
            Validated and deduplicated openings
        """
        validated = []
        
        for opening in openings:
            pos = opening["position"]
            width = opening["width"]
            
            # Validate dimensions
            # Doors: 0.6m - 1.2m wide
            # Windows: 0.8m - 2.0m wide
            if opening["type"] == "door":
                if not (0.6 <= width <= 1.2):
                    continue
            elif opening["type"] == "window":
                if not (0.8 <= width <= 2.0):
                    continue
            
            # Check if opening is near a wall
            is_near_wall = False
            for wall in walls:
                dist = self._distance_to_wall(pos, wall)
                if dist < 50:  # Within 50 pixels of a wall
                    is_near_wall = True
                    break
            
            if is_near_wall or len(walls) == 0:  # Allow if no walls detected
                validated.append(opening)
        
        # Deduplicate: remove openings that are too close together
        deduplicated = []
        used = set()
        
        for i, opening1 in enumerate(validated):
            if i in used:
                continue
            
            group = [opening1]
            for j, opening2 in enumerate(validated[i+1:], start=i+1):
                if j in used:
                    continue
                
                # Check distance between openings
                dist = np.sqrt((opening1["position"][0] - opening2["position"][0])**2 +
                              (opening1["position"][1] - opening2["position"][1])**2)
                
                if dist < 30:  # Too close, merge them
                    group.append(opening2)
                    used.add(j)
            
            # Use the opening with highest confidence (prefer gap method)
            best = max(group, key=lambda o: 1 if o.get("method") == "gap" else 0)
            deduplicated.append(best)
            used.add(i)
        
        return deduplicated
    
    def _distance_to_wall(self, point: List[float], wall: Dict) -> float:
        """Calculate distance from point to wall line segment"""
        p = np.array(point)
        p1 = np.array(wall["start"])
        p2 = np.array(wall["end"])
        
        # Vector from p1 to p2
        v = p2 - p1
        # Vector from p1 to p
        w = p - p1
        
        # Project w onto v
        if np.dot(v, v) == 0:
            return float(np.linalg.norm(p - p1))
        
        t = max(0, min(1, np.dot(w, v) / np.dot(v, v)))
        proj = p1 + t * v
        
        return float(np.linalg.norm(p - proj))
    
    def _calculate_confidence(self, rooms: List, walls: List, 
                             legend_data: Optional[Dict[str, Any]] = None,
                             openings: Optional[List] = None) -> float:
        """
        Enhanced confidence scoring with feature quality metrics and consistency checks
        
        Args:
            rooms: List of detected rooms
            walls: List of detected walls
            legend_data: Optional legend data
            openings: Optional list of detected openings
            
        Returns:
            Confidence score (0-100)
        """
        if not rooms:
            return 0.0
        
        # Base confidence from feature counts
        base_confidence = min(100.0, (len(rooms) * 15 + len(walls) * 0.3))
        
        # Feature quality metrics
        quality_score = 0.0
        
        # Room quality: check average room area (reasonable rooms are 10-50 sqm)
        if rooms:
            avg_area = sum(r.get("area", 0) for r in rooms) / len(rooms)
            if 10 <= avg_area <= 50:
                quality_score += 15.0
            elif 5 <= avg_area <= 100:
                quality_score += 10.0
        
        # Wall quality: check if walls form reasonable structure
        if walls:
            # Check if walls are mostly aligned to common angles
            aligned_count = sum(1 for w in walls if abs(w.get("angle", 0) % 90) < 5)
            alignment_ratio = aligned_count / len(walls) if walls else 0
            quality_score += alignment_ratio * 10.0
        
        # Consistency checks
        consistency_score = 0.0
        
        # Check if rooms are bounded by walls (spatial consistency)
        if walls and rooms:
            # Simple check: are rooms near walls?
            rooms_near_walls = 0
            for room in rooms:
                room_center = self._get_room_center(room)
                for wall in walls[:5]:  # Check first 5 walls
                    if self._distance_to_wall(room_center, wall) < 100:
                        rooms_near_walls += 1
                        break
            
            consistency_ratio = rooms_near_walls / len(rooms) if rooms else 0
            consistency_score += consistency_ratio * 15.0
        
        # Check if openings are on walls
        if openings and walls:
            openings_on_walls = sum(1 for o in openings 
                                   if any(self._distance_to_wall(o["position"], w) < 50 
                                         for w in walls))
            if openings:
                consistency_score += (openings_on_walls / len(openings)) * 10.0
        
        # Scale validation: check if detected dimensions are reasonable
        scale_score = 0.0
        if legend_data and legend_data.get("scale_ratio"):
            # If we have scale info, boost confidence
            scale_score = 10.0
        
        # Legend data boost
        legend_boost = 0.0
        if legend_data:
            if legend_data.get("scale"):
                legend_boost += 10.0
            if legend_data.get("room_labels"):
                legend_boost += 5.0
            if legend_data.get("confidence"):
                # Use legend confidence as additional factor
                legend_boost = (legend_boost + legend_data["confidence"] * 0.3)
        
        # Combine all scores
        total_confidence = (base_confidence * 0.4 + 
                           quality_score * 0.3 + 
                           consistency_score * 0.2 + 
                           scale_score * 0.05 + 
                           legend_boost * 0.05)
        
        return min(100.0, max(0.0, total_confidence))
    
    def _get_room_center(self, room: Dict) -> List[float]:
        """Calculate center point of a room"""
        polygon = room.get("polygon", [])
        if not polygon:
            return [0, 0]
        
        x_sum = sum(p[0] for p in polygon)
        y_sum = sum(p[1] for p in polygon)
        n = len(polygon)
        
        return [x_sum / n, y_sum / n]


def get_sketch_reader() -> SketchReader:
    """
    Factory function to get sketch reader
    Always returns OpenCVReader (Replicate/ControlNet removed - not adding value)
    """
    return OpenCVReader()


def read_sketch(image_path: str, legend_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to read sketch using configured reader
    
    Args:
        image_path: Path to sketch image
        legend_data: Optional parsed legend data
    """
    reader = get_sketch_reader()
    return reader.read_sketch(image_path, legend_data)

