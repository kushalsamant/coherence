# Symbol Recognition Pipeline

This document tracks the end-to-end workflow for detecting and validating architectural symbols inside uploaded sketches.

## 1. Dataset Ingestion

- Drop raw symbol libraries into `data/symbols/<category>/`.
- Update `data/symbols/catalog.json` for every new source (license, coverage, conversion status).
- Keep SVG/PNG versions alongside the originals. Use `shared_assets/` for standards, legends, and reference PDFs.

## 2. Annotation Workflow

1. Define class taxonomy in `train/annotations/classes.yaml`.
2. Label sketches via Label Studio/CVAT using the template in `train/annotations/labelstudio_template.xml`.
3. Export both COCO + YOLO formats into `train/annotations/coco/` and `train/annotations/yolo/`.
4. Track annotation notes in `train/annotations/README.md`.

## 3. Training

```
cd train
python symbol_detector.py --config configs/symbol_detector.yaml
```

Key files:

- `train/symbol_dataset.py` — COCO dataset wrapper & augmentations.
- `train/configs/symbol_detector.yaml` — dataset paths & hyperparameters.
- Checkpoints land in `models/symbols/`.

## 4. Backend Integration

- New `SymbolDetector` wrapper in `backend/app/ai/symbol_detector.py`.
- `OpenCVReader` calls the detector when `SYMBOL_DETECTOR_ENABLED` is true and attaches results to `plan_data.symbols`.
- IFC generator (`backend/app/ai/ifc_generator.py`) converts each detection into an IFC element + property set.
- API responses now include `symbol_summary` plus a dedicated `GET /api/v1/generate/jobs/{job_id}/plan-data` endpoint for QA tooling.

## 5. Frontend QA Tools

- `SymbolDetectionPanel` component renders summary chips, modal QA table, category filters, and CSV export.
- Integrated into dashboard job cards and the viewer header (link-style button for quick access).

## 6. Testing

- Unit tests in `backend/tests/test_symbol_summary.py` cover summary aggregation edge cases.
- When adding new categories, extend the test fixtures accordingly.

## 7. Deployment Checklist

- [ ] Upload/verify latest `models/symbols/*.pth` artifacts.
- [ ] Set environment variables:
  - `SYMBOL_DETECTOR_ENABLED`
  - `SYMBOL_DETECTOR_MODEL_PATH`
  - `SYMBOL_DETECTOR_CLASS_FILE`
  - `SYMBOL_DETECTOR_CONFIDENCE`
- [ ] Warm up Torch cache on the server (first inference may be slower).
- [ ] Smoke test `GET /api/v1/generate/jobs/{job}/plan-data`.
- [ ] QA symbol overlay via dashboard modal and viewer page.

> Tip: When retraining, keep legacy checkpoints with semantic version numbers (`symbol-detector-v1.0.pth`) so you can roll back quickly.

