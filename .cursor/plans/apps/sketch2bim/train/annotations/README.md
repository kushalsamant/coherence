# Symbol Annotation Workspace

Use this folder to store the canonical annotations that drive the symbol detector.

## Class Taxonomy

Reference `classes.yaml` for the authoritative list. High-level groupings:

- **Architectural Core:** `door_single`, `door_double`, `window_fixed`, `window_sliding`, `stair`, `ramp`, `elevator`, `column`
- **Interior Fixtures:** `bed`, `sofa`, `table`, `chair`, `kitchen_sink`, `cooktop`, `toilet`, `shower`, `bathtub`
- **MEP & Equipment:** `light_fixture`, `switch`, `outlet`, `thermostat`, `smoke_detector`, `hvac_register`, `sprinkler`
- **Structural / Misc:** `beam`, `grid_marker`, `section_cut`, `dimension_marker`, `north_arrow`

## Annotation Pipeline

1. **Labeling Tool** – Use CVAT or Label Studio. Export both COCO + YOLO formats.
2. **Storage** – Drop raw project exports inside `labelstudio_projects/<project_name>/`.
3. **COCO Exports** – Place JSON + images under `coco/<dataset_name>/`.
4. **YOLO Exports** – Place `.txt` labels + images under `yolo/<dataset_name>/`.
5. **Validation** – Run `python train/tools/verify_annotations.py --dataset <dataset_name>` (to be added in later tasks) to ensure class names + bounding boxes are valid.

## Tips

- Keep sketch resolutions consistent (prefer 2048x2048) to simplify augmentation.
- Annotate legends separately when possible—legend detection may reuse the same pipeline.
- Document any class changes in `classes.yaml` before labeling to avoid drift.


