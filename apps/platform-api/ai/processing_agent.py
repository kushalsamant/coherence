"""
World-Class Processing Agent
Intelligent orchestration with adaptive parameter selection and self-learning capabilities
Multi-stage quality gates with automatic retry and improvement strategies
"""
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from loguru import logger
import cv2
import numpy as np
import copy

from .quality_assessor import (
    QualityAssessor,
    QualityMetrics,
    DetectionQualityMetrics,
    QualityGateResult,
    run_preprocessing_gate,
    run_detection_gate,
)
from .room_classifier import MLRoomClassifier, RoomClassification
from .sketch_reader import read_sketch, get_sketch_reader
from .legend_parser import parse_legend_from_sketch
from config.sketch2bim import settings


@dataclass
class ProcessingStrategy:
    """Strategy for processing a sketch"""
    preprocessing_required: bool = False
    preprocessing_steps: List[str] = field(default_factory=list)
    detection_parameters: Dict[str, Any] = field(default_factory=dict)
    reader_type: str = "opencv"  # Always uses OpenCV
    enhancement_level: str = "normal"  # low, normal, high
    confidence_threshold: float = 30.0
    retry_on_low_quality: bool = True
    max_retries: int = 2


@dataclass
class ProcessingResult:
    """Result from processing agent"""
    success: bool
    plan_data: Optional[Dict[str, Any]] = None
    confidence: float = 0.0
    quality_metrics: Dict[str, Any] = field(default_factory=dict)
    gate_results: List[QualityGateResult] = field(default_factory=list)
    strategy_used: Optional[ProcessingStrategy] = None
    retry_count: int = 0
    error: Optional[str] = None
    recommendations: List[str] = field(default_factory=list)


class ProcessingAgent:
    """
    World-class processing agent with intelligent orchestration
    Implements multi-stage quality gates with adaptive strategies
    """
    
    def __init__(self):
        self.quality_assessor = QualityAssessor()
        self.room_classifier = MLRoomClassifier()
        self.strategy_history = []  # For learning/optimization
    
    def process_sketch(
        self,
        sketch_path: str,
        legend_data: Optional[Dict[str, Any]] = None,
        max_retries: int = 2,
        project_type: str = "architecture"
    ) -> ProcessingResult:
        """
        Main entry point: Process sketch with intelligent orchestration
        
        Args:
            sketch_path: Path to sketch image
            legend_data: Optional pre-parsed legend data
            max_retries: Maximum retry attempts
            
        Returns:
            ProcessingResult with full pipeline results
        """
        result = ProcessingResult(success=False)
        gate_results = []
        
        try:
            # Step 1: Run pre-processing gate
            logger.info("Running pre-processing quality gate...")
            pre_gate = self.quality_assessor.run_preprocessing_gate(sketch_path)
            gate_results.append(pre_gate)
            
            if not pre_gate.passed:
                logger.warning(f"Pre-processing gate failed: {pre_gate.message}")
                # Still proceed but with recommendations
            
            # Step 2: Analyze sketch and select strategy
            logger.info("Analyzing sketch and selecting processing strategy...")
            strategy = self.select_detection_strategy(sketch_path, legend_data, pre_gate.metrics)
            result.strategy_used = strategy
            
            # Step 3: Apply preprocessing if needed
            processed_path = sketch_path
            if strategy.preprocessing_required:
                logger.info(f"Applying preprocessing: {strategy.preprocessing_steps}")
                processed_path = self._apply_preprocessing(
                    sketch_path,
                    strategy.preprocessing_steps
                )
            
            # Step 4: Parse legend if not provided
            if legend_data is None:
                logger.info("Parsing legend from sketch...")
                legend_data = parse_legend_from_sketch(processed_path)
            
            # Step 5: Process with retry logic
            plan_data = None
            detection_gate = None
            retry_count = 0
            
            while retry_count <= max_retries:
                try:
                    logger.info(f"Processing sketch (attempt {retry_count + 1}/{max_retries + 1})...")
                    
                    # Read sketch with selected strategy
                    plan_data = self._read_sketch_with_strategy(
                        processed_path,
                        legend_data,
                        strategy,
                        project_type
                    )
                    
                    # Step 6: Enhance room classifications with ML
                    if plan_data and plan_data.get("rooms"):
                        logger.info("Enhancing room classifications with ML...")
                        plan_data = self._enhance_room_classifications(
                            processed_path,
                            plan_data,
                            legend_data
                        )
                    
                    # Step 7: Run detection gate
                    logger.info("Running detection quality gate...")
                    detection_gate = self.quality_assessor.run_detection_gate(
                        plan_data,
                        strategy.confidence_threshold
                    )
                    gate_results.append(detection_gate)
                    
                    # Check if quality is acceptable
                    if detection_gate.passed or not strategy.retry_on_low_quality:
                        break
                    
                    # Quality too low, retry with adjusted strategy
                    retry_count += 1
                    if retry_count <= max_retries:
                        logger.info(f"Quality below threshold, retrying with adjusted strategy...")
                        strategy = self._adjust_strategy_for_retry(
                            strategy,
                            detection_gate,
                            retry_count
                        )
                        # Apply enhanced preprocessing for retry
                        processed_path = self._apply_preprocessing(
                            sketch_path,
                            strategy.preprocessing_steps
                        )
                
                except Exception as e:
                    logger.error(f"Error in processing attempt {retry_count + 1}: {e}")
                    if retry_count >= max_retries:
                        raise
                    retry_count += 1
            
            result.retry_count = retry_count
            
            # Step 8: Validate final result
            if not plan_data:
                result.error = "Failed to detect any geometry"
                return result
            
            if not detection_gate or not detection_gate.passed:
                result.error = f"Detection quality below threshold: {detection_gate.message if detection_gate else 'Unknown'}"
                result.recommendations = detection_gate.recommendations if detection_gate else []
            
            # Step 9: Calculate overall metrics
            sketch_metrics = pre_gate.metrics if pre_gate.metrics else QualityMetrics()
            detection_metrics = detection_gate.metrics if detection_gate else DetectionQualityMetrics()
            
            overall_confidence = self.quality_assessor.calculate_overall_confidence(
                sketch_metrics,
                detection_metrics,
                0.0  # IFC confidence not available yet
            )
            
            result.success = True
            result.plan_data = plan_data
            result.confidence = overall_confidence
            result.quality_metrics = {
                "legend_data": legend_data,  # Store legend data for retrieval
                "sketch": {
                    "score": sketch_metrics.overall_score,
                    "sharpness": sketch_metrics.sharpness,
                    "contrast": sketch_metrics.contrast,
                    "noise": sketch_metrics.noise_level,
                },
                "detection": {
                    "confidence": detection_metrics.confidence_score,
                    "coherence": detection_metrics.geometry_coherence,
                    "rooms": detection_metrics.room_count,
                    "walls": detection_metrics.wall_count,
                }
            }
            result.gate_results = gate_results
            result.recommendations = detection_gate.recommendations if detection_gate else []
            
            logger.info(f"Processing complete: confidence={overall_confidence:.1f}%, "
                       f"retries={retry_count}")
            
        except Exception as e:
            logger.error(f"Processing agent error: {e}")
            result.error = str(e)
            result.gate_results = gate_results
        
        return result
    
    def select_detection_strategy(
        self,
        image_path: str,
        legend_data: Optional[Dict[str, Any]],
        quality_metrics: Optional[QualityMetrics] = None
    ) -> ProcessingStrategy:
        """
        Intelligently select processing strategy based on sketch characteristics
        
        Args:
            image_path: Path to sketch
            legend_data: Optional legend data
            quality_metrics: Optional pre-computed quality metrics
            
        Returns:
            ProcessingStrategy
        """
        strategy = ProcessingStrategy()
        
        # Assess quality if not provided
        if quality_metrics is None:
            quality_metrics = self.quality_assessor.assess_sketch_quality(image_path)
        
        # Determine preprocessing needs
        if quality_metrics.sharpness < 30.0:
            strategy.preprocessing_required = True
            strategy.preprocessing_steps.append("sharpen")
        
        if quality_metrics.contrast < 0.3:
            strategy.preprocessing_required = True
            strategy.preprocessing_steps.append("enhance_contrast")
        
        if quality_metrics.noise_level > 0.15:
            strategy.preprocessing_required = True
            strategy.preprocessing_steps.append("denoise")
        
        if quality_metrics.brightness < 0.2 or quality_metrics.brightness > 0.8:
            strategy.preprocessing_required = True
            strategy.preprocessing_steps.append("normalize_brightness")
        
        # Always use OpenCV reader
        strategy.reader_type = "opencv"
        
        # Set confidence threshold based on quality
        if quality_metrics.overall_score > 70.0:
            strategy.confidence_threshold = 40.0  # Higher threshold for good quality
        elif quality_metrics.overall_score < 40.0:
            strategy.confidence_threshold = 20.0  # Lower threshold for poor quality
        else:
            strategy.confidence_threshold = 30.0  # Default
        
        # Enhancement level
        if quality_metrics.overall_score < 50.0:
            strategy.enhancement_level = "high"
        elif quality_metrics.overall_score > 70.0:
            strategy.enhancement_level = "low"
        else:
            strategy.enhancement_level = "normal"
        
        strategy.retry_on_low_quality = True
        strategy.max_retries = 2
        
        logger.info(f"Selected strategy: reader={strategy.reader_type}, "
                   f"preprocessing={strategy.preprocessing_steps}, "
                   f"threshold={strategy.confidence_threshold}")
        
        return strategy
    
    def _apply_preprocessing(
        self,
        image_path: str,
        steps: List[str]
    ) -> str:
        """
        Apply preprocessing steps to image
        
        Args:
            image_path: Path to original image
            steps: List of preprocessing steps
            
        Returns:
            Path to processed image (may be same as input)
        """
        img = cv2.imread(image_path)
        if img is None:
            return image_path
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
        
        for step in steps:
            if step == "sharpen":
                # Unsharp masking
                gaussian = cv2.GaussianBlur(gray, (0, 0), 2.0)
                gray = cv2.addWeighted(gray, 1.5, gaussian, -0.5, 0)
            elif step == "enhance_contrast":
                # CLAHE
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
                gray = clahe.apply(gray)
            elif step == "denoise":
                # Non-local means denoising
                gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            elif step == "normalize_brightness":
                # Histogram equalization
                gray = cv2.equalizeHist(gray)
        
        # Convert back to BGR if needed
        if len(img.shape) == 3:
            processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        else:
            processed = gray
        
        # Save processed image
        output_path = str(Path(image_path).parent / f"processed_{Path(image_path).name}")
        cv2.imwrite(output_path, processed)
        
        return output_path
    
    def _read_sketch_with_strategy(
        self,
        image_path: str,
        legend_data: Optional[Dict[str, Any]],
        strategy: ProcessingStrategy,
        project_type: str = "architecture"
    ) -> Dict[str, Any]:
        """
        Read sketch using selected strategy
        
        Args:
            image_path: Path to image
            legend_data: Legend data
            strategy: Processing strategy
            project_type: Project type (architecture, landscape, urban)
            
        Returns:
            Plan data dictionary
        """
        try:
            # Always use architecture reader (OpenCV)
            logger.info("Using architecture reader")
            plan_data = read_sketch(image_path, legend_data)
            
            return plan_data
            
        except Exception as e:
            logger.error(f"Error reading sketch: {e}")
            raise
    
    def _enhance_room_classifications(
        self,
        sketch_path: str,
        plan_data: Dict[str, Any],
        legend_data: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Enhance room classifications using ML classifier
        
        Args:
            sketch_path: Path to sketch
            plan_data: Plan data with rooms
            legend_data: Legend data
            
        Returns:
            Enhanced plan data
        """
        try:
            # Load sketch image
            img = cv2.imread(sketch_path)
            if img is None:
                return plan_data
            
            rooms = plan_data.get("rooms", [])
            room_labels = legend_data.get("room_labels", {}) if legend_data else {}
            
            # Classify each room
            enhanced_rooms = []
            for room in rooms:
                polygon = room.get("polygon", [])
                if not polygon:
                    enhanced_rooms.append(room)
                    continue
                
                try:
                    # Convert polygon to contour
                    contour = np.array(polygon, dtype=np.int32).reshape(-1, 1, 2)
                    
                    # Extract region
                    x, y, w, h = cv2.boundingRect(contour)
                    if w > 0 and h > 0:
                        region = img[y:y+h, x:x+w]
                    else:
                        region = img
                    
                    context = {
                        "id": room.get("id"),
                        "area": room.get("area", 0),
                        "area_pixels": room.get("area_pixels", 0),
                        "room_type": room.get("room_type"),
                    }
                    
                    # Classify using ML
                    classification = self.room_classifier.classify_room(
                        region,
                        contour,
                        context,
                        room_labels
                    )
                    
                    # Update room with ML classification if confident
                    if classification.confidence > 60.0:
                        room["room_type"] = classification.room_type
                        room["classification_confidence"] = classification.confidence
                        room["classification_method"] = classification.method
                        room["classification_reasoning"] = classification.reasoning
                    
                    enhanced_rooms.append(room)
                    
                except Exception as e:
                    logger.warning(f"Error enhancing room {room.get('id')}: {e}")
                    enhanced_rooms.append(room)
            
            plan_data["rooms"] = enhanced_rooms
            logger.info(f"Enhanced {len(enhanced_rooms)} room classifications")
            
        except Exception as e:
            logger.error(f"Error enhancing room classifications: {e}")
        
        return plan_data
    
    def _adjust_strategy_for_retry(
        self,
        current_strategy: ProcessingStrategy,
        gate_result: QualityGateResult,
        retry_count: int
    ) -> ProcessingStrategy:
        """
        Adjust strategy for retry based on previous results
        
        Args:
            current_strategy: Current strategy
            gate_result: Previous gate result
            retry_count: Current retry count
            
        Returns:
            Adjusted strategy
        """
        strategy = copy.deepcopy(current_strategy)
        
        # More aggressive preprocessing on retry
        if "enhance_contrast" not in strategy.preprocessing_steps:
            strategy.preprocessing_steps.append("enhance_contrast")
        if "sharpen" not in strategy.preprocessing_steps:
            strategy.preprocessing_steps.append("sharpen")
        
        strategy.preprocessing_required = True
        
        # Lower threshold for retry
        strategy.confidence_threshold = max(20.0, strategy.confidence_threshold - 10.0)
        
        # Reader type is always OpenCV
        
        strategy.enhancement_level = "high"
        
        logger.info(f"Adjusted strategy for retry {retry_count}")
        
        return strategy
    
    def should_proceed_to_ifc(self, plan_data: Dict[str, Any], project_type: str = "architecture") -> Tuple[bool, str]:
        """
        Decision gate: Should we proceed to IFC generation?
        
        Args:
            plan_data: Detected plan data
            project_type: Project type (architecture only)
            
        Returns:
            (should_proceed, reason)
        """
        if not plan_data:
            return False, "No plan data available"
        
        confidence = plan_data.get("confidence", 0.0)
        
        # Architecture validation
        rooms = plan_data.get("rooms", [])
        walls = plan_data.get("walls", [])
        
        if len(rooms) == 0:
            return False, "No rooms detected"
        
        if len(walls) < 4:
            return False, "Insufficient walls detected (< 4)"
        
        if confidence < 20.0:
            return False, f"Confidence too low ({confidence:.1f}%)"
        
        return True, "Quality checks passed"
    
    def run_quality_gates(
        self,
        sketch_path: str,
        plan_data: Optional[Dict[str, Any]] = None,
        ifc_path: Optional[str] = None
    ) -> Dict[str, QualityGateResult]:
        """
        Run all quality gates in sequence
        
        Args:
            sketch_path: Path to sketch
            plan_data: Optional plan data
            ifc_path: Optional IFC file path
            
        Returns:
            Dictionary of gate results
        """
        results = {}
        
        # Gate 1: Pre-processing
        results["preprocessing"] = self.quality_assessor.run_preprocessing_gate(sketch_path)
        
        # Gate 2: Detection (if plan data provided)
        if plan_data:
            results["detection"] = self.quality_assessor.run_detection_gate(plan_data)
        
        # Gate 3: Post-IFC (if IFC path provided)
        if ifc_path:
            try:
                from .ifc_qc import validate_ifc
                qc_report = validate_ifc(ifc_path)
                results["post_ifc"] = self.quality_assessor.assess_ifc_quality(qc_report)
            except Exception as e:
                logger.error(f"Error running post-IFC gate: {e}")
        
        return results


# Convenience function
def process_sketch(
    sketch_path: str,
    legend_data: Optional[Dict[str, Any]] = None,
    max_retries: int = 2,
    project_type: str = "architecture"
) -> ProcessingResult:
    """Process sketch with intelligent agent"""
    agent = ProcessingAgent()
    return agent.process_sketch(sketch_path, legend_data, max_retries, project_type)

