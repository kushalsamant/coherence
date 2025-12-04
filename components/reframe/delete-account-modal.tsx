"use client";

import { useState } from "react";
import { Button } from "./ui/button";
import { logger } from "@/lib/logger";

interface DeleteAccountModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => Promise<void>;
}

export function DeleteAccountModal({ isOpen, onClose, onConfirm }: DeleteAccountModalProps) {
  const [confirmText, setConfirmText] = useState("");
  const [finalConfirm, setFinalConfirm] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const canDelete = confirmText === "DELETE" && finalConfirm && !isDeleting;

  const handleDelete = async () => {
    if (!canDelete) return;

    setIsDeleting(true);
    try {
      await onConfirm();
      // Modal will close via redirect after deletion
    } catch (error) {
      logger.error("Delete failed:", error);
      setIsDeleting(false);
    }
  };

  const handleClose = () => {
    if (isDeleting) return;
    setConfirmText("");
    setFinalConfirm(false);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg max-w-md w-full p-6 space-y-6 shadow-xl">
        <div className="space-y-2">
          <h2 className="text-2xl font-bold text-red-600">Delete Account</h2>
          <p className="text-slate-600">
            This action is <strong>permanent and cannot be undone</strong>.
          </p>
        </div>

        <div className="bg-red-50 border border-red-200 rounded-lg p-4 space-y-2">
          <p className="font-semibold text-red-900">The following will be permanently deleted:</p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-red-800">
            <li>Your account and all personal data</li>
            <li>All usage history and statistics</li>
            <li>Active subscriptions will be cancelled</li>
            <li>All consent and authentication records</li>
          </ul>
        </div>

        <div className="space-y-4">
          <div>
            <label htmlFor="confirm-text" className="block text-sm font-medium mb-2">
              Type <span className="font-bold text-red-600">DELETE</span> to confirm:
            </label>
            <input
              id="confirm-text"
              type="text"
              value={confirmText}
              onChange={(e) => setConfirmText(e.target.value)}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500"
              placeholder="Type DELETE"
              disabled={isDeleting}
            />
          </div>

          <div className="flex items-start space-x-3">
            <input
              type="checkbox"
              id="final-confirm"
              checked={finalConfirm}
              onChange={(e) => setFinalConfirm(e.target.checked)}
              className="mt-1 w-4 h-4 rounded border-slate-300 text-red-600 focus:ring-red-500 cursor-pointer"
              disabled={isDeleting}
            />
            <label htmlFor="final-confirm" className="text-sm cursor-pointer">
              I understand this action is permanent and all my data will be deleted
            </label>
          </div>
        </div>

        <div className="flex gap-3">
          <Button
            variant="outline"
            onClick={handleClose}
            className="flex-1"
            disabled={isDeleting}
          >
            Cancel
          </Button>
          <Button
            variant="destructive"
            onClick={handleDelete}
            disabled={!canDelete}
            className="flex-1"
          >
            {isDeleting ? "Deleting..." : "Delete My Account"}
          </Button>
        </div>
      </div>
    </div>
  );
}

