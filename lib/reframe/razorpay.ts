/**
 * Razorpay client for payment and subscription management
 * Reframe-specific implementation
 */

import Razorpay from "razorpay";
import { logger } from '@/lib/logger';

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
    // Check prefixed variables first (app-specific), then unprefixed (shared)
    const keyId = process.env.REFRAME_RAZORPAY_KEY_ID || process.env.RAZORPAY_KEY_ID;
    const keySecret = process.env.REFRAME_RAZORPAY_KEY_SECRET || process.env.RAZORPAY_KEY_SECRET;

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
  const webhookSecret = process.env.REFRAME_RAZORPAY_WEBHOOK_SECRET || process.env.RAZORPAY_WEBHOOK_SECRET;
  
  if (!webhookSecret) {
    logger.error("RAZORPAY_WEBHOOK_SECRET not configured");
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
    logger.error("Webhook signature verification failed:", error);
    return false;
  }
}

