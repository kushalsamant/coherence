'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { api } from '@/lib/api';

export default function UploadForm() {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  // Architecture is the only supported project type
  const projectType = 'architecture' as const;

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    
    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'application/pdf'];
    if (!allowedTypes.includes(file.type)) {
      setError('Please upload a PNG, JPG, or PDF file');
      return;
    }

    // Validate file size (50MB max)
    if (file.size > 50 * 1024 * 1024) {
      setError('File size must be less than 50MB');
      return;
    }

    // Create preview for images
    if (file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    } else {
      setPreview(null); // PDFs don't get preview
    }

    setSelectedFile(file);
    setError(null);
    setSuccess(null);
  }, []);

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError(null);
    setSuccess(null);

    try {
      const result = await api.uploadSketch(selectedFile);
      setSuccess(`Upload successful! Job ID: ${result.job_id}. Processing started.`);
      
      // Reload page after 2 seconds to show new job
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    } catch (err: any) {
      // Sanitize error - never expose internal details
      setError('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleClear = () => {
    setSelectedFile(null);
    setPreview(null);
    setError(null);
    setSuccess(null);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    disabled: uploading,
  });

  const tips = {
    title: '🏗️ Architectural Plan Tips:',
    tips: [
      'Use clear, high-contrast sketches',
      'Draw walls as solid lines',
      'Mark doors and windows clearly',
      'Include room labels if possible',
      'Include a legend with scale (e.g., "1:100" or "1/4" = 1\'-0"") for accurate dimensions'
    ]
  };

  return (
    <div data-tour="upload">
      {!selectedFile ? (
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
            transition-colors
            ${isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300'}
            ${uploading ? 'opacity-50 cursor-not-allowed' : 'hover:border-primary-400'}
          `}
        >
          <input {...getInputProps()} />
          
          <div className="space-y-4">
            <div className="text-4xl">📐</div>
            
            {isDragActive ? (
              <p className="text-primary-600 font-medium">Drop your sketch here</p>
            ) : (
              <>
                <p className="text-gray-700 font-medium">
                  Drag & drop your sketch here
                </p>
                <p className="text-sm text-gray-500">
                  or click to browse
                </p>
                <p className="text-xs text-gray-400 mt-2">
                  Supported: PNG, JPG, PDF (max 50MB)
                </p>
              </>
            )}
          </div>
        </div>
      ) : (
        <div className="border-2 border-gray-300 rounded-lg p-6">
          {/* Preview */}
          {preview ? (
            <div className="mb-4">
              <img
                src={preview}
                alt="Preview"
                className="max-w-full h-auto max-h-96 mx-auto rounded-lg border border-gray-200"
              />
            </div>
          ) : (
            <div className="mb-4 p-8 bg-gray-100 rounded-lg text-center">
              <div className="text-4xl mb-2">📄</div>
              <p className="text-gray-600">{selectedFile.name}</p>
              <p className="text-sm text-gray-500 mt-1">
                {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB
              </p>
            </div>
          )}

          {/* File Info */}
          <div className="mb-4 p-3 bg-gray-50 rounded-lg">
            <p className="text-sm font-medium text-gray-900">{selectedFile.name}</p>
            <p className="text-xs text-gray-500 mt-1">
              {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • {selectedFile.type}
            </p>
          </div>

          {/* Actions */}
          <div className="flex gap-3">
            <button
              onClick={handleUpload}
              disabled={uploading}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Uploading...
                </span>
              ) : (
                'Start Processing'
              )}
            </button>
            <button
              onClick={handleClear}
              disabled={uploading}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50"
            >
              Change File
            </button>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      {/* Success Message */}
      {success && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-800 text-sm">{success}</p>
        </div>
      )}

      {/* Tips & Legend Info */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <h3 className="font-semibold text-blue-900 text-sm mb-2">{tips.title}</h3>
        <ul className="text-xs text-blue-800 space-y-1">
          {tips.tips.map((tip, index) => (
            <li key={index}>• {tip}</li>
          ))}
        </ul>
        <div className="mt-3 pt-3 border-t border-blue-200">
          <p className="text-xs text-blue-700 mb-2">
            <strong>📐 Automatic Legend Detection:</strong> We automatically detect legends from your sketch, including:
          </p>
          <ul className="text-xs text-blue-700 list-disc list-inside space-y-1 ml-2">
            <li>Scale information (e.g., "1:100", "1cm = 1m") for accurate real-world dimensions</li>
            <li>Room labels and annotations</li>
            <li>Measurement references</li>
          </ul>
          <p className="text-xs text-blue-600 mt-2 italic">
            Including a clear legend in your sketch improves dimension accuracy and element identification.
          </p>
        </div>
      </div>
    </div>
  );
}

