import { getRedisClient } from "./redis";
import logger from "@/lib/logger";

/**
 * Consent Tracking System
 * Handles user acceptance of Terms of Service and Privacy Policy
 * Compliant with GDPR/CCPA requirements
 */

const redis = getRedisClient();

export interface ConsentRecord {
  acceptedAt: string; // ISO timestamp
  termsVersion: string; // e.g., "1.0"
  privacyVersion: string; // e.g., "1.0"
  ipAddress?: string; // Optional for audit trail
  userAgent?: string; // Optional for audit trail
}

// Current versions of legal documents
export const CURRENT_TERMS_VERSION = "1.0";
export const CURRENT_PRIVACY_VERSION = "1.0";

/**
 * Record user consent in Redis
 * @param userId - User ID
 * @param termsVersion - Version of Terms accepted
 * @param privacyVersion - Version of Privacy Policy accepted
 * @param ipAddress - Optional IP address for audit
 * @param userAgent - Optional user agent for audit
 */
export async function recordConsent(
  userId: string,
  termsVersion: string = CURRENT_TERMS_VERSION,
  privacyVersion: string = CURRENT_PRIVACY_VERSION,
  ipAddress?: string,
  userAgent?: string
): Promise<void> {
  const key = `consent:${userId}`;
  
  const consentRecord: ConsentRecord = {
    acceptedAt: new Date().toISOString(),
    termsVersion,
    privacyVersion,
    ...(ipAddress && { ipAddress }),
    ...(userAgent && { userAgent }),
  };

  await redis.set(key, JSON.stringify(consentRecord));
}

/**
 * Get consent record for a user
 * @param userId - User ID
 * @returns Consent record or null if not found
 */
export async function getConsent(userId: string): Promise<ConsentRecord | null> {
  const key = `consent:${userId}`;
  const data = await redis.get(key);

  if (!data) {
    return null;
  }

  // Parse if it's a string, otherwise return as-is
  if (typeof data === "string") {
    try {
      return JSON.parse(data);
    } catch (e) {
      logger.error("Failed to parse consent record:", e);
      return null;
    }
  }

  return data as ConsentRecord;
}


