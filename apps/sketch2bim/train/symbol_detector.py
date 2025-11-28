"""
Training script for multi-category symbol detection.

Usage:
    python symbol_detector.py --config configs/symbol_detector.yaml
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Dict, Any

import torch
from torch.utils.data import DataLoader, random_split
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torch.optim import AdamW
from torch.optim.lr_scheduler import StepLR
from tqdm import tqdm
import yaml

from symbol_dataset import SymbolDetectionDataset, collate_fn


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fp:
        return yaml.safe_load(fp)


def build_model(num_classes: int) -> torch.nn.Module:
    model = fasterrcnn_resnet50_fpn(weights="DEFAULT")
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model


def split_dataset(dataset: SymbolDetectionDataset, val_ratio: float = 0.1):
    val_size = max(1, int(len(dataset) * val_ratio))
    train_size = len(dataset) - val_size
    return random_split(dataset, [train_size, val_size])


def save_checkpoint(model, optimizer, epoch, ckpt_dir: Path, run_name: str):
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ckpt_path = ckpt_dir / f"{run_name}_epoch{epoch:03d}.pth"
    torch.save(
        {
            "epoch": epoch,
            "model_state": model.state_dict(),
            "optimizer_state": optimizer.state_dict(),
        },
        ckpt_path,
    )
    return ckpt_path


def train(config: Dict[str, Any], cli_args: argparse.Namespace):
    device = torch.device("cuda" if torch.cuda.is_available() and not cli_args.cpu else "cpu")
    dataset_cfg = config["dataset"]
    training_cfg = config["training"]

    dataset = SymbolDetectionDataset(
        annotations_path=dataset_cfg["coco_annotations"],
        images_dir=dataset_cfg.get("images_dir"),
    )

    train_ds, val_ds = split_dataset(dataset)

    train_loader = DataLoader(
        train_ds,
        batch_size=training_cfg["batch_size"],
        shuffle=True,
        num_workers=training_cfg.get("num_workers", 4),
        collate_fn=collate_fn,
    )
    val_loader = DataLoader(
        val_ds,
        batch_size=training_cfg["batch_size"],
        shuffle=False,
        num_workers=training_cfg.get("num_workers", 4),
        collate_fn=collate_fn,
    )

    model = build_model(dataset.get_num_classes())
    model.to(device)

    optimizer = AdamW(model.parameters(), lr=training_cfg["learning_rate"], weight_decay=training_cfg["weight_decay"])
    scheduler = StepLR(optimizer, step_size=training_cfg["lr_step_size"], gamma=training_cfg["lr_gamma"])

    start_epoch = 1
    if training_cfg.get("resume_from"):
        checkpoint = torch.load(training_cfg["resume_from"], map_location=device)
        model.load_state_dict(checkpoint["model_state"])
        optimizer.load_state_dict(checkpoint["optimizer_state"])
        start_epoch = checkpoint["epoch"] + 1

    run_name = training_cfg.get("run_name") or config.get("run_name") or f"symbol-detector-{dt.datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
    checkpoint_dir = Path(training_cfg["checkpoint_dir"]).resolve()

    for epoch in range(start_epoch, training_cfg["epochs"] + 1):
        model.train()
        train_loss = 0.0
        for images, targets in tqdm(train_loader, desc=f"Epoch {epoch} [train]"):
            images = [img.to(device) for img in images]
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())

            optimizer.zero_grad()
            losses.backward()
            if training_cfg.get("gradient_clip_norm"):
                torch.nn.utils.clip_grad_norm_(model.parameters(), training_cfg["gradient_clip_norm"])
            optimizer.step()

            train_loss += losses.item()

        scheduler.step()

        avg_train_loss = train_loss / max(1, len(train_loader))
        val_metrics = evaluate(model, val_loader, device)

        print(
            f"Epoch {epoch}/{training_cfg['epochs']} "
            f"- train loss: {avg_train_loss:.4f} "
            f"- val loss: {val_metrics['loss']:.4f} "
            f"- val mAP (IoU=0.5): {val_metrics['map50']:.4f}"
        )

        if epoch % training_cfg.get("checkpoint_every", 5) == 0 or epoch == training_cfg["epochs"]:
            ckpt_path = save_checkpoint(model, optimizer, epoch, checkpoint_dir, run_name)
            print(f"Saved checkpoint to {ckpt_path}")


@torch.no_grad()
def evaluate(model, dataloader, device):
    model.eval()
    total_loss = 0.0
    total_batches = 0

    # Placeholder mAP - integrate proper metrics once detections exist.
    # For now compute classification accuracy-like proxy.
    total_predictions = 0
    correct_predictions = 0

    for images, targets in dataloader:
        images = [img.to(device) for img in images]
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        loss_dict = model(images, targets)
        losses = sum(loss for loss in loss_dict.values())
        total_loss += losses.item()
        total_batches += 1

        outputs = model(images)
        for output, target in zip(outputs, targets):
            pred_labels = output["labels"]
            gt_labels = target["labels"]
            matched = min(len(pred_labels), len(gt_labels))
            correct_predictions += (pred_labels[:matched] == gt_labels[:matched]).sum().item()
            total_predictions += max(len(pred_labels), len(gt_labels))

    avg_loss = total_loss / max(1, total_batches)
    map50 = correct_predictions / max(1, total_predictions)
    return {"loss": avg_loss, "map50": map50}


def parse_args():
    parser = argparse.ArgumentParser(description="Symbol detector training script")
    parser.add_argument("--config", type=str, default="configs/symbol_detector.yaml", help="Path to YAML config")
    parser.add_argument("--cpu", action="store_true", help="Force CPU training")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cfg = load_config(args.config)
    train(cfg, args)

