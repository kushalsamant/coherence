import { NextResponse } from "next/server";
import { auth } from "@/auth";
import { getUserMetadata } from "@/lib/user-metadata";
import { getConsent } from "@/lib/consent";
import { getRedisClient } from "@/lib/redis";
// Razorpay payment data - handled via webhook, stored in user metadata

export const dynamic = 'force-dynamic';

/**
 * GET /api/account/export
 * Export all user data in JSON format (GDPR Right to Access)
 */
export async function GET() {
  const session = await auth();
  const redis = getRedisClient();

  if (!session?.user?.id || !session?.user?.email) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const userId = session.user.id;

  try {
    // 1. Fetch user metadata from Redis
    const metadata = await getUserMetadata(userId);

    // 2. Fetch consent record
    const consent = await getConsent(userId);

    // 3. Fetch usage data from Redis (free tier lifetime counter)
    const usageTotal = await redis.get(`usage:${userId}:total`);

    // 4. Payment data stored in user metadata (Razorpay)
    // Payment history is tracked via webhooks and stored in Redis/user metadata
    const paymentData = metadata?.razorpay_subscription_id || metadata?.razorpay_customer_id || null;

    // Compile export data
    const exportData = {
      exportDate: new Date().toISOString(),
      exportVersion: "2.0",
      account: {
        id: userId,
        email: session.user.email,
        name: session.user.name || null,
        image: session.user.image || null,
      },
      subscription: {
        tier: metadata?.subscription_tier || metadata?.subscription || "free",
        status: metadata?.subscription_status || "inactive",
        expiresAt: metadata?.subscription_expires_at || null,
        autoRenew: metadata?.subscription_auto_renew || false,
        razorpaySubscriptionId: metadata?.razorpay_subscription_id || null,
        razorpayCustomerId: metadata?.razorpay_customer_id || null,
      },
      usage: {
        freeTierUsage: parseInt(usageTotal || "0", 10),
      },
      consent: consent
        ? {
            acceptedAt: consent.acceptedAt,
            termsVersion: consent.termsVersion,
            privacyVersion: consent.privacyVersion,
            ipAddress: consent.ipAddress || null,
          }
        : null,
      payments: paymentData ? {
        razorpaySubscriptionId: metadata?.razorpay_subscription_id,
        razorpayCustomerId: metadata?.razorpay_customer_id,
      } : null,
    };

    return NextResponse.json(exportData);
  } catch (error: any) {
    console.error("Error exporting user data:", error);
    return NextResponse.json(
      { error: "Failed to export data" },
      { status: 500 }
    );
  }
}

