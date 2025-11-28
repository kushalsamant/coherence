'use client';

import { useState, useMemo } from 'react';
import { api, SymbolSummary, PlanData, SymbolDetectionEntry } from '@/lib/api';

interface SymbolDetectionPanelProps {
  jobId: string;
  summary?: SymbolSummary | null;
  buttonVariant?: 'link' | 'badge';
}

export default function SymbolDetectionPanel({ jobId, summary, buttonVariant = 'badge' }: SymbolDetectionPanelProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [planData, setPlanData] = useState<PlanData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [sortKey, setSortKey] = useState<'confidence' | 'label'>('confidence');

  const hasSymbols = summary?.enabled || (summary?.total_detected ?? 0) > 0;

  const handleOpen = async () => {
    setIsOpen(true);
    if (planData || loading) return;
    setLoading(true);
    setError(null);
    try {
      const data = await api.getJobPlanData(jobId);
      setPlanData(data);
    } catch (err) {
      setError('Failed to load plan data. Try again later.');
    } finally {
      setLoading(false);
    }
  };

  const closeModal = () => {
    setIsOpen(false);
  };

  const symbols: SymbolDetectionEntry[] = planData?.symbols ?? [];

  const categoryOptions = useMemo(() => {
    const categories = new Set<string>();
    symbols.forEach((symbol) => {
      if (symbol.category) {
        categories.add(symbol.category);
      }
    });
    return Array.from(categories);
  }, [symbols]);

  const filteredSymbols = useMemo(() => {
    let items = symbols;
    if (categoryFilter !== 'all') {
      items = items.filter((symbol) => symbol.category === categoryFilter);
    }
    if (sortKey === 'confidence') {
      return [...items].sort((a, b) => b.confidence - a.confidence);
    }
    return [...items].sort((a, b) => (a.label || '').localeCompare(b.label || ''));
  }, [symbols, categoryFilter, sortKey]);

  const downloadCsv = () => {
    if (!symbols.length) return;
    const header = ['Label', 'Display Name', 'Category', 'Confidence', 'IFC Type', 'BBox', 'Source'];
    const rows = symbols.map((symbol) => [
      symbol.label,
      symbol.display_name || '',
      symbol.category || '',
      symbol.confidence.toFixed(3),
      symbol.ifc_type || '',
      symbol.bbox.map((v) => v.toFixed(2)).join('|'),
      symbol.source || '',
    ]);
    const csv = [header, ...rows].map((row) => row.map((cell) => `"${cell}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `symbol-detections-${jobId}.csv`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const triggerButton = (
    <button
      onClick={handleOpen}
      disabled={!hasSymbols}
      className={
        buttonVariant === 'link'
          ? 'text-sm text-primary-700 underline disabled:text-gray-400 disabled:no-underline'
          : 'px-3 py-1 rounded-full text-xs font-medium bg-purple-50 text-purple-700 hover:bg-purple-100 disabled:bg-gray-100 disabled:text-gray-400'
      }
    >
      {hasSymbols ? `Review Symbols (${summary?.total_detected ?? '?'})` : 'No symbols detected'}
    </button>
  );

  return (
    <>
      {triggerButton}

      {isOpen && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-5xl rounded-2xl shadow-2xl flex flex-col max-h-[90vh]">
            <div className="p-4 border-b flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold">Symbol QA</h3>
                <p className="text-sm text-gray-500">
                  Job {jobId} · {summary?.total_detected ?? 0} detections
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={downloadCsv}
                  disabled={!symbols.length}
                  className="px-3 py-1 text-sm rounded-lg bg-gray-100 hover:bg-gray-200 disabled:opacity-50"
                >
                  Export CSV
                </button>
                <button
                  onClick={closeModal}
                  className="px-3 py-1 text-sm rounded-lg bg-gray-100 hover:bg-gray-200"
                >
                  Close
                </button>
              </div>
            </div>

            <div className="p-4 border-b grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div className="bg-purple-50 rounded-xl p-3">
                <div className="text-xs uppercase tracking-wide text-purple-600 mb-1">Total Symbols</div>
                <div className="text-2xl font-bold text-purple-800">{summary?.total_detected ?? symbols.length}</div>
                <div className="text-xs text-purple-700 mt-1">Model: {summary?.model_path || 'N/A'}</div>
              </div>
              <div className="bg-blue-50 rounded-xl p-3">
                <div className="text-xs uppercase tracking-wide text-blue-600 mb-1">Top Labels</div>
                <div className="text-sm text-blue-800">
                  {summary?.sample_labels?.length
                    ? summary.sample_labels.join(', ')
                    : 'No detections available'}
                </div>
              </div>
              <div className="bg-emerald-50 rounded-xl p-3">
                <div className="text-xs uppercase tracking-wide text-emerald-600 mb-1">Inference (ms)</div>
                <div className="text-2xl font-bold text-emerald-800">
                  {summary?.inference_ms ? summary.inference_ms.toFixed(1) : '—'}
                </div>
              </div>
            </div>

            <div className="p-4 flex flex-wrap gap-3 items-center border-b">
              <label className="text-sm text-gray-600 flex items-center gap-2">
                Category:
                <select
                  className="border rounded-lg px-2 py-1 text-sm"
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                >
                  <option value="all">All</option>
                  {categoryOptions.map((category) => (
                    <option key={category} value={category}>
                      {category} ({summary?.categories?.[category] ?? 0})
                    </option>
                  ))}
                </select>
              </label>
              <label className="text-sm text-gray-600 flex items-center gap-2">
                Sort by:
                <select
                  className="border rounded-lg px-2 py-1 text-sm"
                  value={sortKey}
                  onChange={(e) => setSortKey(e.target.value as 'confidence' | 'label')}
                >
                  <option value="confidence">Confidence</option>
                  <option value="label">Label</option>
                </select>
              </label>
            </div>

            <div className="flex-1 overflow-y-auto">
              {loading ? (
                <div className="p-6 text-center text-gray-500">Loading plan data…</div>
              ) : error ? (
                <div className="p-6 text-center text-red-500">{error}</div>
              ) : filteredSymbols.length === 0 ? (
                <div className="p-6 text-center text-gray-500">No symbols to display.</div>
              ) : (
                <table className="w-full text-sm">
                  <thead className="sticky top-0 bg-white shadow">
                    <tr>
                      <th className="text-left px-4 py-2">Label</th>
                      <th className="text-left px-4 py-2">Category</th>
                      <th className="text-left px-4 py-2">Confidence</th>
                      <th className="text-left px-4 py-2">IFC Type</th>
                      <th className="text-left px-4 py-2">BBox</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredSymbols.map((symbol, idx) => (
                      <tr key={`${symbol.label}-${idx}`} className="border-t">
                        <td className="px-4 py-2">
                          <div className="font-medium text-gray-900">{symbol.display_name || symbol.label}</div>
                          <div className="text-xs text-gray-500">{symbol.source}</div>
                        </td>
                        <td className="px-4 py-2 text-gray-700 capitalize">{symbol.category || '—'}</td>
                        <td className="px-4 py-2 text-gray-900 font-semibold">{(symbol.confidence * 100).toFixed(1)}%</td>
                        <td className="px-4 py-2 text-gray-600">{symbol.ifc_type || '—'}</td>
                        <td className="px-4 py-2 text-xs text-gray-500">
                          {symbol.bbox.map((v) => v.toFixed(1)).join(', ')}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

