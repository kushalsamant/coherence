/**
 * Profile Section Component
 * Displays user account information
 */
"use client";

import React from "react";
import type { UserMetadata } from "./types";

export interface ProfileSectionProps {
  /** User metadata */
  user: UserMetadata;
  /** Optional user ID display format */
  userIdFormat?: "full" | "truncated";
  /** Show user ID field */
  showUserId?: boolean;
  /** Additional fields to display */
  additionalFields?: Array<{
    label: string;
    value: string | React.ReactNode;
  }>;
  /** Custom styling className */
  className?: string;
}

export function ProfileSection({
  user,
  userIdFormat = "truncated",
  showUserId = false,
  additionalFields = [],
  className = "",
}: ProfileSectionProps) {
  const displayUserId = userIdFormat === "truncated" && user.id
    ? `${user.id.slice(0, 16)}...`
    : user.id;

  return (
    <div className={className}>
      <h2 className="text-xl font-semibold mb-4">Account Information</h2>
      <div className="space-y-4">
        {user.email && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Email
            </label>
            <div className="text-gray-900 dark:text-gray-100">{user.email}</div>
          </div>
        )}
        {user.name && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Name
            </label>
            <div className="text-gray-900 dark:text-gray-100">{user.name}</div>
          </div>
        )}
        {showUserId && displayUserId && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              User ID
            </label>
            <div className="font-mono text-sm text-gray-900 dark:text-gray-100">{displayUserId}</div>
          </div>
        )}
        {additionalFields.map((field, index) => (
          <div key={index}>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              {field.label}
            </label>
            <div className="text-gray-900 dark:text-gray-100">{field.value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

