"""
Training script for full BIM detection model
Trains model to detect walls, rooms, doors, and windows
"""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms
import os
from pathlib import Path
from tqdm import tqdm
import json

from dataset import SketchBIMDataset
from models import BIMDetectorCNN


# Hyperparameters
BATCH_SIZE = 8
LEARNING_RATE = 1e-3
EPOCHS = 50
IMG_SIZE = 128
DATA_DIR = "../dataset"
MODEL_DIR = "../models"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Create model directory
Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)


def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch"""
    model.train()
    running_loss = 0.0
    
    for images, labels in tqdm(dataloader, desc="Training"):
        images = images.to(device)
        labels = {k: v.to(device) for k, v in labels.items()}
        
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(images)
        
        # Calculate loss for each head
        loss = 0.0
        for key in ["walls", "rooms", "doors", "windows"]:
            loss += criterion(outputs[key], labels[key])
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    return running_loss / len(dataloader)


def validate(model, dataloader, criterion, device):
    """Validate model"""
    model.eval()
    running_loss = 0.0
    
    with torch.no_grad():
        for images, labels in tqdm(dataloader, desc="Validating"):
            images = images.to(device)
            labels = {k: v.to(device) for k, v in labels.items()}
            
            outputs = model(images)
            
            loss = 0.0
            for key in ["walls", "rooms", "doors", "windows"]:
                loss += criterion(outputs[key], labels[key])
            
            running_loss += loss.item()
    
    return running_loss / len(dataloader)


def main():
    print(f"Using device: {DEVICE}")
    print(f"Data directory: {DATA_DIR}")
    
    # Transforms
    transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])  # Normalize to [-1, 1]
    ])
    
    # Dataset
    try:
        dataset = SketchBIMDataset(DATA_DIR, transform=transform)
        print(f"Dataset size: {len(dataset)}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        print("Creating dummy dataset for testing...")
        # Create minimal dataset structure for testing
        return
    
    # Split dataset (80/20)
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )
    
    # Data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=2
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=2
    )
    
    # Model
    model = BIMDetectorCNN(input_size=IMG_SIZE).to(DEVICE)
    
    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5
    )
    
    # Training loop
    best_val_loss = float('inf')
    
    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch+1}/{EPOCHS}")
        
        # Train
        train_loss = train_epoch(model, train_loader, criterion, optimizer, DEVICE)
        
        # Validate
        val_loss = validate(model, val_loader, criterion, DEVICE)
        
        print(f"Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}")
        
        # Learning rate scheduling
        scheduler.step(val_loss)
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            model_path = Path(MODEL_DIR) / "bim_detector_best.pth"
            torch.save(model.state_dict(), model_path)
            print(f"Saved best model (val_loss: {val_loss:.4f})")
        
        # Save checkpoint every 10 epochs
        if (epoch + 1) % 10 == 0:
            checkpoint_path = Path(MODEL_DIR) / f"bim_detector_epoch_{epoch+1}.pth"
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_loss,
            }, checkpoint_path)
    
    # Save final model
    final_model_path = Path(MODEL_DIR) / "bim_detector_final.pth"
    torch.save(model.state_dict(), final_model_path)
    print(f"\nTraining complete. Final model saved to {final_model_path}")


if __name__ == "__main__":
    main()

