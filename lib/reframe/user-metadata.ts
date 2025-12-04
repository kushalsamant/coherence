import { getRedisClient } from "./redis";
import logger from "@/lib/logger";

/**
 * User Metadata Management Utilities
 * Handles user subscription and metadata storage in Redis
 */

const redis = getRedisClient();

export type UserMetadata = {
  subscription_tier?: "trial" | "daily" | "weekly" | "monthly" | "yearly";
  subscription_status?: "inactive" | "active" | "cancelled" | "expired";
  subscription_expires_at?: string; // ISO timestamp
  subscription_auto_renew?: boolean; // True for recurring subscriptions
  razorpay_subscription_id?: string; // Active Razorpay subscription ID
  razorpay_customer_id?: string; // Razorpay customer ID
  email?: string;
  // Legacy field - kept for backward compatibility, use subscription_tier instead
  subscription?: "daily" | "monthly" | "yearly";
  subscriptionStartDate?: string;
};

/**
 * Get user metadata from Redis
 * @param userId - User ID
 * @returns User metadata object or null if not found
 */
export async function getUserMetadata(userId: string): Promise<UserMetadata | null> {
  const key = `user:metadata:${userId}`;
  const data = await redis.get(key);
  
  if (!data) {
    return null;
  }
  
  // Parse if it's a string, otherwise return as-is
  if (typeof data === "string") {
    try {
      return JSON.parse(data);
    } catch (e) {
      logger.error("Failed to parse user metadata:", e);
      return null;
    }
  }
  
  return data as UserMetadata;
}

/**
 * Set complete user metadata in Redis
 * @param userId - User ID
 * @param metadata - Complete metadata object
 */
export async function setUserMetadata(userId: string, metadata: UserMetadata): Promise<void> {
  const key = `user:metadata:${userId}`;
  await redis.set(key, JSON.stringify(metadata));
}

/**
 * Initialize user with trial subscription (7 days)
 * @param userId - User ID
 * @param email - User email
 */
export async function initializeUserTrial(userId: string, email?: string): Promise<void> {
  const key = `user:metadata:${userId}`;
  const now = new Date();
  const trialExpiry = new Date(now);
  trialExpiry.setDate(trialExpiry.getDate() + 7); // 7 days trial
  
  const metadata: UserMetadata = {
    subscription_tier: "trial",
    subscription_status: "active",
    subscription_expires_at: trialExpiry.toISOString(),
    subscription_auto_renew: false,
    email: email,
  };
  
  await redis.set(key, JSON.stringify(metadata));
}

/**
 * Update user subscription information
 * @param userId - User ID
 * @param tier - Subscription tier
 * @param expiresAt - Expiry date (ISO string)
 * @param autoRenew - Whether subscription auto-renews
 * @param razorpaySubscriptionId - Razorpay subscription ID (optional)
 * @param razorpayCustomerId - Razorpay customer ID (optional)
 */
export async function updateSubscription(
  userId: string,
  tier: "daily" | "weekly" | "monthly" | "yearly",
  expiresAt: string,
  autoRenew: boolean = false,
  razorpaySubscriptionId?: string,
  razorpayCustomerId?: string
): Promise<void> {
  const key = `user:metadata:${userId}`;
  const existingMetadata = await getUserMetadata(userId) || {};
  
  const updatedMetadata: UserMetadata = {
    ...existingMetadata,
    subscription_tier: tier,
    subscription_status: "active",
    subscription_expires_at: expiresAt,
    subscription_auto_renew: autoRenew,
    ...(razorpaySubscriptionId && { razorpay_subscription_id: razorpaySubscriptionId }),
    ...(razorpayCustomerId && { razorpay_customer_id: razorpayCustomerId }),
    // Legacy compatibility
    subscription: tier === "weekly" ? "daily" : tier,
    subscriptionStartDate: expiresAt,
  };
  
  await redis.set(key, JSON.stringify(updatedMetadata));
}

/**
 * Remove subscription from user (downgrade to expired)
 * @param userId - User ID
 */
export async function removeSubscription(userId: string): Promise<void> {
  const key = `user:metadata:${userId}`;
  const existingMetadata = await getUserMetadata(userId) || {};
  
  const updatedMetadata: UserMetadata = {
    ...existingMetadata,
    subscription_tier: "trial",
    subscription_status: "expired",
    subscription_expires_at: undefined,
    subscription_auto_renew: false,
    razorpay_subscription_id: undefined,
    // Legacy compatibility
    subscription: undefined,
    subscriptionStartDate: undefined,
  };
  
  await redis.set(key, JSON.stringify(updatedMetadata));
}

/**
 * Delete all user data from Redis
 * Used during account deletion
 * @param userId - User ID
 */
export async function deleteAllUserData(userId: string): Promise<void> {
  // Delete all user-specific Redis keys
  await redis.del(`user:metadata:${userId}`);
  await redis.del(`consent:${userId}`);
  await redis.del(`usage:${userId}:total`); // Free tier lifetime counter
  
  logger.info(`Deleted all Redis data for user ${userId}`);
}

