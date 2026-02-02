/**
 * Settings Page Layout Component
 * Provides a standardized settings page structure with configurable sections
 */
"use client";

import React from "react";
import { ProfileSection } from "./ProfileSection";
import { SubscriptionSection } from "./SubscriptionSection";
import { PaymentHistorySection } from "./PaymentHistorySection";
import type { UserMetadata } from "./types";

export interface SettingsPageProps {
  /** Page title */
  title?: string;
  /** Page description */
  description?: string;
  /** User metadata */
  user: UserMetadata | null;
  /** Show profile section */
  showProfile?: boolean;
  /** Show subscription section */
  showSubscription?: boolean;
  /** Show payment history section */
  showPaymentHistory?: boolean;
  /** Custom sections */
  customSections?: Array<{
    title: string;
    content: React.ReactNode;
  }>;
  /** Callback when sign out is clicked */
  onSignOut?: () => void;
  /** API endpoints */
  apiEndpoints?: {
    subscription?: string;
    paymentHistory?: string;
  };
  /** Subscription display configuration */
  subscriptionConfig?: Parameters<typeof SubscriptionSection>[0]["config"];
  /** Loading state */
  loading?: boolean;
  /** Custom styling className */
  className?: string;
}

export function SettingsPage({
  title = "Settings",
  description = "Manage your account settings",
  user,
  showProfile = true,
  showSubscription = true,
  showPaymentHistory = false,
  customSections = [],
  onSignOut,
  apiEndpoints = {},
  subscriptionConfig,
  loading = false,
  className = "",
}: SettingsPageProps) {
  if (loading || !user) {
    return (
      <div className={`p-8 text-center ${className}`}>
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen p-4 py-12 ${className}`}>
      <div className="container mx-auto max-w-4xl space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold mb-2">{title}</h1>
          <p className="text-gray-600 dark:text-gray-400">{description}</p>
        </div>

        {/* Profile Section */}
        {showProfile && (
          <div className="p-6 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900">
            <ProfileSection
              user={user}
              showUserId={true}
              userIdFormat="truncated"
            />
            {onSignOut && (
              <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                <button
                  onClick={onSignOut}
                  className="px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                >
                  Sign Out
                </button>
              </div>
            )}
          </div>
        )}

        {/* Subscription Section */}
        {showSubscription && user.subscription_tier && (
          <div className="p-6 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900">
            <SubscriptionSection
              user={user}
              config={subscriptionConfig}
              subscriptionApiEndpoint={apiEndpoints.subscription}
            />
          </div>
        )}

        {/* Payment History Section */}
        {showPaymentHistory && user.id && (
          <div className="p-6 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900">
            <PaymentHistorySection
              userId={user.id}
              apiEndpoint={apiEndpoints.paymentHistory}
            />
          </div>
        )}

        {/* Custom Sections */}
        {customSections.map((section, index) => (
          <div
            key={index}
            className="p-6 border border-gray-200 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-900"
          >
            <h2 className="text-xl font-semibold mb-4">{section.title}</h2>
            {section.content}
          </div>
        ))}
      </div>
    </div>
  );
}

