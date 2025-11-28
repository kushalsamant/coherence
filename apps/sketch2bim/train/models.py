"""
PyTorch models for Sketch-to-BIM detection
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


class BIMDetectorCNN(nn.Module):
    """
    Multi-head CNN for detecting walls, rooms, doors, and windows
    
    Architecture:
    - Shared CNN backbone for feature extraction
    - Separate heads for each detection task
    """
    
    def __init__(
        self,
        input_size: int = 128,
        max_walls: int = 10,
        max_rooms: int = 5,
        max_doors: int = 10,
        max_windows: int = 10
    ):
        super().__init__()
        
        self.max_walls = max_walls
        self.max_rooms = max_rooms
        self.max_doors = max_doors
        self.max_windows = max_windows
        
        # Shared CNN backbone
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        
        # Calculate flattened size after convolutions
        # Input: 128x128 -> after 3 pools: 16x16
        flattened_size = 64 * 16 * 16
        
        # Shared fully connected layers
        self.fc1 = nn.Linear(flattened_size, 256)
        self.fc2 = nn.Linear(256, 128)
        
        # Separate heads for each task
        self.fc_walls = nn.Linear(128, 4 * max_walls)
        self.fc_rooms = nn.Linear(128, 4 * max_rooms)
        self.fc_doors = nn.Linear(128, 4 * max_doors)
        self.fc_windows = nn.Linear(128, 4 * max_windows)
        
        # Dropout for regularization
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Forward pass
        
        Args:
            x: Input image tensor [B, 1, H, W]
            
        Returns:
            Dict with keys: walls, rooms, doors, windows
            Each tensor shape: [B, max_count, 4]
        """
        # Shared backbone
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        
        # Flatten
        x = x.view(x.size(0), -1)
        
        # Shared FC layers
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        
        # Separate heads
        walls = self.fc_walls(x).view(-1, self.max_walls, 4)
        rooms = self.fc_rooms(x).view(-1, self.max_rooms, 4)
        doors = self.fc_doors(x).view(-1, self.max_doors, 4)
        windows = self.fc_windows(x).view(-1, self.max_windows, 4)
        
        return {
            "walls": walls,
            "rooms": rooms,
            "doors": doors,
            "windows": windows
        }


class WallDetectorCNN(nn.Module):
    """
    Simplified model for wall detection only
    """
    
    def __init__(self, max_walls: int = 10):
        super().__init__()
        self.max_walls = max_walls
        
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        
        flattened_size = 32 * 32 * 32  # Assuming 128x128 input
        
        self.fc1 = nn.Linear(flattened_size, 128)
        self.fc2 = nn.Linear(128, 4 * max_walls)
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x.view(-1, self.max_walls, 4)

