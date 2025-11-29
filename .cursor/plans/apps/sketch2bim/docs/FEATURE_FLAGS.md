# Feature Flags and Experimental Features

This document describes feature flags and experimental features in Sketch2BIM.

## Feature Flags

### Symbol Detection
- **Status**: Optional, disabled by default
- **Configuration**: `SYMBOL_DETECTOR_ENABLED` in `backend/app/config.py`
- **Requirements**:
  - Trained PyTorch Faster R-CNN model file (.pth)
  - PyTorch and torchvision installed
  - Model file path set in `SYMBOL_DETECTOR_MODEL_PATH`
- **How to Enable**:
  1. Train a model using scripts in `/train` directory
  2. Set `SYMBOL_DETECTOR_ENABLED=True` in environment variables
  3. Set `SYMBOL_DETECTOR_MODEL_PATH` to your model file path
- **Fallback**: Without symbol detection, only geometric detection (walls, rooms, openings) is available

## Experimental Features

### Legend Parsing
- **Status**: Available but effectiveness varies
- **Location**: `backend/app/ai/legend_parser.py`
- **Requirements**: pytesseract (Tesseract OCR) for full functionality
- **Limitations**:
  - May return empty results if text is unclear
  - Requires pytesseract for OCR
  - Works best with standard legend formats and locations
  - Gracefully degrades if OCR unavailable (uses edge density only)
- **Best Results With**:
  - Clear, readable text in legends
  - Standard legend locations (bottom-right, bottom-left, top-right)
  - Standard scale formats (1:100, 1/4" = 1'-0", etc.)

## Production-Ready Features

### Architecture (Floor Plans)
- **Status**: Production-ready
- **Technology**: OpenCV computer vision (edge detection, contour analysis, Hough line transforms)
- **Reliability**: High for clear, well-drawn sketches

### IFC Generation
- **Status**: Production-ready
- **Technology**: Pure Python IfcOpenShell
- **Reliability**: High

### DWG Export
- **Status**: Production-ready
- **Technology**: ezdxf library
- **Reliability**: High

### SketchUp Export (OBJ)
- **Status**: Production-ready
- **Technology**: IfcOpenShell geometry extraction + OBJ format
- **Reliability**: High

### RVT/Revit Support
- **Status**: Production-ready (via IFC import)
- **Technology**: IFC files (Revit imports IFC natively)
- **Note**: We provide IFC files that Revit can import directly. No native RVT file generation.

### Layout Variations
- **Status**: Implemented
- **Location**: `backend/app/routes/variations.py`, `backend/app/ai/layout_generator.py`
- **Technology**: Geometric room rearrangement algorithms
- **Reliability**: Moderate - works for simple layouts

### Iterations
- **Status**: Implemented
- **Location**: `backend/app/routes/iterations.py`
- **Technology**: IFC file versioning and editing
- **Reliability**: High

## Configuration

All feature flags can be configured via environment variables. See `backend/app/config.py` for available settings.

