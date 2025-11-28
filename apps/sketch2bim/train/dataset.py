"""
Dataset for training Sketch-to-BIM detection models
"""
import torch
from torch.utils.data import Dataset
from PIL import Image
import os
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np


class SketchBIMDataset(Dataset):
    """
    Dataset for training wall/room/door/window detection
    
    Expected structure:
    dataset/
      images/
        sketch1.png
        sketch2.png
      labels/
        sketch1.json
        sketch2.json
    
    Each JSON contains:
    {
        "walls": [{"x1":0,"y1":0,"x2":2,"y2":2}, ...],
        "rooms": [{"x":0,"y":0,"width":10,"height":10}, ...],
        "doors": [{"x1":0,"y1":0,"x2":1,"y2":1}, ...],
        "windows": [{"x1":0,"y1":0,"x2":1,"y2":1}, ...]
    }
    """
    
    def __init__(
        self,
        root_dir: str,
        transform=None,
        max_walls: int = 10,
        max_rooms: int = 5,
        max_doors: int = 10,
        max_windows: int = 10
    ):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.max_walls = max_walls
        self.max_rooms = max_rooms
        self.max_doors = max_doors
        self.max_windows = max_windows
        
        # Get all image files
        images_dir = self.root_dir / "images"
        labels_dir = self.root_dir / "labels"
        
        if not images_dir.exists():
            raise ValueError(f"Images directory not found: {images_dir}")
        if not labels_dir.exists():
            raise ValueError(f"Labels directory not found: {labels_dir}")
        
        self.image_files = sorted([
            f for f in os.listdir(images_dir)
            if f.lower().endswith(('.png', '.jpg', '.jpeg'))
        ])
        
        # Verify labels exist
        self.valid_files = []
        for img_file in self.image_files:
            label_file = labels_dir / img_file.replace('.png', '.json').replace('.jpg', '.json').replace('.jpeg', '.json')
            if label_file.exists():
                self.valid_files.append(img_file)
    
    def __len__(self) -> int:
        return len(self.valid_files)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        """
        Get item: (image_tensor, labels_dict)
        
        Returns:
            image: Tensor of shape [1, H, W] (grayscale)
            labels: Dict with keys: walls, rooms, doors, windows
                   Each is a tensor of shape [max_count, 4] (x1,y1,x2,y2 or x,y,w,h)
        """
        img_name = self.valid_files[idx]
        img_path = self.root_dir / "images" / img_name
        label_path = self.root_dir / "labels" / img_name.replace('.png', '.json').replace('.jpg', '.json').replace('.jpeg', '.json')
        
        # Load image
        image = Image.open(img_path).convert("L")  # Grayscale
        
        if self.transform:
            image = self.transform(image)
        else:
            # Default transform: resize and to tensor
            from torchvision import transforms
            transform = transforms.Compose([
                transforms.Resize((128, 128)),
                transforms.ToTensor()
            ])
            image = transform(image)
        
        # Load labels
        with open(label_path) as f:
            labels = json.load(f)
        
        # Convert to tensors
        walls = self._parse_walls(labels.get("walls", []))
        rooms = self._parse_rooms(labels.get("rooms", []))
        doors = self._parse_openings(labels.get("doors", []), self.max_doors)
        windows = self._parse_openings(labels.get("windows", []), self.max_windows)
        
        return image, {
            "walls": walls,
            "rooms": rooms,
            "doors": doors,
            "windows": windows
        }
    
    def _parse_walls(self, walls: List[Dict]) -> torch.Tensor:
        """Parse walls to tensor [max_walls, 4] (x1, y1, x2, y2)"""
        tensor = torch.zeros(self.max_walls, 4)
        for i, wall in enumerate(walls[:self.max_walls]):
            tensor[i] = torch.tensor([
                wall.get("x1", 0.0),
                wall.get("y1", 0.0),
                wall.get("x2", 0.0),
                wall.get("y2", 0.0)
            ], dtype=torch.float)
        return tensor
    
    def _parse_rooms(self, rooms: List[Dict]) -> torch.Tensor:
        """Parse rooms to tensor [max_rooms, 4] (x, y, width, height)"""
        tensor = torch.zeros(self.max_rooms, 4)
        for i, room in enumerate(rooms[:self.max_rooms]):
            tensor[i] = torch.tensor([
                room.get("x", 0.0),
                room.get("y", 0.0),
                room.get("width", 0.0),
                room.get("height", 0.0)
            ], dtype=torch.float)
        return tensor
    
    def _parse_openings(self, openings: List[Dict], max_count: int) -> torch.Tensor:
        """Parse doors/windows to tensor [max_count, 4] (x1, y1, x2, y2)"""
        tensor = torch.zeros(max_count, 4)
        for i, opening in enumerate(openings[:max_count]):
            tensor[i] = torch.tensor([
                opening.get("x1", 0.0),
                opening.get("y1", 0.0),
                opening.get("x2", 0.0),
                opening.get("y2", 0.0)
            ], dtype=torch.float)
        return tensor

