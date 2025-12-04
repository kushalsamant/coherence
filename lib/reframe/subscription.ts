/**
 * Subscription utility functions for tier durations and status management.
 * Adapted from sketch2bim backend subscription utilities.
 */

// Subscription tier durations in days
// Unified pricing tiers shared across all apps (ASK, Reframe, Sketch2BIM)
const SUBSCRIPTION_DURATIONS: Record<string, number> = {
  trial: 7,
  daily: 1,   // 1 day pass
  weekly: 7,    // 7-day pass (unified pricing)
  monthly: 30,
  yearly: 365,
};

// Paid subscription tiers
const PAID_TIERS = new Set(["daily", "weekly", "monthly", "yearly"]);

/**
 * Calculate expiry date for a subscription tier
 * @param tier - Subscription tier (trial, daily, week, monthly, yearly)
 * @param referenceDate - Optional reference date (defaults to now)
 * @returns Expiry date as ISO string or null if invalid tier
 */
export function calculateExpiry(tier: string, referenceDate?: Date): string | null {
  const days = SUBSCRIPTION_DURATIONS[tier.toLowerCase()];
  if (!days) {
    return null;
  }

  const start = referenceDate || new Date();
  const expiry = new Date(start);
  expiry.setDate(expiry.getDate() + days);
  
  return expiry.toISOString();
}

/**
 * Check if a tier is a paid tier
 * @param tier - Subscription tier
 * @returns true if tier is paid
 */
export function isPaidTier(tier: string | undefined | null): boolean {
  if (!tier) return false;
  return PAID_TIERS.has(tier.toLowerCase());
}

/**
 * Check if user has an active trial period
 * @param metadata - User metadata with subscription info
 * @returns true if user is in active trial
 */
export function isActiveTrial(metadata: {
  subscription_tier?: string;
  subscription_status?: string;
  subscription_expires_at?: string;
}): boolean {
  if (metadata.subscription_tier !== "trial") {
    return false;
  }
  if (metadata.subscription_status !== "active") {
    return false;
  }
  if (!metadata.subscription_expires_at) {
    return false;
  }
  
  const expiry = new Date(metadata.subscription_expires_at);
  return expiry > new Date();
}

/**
 * Check if user has an active subscription (trial or paid tier)
 * @param metadata - User metadata with subscription info
 * @returns true if user has active subscription
 */
export function hasActiveSubscription(metadata: {
  subscription_tier?: string;
  subscription_status?: string;
  subscription_expires_at?: string;
  subscription_auto_renew?: boolean;
}): boolean {
  // Check if user is in active trial
  if (isActiveTrial(metadata)) {
    return true;
  }

  // Check if user has active paid tier subscription
  if (isPaidTier(metadata.subscription_tier)) {
    if (metadata.subscription_status !== "active") {
      return false;
    }
    if (!metadata.subscription_expires_at) {
      return false;
    }
    
    const expiry = new Date(metadata.subscription_expires_at);
    const isExpired = expiry <= new Date();
    
    // If auto-renew is enabled, consider it active even if slightly expired
    // (webhook will update expiry)
    if (isExpired && metadata.subscription_auto_renew) {
      return true; // Still active, waiting for renewal webhook
    }
    
    return !isExpired;
  }

  return false;
}

/**
 * Ensure subscription status matches expiry date
 * Downgrades to trial if expired (unless auto-renew is active)
 * @param metadata - User metadata
 * @returns Updated metadata
 */
export function ensureSubscriptionStatus(metadata: {
  subscription_tier?: "trial" | "daily" | "weekly" | "monthly" | "yearly";
  subscription_status?: "inactive" | "active" | "cancelled" | "expired";
  subscription_expires_at?: string;
  subscription_auto_renew?: boolean;
  razorpay_subscription_id?: string;
}): typeof metadata {
  // Check if subscription expired
  if (metadata.subscription_expires_at) {
    const expiry = new Date(metadata.subscription_expires_at);
    const now = new Date();
    
    if (expiry < now) {
      // If it's a subscription with auto-renew, don't downgrade yet
      // The webhook will update the expiry date
      if (metadata.subscription_auto_renew && metadata.razorpay_subscription_id) {
        return metadata; // Keep status, webhook will update
      }

      // One-time payment expired or subscription cancelled
      return {
        ...metadata,
        subscription_tier: "trial",
        subscription_status: "expired",
        subscription_expires_at: undefined,
        subscription_auto_renew: false,
        razorpay_subscription_id: undefined,
      };
    }
  }

  return metadata;
}

