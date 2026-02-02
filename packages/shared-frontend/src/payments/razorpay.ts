/**
 * Razorpay client for payment and subscription management
 * Shared across KVSHVL platform applications
 * 
 * Note: This shared package uses unprefixed environment variables (RAZORPAY_KEY_ID, etc.)
 * for cross-app compatibility. Individual apps should set prefixed variables
 * (SKETCH2BIM_RAZORPAY_KEY_ID, etc.) in their .env files,
 * but the code checks unprefixed variables first for shared functionality.
 */

import Razorpay from "razorpay";
// Note: Using console methods in shared package since logger is not available

/**
 * Razorpay client instance (lazy initialization)
 */
let razorpayInstance: Razorpay | null = null;

/**
 * Get the Razorpay client instance (lazy initialization)
 * Only creates the client when first called, not during module import
 */
export function getRazorpayClient(): Razorpay {
  if (!razorpayInstance) {
    // Check unprefixed variables first (shared across all apps)
    // Apps can set prefixed variables (SKETCH2BIM_RAZORPAY_KEY_ID, etc.) but
    // this shared package uses unprefixed for compatibility
    const keyId = process.env.RAZORPAY_KEY_ID;
    const keySecret = process.env.RAZORPAY_KEY_SECRET;

    if (!keyId || !keySecret) {
      throw new Error("Razorpay credentials not configured. Please set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET environment variables.");
    }

    razorpayInstance = new Razorpay({
      key_id: keyId,
      key_secret: keySecret,
    });
  }
  return razorpayInstance;
}

/**
 * Verify Razorpay webhook signature
 * @param payload - Raw webhook payload string
 * @param signature - Webhook signature from x-razorpay-signature header
 * @returns true if signature is valid
 */
export function verifyWebhookSignature(payload: string, signature: string): boolean {
  const webhookSecret = process.env.RAZORPAY_WEBHOOK_SECRET;
  
  if (!webhookSecret) {
    console.error("RAZORPAY_WEBHOOK_SECRET not configured");
    return false;
  }

  try {
    const crypto = require("crypto");
    const expectedSignature = crypto
      .createHmac("sha256", webhookSecret)
      .update(payload)
      .digest("hex");

    return expectedSignature === signature;
  } catch (error) {
    console.error("Webhook signature verification failed:", error);
    return false;
  }
}

