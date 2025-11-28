"""
World-Class Quality Assessment Module
Multi-stage quality gates with dynamic thresholds and automatic calibration
Inspired by SortDesk's Gates validation approach
"""
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger

from ..config import settings


@dataclass
class QualityMetrics:
    """Quality metrics for a single assessment stage"""
    sharpness: float = 0.0
    contrast: float = 0.0
    noise_level: float = 0.0
    brightness: float = 0.0
    edge_density: float = 0.0
    resolution_score: float = 0.0
    overall_score: float = 0.0
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class DetectionQualityMetrics:
    """Quality metrics for detection stage"""
    room_count: int = 0
    wall_count: int = 0
    opening_count: int = 0
    geometry_coherence: float = 0.0
    area_consistency: float = 0.0
    connectivity_score: float = 0.0
    confidence_score: float = 0.0
    issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class QualityGateResult:
    """Result from a quality gate"""
    passed: bool
    confidence: float  # 0-100
    metrics: Any  # QualityMetrics or DetectionQualityMetrics
    threshold_used: float
    message: str
    recommendations: List[str] = field(default_factory=list)


class QualityAssessor:
    """
    World-class quality assessor with multi-stage validation
    Provides pre-processing, detection, and post-IFC quality gates
    """
    
    def __init__(self):
        # Dynamic thresholds that can be calibrated
        self.preprocessing_thresholds = {
            "min_sharpness": 30.0,
            "min_contrast": 0.3,
            "max_noise": 0.15,
            "min_brightness": 0.2,
            "max_brightness": 0.8,
            "min_edge_density": 0.05,
            "min_resolution": 500,  # pixels
        }
        
        self.detection_thresholds = {
            "min_rooms": 1,
            "min_walls": 4,
            "min_geometry_coherence": 0.5,
            "min_area_consistency": 0.6,
            "min_connectivity": 0.4,
            "min_confidence": 30.0,
        }
        
        self.ifc_thresholds = {
            "min_confidence": 50.0,
            "max_errors": 0,
            "max_warnings": 10,
        }
    
    def assess_sketch_quality(self, image_path: str) -> QualityMetrics:
        """
        Gate 1: Pre-processing quality assessment
        Assesses sketch quality before detection begins
        
        Args:
            image_path: Path to sketch image
            
        Returns:
            QualityMetrics with detailed assessment
        """
        metrics = QualityMetrics()
        issues = []
        recommendations = []
        
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                metrics.issues.append("Failed to load image")
                return metrics
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            height, width = gray.shape
            
            # 1. Sharpness assessment (Laplacian variance)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            metrics.sharpness = float(laplacian_var)
            if metrics.sharpness < self.preprocessing_thresholds["min_sharpness"]:
                issues.append(f"Low sharpness ({metrics.sharpness:.1f}), image may be blurred")
                recommendations.append("Apply sharpening filter before processing")
            
            # 2. Contrast assessment (standard deviation)
            contrast = float(np.std(gray))
            normalized_contrast = contrast / 255.0
            metrics.contrast = normalized_contrast
            if metrics.contrast < self.preprocessing_thresholds["min_contrast"]:
                issues.append(f"Low contrast ({metrics.contrast:.2f}), features may be hard to detect")
                recommendations.append("Enhance contrast using CLAHE")
            
            # 3. Noise level assessment (using median filter difference)
            median = cv2.medianBlur(gray, 5)
            noise = np.mean(np.abs(gray.astype(float) - median.astype(float))) / 255.0
            metrics.noise_level = float(noise)
            if metrics.noise_level > self.preprocessing_thresholds["max_noise"]:
                issues.append(f"High noise level ({metrics.noise_level:.3f})")
                recommendations.append("Apply denoising filter")
            
            # 4. Brightness assessment
            mean_brightness = float(np.mean(gray)) / 255.0
            metrics.brightness = mean_brightness
            if mean_brightness < self.preprocessing_thresholds["min_brightness"]:
                issues.append("Image too dark")
                recommendations.append("Brighten image before processing")
            elif mean_brightness > self.preprocessing_thresholds["max_brightness"]:
                issues.append("Image too bright")
                recommendations.append("Darken image before processing")
            
            # 5. Edge density (indicator of content richness)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (height * width)
            metrics.edge_density = float(edge_density)
            if edge_density < self.preprocessing_thresholds["min_edge_density"]:
                issues.append(f"Low edge density ({edge_density:.3f}), sketch may be too sparse")
                recommendations.append("Verify sketch contains sufficient detail")
            
            # 6. Resolution assessment
            min_dimension = min(height, width)
            metrics.resolution_score = float(min_dimension) / 1000.0  # Normalized to 1.0 for 1000px
            if min_dimension < self.preprocessing_thresholds["min_resolution"]:
                issues.append(f"Low resolution ({min_dimension}px), may affect detection accuracy")
                recommendations.append("Use higher resolution image if available")
            
            # Calculate overall score (weighted average)
            weights = {
                "sharpness": 0.25,
                "contrast": 0.25,
                "noise": 0.20,
                "brightness": 0.10,
                "edge_density": 0.15,
                "resolution": 0.05,
            }
            
            # Normalize components to 0-1 scale
            sharpness_norm = min(1.0, metrics.sharpness / 100.0)
            contrast_norm = min(1.0, metrics.contrast / 0.5)
            noise_norm = 1.0 - min(1.0, metrics.noise_level / 0.2)
            brightness_norm = 1.0 - abs(metrics.brightness - 0.5) * 2
            edge_norm = min(1.0, metrics.edge_density / 0.1)
            resolution_norm = min(1.0, metrics.resolution_score)
            
            overall = (
                weights["sharpness"] * sharpness_norm +
                weights["contrast"] * contrast_norm +
                weights["noise"] * noise_norm +
                weights["brightness"] * brightness_norm +
                weights["edge_density"] * edge_norm +
                weights["resolution"] * resolution_norm
            ) * 100.0
            
            metrics.overall_score = float(overall)
            metrics.issues = issues
            metrics.recommendations = recommendations
            
            logger.info(f"Sketch quality assessment: {metrics.overall_score:.1f}/100")
            
        except Exception as e:
            logger.error(f"Error assessing sketch quality: {e}")
            metrics.issues.append(f"Assessment error: {str(e)}")
        
        return metrics
    
    def assess_detection_quality(self, plan_data: Dict[str, Any]) -> DetectionQualityMetrics:
        """
        Gate 2: Detection quality assessment
        Validates detected geometry coherence and consistency
        
        Args:
            plan_data: Detected plan geometry data
            
        Returns:
            DetectionQualityMetrics with assessment
        """
        metrics = DetectionQualityMetrics()
        issues = []
        recommendations = []
        
        try:
            rooms = plan_data.get("rooms", [])
            walls = plan_data.get("walls", [])
            openings = plan_data.get("openings", [])
            
            metrics.room_count = len(rooms)
            metrics.wall_count = len(walls)
            metrics.opening_count = len(openings)
            
            # 1. Basic counts validation
            if metrics.room_count < self.detection_thresholds["min_rooms"]:
                issues.append(f"Insufficient rooms detected ({metrics.room_count})")
                recommendations.append("Check sketch for closed room boundaries")
            
            if metrics.wall_count < self.detection_thresholds["min_walls"]:
                issues.append(f"Insufficient walls detected ({metrics.wall_count})")
                recommendations.append("Verify wall lines are clear and continuous")
            
            # 2. Geometry coherence (area consistency, reasonable sizes)
            if rooms:
                areas = [r.get("area", 0) for r in rooms if r.get("area", 0) > 0]
                if areas:
                    mean_area = np.mean(areas)
                    std_area = np.std(areas)
                    # Coherence: lower std relative to mean is better
                    cv_area = std_area / mean_area if mean_area > 0 else 1.0
                    metrics.area_consistency = float(max(0.0, 1.0 - cv_area))
                    
                    # Check for unreasonable sizes
                    min_reasonable = 3.0  # sq meters
                    max_reasonable = 100.0  # sq meters
                    unreasonable = [a for a in areas if a < min_reasonable or a > max_reasonable]
                    if unreasonable:
                        issues.append(f"Some rooms have unreasonable sizes: {unreasonable}")
                        recommendations.append("Verify scale ratio is correct")
            
            # 3. Connectivity score (rooms should be connected by walls/openings)
            # Simplified: check if openings align with walls
            if walls and openings:
                # Count openings that could reasonably align with walls
                aligned_count = 0
                for opening in openings:
                    pos = opening.get("position", [0, 0])
                    # Check if opening is near any wall
                    for wall in walls[:10]:  # Sample walls
                        start = wall.get("start", [0, 0])
                        end = wall.get("end", [0, 0])
                        # Simple distance check
                        dist_to_start = np.sqrt((pos[0] - start[0])**2 + (pos[1] - start[1])**2)
                        dist_to_end = np.sqrt((pos[0] - end[0])**2 + (pos[1] - end[1])**2)
                        min_dist = min(dist_to_start, dist_to_end)
                        if min_dist < 50:  # 50 pixels threshold
                            aligned_count += 1
                            break
                
                if openings:
                    metrics.connectivity_score = float(aligned_count / len(openings))
                    if metrics.connectivity_score < self.detection_thresholds["min_connectivity"]:
                        issues.append(f"Low connectivity ({metrics.connectivity_score:.2f}), openings may not align with walls")
            
            # 4. Overall geometry coherence (simplified heuristic)
            # Based on ratios and consistency
            coherence_factors = []
            
            # Room-to-wall ratio (should be reasonable)
            if metrics.wall_count > 0:
                room_wall_ratio = metrics.room_count / metrics.wall_count
                # Reasonable range: 0.1 to 0.5
                if 0.1 <= room_wall_ratio <= 0.5:
                    coherence_factors.append(1.0)
                else:
                    coherence_factors.append(0.5)
            
            # Opening-to-room ratio
            if metrics.room_count > 0:
                opening_room_ratio = metrics.opening_count / metrics.room_count
                # Reasonable range: 0.5 to 3.0
                if 0.5 <= opening_room_ratio <= 3.0:
                    coherence_factors.append(1.0)
                else:
                    coherence_factors.append(0.7)
            
            metrics.geometry_coherence = float(np.mean(coherence_factors)) if coherence_factors else 0.0
            
            # 5. Use provided confidence or calculate
            metrics.confidence_score = float(plan_data.get("confidence", 0.0))
            
            # Validate confidence thresholds
            if metrics.confidence_score < self.detection_thresholds["min_confidence"]:
                issues.append(f"Low detection confidence ({metrics.confidence_score:.1f}%)")
                recommendations.append("Consider retrying with enhanced preprocessing")
            
            if metrics.geometry_coherence < self.detection_thresholds["min_geometry_coherence"]:
                issues.append(f"Low geometry coherence ({metrics.geometry_coherence:.2f})")
                recommendations.append("Review detected geometry for consistency")
            
            metrics.issues = issues
            metrics.recommendations = recommendations
            
            logger.info(f"Detection quality: confidence={metrics.confidence_score:.1f}%, "
                       f"coherence={metrics.geometry_coherence:.2f}")
            
        except Exception as e:
            logger.error(f"Error assessing detection quality: {e}")
            metrics.issues.append(f"Assessment error: {str(e)}")
        
        return metrics
    
    def assess_ifc_quality(self, qc_report: Any) -> QualityGateResult:
        """
        Gate 3: Post-IFC quality assessment
        Validates generated IFC file quality
        
        Args:
            qc_report: QCReport from ifc_qc module
            
        Returns:
            QualityGateResult with validation
        """
        try:
            confidence = qc_report.confidence_score
            errors = qc_report.errors
            warnings = qc_report.warnings
            
            # Count critical errors
            critical_errors = [e for e in errors if e.severity == "critical"]
            
            # Check thresholds
            passed = (
                confidence >= self.ifc_thresholds["min_confidence"] and
                len(critical_errors) <= self.ifc_thresholds["max_errors"] and
                len(warnings) <= self.ifc_thresholds["max_warnings"]
            )
            
            recommendations = []
            if not passed:
                if confidence < self.ifc_thresholds["min_confidence"]:
                    recommendations.append(f"IFC confidence ({confidence:.1f}%) below threshold")
                if len(critical_errors) > self.ifc_thresholds["max_errors"]:
                    recommendations.append(f"Too many critical errors ({len(critical_errors)})")
                if len(warnings) > self.ifc_thresholds["max_warnings"]:
                    recommendations.append(f"Too many warnings ({len(warnings)})")
            
            message = f"IFC quality: {confidence:.1f}% confidence, "
            message += f"{len(critical_errors)} errors, {len(warnings)} warnings"
            
            return QualityGateResult(
                passed=passed,
                confidence=confidence,
                metrics=qc_report,
                threshold_used=self.ifc_thresholds["min_confidence"],
                message=message,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Error assessing IFC quality: {e}")
            return QualityGateResult(
                passed=False,
                confidence=0.0,
                metrics=None,
                threshold_used=0.0,
                message=f"Assessment error: {str(e)}",
                recommendations=["Review IFC file manually"]
            )
    
    def run_preprocessing_gate(self, image_path: str, threshold: Optional[float] = None) -> QualityGateResult:
        """
        Run Gate 1: Pre-processing quality gate
        
        Args:
            image_path: Path to sketch
            threshold: Optional custom threshold (uses default if None)
            
        Returns:
            QualityGateResult
        """
        metrics = self.assess_sketch_quality(image_path)
        threshold_used = threshold or 50.0  # Default 50% threshold
        
        passed = metrics.overall_score >= threshold_used
        message = f"Pre-processing gate: {metrics.overall_score:.1f}/100"
        if not passed:
            message += f" (threshold: {threshold_used:.1f})"
        
        return QualityGateResult(
            passed=passed,
            confidence=metrics.overall_score,
            metrics=metrics,
            threshold_used=threshold_used,
            message=message,
            recommendations=metrics.recommendations
        )
    
    def run_detection_gate(self, plan_data: Dict[str, Any], threshold: Optional[float] = None) -> QualityGateResult:
        """
        Run Gate 2: Detection quality gate
        
        Args:
            plan_data: Detected plan data
            threshold: Optional custom confidence threshold
            
        Returns:
            QualityGateResult
        """
        metrics = self.assess_detection_quality(plan_data)
        threshold_used = threshold or self.detection_thresholds["min_confidence"]
        
        # Combine multiple factors for gate decision
        gate_score = (
            metrics.confidence_score * 0.5 +
            metrics.geometry_coherence * 100 * 0.3 +
            (1.0 if metrics.room_count >= self.detection_thresholds["min_rooms"] else 0.0) * 100 * 0.2
        )
        
        passed = gate_score >= threshold_used
        
        message = f"Detection gate: {gate_score:.1f}/100 "
        message += f"(confidence: {metrics.confidence_score:.1f}%, "
        message += f"coherence: {metrics.geometry_coherence:.2f})"
        
        return QualityGateResult(
            passed=passed,
            confidence=gate_score,
            metrics=metrics,
            threshold_used=threshold_used,
            message=message,
            recommendations=metrics.recommendations
        )
    
    def calculate_overall_confidence(self, 
                                    sketch_metrics: QualityMetrics,
                                    detection_metrics: DetectionQualityMetrics,
                                    ifc_confidence: float = 0.0) -> float:
        """
        Calculate overall confidence across all stages
        
        Args:
            sketch_metrics: Pre-processing metrics
            detection_metrics: Detection metrics
            ifc_confidence: Post-IFC confidence score
            
        Returns:
            Overall confidence score (0-100)
        """
        weights = {
            "sketch": 0.20,
            "detection": 0.50,
            "ifc": 0.30,
        }
        
        overall = (
            weights["sketch"] * sketch_metrics.overall_score +
            weights["detection"] * detection_metrics.confidence_score +
            weights["ifc"] * ifc_confidence
        )
        
        return float(overall)
    
    def recommend_preprocessing(self, image_path: str) -> List[str]:
        """
        Recommend preprocessing steps based on quality assessment
        
        Args:
            image_path: Path to sketch
            
        Returns:
            List of recommended preprocessing steps
        """
        metrics = self.assess_sketch_quality(image_path)
        return metrics.recommendations


# Convenience functions
def assess_sketch_quality(image_path: str) -> QualityMetrics:
    """Assess sketch quality"""
    assessor = QualityAssessor()
    return assessor.assess_sketch_quality(image_path)


def assess_detection_quality(plan_data: Dict[str, Any]) -> DetectionQualityMetrics:
    """Assess detection quality"""
    assessor = QualityAssessor()
    return assessor.assess_detection_quality(plan_data)


def run_preprocessing_gate(image_path: str, threshold: Optional[float] = None) -> QualityGateResult:
    """Run pre-processing quality gate"""
    assessor = QualityAssessor()
    return assessor.run_preprocessing_gate(image_path, threshold)


def run_detection_gate(plan_data: Dict[str, Any], threshold: Optional[float] = None) -> QualityGateResult:
    """Run detection quality gate"""
    assessor = QualityAssessor()
    return assessor.run_detection_gate(plan_data, threshold)

