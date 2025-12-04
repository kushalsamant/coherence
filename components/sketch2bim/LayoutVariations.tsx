'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import Link from 'next/link';
import { logger } from '@/lib/logger';

interface LayoutVariationsProps {
  jobId: string;
}

export default function LayoutVariations({ jobId }: LayoutVariationsProps) {
  const [variations, setVariations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [numVariations, setNumVariations] = useState(3);

  useEffect(() => {
    loadVariations();
  }, [jobId]);

  const loadVariations = async () => {
    try {
      setLoading(true);
      const data = await api.listVariations(jobId);
      setVariations(data);
    } catch (error) {
      if (process.env.NODE_ENV === 'development') {
        logger.error('Failed to load variations');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    try {
      setGenerating(true);
      await api.generateVariations(jobId, numVariations);
      // Reload variations after generation
      setTimeout(() => {
        loadVariations();
      }, 2000);
    } catch (error: any) {
      alert('Failed to generate variations: ' + (error.message || 'Unknown error'));
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-48 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Layout Variations</h2>
          <p className="text-sm text-gray-600 mt-1">
            Explore alternative room arrangements from your sketch
          </p>
        </div>
        <div className="flex items-center gap-3">
          <input
            type="number"
            min="1"
            max="10"
            value={numVariations}
            onChange={(e) => setNumVariations(parseInt(e.target.value) || 3)}
            className="w-20 px-3 py-2 border border-gray-300 rounded-lg text-sm"
            disabled={generating}
          />
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {generating ? 'Generating...' : 'Generate Variations'}
          </button>
        </div>
      </div>

      {variations.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
          <svg className="mx-auto h-12 w-12 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <p className="text-gray-600 mb-4">No variations generated yet</p>
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50"
          >
            {generating ? 'Generating...' : 'Generate Your First Variations'}
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {variations.map((variation) => (
            <div
              key={variation.id}
              className="bg-white border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
            >
              {/* Preview Image or Placeholder */}
              <div className="aspect-video bg-gray-100 flex items-center justify-center">
                {variation.preview_image_url ? (
                  <img
                    src={variation.preview_image_url}
                    alt={`Variation ${variation.variation_number}`}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="text-center text-gray-400">
                    <svg className="mx-auto h-12 w-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    <p className="text-sm">Preview</p>
                  </div>
                )}
              </div>

              {/* Variation Info */}
              <div className="p-4">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-gray-900">
                    Variation {variation.variation_number}
                  </h3>
                  {variation.confidence && (
                    <span className="text-xs px-2 py-1 bg-green-100 text-green-800 rounded">
                      {Math.round(variation.confidence * 100)}% confidence
                    </span>
                  )}
                </div>
                <p className="text-xs text-gray-500 mb-3">
                  {new Date(variation.created_at).toLocaleDateString()}
                </p>

                {/* Actions */}
                <div className="flex gap-2">
                  {variation.ifc_url ? (
                    <Link
                      href={`/viewer/${jobId}?variation=${variation.id}`}
                      className="flex-1 px-3 py-2 bg-primary-600 text-white text-sm rounded-lg hover:bg-primary-700 transition-colors text-center"
                    >
                      View & Edit
                    </Link>
                  ) : (
                    <button
                      disabled
                      className="flex-1 px-3 py-2 bg-gray-300 text-gray-600 text-sm rounded-lg cursor-not-allowed"
                    >
                      Processing...
                    </button>
                  )}
                  <button
                    onClick={async () => {
                      if (confirm('Delete this variation?')) {
                        try {
                          await api.deleteVariation(variation.id);
                          loadVariations();
                        } catch (error) {
                          alert('Failed to delete variation');
                        }
                      }
                    }}
                    className="px-3 py-2 bg-red-100 text-red-700 text-sm rounded-lg hover:bg-red-200 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

