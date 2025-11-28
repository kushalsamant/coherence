'use client';

import * as THREE from 'three';

export interface Measurement {
  id: string;
  start: THREE.Vector3;
  end: THREE.Vector3;
  distance: number;
}

export class MeasurementManager {
  private scene: THREE.Scene;
  private measurements: Measurement[] = [];
  private measurementGroup: THREE.Group;
  private raycaster: THREE.Raycaster;
  private mouse: THREE.Vector2;
  private isMeasuring: boolean = false;
  private currentStartPoint: THREE.Vector3 | null = null;
  private tempLine: THREE.Line | null = null;
  private onMeasurementComplete?: (measurement: Measurement) => void;

  constructor(scene: THREE.Scene, onMeasurementComplete?: (measurement: Measurement) => void) {
    this.scene = scene;
    this.onMeasurementComplete = onMeasurementComplete;
    this.measurementGroup = new THREE.Group();
    this.measurementGroup.name = 'measurements';
    this.scene.add(this.measurementGroup);
    this.raycaster = new THREE.Raycaster();
    this.mouse = new THREE.Vector2();
  }

  startMeasurement() {
    this.isMeasuring = true;
    this.currentStartPoint = null;
  }

  stopMeasurement() {
    this.isMeasuring = false;
    if (this.tempLine) {
      this.scene.remove(this.tempLine);
      this.tempLine = null;
    }
    this.currentStartPoint = null;
  }

  handleClick(
    event: MouseEvent,
    camera: THREE.Camera,
    meshes: THREE.Mesh[],
    container: HTMLElement
  ): boolean {
    if (!this.isMeasuring) return false;

    const rect = container.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    this.raycaster.setFromCamera(this.mouse, camera);
    const intersects = this.raycaster.intersectObjects(meshes, true);

    if (intersects.length > 0) {
      const point = intersects[0].point;

      if (!this.currentStartPoint) {
        // First point
        this.currentStartPoint = point.clone();
        this.createTempLine(this.currentStartPoint, point);
      } else {
        // Second point - complete measurement
        const distance = this.currentStartPoint.distanceTo(point);
        const measurement: Measurement = {
          id: `measurement-${Date.now()}`,
          start: this.currentStartPoint.clone(),
          end: point.clone(),
          distance,
        };

        this.addMeasurement(measurement);
        this.currentStartPoint = null;
        if (this.tempLine) {
          this.scene.remove(this.tempLine);
          this.tempLine = null;
        }
        return true;
      }
    }

    return false;
  }

  handleMouseMove(
    event: MouseEvent,
    camera: THREE.Camera,
    meshes: THREE.Mesh[],
    container: HTMLElement
  ) {
    if (!this.isMeasuring || !this.currentStartPoint) return;

    const rect = container.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    this.raycaster.setFromCamera(this.mouse, camera);
    const intersects = this.raycaster.intersectObjects(meshes, true);

    if (intersects.length > 0) {
      const point = intersects[0].point;
      this.updateTempLine(this.currentStartPoint, point);
    }
  }

  private createTempLine(start: THREE.Vector3, end: THREE.Vector3) {
    const geometry = new THREE.BufferGeometry().setFromPoints([start, end]);
    const material = new THREE.LineDashedMaterial({
      color: 0x00ff00,
      dashSize: 0.1,
      gapSize: 0.05,
      linewidth: 2,
    });
    this.tempLine = new THREE.Line(geometry, material);
    this.tempLine.computeLineDistances();
    this.scene.add(this.tempLine);
  }

  private updateTempLine(start: THREE.Vector3, end: THREE.Vector3) {
    if (this.tempLine) {
      this.scene.remove(this.tempLine);
    }
    this.createTempLine(start, end);
  }

  private addMeasurement(measurement: Measurement) {
    this.measurements.push(measurement);

    // Create line
    const geometry = new THREE.BufferGeometry().setFromPoints([
      measurement.start,
      measurement.end,
    ]);
    const material = new THREE.LineBasicMaterial({ color: 0xff0000, linewidth: 2 });
    const line = new THREE.Line(geometry, material);
    line.userData.measurementId = measurement.id;

    // Create start point marker
    const startMarker = this.createPointMarker(measurement.start, 'start');
    startMarker.userData.measurementId = measurement.id;

    // Create end point marker
    const endMarker = this.createPointMarker(measurement.end, 'end');
    endMarker.userData.measurementId = measurement.id;

    // Create label
    const label = this.createLabel(measurement);
    label.userData.measurementId = measurement.id;

    this.measurementGroup.add(line);
    this.measurementGroup.add(startMarker);
    this.measurementGroup.add(endMarker);
    this.measurementGroup.add(label);

    if (this.onMeasurementComplete) {
      this.onMeasurementComplete(measurement);
    }
  }

  private createPointMarker(position: THREE.Vector3, type: 'start' | 'end'): THREE.Mesh {
    const geometry = new THREE.SphereGeometry(0.1, 16, 16);
    const material = new THREE.MeshBasicMaterial({
      color: type === 'start' ? 0x00ff00 : 0xff0000,
    });
    const marker = new THREE.Mesh(geometry, material);
    marker.position.copy(position);
    return marker;
  }

  private createLabel(measurement: Measurement): THREE.Group {
    const group = new THREE.Group();
    const midPoint = new THREE.Vector3()
      .addVectors(measurement.start, measurement.end)
      .multiplyScalar(0.5);

    // Create canvas for text
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d')!;
    canvas.width = 256;
    canvas.height = 64;

    // Draw background
    context.fillStyle = 'rgba(255, 255, 255, 0.9)';
    context.fillRect(0, 0, canvas.width, canvas.height);

    // Draw border
    context.strokeStyle = '#333';
    context.lineWidth = 2;
    context.strokeRect(0, 0, canvas.width, canvas.height);

    // Draw text
    context.fillStyle = '#000';
    context.font = 'bold 24px Arial';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    const distanceText = `${measurement.distance.toFixed(2)} m`;
    context.fillText(distanceText, canvas.width / 2, canvas.height / 2);

    // Create texture and sprite
    const texture = new THREE.CanvasTexture(canvas);
    const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(spriteMaterial);
    sprite.scale.set(2, 0.5, 1);
    sprite.position.copy(midPoint);
    sprite.position.y += 0.5; // Offset above line

    group.add(sprite);
    group.position.copy(midPoint);

    return group;
  }

  removeMeasurement(id: string) {
    this.measurements = this.measurements.filter((m) => m.id !== id);
    const toRemove: THREE.Object3D[] = [];
    this.measurementGroup.traverse((child) => {
      if (child.userData.measurementId === id) {
        toRemove.push(child);
      }
    });
    toRemove.forEach((obj) => {
      this.measurementGroup.remove(obj);
      if (obj instanceof THREE.Mesh || obj instanceof THREE.Line) {
        obj.geometry.dispose();
        if (obj.material instanceof THREE.Material) {
          obj.material.dispose();
        }
      }
    });
  }

  clearAll() {
    this.measurements = [];
    this.measurementGroup.clear();
    if (this.tempLine) {
      this.scene.remove(this.tempLine);
      this.tempLine = null;
    }
  }

  getMeasurements(): Measurement[] {
    return [...this.measurements];
  }

  dispose() {
    this.clearAll();
    this.scene.remove(this.measurementGroup);
  }
}

