"""
Legend parser module
Attempts to detect and parse standard architectural legends from sketches

Note: Requires pytesseract (Tesseract OCR) for full functionality.
May return empty results if:
- Text is unclear or in non-standard locations
- OCR is unavailable or fails
- Legend format is non-standard

System gracefully degrades if OCR is unavailable, using edge density detection only.
"""
import cv2
import numpy as np
import re
from typing import Dict, Any, Optional, Tuple, List
from pathlib import Path
from PIL import Image
from loguru import logger

# Try to import pytesseract, fallback if not available
try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False
    logger.warning("pytesseract not available. Legend parsing will be limited.")


class LegendParser:
    """
    Parses architectural legends from sketch images
    Detects scale, room labels, line types, and symbols
    
    Effectiveness varies based on:
    - Image quality and clarity
    - Legend location (works best in standard corners)
    - Text readability (requires OCR for text detection)
    - Format standardization
    
    May return empty or partial results if:
    - Text is unclear or handwritten
    - Legend is in non-standard location
    - OCR is unavailable or fails
    - Scale format is non-standard
    
    Best results with: Clear printed text, standard legend locations (bottom-right/left),
    standard scale formats (1:100, 1/4" = 1'-0", etc.)
    """
    
    # Standard room type keywords
    ROOM_KEYWORDS = [
        "bedroom", "bath", "bathroom", "kitchen", "living", "dining",
        "office", "study", "closet", "pantry", "laundry", "garage",
        "hall", "hallway", "entry", "foyer", "stair", "staircase"
    ]
    
    # Scale patterns
    SCALE_PATTERNS = [
        r'1\s*[:/]\s*(\d+)',  # 1:100, 1/100
        r'(\d+)\s*/\s*(\d+)"\s*=\s*(\d+)\s*[\'-]?(\d+)?"',  # 1/4" = 1'-0"
        r'(\d+)"\s*=\s*(\d+)\s*[\'-]?(\d+)?"',  # 1" = 10'-0"
        r'(\d+)\s*inch(es)?\s*=\s*(\d+)\s*feet?',  # 1 inch = 10 feet
        r'scale\s*[:]?\s*1\s*[:/]\s*(\d+)',  # Scale: 1:100
        r'(\d+)\s*mm\s*=\s*(\d+)\s*m',  # 100mm = 1m
    ]
    
    def __init__(self):
        """Initialize legend parser"""
        pass
    
    def parse_legend_from_sketch(self, image_path: str) -> Dict[str, Any]:
        """
        Main method: Auto-detect and parse legend from sketch image
        
        Args:
            image_path: Path to sketch image
            
        Returns:
            dict with parsed legend data
        """
        result = {
            "scale": None,
            "scale_ratio": None,
            "room_labels": {},
            "line_types": {
                "solid": "wall",
                "dashed": "hidden",
                "dotted": "centerline"
            },
            "symbols": {},
            "confidence": 0.0
        }
        
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                logger.warning(f"Could not read image: {image_path}")
                return result
            
            # Detect legend region
            legend_region = self.detect_legend_region(img)
            
            if legend_region is None:
                logger.info("No legend region detected in sketch")
                # Still try to extract scale from entire image
                result["scale"], result["scale_ratio"] = self.extract_scale(img)
                result["confidence"] = 0.3  # Low confidence if no legend region
                return result
            
            # Extract text from legend region
            try:
                legend_text = self._extract_text_from_region(img, legend_region)
            except Exception as e:
                logger.warning(f"Error extracting text from legend region: {e}")
                legend_text = ""
            
            # Parse scale
            try:
                scale_text, scale_ratio = self.extract_scale(img, legend_text)
                result["scale"] = scale_text
                result["scale_ratio"] = scale_ratio
            except Exception as e:
                logger.warning(f"Error extracting scale: {e}")
                result["scale"] = None
                result["scale_ratio"] = None
            
            # Extract room labels
            try:
                room_labels = self.extract_room_labels(img, legend_text)
                result["room_labels"] = room_labels
            except Exception as e:
                logger.warning(f"Error extracting room labels: {e}")
                result["room_labels"] = {}
            
            # Extract standard symbols (door swing, windows, etc.)
            try:
                symbols = self.extract_standard_symbols(img, legend_region)
                result["symbols"] = symbols
            except Exception as e:
                logger.warning(f"Error extracting symbols: {e}")
                result["symbols"] = {}
            
            # Calculate confidence
            confidence = self._calculate_confidence(result, legend_region)
            result["confidence"] = confidence
            
            logger.info(f"Legend parsed: scale={scale_text}, rooms={len(room_labels)}, confidence={confidence:.2f}")
            
        except Exception as e:
            logger.error(f"Error parsing legend: {e}")
            result["confidence"] = 0.0
        
        return result
    
    def detect_legend_region(self, img: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect legend box/region in sketch
        
        Looks for rectangular regions in corners/bottom-right with text
        
        Args:
            img: Image array
            
        Returns:
            (x, y, width, height) bounding box or None
        """
        height, width = img.shape[:2]
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Common legend locations (bottom-right, bottom-left, top-right)
        legend_candidates = [
            (int(width * 0.7), int(height * 0.7), int(width * 0.3), int(height * 0.3)),  # Bottom-right
            (int(width * 0.05), int(height * 0.7), int(width * 0.3), int(height * 0.3)),  # Bottom-left
            (int(width * 0.7), int(height * 0.05), int(width * 0.3), int(height * 0.3)),  # Top-right
        ]
        
        # Check each candidate region
        for x, y, w, h in legend_candidates:
            region = gray[y:y+h, x:x+w]
            
            # Check if region has significant text
            # Use edge density as proxy for text content
            edges = cv2.Canny(region, 50, 150)
            edge_density = np.sum(edges > 0) / (w * h)
            
            # Also check for text using OCR
            if HAS_TESSERACT:
                region_img = Image.fromarray(region)
                try:
                    text = pytesseract.image_to_string(region_img, config='--psm 6')
                    text_length = len(text.strip())
                    
                    # If region has text and reasonable edge density, it's likely a legend
                    if text_length > 20 and edge_density > 0.05:
                        logger.info(f"Legend region detected at ({x}, {y}, {w}, {h})")
                        return (x, y, w, h)
                except Exception as e:
                    logger.debug(f"OCR error on region: {e}")
                    continue
            else:
                # Fallback: use edge density only if tesseract not available
                if edge_density > 0.1:
                    logger.info(f"Legend region detected at ({x}, {y}, {w}, {h}) (edge density only)")
                    return (x, y, w, h)
        
        return None
    
    def extract_scale(self, img: np.ndarray, text: Optional[str] = None) -> Tuple[Optional[str], Optional[float]]:
        """
        Extract scale information from image or text
        
        Args:
            img: Image array
            text: Optional pre-extracted text
            
        Returns:
            (scale_text, scale_ratio) tuple
        """
        if text is None:
            if not HAS_TESSERACT:
                logger.warning("pytesseract not available, cannot extract scale")
                return None, None
            
            # Extract text from entire image (fallback)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pil_img = Image.fromarray(gray)
            try:
                text = pytesseract.image_to_string(pil_img, config='--psm 6')
            except Exception as e:
                logger.warning(f"OCR error: {e}")
                return None, None
        
        # Search for scale patterns
        for pattern in self.SCALE_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                scale_text = match.group(0)
                scale_ratio = self._calculate_scale_ratio(scale_text, match.groups())
                if scale_ratio:
                    logger.info(f"Scale found: {scale_text}, ratio: {scale_ratio}")
                    return scale_text, scale_ratio
        
        # Default scale (assume 100 pixels = 1 meter if no scale found)
        logger.info("No scale found, using default: 100 pixels = 1 meter")
        return None, 0.01
    
    def _calculate_scale_ratio(self, scale_text: str, groups: Tuple) -> Optional[float]:
        """
        Calculate meters-per-pixel ratio from scale text
        
        Args:
            scale_text: Scale text (e.g., "1:100")
            groups: Regex match groups
            
        Returns:
            Scale ratio (meters per pixel) or None
        """
        try:
            # Pattern 1: 1:100 or 1/100
            if len(groups) == 1:
                denominator = int(groups[0])
                # Scale 1:100 means 1 drawing unit = 100 real units
                # Assume 1 meter in drawing = denominator meters in real world
                # We need to estimate pixel density - assume 100 pixels per drawing unit (1 meter)
                pixels_per_drawing_meter = 100.0
                # If scale is 1:100, then 100 pixels = 100 meters in real world
                # So 1 pixel = 1 meter / 100 pixels = 0.01 meters per pixel
                real_meters_per_drawing_meter = denominator
                meters_per_pixel = real_meters_per_drawing_meter / pixels_per_drawing_meter
                return meters_per_pixel
            
            # Pattern 2: 1/4" = 1'-0" or similar
            if len(groups) >= 3:
                drawing_units = int(groups[0])
                drawing_denom = int(groups[1]) if groups[1] else 1
                real_units = int(groups[2])
                real_denom = int(groups[3]) if len(groups) > 3 and groups[3] else 0
                
                # Convert to inches
                drawing_inches = drawing_units / drawing_denom
                real_inches = real_units * 12 + real_denom
                
                # Convert to meters (1 inch = 0.0254 meters)
                real_meters = real_inches * 0.0254
                
                # Assume drawing is at 100 DPI (dots per inch)
                pixels_per_drawing_inch = 100.0
                pixels = drawing_inches * pixels_per_drawing_inch
                
                # Calculate meters per pixel
                if pixels > 0:
                    meters_per_pixel = real_meters / pixels
                    return meters_per_pixel
                return None
            
        except Exception as e:
            logger.warning(f"Error calculating scale ratio: {e}")
        
        return None
    
    def extract_room_labels(self, img: np.ndarray, text: Optional[str] = None) -> Dict[str, str]:
        """
        Extract room labels from image or text
        
        Args:
            img: Image array
            text: Optional pre-extracted text
            
        Returns:
            dict mapping room labels to room types
        """
        room_labels = {}
        
        if text is None:
            if not HAS_TESSERACT:
                logger.warning("pytesseract not available, cannot extract room labels")
                return room_labels
            
            # Extract text from entire image
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            pil_img = Image.fromarray(gray)
            try:
                text = pytesseract.image_to_string(pil_img, config='--psm 6')
            except Exception as e:
                logger.warning(f"OCR error: {e}")
                return room_labels
        
        # Search for room keywords
        text_lower = text.lower()
        for keyword in self.ROOM_KEYWORDS:
            # Find keyword in text (with context)
            pattern = rf'\b(\w+)\s*{keyword}\b'
            matches = re.finditer(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                label = match.group(0).strip()
                room_type = keyword
                room_labels[label] = room_type
        
        return room_labels
    
    def extract_standard_symbols(self, img: np.ndarray, legend_region: Optional[Tuple] = None) -> Dict[str, str]:
        """
        Extract standard architectural symbols
        
        Args:
            img: Image array
            legend_region: Optional legend region bounding box
            
        Returns:
            dict mapping symbol descriptions to meanings
        """
        symbols = {
            "door_swing": "door",
            "window": "window",
            "wall": "wall",
            "column": "column"
        }
        
        # In a full implementation, this would use computer vision
        # to detect symbols in the legend region
        # For now, return standard symbols
        
        return symbols
    
    def _extract_text_from_region(self, img: np.ndarray, region: Tuple[int, int, int, int]) -> str:
        """
        Extract text from a specific region
        
        Args:
            img: Image array
            region: (x, y, width, height) bounding box
            
        Returns:
            Extracted text
        """
        x, y, w, h = region
        region_img = img[y:y+h, x:x+w]
        
        # Convert to grayscale
        gray = cv2.cvtColor(region_img, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        if not HAS_TESSERACT:
            logger.warning("pytesseract not available, cannot extract text")
            return ""
        
        # Convert to PIL Image
        pil_img = Image.fromarray(enhanced)
        
        try:
            text = pytesseract.image_to_string(pil_img, config='--psm 6')
            return text
        except Exception as e:
            logger.warning(f"OCR error: {e}")
            return ""
    
    def _calculate_confidence(self, result: Dict[str, Any], legend_region: Optional[Tuple]) -> float:
        """
        Calculate confidence score for legend detection
        
        Args:
            result: Parsed legend data
            legend_region: Detected legend region
            
        Returns:
            Confidence score (0.0 to 1.0)
        """
        confidence = 0.0
        
        # Base confidence if legend region found
        if legend_region is not None:
            confidence += 0.3
        
        # Scale found
        if result["scale"]:
            confidence += 0.3
        
        # Room labels found
        if result["room_labels"]:
            confidence += 0.2 * min(1.0, len(result["room_labels"]) / 5.0)
        
        # Symbols found
        if result["symbols"]:
            confidence += 0.2
        
        return min(1.0, confidence)


def parse_legend_from_sketch(image_path: str) -> Dict[str, Any]:
    """
    Convenience function to parse legend from sketch
    
    Args:
        image_path: Path to sketch image
        
    Returns:
        dict with parsed legend data
    """
    parser = LegendParser()
    return parser.parse_legend_from_sketch(image_path)

