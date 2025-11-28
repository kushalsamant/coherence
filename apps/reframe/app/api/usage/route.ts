import { NextResponse } from "next/server";
import { getRedisClient } from "@/lib/redis";
import { auth } from "@/auth";
import { getUserMetadata } from "@/lib/user-metadata";
import { hasActiveSubscription, ensureSubscriptionStatus } from "@/lib/subscription";

const FREE_LIMIT = parseInt(process.env.REFRAME_NEXT_PUBLIC_FREE_LIMIT || process.env.NEXT_PUBLIC_FREE_LIMIT || "5");

export const dynamic = 'force-dynamic';

export async function GET(req: Request) {
  const session = await auth();
  const { searchParams } = new URL(req.url);
  const userId = searchParams.get("userId");

  if (!session?.user?.id || session.user.id !== userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const redis = getRedisClient();
  let metadata = await getUserMetadata(userId);
  
  if (!metadata) {
    return NextResponse.json({ 
      usage: 0,
      subscription_tier: undefined,
      subscription_status: "inactive",
      hasActiveSubscription: false
    });
  }

  // Ensure subscription status is up to date
  metadata = ensureSubscriptionStatus(metadata);

  // Check if user has active subscription
  const hasActiveSub = hasActiveSubscription(metadata);
  const subscriptionTier = metadata.subscription_tier;
  const subscriptionStatus = metadata.subscription_status;

  // Get usage based on subscription type
  let usage = 0;
  let usageKey = "";

  if (hasActiveSub) {
    // User has active subscription (trial or paid) - unlimited access
    usage = 0; // Not applicable for subscription users
  } else {
    // Free user after trial expired - get lifetime usage count
    usageKey = `usage:${userId}:total`;
    usage = parseInt((await redis.get(usageKey)) || "0", 10);
  }

  return NextResponse.json({ 
    usage,
    subscription_tier: subscriptionTier,
    subscription_status: subscriptionStatus,
    subscription_expires_at: metadata.subscription_expires_at,
    hasActiveSubscription: hasActiveSub,
    free_limit: FREE_LIMIT,
    // Legacy fields for backward compatibility
    subscription: subscriptionTier === "trial" ? undefined : subscriptionTier,
  });
}
