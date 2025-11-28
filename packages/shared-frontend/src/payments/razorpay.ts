/**
 * Razorpay client for payment and subscription management
 * Shared across KVSHVL platform applications
 */

import Razorpay from "razorpay";

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

