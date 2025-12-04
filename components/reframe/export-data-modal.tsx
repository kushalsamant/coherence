"use client";

import { useState } from "react";
import { Button } from "./ui/button";
import { logger } from "@/lib/logger";

interface ExportDataModalProps {
  isOpen: boolean;
  onClose: () => void;
  userId: string;
}

export function ExportDataModal({ isOpen, onClose, userId }: ExportDataModalProps) {
  const [isExporting, setIsExporting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleExport = async () => {
    setIsExporting(true);
    setError(null);

    try {
      const response = await fetch("/api/account/export");
      
      if (!response.ok) {
        throw new Error("Failed to export data");
      }

      // Get the data
      const data = await response.json();
      
      // Create blob and download
      const blob = new Blob([JSON.stringify(data, null, 2)], {
        type: "application/json",
      });
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      
      const date = new Date().toISOString().split("T")[0];
      a.download = `reframe-data-export-${userId}-${date}.json`;
      
      document.body.appendChild(a);
      a.click();
      
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      // Close modal after successful export
      setTimeout(() => {
        onClose();
      }, 1000);
    } catch (err) {
      logger.error("Export error:", err);
      setError("Failed to export data. Please try again.");
    } finally {
      setIsExporting(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full p-6 space-y-6 shadow-xl">
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">Export Your Data</h2>
          <p className="text-slate-600">
            Download a complete copy of your personal data in JSON format.
          </p>
        </div>

        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-2">
          <p className="font-semibold text-blue-900">Your export will include:</p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-blue-800">
            <li>Account information (email, ID, created date)</li>
            <li>Subscription details and tier</li>
            <li>Usage statistics and history</li>
            <li>Consent records</li>
            <li>Payment history (last 12 months)</li>
          </ul>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {isExporting && (
          <div className="text-center py-4">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <p className="mt-2 text-sm text-slate-600">Preparing your data export...</p>
          </div>
        )}

        <div className="flex gap-3">
          <Button
            variant="outline"
            onClick={onClose}
            className="flex-1"
            disabled={isExporting}
          >
            Cancel
          </Button>
          <Button
            onClick={handleExport}
            disabled={isExporting}
            className="flex-1"
          >
            {isExporting ? "Exporting..." : "Download Data"}
          </Button>
        </div>

        <p className="text-xs text-slate-500 text-center">
          This complies with GDPR Right to Data Portability
        </p>
      </div>
    </div>
  );
}

