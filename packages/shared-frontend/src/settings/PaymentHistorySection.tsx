/**
 * Payment History Section Component
 * Displays user payment history
 */
"use client";

import React, { useState, useEffect } from "react";
import type { PaymentHistoryItem } from "./types";

export interface PaymentHistorySectionProps {
  /** User ID */
  userId: string;
  /** API endpoint to fetch payment history */
  apiEndpoint?: string;
  /** Custom styling className */
  className?: string;
  /** Maximum items to display */
  maxItems?: number;
  /** Callback to format product type display */
  formatProductType?: (type: string) => string;
  /** Callback to format amount display */
  formatAmount?: (amount: number, currency: string) => string;
}

export function PaymentHistorySection({
  userId,
  apiEndpoint = "/api/payments/history",
  className = "",
  maxItems = 10,
  formatProductType,
  formatAmount,
}: PaymentHistorySectionProps) {
  const [payments, setPayments] = useState<PaymentHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPayments = async () => {
      try {
        const response = await fetch(`${apiEndpoint}?user_id=${userId}`);
        if (!response.ok) {
          throw new Error("Failed to fetch payment history");
        }
        const data = await response.json();
        setPayments(Array.isArray(data) ? data.slice(0, maxItems) : []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load payment history");
      } finally {
        setLoading(false);
      }
    };

    if (userId) {
      fetchPayments();
    }
  }, [userId, apiEndpoint, maxItems]);

  const getProductTypeLabel = (type: string) => {
    if (formatProductType) return formatProductType(type);
    switch (type) {
      case "week":
        return "Week Access";
      case "monthly":
        return "Monthly Subscription";
      case "yearly":
        return "Yearly Subscription";
      case "one_time":
        return "One-time Payment";
      default:
        return type;
    }
  };

  const getAmountDisplay = (amount: number, currency: string) => {
    if (formatAmount) return formatAmount(amount, currency);
    // Amount is typically in paise (₹1 = 100 paise)
    const inrAmount = amount / 100;
    return `₹${inrAmount.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "succeeded":
      case "success":
        return "text-green-600 dark:text-green-400";
      case "pending":
        return "text-yellow-600 dark:text-yellow-400";
      case "failed":
        return "text-red-600 dark:text-red-400";
      default:
        return "text-gray-600 dark:text-gray-400";
    }
  };

  if (loading) {
    return (
      <div className={className}>
        <h2 className="text-xl font-semibold mb-4">Payment History</h2>
        <div className="text-gray-600 dark:text-gray-400">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={className}>
        <h2 className="text-xl font-semibold mb-4">Payment History</h2>
        <div className="text-red-600 dark:text-red-400">{error}</div>
      </div>
    );
  }

  if (payments.length === 0) {
    return (
      <div className={className}>
        <h2 className="text-xl font-semibold mb-4">Payment History</h2>
        <div className="text-gray-600 dark:text-gray-400">No payment history available.</div>
      </div>
    );
  }

  return (
    <div className={className}>
      <h2 className="text-xl font-semibold mb-4">Payment History</h2>
      <div className="space-y-3">
        {payments.map((payment) => (
          <div
            key={payment.id}
            className="p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
          >
            <div className="flex justify-between items-start mb-2">
              <div>
                <div className="font-medium text-gray-900 dark:text-gray-100">
                  {getProductTypeLabel(payment.product_type)}
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">
                  {new Date(payment.created_at).toLocaleDateString()}
                </div>
              </div>
              <div className="text-right">
                <div className="font-medium text-gray-900 dark:text-gray-100">
                  {getAmountDisplay(payment.amount, payment.currency)}
                </div>
                <div className={`text-sm ${getStatusColor(payment.status)}`}>
                  {payment.status.charAt(0).toUpperCase() + payment.status.slice(1)}
                </div>
              </div>
            </div>
            {payment.razorpay_payment_id && (
              <div className="text-xs text-gray-500 dark:text-gray-400 font-mono mt-2">
                Payment ID: {payment.razorpay_payment_id.slice(0, 20)}...
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

