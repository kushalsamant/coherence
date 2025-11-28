'use client';

import { useState, useRef, useEffect } from 'react';
import * as THREE from 'three';
import IfcViewer from './IfcViewer';
import { api } from '@/lib/api';

interface IfcEditorProps {
  ifc_url: string;
  job_id: string;
  onSave?: (iterationId: string) => void;
}

interface EditChange {
  type: 'move' | 'resize' | 'delete' | 'add' | 'property';
  elementId: string;
  data: any;
}

export default function IfcEditor({ ifc_url, job_id, onSave }: IfcEditorProps) {
  const [editMode, setEditMode] = useState(false);
  const [selectedElement, setSelectedElement] = useState<string | null>(null);
  const [changes, setChanges] = useState<EditChange[]>([]);
  const [saving, setSaving] = useState(false);
  const [iterationName, setIterationName] = useState('');

  const handleSave = async () => {
    if (changes.length === 0) {
      alert('No changes to save');
      return;
    }

    setSaving(true);
    try {
      const changesJson = {
        changes: changes,
        timestamp: new Date().toISOString()
      };

      const iteration = await api.createIteration(job_id, {
        name: iterationName || `Iteration ${new Date().toLocaleString()}`,
        changes_json: changesJson
      });

      if (onSave) {
        onSave(iteration.id);
      }

      // Reset editor
      setChanges([]);
      setSelectedElement(null);
      setEditMode(false);
      setIterationName('');

      alert('Iteration saved successfully!');
    } catch (error: any) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to save iteration');
      }
      // Never expose internal error details
      alert('Failed to save iteration. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    setChanges([]);
    setSelectedElement(null);
    setEditMode(false);
    setIterationName('');
  };

  return (
    <div className="relative w-full h-full">
      {/* Edit Mode Toggle */}
      <div className="absolute top-4 right-4 z-50 flex gap-2">
        {!editMode ? (
          <button
            onClick={() => setEditMode(true)}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors shadow-lg"
          >
            Edit Mode
          </button>
        ) : (
          <>
            <button
              onClick={handleCancel}
              className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors shadow-lg"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              disabled={saving || changes.length === 0}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {saving ? 'Saving...' : `Save Changes (${changes.length})`}
            </button>
          </>
        )}
      </div>

      {/* Edit Mode Info */}
      {editMode && (
        <div className="absolute top-4 left-4 z-50 bg-yellow-50 border border-yellow-200 rounded-lg p-3 shadow-lg max-w-sm">
          <div className="flex items-start gap-2">
            <svg className="w-5 h-5 text-yellow-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="flex-1">
              <p className="text-sm font-semibold text-yellow-800 mb-1">Edit Mode Active</p>
              <p className="text-xs text-yellow-700">
                Click elements to select them. Changes will be saved as a new iteration.
              </p>
              {changes.length > 0 && (
                <div className="mt-2">
                  <input
                    type="text"
                    placeholder="Iteration name (optional)"
                    value={iterationName}
                    onChange={(e) => setIterationName(e.target.value)}
                    className="w-full px-2 py-1 text-xs border border-yellow-300 rounded"
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* IFC Viewer */}
      <div className="w-full h-full">
        <IfcViewer ifc_url={ifc_url} />
      </div>

      {/* Changes Summary */}
      {editMode && changes.length > 0 && (
        <div className="absolute bottom-4 left-4 z-50 bg-white border border-gray-200 rounded-lg p-3 shadow-lg max-w-sm">
          <p className="text-sm font-semibold text-gray-800 mb-2">
            Changes ({changes.length})
          </p>
          <div className="space-y-1 max-h-32 overflow-y-auto">
            {changes.map((change, idx) => (
              <div key={idx} className="text-xs text-gray-600">
                • {change.type}: {change.elementId}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

