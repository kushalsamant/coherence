# ML Training Scripts

This directory contains scripts for training machine learning models to improve sketch detection accuracy.

## Overview

The training scripts are designed to train PyTorch-based CNN models for detecting architectural elements (walls, rooms, doors, windows) from hand-drawn sketches. These models can potentially improve the accuracy of the sketch-to-BIM conversion pipeline.

## Current Status

**Note:** The current production system uses OpenCV-based processing (`backend/app/ai/sketch_reader.py`). These training scripts are for future ML model improvements and are not currently integrated into the production pipeline.

## Files

- **`train_full_bim.py`** - Main training script for the full BIM detection model
- **`models.py`** - PyTorch model definitions (BIMDetectorCNN, WallDetectorCNN)
- **`dataset.py`** - Dataset loader for training data
- **`symbol_dataset.py`** - COCO-friendly dataset + transforms for symbol detection
- **`symbol_detector.py`** - Training loop for the symbol detector (Faster R-CNN backbone)
- **`configs/symbol_detector.yaml`** - Default hyperparameters + dataset paths for symbol detector
- **`annotations/`** - Class taxonomy, Label Studio template, and export folders

## Prerequisites

```bash
pip install torch torchvision tqdm pillow numpy
```

## Dataset Structure

Prepare your training data in the following structure:

```
dataset/
  images/
    sketch1.png
    sketch2.png
    ...
  labels/
    sketch1.json
    sketch2.json
    ...
```

Each JSON label file should contain:

```json
{
  "walls": [{"x1": 0, "y1": 0, "x2": 2, "y2": 2}, ...],
  "rooms": [{"x": 0, "y": 0, "width": 10, "height": 10}, ...],
  "doors": [{"x1": 0, "y1": 0, "x2": 1, "y2": 1}, ...],
  "windows": [{"x1": 0, "y1": 0, "x2": 1, "y2": 1}, ...]
}
```

## Usage

### Training the BIM model

```bash
cd train
python train_full_bim.py
```

### Training the Symbol Detector

```bash
cd train
python symbol_detector.py --config configs/symbol_detector.yaml
```

The config expects COCO-format annotations + matching images. Update the paths in `configs/symbol_detector.yaml` after exporting your labeled datasets to `train/annotations/coco/<dataset_name>/`.

### Default Hyperparameters

`train_full_bim.py`:
- Batch size: 8
- Learning rate: 1e-3
- Epochs: 50
- Image size: 128x128

`symbol_detector.py` (configurable via YAML):
- Model: `fasterrcnn_resnet50_fpn`
- Epochs: 25
- Batch size: 4
- Base LR: 5e-4
- Optimizer: AdamW

## When to Retrain

Consider retraining models when:
1. You have collected a significant amount of new training data
2. Detection accuracy needs improvement
3. New architectural element types need to be detected
4. The model needs to adapt to different sketch styles

## Integration

To integrate trained models into the production pipeline:

1. Train and save the model weights
2. Update `backend/app/ai/sketch_reader.py` to load and use the trained model
3. Test thoroughly with production sketches
4. Deploy gradually (A/B testing recommended)

## Notes

- Models are saved to `../models/` directory
- Training requires GPU for reasonable training times
- Ensure sufficient training data (recommended: 1000+ labeled sketches)

