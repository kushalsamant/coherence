/**
 * Subscription Section Component
 * Displays subscription status and management options
 */
"use client";

import React from "react";
import type { UserMetadata, SubscriptionDisplayConfig } from "./types";

export interface SubscriptionSectionProps {
  /** User metadata */
  user: UserMetadata;
  /** Subscription display configuration */
  config?: SubscriptionDisplayConfig;
  /** Callback when manage subscription is clicked */
  onManageSubscription?: () => void;
  /** Callback when cancel subscription is clicked */
  onCancelSubscription?: () => void;
  /** Callback when resume subscription is clicked */
  onResumeSubscription?: () => void;
  /** API endpoint for subscription actions */
  subscriptionApiEndpoint?: string;
  /** Custom styling className */
  className?: string;
}

export function SubscriptionSection({
  user,
  config = {},
  onManageSubscription,
  onCancelSubscription,
  onResumeSubscription,
  subscriptionApiEndpoint = "/api/razorpay/subscriptions",
  className = "",
}: SubscriptionSectionProps) {
  const tier = user.subscription_tier || user.subscription || "trial";
  const status = user.subscription_status || "inactive";
  const { tierLabel, statusLabel, tierColors = {}, customInfo } = config;

  const getTierDisplay = () => {
    if (tierLabel) return tierLabel(tier);
    switch (tier) {
      case "trial":
        return "Free / Trial";
      case "weekly":
        return "Week Pro";
      case "monthly":
        return "Monthly Pro";
      case "yearly":
        return "Yearly Pro";
      default:
        return tier;
    }
  };

  const getStatusDisplay = () => {
    if (statusLabel) return statusLabel(status);
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  const getTierColor = (t: string) => {
    if (tierColors[t]) return tierColors[t];
    switch (t) {
      case "trial":
        return "bg-gray-100 text-gray-800";
      case "weekly":
        return "bg-blue-100 text-blue-800";
      case "monthly":
        return "bg-purple-100 text-purple-800";
      case "yearly":
        return "bg-green-100 text-green-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case "active":
        return "bg-green-100 text-green-800";
      case "expired":
        return "bg-amber-100 text-amber-800";
      case "cancelled":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const hasSubscription = tier !== "trial" && user.razorpay_subscription_id;
  const canManage = hasSubscription && status === "active";
  const canResume = hasSubscription && status === "cancelled";

  return (
    <div className={className}>
      <h2 className="text-xl font-semibold mb-4">Subscription</h2>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Current Plan
          </label>
          <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getTierColor(tier)}`}>
            {getTierDisplay()}
          </span>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
            Status
          </label>
          <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusColor()}`}>
            {getStatusDisplay()}
          </span>
        </div>
        {user.subscription_expires_at && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Expires
            </label>
            <div className="text-gray-900 dark:text-gray-100">
              {new Date(user.subscription_expires_at).toLocaleDateString()}
            </div>
          </div>
        )}
        {user.subscription_auto_renew !== undefined && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Auto-Renew
            </label>
            <div className="text-gray-900 dark:text-gray-100">
              {user.subscription_auto_renew ? "Yes (Subscription)" : "No (One-time)"}
            </div>
          </div>
        )}
        {customInfo}
        
        {canManage && (
          <div className="pt-4 border-t border-gray-200 dark:border-gray-700 space-y-3">
            {onManageSubscription && (
              <button
                onClick={onManageSubscription}
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
              >
                Manage Subscription
              </button>
            )}
            {onCancelSubscription && (
              <button
                onClick={onCancelSubscription}
                className="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Cancel Subscription
              </button>
            )}
          </div>
        )}
        {canResume && onResumeSubscription && (
          <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              onClick={onResumeSubscription}
              className="w-full px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Resume Subscription
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

