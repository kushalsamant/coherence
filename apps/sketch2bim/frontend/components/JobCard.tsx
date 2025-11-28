'use client';

import { Job } from '@/lib/api';
import Link from 'next/link';
import SymbolDetectionPanel from './SymbolDetectionPanel';

interface JobCardProps {
  job: Job;
  onDelete: () => void;
}

export default function JobCard({ job, onDelete }: JobCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      case 'review':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return '✓';
      case 'processing':
        return '⟳';
      case 'failed':
        return '✗';
      case 'review':
        return '⚠';
      default:
        return '⋯';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {/* Status Badge */}
          <div className="flex items-center gap-3 mb-3 flex-wrap">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(job.status)}`}>
              <span className="mr-1">{getStatusIcon(job.status)}</span>
              {job.status.charAt(0).toUpperCase() + job.status.slice(1)}
            </span>
            {job.status === 'review' && (
              <span className="px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                ⚠️ Requires Review
              </span>
            )}
            {job.detection_confidence && (
              <span className="text-sm text-gray-500">
                Confidence: {job.detection_confidence.toFixed(0)}%
              </span>
            )}
            {job.legend_detected && job.legend_data && (
              <span className="text-sm text-green-600" title="Legend detected from sketch">
                📐 Legend: {job.legend_data.scale || 'Detected'}
              </span>
            )}
            {(job as any).cost_usd && (job as any).cost_usd > 0 && (
              <span className="text-sm text-gray-500">
                Cost: ${((job as any).cost_usd).toFixed(4)}
              </span>
            )}
            {job.symbol_summary && (
              <span className="text-sm text-purple-700 bg-purple-50 px-3 py-1 rounded-full">
                🔍 Symbols: {job.symbol_summary.total_detected}
              </span>
            )}
          </div>

          {/* Filename */}
          <h3 className="font-semibold text-gray-900 mb-2">
            {job.sketch_filename}
          </h3>

          {/* Progress Bar */}
          {job.status === 'processing' && (
            <div className="mb-3">
              <div className="flex justify-between text-sm text-gray-600 mb-1">
                <span>
                  {job.progress < 20 && 'Initializing...'}
                  {job.progress >= 20 && job.progress < 40 && 'Analyzing sketch...'}
                  {job.progress >= 40 && job.progress < 60 && 'Detecting elements...'}
                  {job.progress >= 60 && job.progress < 80 && 'Generating model...'}
                  {job.progress >= 80 && job.progress < 95 && 'Finalizing...'}
                  {job.progress >= 95 && 'Almost done...'}
                </span>
                <span>{job.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${job.progress}%` }}
                ></div>
              </div>
              {job.progress > 0 && (
                <p className="text-xs text-gray-500 mt-1">
                  {job.progress < 20 && 'Setting up processing environment...'}
                  {job.progress >= 20 && job.progress < 40 && 'Analyzing image quality and structure...'}
                  {job.progress >= 40 && job.progress < 60 && 'Detecting walls, doors, windows, and rooms...'}
                  {job.progress >= 60 && job.progress < 80 && 'Creating 3D geometry and IFC model...'}
                  {job.progress >= 80 && job.progress < 95 && 'Generating export files and preparing download...'}
                  {job.progress >= 95 && 'Finalizing and uploading files...'}
                </p>
              )}
            </div>
          )}

          {/* Error Message */}
          {job.status === 'failed' && job.error_message && (
            <div className="mb-3 p-3 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-start justify-between mb-2">
                <p className="text-sm font-semibold text-red-800">Processing Failed</p>
                <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p className="text-sm text-red-700 mb-3">{job.error_message}</p>
              <div className="text-xs text-red-600 space-y-1">
                <p className="font-semibold mb-1">Troubleshooting tips:</p>
                <ul className="list-disc list-inside space-y-0.5 ml-1">
                  {job.error_message.toLowerCase().includes('network') || job.error_message.toLowerCase().includes('timeout') ? (
                    <>
                      <li>Check your internet connection and try again</li>
                      <li>The server may be temporarily unavailable</li>
                    </>
                  ) : job.error_message.toLowerCase().includes('file') || job.error_message.toLowerCase().includes('format') || job.error_message.toLowerCase().includes('invalid') ? (
                    <>
                      <li>Ensure the file is a valid image format (PNG, JPG, JPEG)</li>
                      <li>Check that the file is not corrupted</li>
                      <li>Try a different image file</li>
                    </>
                  ) : job.error_message.toLowerCase().includes('size') || job.error_message.toLowerCase().includes('large') || job.error_message.toLowerCase().includes('exceed') ? (
                    <>
                      <li>The file may be too large - try compressing it</li>
                      <li>Maximum file size is typically 10MB</li>
                    </>
                  ) : (
                    <>
                      <li>Check that your sketch image is clear and high-resolution</li>
                      <li>Ensure the sketch contains recognizable architectural elements</li>
                      <li>Try uploading a different sketch or contact support</li>
                    </>
                  )}
                </ul>
              </div>
            </div>
          )}

          {/* Review Actions */}
          {job.status === 'review' && (
            <div className="flex flex-wrap gap-2 mb-3">
              <button
                onClick={async () => {
                  try {
                    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
                    await fetch(`${apiUrl}/api/v1/generate/review/${job.id}?action=approve`, {
                      method: 'POST',
                      credentials: 'include'
                    });
                    window.location.reload();
                  } catch (err) {
                    if (process.env.NODE_ENV === 'development') {
                      console.error('Failed to approve');
                    }
                  }
                }}
                className="px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition-colors"
              >
                Approve
              </button>
              <button
                onClick={async () => {
                  try {
                    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
                    await fetch(`${apiUrl}/api/v1/generate/review/${job.id}?action=reject`, {
                      method: 'POST',
                      credentials: 'include'
                    });
                    window.location.reload();
                  } catch (err) {
                    if (process.env.NODE_ENV === 'development') {
                      console.error('Failed to reject');
                    }
                  }
                }}
                className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition-colors"
              >
                Reject
              </button>
            </div>
          )}

          {/* Download Links */}
          {(job.status === 'completed' || job.status === 'review') && (
            <div className="flex flex-wrap gap-2 mb-3">
              {job.ifc_url && (
                <a
                  href={job.ifc_url}
                  download
                  className="px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700 transition-colors"
                >
                  Download IFC
                </a>
              )}
              {job.dwg_url && (
                <a
                  href={job.dwg_url}
                  download
                  className="px-4 py-2 bg-gray-600 text-white rounded-lg text-sm hover:bg-gray-700 transition-colors"
                >
                  Download DWG
                </a>
              )}
              {job.rvt_url && (
                <a
                  href={job.rvt_url}
                  download
                  className="px-4 py-2 bg-gray-600 text-white rounded-lg text-sm hover:bg-gray-700 transition-colors"
                >
                  Download IFC (Revit)
                </a>
              )}
              {job.sketchup_url && (
                <a
                  href={job.sketchup_url}
                  download
                  className="px-4 py-2 bg-orange-600 text-white rounded-lg text-sm hover:bg-orange-700 transition-colors"
                  title="Download OBJ file for SketchUp"
                >
                  Download SketchUp
                </a>
              )}
              <Link
                href={`/viewer/${job.id}`}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700 transition-colors"
              >
                View 3D
              </Link>
            </div>
          )}

          {/* Legend Info */}
          {job.legend_detected && job.legend_data && (
            <div className="mb-3 p-2 bg-green-50 border border-green-200 rounded-lg">
              <div className="text-xs font-semibold text-green-800 mb-1">📐 Legend Detected</div>
              {job.legend_data.scale && (
                <div className="text-xs text-green-700">Scale: {job.legend_data.scale}</div>
              )}
              {job.legend_data.room_labels && Object.keys(job.legend_data.room_labels).length > 0 && (
                <div className="text-xs text-green-700 mt-1">
                  Rooms: {Object.keys(job.legend_data.room_labels).length} labels found
                </div>
              )}

          {/* Symbol QA */}
          <div className="flex items-center justify-between border-t pt-3 mt-4">
            <div>
              <p className="text-sm font-semibold text-gray-800">Symbol QA</p>
              <p className="text-xs text-gray-500">
                {job.symbol_summary
                  ? `Detected ${job.symbol_summary.total_detected} elements across ${Object.keys(
                      job.symbol_summary.categories || {}
                    ).length} categories.`
                  : 'No symbol detections available for this job.'}
              </p>
            </div>
            <SymbolDetectionPanel jobId={job.id} summary={job.symbol_summary} />
          </div>
            </div>
          )}

          {/* Metadata */}
          <div className="text-xs text-gray-500">
            <span>Created: {formatDate(job.created_at)}</span>
            {job.completed_at && (
              <span className="ml-4">
                Completed: {formatDate(job.completed_at)}
              </span>
            )}
            {job.expires_at && (
              <span className="ml-4">
                Expires: {formatDate(job.expires_at)}
              </span>
            )}
          </div>
        </div>

        {/* Delete Button */}
        <button
          onClick={onDelete}
          className="ml-4 text-gray-400 hover:text-red-600 transition-colors"
          title="Delete job"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  );
}

