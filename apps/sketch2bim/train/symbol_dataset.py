"""
Dataset + transforms for symbol detection training
Supports COCO-format annotations with torchvision detection models.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

import torch
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as T


class SymbolDetectionDataset(Dataset):
    """
    Torch dataset that reads COCO-format annotations.

    Args:
        annotations_path: Path to COCO annotations JSON.
        images_dir: Optional explicit path to images folder. If None, uses the folder declared inside COCO file.
        transforms: Optional torchvision transform pipeline.
        min_area: Filter out annotations below this area (in px^2) to avoid noise.
    """

    def __init__(
        self,
        annotations_path: str,
        images_dir: Optional[str] = None,
        transforms: Optional[Any] = None,
        min_area: float = 16.0,
    ):
        self.annotations_path = Path(annotations_path)
        if not self.annotations_path.exists():
            raise FileNotFoundError(f"COCO annotations not found: {self.annotations_path}")

        with open(self.annotations_path, "r", encoding="utf-8") as fp:
            coco = json.load(fp)

        self.categories = coco.get("categories", [])
        if not self.categories:
            raise ValueError("COCO annotations must include 'categories'")

        self.category_id_to_index = {cat["id"]: idx + 1 for idx, cat in enumerate(self.categories)}  # +1 for background=0
        self.category_index_to_name = {idx + 1: cat["name"] for idx, cat in enumerate(self.categories)}

        self.images = {img["id"]: img for img in coco.get("images", [])}
        if not self.images:
            raise ValueError("COCO annotations must include 'images'")

        # Resolve image directory
        if images_dir:
            self.images_dir = Path(images_dir)
        else:
            # Use relative path from annotation file
            self.images_dir = self.annotations_path.parent / "images"

        if not self.images_dir.exists():
            raise FileNotFoundError(f"Images directory not found: {self.images_dir}")

        # Map image -> annotations
        self.image_to_annotations: Dict[int, List[Dict[str, Any]]] = {img_id: [] for img_id in self.images.keys()}
        for ann in coco.get("annotations", []):
            image_id = ann["image_id"]
            if ann.get("area", 0) < min_area:
                continue
            if ann.get("category_id") not in self.category_id_to_index:
                continue
            if image_id not in self.image_to_annotations:
                continue
            self.image_to_annotations[image_id].append(ann)

        # Keep deterministically sorted IDs for reproducibility
        self.image_ids: List[int] = sorted(self.image_to_annotations.keys())
        self.transforms = transforms if transforms is not None else default_transforms(train=True)

    def __len__(self) -> int:
        return len(self.image_ids)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        image_id = self.image_ids[idx]
        image_info = self.images[image_id]
        img_path = self.images_dir / image_info["file_name"]
        if not img_path.exists():
            raise FileNotFoundError(f"Image referenced in COCO file not found: {img_path}")

        img = Image.open(img_path).convert("RGB")
        width, height = img.size
        annotations = self.image_to_annotations[image_id]

        boxes = []
        labels = []
        areas = []
        iscrowd = []

        for ann in annotations:
            x, y, w, h = ann["bbox"]
            boxes.append([x, y, x + w, y + h])
            areas.append(ann.get("area", w * h))
            labels.append(self.category_id_to_index[ann["category_id"]])
            iscrowd.append(ann.get("iscrowd", 0))

        boxes_tensor = torch.as_tensor(boxes, dtype=torch.float32) if boxes else torch.zeros((0, 4), dtype=torch.float32)
        labels_tensor = torch.as_tensor(labels, dtype=torch.int64) if labels else torch.zeros((0,), dtype=torch.int64)

        target = {
            "boxes": boxes_tensor,
            "labels": labels_tensor,
            "image_id": torch.tensor([image_id]),
            "area": torch.as_tensor(areas, dtype=torch.float32) if areas else torch.zeros((0,), dtype=torch.float32),
            "iscrowd": torch.as_tensor(iscrowd, dtype=torch.int64) if iscrowd else torch.zeros((0,), dtype=torch.int64),
            "orig_size": torch.tensor([height, width]),
        }

        if self.transforms:
            img = self.transforms(img)

        return img, target

    def get_num_classes(self) -> int:
        """Return number of classes including background index zero."""
        return len(self.categories) + 1

    def get_class_names(self) -> List[str]:
        return [cat["name"] for cat in self.categories]


def default_transforms(train: bool = True):
    """Simple augmentation pipeline; extend later as needed."""
    t_list = [T.ToTensor()]
    if train:
        t_list.extend(
            [
                T.RandomHorizontalFlip(0.5),
                T.RandomVerticalFlip(0.2),
            ]
        )
    return T.Compose(t_list)


def collate_fn(batch):
    """DataLoader helper for variable-sized targets."""
    return tuple(zip(*batch))

