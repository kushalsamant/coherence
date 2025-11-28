'use client';

import { useState } from 'react';

export interface SectionPlane {
  id: string;
  axis: 'x' | 'y' | 'z';
  position: number;
  enabled: boolean;
}

interface SectionPlaneControlsProps {
  planes: SectionPlane[];
  onPlaneChange: (plane: SectionPlane) => void;
  onPlaneRemove: (id: string) => void;
  onPlaneAdd: (axis: 'x' | 'y' | 'z') => void;
  onClose?: () => void;
}

export default function SectionPlaneControls({
  planes,
  onPlaneChange,
  onPlaneRemove,
  onPlaneAdd,
  onClose,
}: SectionPlaneControlsProps) {
  const [localPlanes, setLocalPlanes] = useState<SectionPlane[]>(planes);

  const handlePositionChange = (id: string, delta: number) => {
    const plane = localPlanes.find((p) => p.id === id);
    if (plane) {
      const updated = { ...plane, position: Math.max(-100, Math.min(100, plane.position + delta)) };
      setLocalPlanes(localPlanes.map((p) => (p.id === id ? updated : p)));
      onPlaneChange(updated);
    }
  };

  const handleToggle = (id: string) => {
    const plane = localPlanes.find((p) => p.id === id);
    if (plane) {
      const updated = { ...plane, enabled: !plane.enabled };
      setLocalPlanes(localPlanes.map((p) => (p.id === id ? updated : p)));
      onPlaneChange(updated);
    }
  };

  const axisLabels = {
    x: 'X-Axis (Left/Right)',
    y: 'Y-Axis (Up/Down)',
    z: 'Z-Axis (Front/Back)',
  };

  return (
    <div className="absolute bottom-4 left-4 bg-white/95 backdrop-blur-sm rounded-lg shadow-xl border border-gray-200 p-4 z-50 min-w-[300px]">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-gray-900">Section Planes</h3>
        {onClose && (
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded transition-colors"
            aria-label="Close panel"
          >
            <svg className="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      {/* Add Plane Buttons */}
      <div className="flex gap-2 mb-4">
        {(['x', 'y', 'z'] as const).map((axis) => {
          const hasPlane = localPlanes.some((p) => p.axis === axis);
          return (
            <button
              key={axis}
              onClick={() => !hasPlane && onPlaneAdd(axis)}
              disabled={hasPlane}
              className={`px-3 py-1.5 text-sm rounded transition-colors ${
                hasPlane
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-primary-600 text-white hover:bg-primary-700'
              }`}
            >
              Add {axis.toUpperCase()}
            </button>
          );
        })}
      </div>

      {/* Plane Controls */}
      <div className="space-y-3 max-h-64 overflow-y-auto">
        {localPlanes.length === 0 ? (
          <p className="text-sm text-gray-500 text-center py-4">
            No section planes. Add one to start clipping the model.
          </p>
        ) : (
          localPlanes.map((plane) => (
            <div
              key={plane.id}
              className="border border-gray-200 rounded-lg p-3 bg-gray-50"
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={plane.enabled}
                    onChange={() => handleToggle(plane.id)}
                    className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500"
                  />
                  <label className="text-sm font-medium text-gray-900">
                    {axisLabels[plane.axis]}
                  </label>
                </div>
                <button
                  onClick={() => onPlaneRemove(plane.id)}
                  className="p-1 hover:bg-gray-200 rounded transition-colors"
                  aria-label="Remove plane"
                >
                  <svg className="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => handlePositionChange(plane.id, -1)}
                  className="p-1 hover:bg-gray-200 rounded transition-colors"
                  aria-label="Decrease position"
                >
                  <svg className="w-4 h-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
                  </svg>
                </button>
                <input
                  type="range"
                  min="-100"
                  max="100"
                  step="0.1"
                  value={plane.position}
                  onChange={(e) => {
                    const updated = {
                      ...plane,
                      position: parseFloat(e.target.value),
                    };
                    setLocalPlanes(
                      localPlanes.map((p) => (p.id === plane.id ? updated : p))
                    );
                    onPlaneChange(updated);
                  }}
                  className="flex-1"
                />
                <button
                  onClick={() => handlePositionChange(plane.id, 1)}
                  className="p-1 hover:bg-gray-200 rounded transition-colors"
                  aria-label="Increase position"
                >
                  <svg className="w-4 h-4 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                  </svg>
                </button>
                <span className="text-xs text-gray-600 w-12 text-right">
                  {plane.position.toFixed(1)}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

