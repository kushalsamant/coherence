'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import IfcViewer from './IfcViewer';
import { logger } from '@/lib/logger';

interface IterationCompareProps {
  jobId: string;
  iteration1Id?: string;
  iteration2Id?: string;
}

export default function IterationCompare({ jobId, iteration1Id, iteration2Id }: IterationCompareProps) {
  const [iterations, setIterations] = useState<any[]>([]);
  const [selected1, setSelected1] = useState<string | null>(iteration1Id || null);
  const [selected2, setSelected2] = useState<string | null>(iteration2Id || null);
  const [loading, setLoading] = useState(true);
  const [originalJob, setOriginalJob] = useState<any>(null);

  useEffect(() => {
    loadData();
  }, [jobId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [iterationsData, jobData] = await Promise.all([
        api.listIterations(jobId),
        api.getJob(jobId)
      ]);
      setIterations(iterationsData);
      setOriginalJob(jobData);
      
      // Set defaults if not provided
      if (!selected1 && iterationsData.length > 0) {
        setSelected1(iterationsData[0].id);
      }
      if (!selected2 && iterationsData.length > 1) {
        setSelected2(iterationsData[1].id);
      } else if (!selected2 && originalJob?.ifc_url) {
        // Compare first iteration with original
        setSelected2('original');
      }
    } catch (error) {
      if (process.env.NODE_ENV === 'development') {
        logger.error('Failed to load iterations');
      }
    } finally {
      setLoading(false);
    }
  };

  const getIfcUrl = (id: string | null): string | null => {
    if (!id) return null;
    if (id === 'original') return originalJob?.ifc_url || null;
    const iteration = iterations.find(i => i.id === id);
    return iteration?.ifc_url || null;
  };

  const getIterationName = (id: string | null): string => {
    if (!id) return 'None';
    if (id === 'original') return 'Original';
    const iteration = iterations.find(i => i.id === id);
    return iteration?.name || `Iteration ${id.slice(0, 8)}`;
  };

  const getChanges = (id: string | null): any => {
    if (!id || id === 'original') return null;
    const iteration = iterations.find(i => i.id === id);
    return iteration?.changes_json || null;
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="grid grid-cols-2 gap-4 h-96">
            <div className="bg-gray-200 rounded"></div>
            <div className="bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  const ifcUrl1 = getIfcUrl(selected1);
  const ifcUrl2 = getIfcUrl(selected2);
  const changes1 = getChanges(selected1);
  const changes2 = getChanges(selected2);

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Compare Iterations</h2>
          <button
            onClick={() => window.history.back()}
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            Back
          </button>
        </div>

        {/* Selection Controls */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Left View
            </label>
            <select
              value={selected1 || ''}
              onChange={(e) => setSelected1(e.target.value || null)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="original">Original</option>
              {iterations.map((iter) => (
                <option key={iter.id} value={iter.id}>
                  {iter.name || `Iteration ${iter.id.slice(0, 8)}`}
                </option>
              ))}
            </select>
            {changes1 && (
              <div className="mt-2 text-xs text-gray-600">
                <p className="font-semibold">Changes:</p>
                <p>{changes1.change_summary || 'No summary available'}</p>
              </div>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Right View
            </label>
            <select
              value={selected2 || ''}
              onChange={(e) => setSelected2(e.target.value || null)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg"
            >
              <option value="original">Original</option>
              {iterations.map((iter) => (
                <option key={iter.id} value={iter.id}>
                  {iter.name || `Iteration ${iter.id.slice(0, 8)}`}
                </option>
              ))}
            </select>
            {changes2 && (
              <div className="mt-2 text-xs text-gray-600">
                <p className="font-semibold">Changes:</p>
                <p>{changes2.change_summary || 'No summary available'}</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Side-by-Side Viewers */}
      <div className="flex-1 grid grid-cols-2 gap-4 p-4 overflow-hidden">
        <div className="border border-gray-200 rounded-lg overflow-hidden">
          <div className="bg-gray-100 px-3 py-2 border-b border-gray-200">
            <h3 className="font-semibold text-sm text-gray-700">
              {getIterationName(selected1)}
            </h3>
          </div>
          <div className="h-full">
            {ifcUrl1 ? (
              <IfcViewer ifc_url={ifcUrl1} />
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400">
                <p>No IFC file available</p>
              </div>
            )}
          </div>
        </div>

        <div className="border border-gray-200 rounded-lg overflow-hidden">
          <div className="bg-gray-100 px-3 py-2 border-b border-gray-200">
            <h3 className="font-semibold text-sm text-gray-700">
              {getIterationName(selected2)}
            </h3>
          </div>
          <div className="h-full">
            {ifcUrl2 ? (
              <IfcViewer ifc_url={ifcUrl2} />
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400">
                <p>No IFC file available</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Differences Summary */}
      {(changes1 || changes2) && (
        <div className="bg-gray-50 border-t border-gray-200 p-4">
          <h3 className="font-semibold text-gray-900 mb-2">Differences Summary</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <p className="font-medium text-gray-700 mb-1">Left View Changes:</p>
              <p className="text-gray-600">
                {changes1?.change_summary || 'No changes (original)'}
              </p>
            </div>
            <div>
              <p className="font-medium text-gray-700 mb-1">Right View Changes:</p>
              <p className="text-gray-600">
                {changes2?.change_summary || 'No changes (original)'}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

