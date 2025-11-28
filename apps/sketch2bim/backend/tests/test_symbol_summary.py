from app.routes.generate import _build_symbol_summary


def test_symbol_summary_counts():
    plan_data = {
        "symbols": [
            {"label": "door_single", "category": "architectural_core", "bbox": [0, 0, 10, 10], "confidence": 0.9},
            {"label": "sofa", "category": "interior_furniture", "bbox": [5, 5, 15, 15], "confidence": 0.8},
            {"label": "sofa", "category": "interior_furniture", "bbox": [20, 10, 30, 25], "confidence": 0.75},
        ],
        "symbol_metadata": {"enabled": True, "inference_ms": 42.5, "model_path": "/models/symbols/latest.pth"},
    }

    summary = _build_symbol_summary(plan_data)

    assert summary is not None
    assert summary.total_detected == 3
    assert summary.categories["interior_furniture"] == 2
    assert summary.categories["architectural_core"] == 1
    assert summary.sample_labels[0] == "sofa"
    assert summary.inference_ms == 42.5
    assert summary.model_path.endswith("latest.pth")


def test_symbol_summary_handles_missing_data():
    assert _build_symbol_summary(None) is None
    assert _build_symbol_summary({"symbols": []}) is None

    plan_data = {"symbols": [], "symbol_metadata": {"enabled": True}}
    summary = _build_symbol_summary(plan_data)
    assert summary is not None
    assert summary.total_detected == 0
    assert summary.enabled is True

