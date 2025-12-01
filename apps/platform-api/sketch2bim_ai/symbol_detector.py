"""
Utility wrapper for loading and running the trained symbol detector.
Gracefully degrades when the model or dependencies are not available.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List, Optional
import time

from loguru import logger

try:
    import torch
    from torchvision.models.detection import fasterrcnn_resnet50_fpn
    from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
    import torchvision.transforms as T
    TORCH_AVAILABLE = True
except Exception as e:  # pragma: no cover - optional dependency
    logger.warning(f"Torch/Torchvision not available for symbol detection: {e}")
    TORCH_AVAILABLE = False

import yaml


def _build_model(num_classes: int):
    model = fasterrcnn_resnet50_fpn(weights=None)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model


class SymbolDetector:
    """
    Lazy loader for torch-based symbol detector weights.
    """

    def __init__(
        self,
        model_path: str,
        class_map_path: str,
        confidence_threshold: float = 0.4,
        device_preference: str = "auto",
        max_results: int = 200,
    ):
        self.model_path = Path(model_path) if model_path else None
        self.class_map_path = Path(class_map_path) if class_map_path else None
        self.confidence_threshold = confidence_threshold
        self.device_preference = device_preference
        self.max_results = max_results

        self.available = False
        self.model = None
        self.device = None
        self.transforms = T.Compose([T.ToTensor()]) if TORCH_AVAILABLE else None
        self.class_index_to_meta: Dict[int, Dict[str, Any]] = {}

        self._load()

    def _load(self):
        if not TORCH_AVAILABLE:
            logger.warning("Symbol detector disabled: torch not installed.")
            return

        if not self.model_path or not self.model_path.exists():
            logger.info("Symbol detector model path not configured or missing.")
            return

        if not self.class_map_path or not self.class_map_path.exists():
            logger.info("Symbol detector class map not found.")
            return

        try:
            with open(self.class_map_path, "r", encoding="utf-8") as fp:
                class_config = yaml.safe_load(fp)
        except Exception as e:
            logger.error(f"Failed to load class map: {e}")
            return

        flattened = []
        groups = class_config.get("groups", {})
        for group_name, entries in groups.items():
            for entry in entries:
                flattened.append(
                    {
                        "id": entry["id"],
                        "name": entry.get("name", entry["id"]),
                        "ifc_type": entry.get("ifc_type"),
                        "category": group_name,
                    }
                )

        if not flattened:
            logger.warning("No classes defined in class map.")
            return

        self.class_index_to_meta = {idx + 1: meta for idx, meta in enumerate(flattened)}

        num_classes = len(flattened) + 1  # add background

        device = torch.device("cpu")
        if self.device_preference == "cuda" and torch.cuda.is_available():
            device = torch.device("cuda")
        elif self.device_preference == "auto" and torch.cuda.is_available():
            device = torch.device("cuda")

        model = _build_model(num_classes)
        try:
            checkpoint = torch.load(self.model_path, map_location=device)
            state_dict = checkpoint.get("model_state") or checkpoint
            model.load_state_dict(state_dict)
            model.eval()
            model.to(device)
        except Exception as e:
            logger.error(f"Failed to load symbol detector weights: {e}")
            return

        self.device = device
        self.model = model
        self.available = True
        logger.info(f"Symbol detector loaded ({len(flattened)} classes) from {self.model_path}")

    def detect(self, image_path: str) -> Dict[str, Any]:
        if not self.available or not self.model:
            return {"symbols": [], "enabled": False, "reason": "model_unavailable"}

        from PIL import Image

        start_time = time.time()
        try:
            image = Image.open(image_path).convert("RGB")
        except Exception as e:
            logger.error(f"Failed to open image for symbol detection: {e}")
            return {"symbols": [], "enabled": False, "reason": "invalid_image"}

        tensor = self.transforms(image).to(self.device)

        with torch.no_grad():
            outputs = self.model([tensor])[0]

        boxes = outputs["boxes"].cpu().numpy()
        scores = outputs["scores"].cpu().numpy()
        labels = outputs["labels"].cpu().numpy()

        symbols: List[Dict[str, Any]] = []
        for bbox, score, label_idx in zip(boxes, scores, labels):
            if score < self.confidence_threshold:
                continue
            meta = self.class_index_to_meta.get(int(label_idx))
            if not meta:
                continue
            x1, y1, x2, y2 = bbox.tolist()
            symbols.append(
                {
                    "label": meta["id"],
                    "display_name": meta["name"],
                    "category": meta["category"],
                    "ifc_type": meta.get("ifc_type"),
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "confidence": float(score),
                    "area_pixels": float((x2 - x1) * (y2 - y1)),
                    "source": "ml_detector",
                }
            )
            if len(symbols) >= self.max_results:
                break

        inference_ms = (time.time() - start_time) * 1000.0
        return {
            "symbols": symbols,
            "enabled": True,
            "inference_ms": inference_ms,
            "model_path": str(self.model_path),
            "confidence_threshold": self.confidence_threshold,
            "total_candidates": len(scores),
        }

