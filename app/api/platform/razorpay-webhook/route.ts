import { NextResponse } from "next/server";
import { verifyWebhookSignature } from "@/lib/reframe/razorpay";
import { getUserMetadata, setUserMetadata, updateSubscription, removeSubscription } from "@/lib/reframe/user-metadata";
import { calculateExpiry, ensureSubscriptionStatus } from "@/lib/reframe/subscription";
import {
  getRazorpayWeeklyAmount,
  getRazorpayMonthlyAmount,
  getRazorpayYearlyAmount,
  getRazorpayPlanWeekly,
  getRazorpayPlanMonthly,
  getRazorpayPlanYearly,
} from "@/lib/reframe/app-config";
import { logger } from "@/lib/logger";

export const runtime = "nodejs";
export const dynamic = 'force-dynamic';

// Map Razorpay amounts to tiers (in paise, ₹1 = 100 paise)
// Unified pricing shared across all apps (ASK, Reframe, Sketch2BIM)
const AMOUNT_TO_TIER: Record<number, "weekly" | "monthly" | "yearly"> = {
  [getRazorpayWeeklyAmount()]: "weekly",  // ₹1,299 = 129900 paise
  [getRazorpayMonthlyAmount()]: "monthly",  // ₹3,499 = 349900 paise
  [getRazorpayYearlyAmount()]: "yearly",  // ₹29,999 = 2999900 paise
};

// Map Razorpay plan IDs to tiers (shared plan IDs across all apps)
const PLAN_TO_TIER: Record<string, "weekly" | "monthly" | "yearly"> = {
  [getRazorpayPlanWeekly()]: "weekly",
  [getRazorpayPlanMonthly()]: "monthly",
  [getRazorpayPlanYearly()]: "yearly",
};

export async function POST(req: Request) {
  const body = await req.text();
  const signature = req.headers.get("x-razorpay-signature");

  if (!signature) {
    return new NextResponse("Missing signature", { status: 400 });
  }

  // Verify webhook signature
  if (!verifyWebhookSignature(body, signature)) {
    logger.error("Platform Razorpay webhook signature verification failed");
    return new NextResponse("Invalid signature", { status: 400 });
  }

  try {
    const event = JSON.parse(body);
    const eventType = event.event;

    switch (eventType) {
      case "payment.captured":
        // Handle one-time payment (subscription purchase)
        const payment = event.payload.payment.entity;
        const orderId = payment.order_id;
        const amount = payment.amount; // in paise
        const notes = payment.notes || {};
        const userId = notes.user_id as string;
        const paymentType = notes.type; // "one_time" or "subscription"
        const tier = notes.tier as string;

        if (!userId) {
          logger.error("Missing user_id in payment notes");
          break;
        }

        // Track payment processing fee (2% of amount)
        const processingFee = Math.floor(amount * 0.02); // 2% fee in paise
        const { getRedisClient } = await import("@/lib/reframe/redis");
        const redis = getRedisClient();
        const now = new Date();
        const dateKey = now.toISOString().split('T')[0]; // YYYY-MM-DD
        const monthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`; // YYYY-MM
        
        // Track daily payment metrics in Redis
        // Keys: payment:fees:daily:{YYYY-MM-DD}, payment:revenue:daily:{YYYY-MM-DD}, payment:count:daily:{YYYY-MM-DD}
        // Data retention: 30 days for daily keys, 90 days for monthly keys
        await redis.incrby(`payment:fees:daily:${dateKey}`, processingFee);
        await redis.incrby(`payment:revenue:daily:${dateKey}`, amount);
        await redis.incr(`payment:count:daily:${dateKey}`); // Increment payment count
        await redis.expire(`payment:fees:daily:${dateKey}`, 30 * 24 * 60 * 60); // 30 days
        await redis.expire(`payment:revenue:daily:${dateKey}`, 30 * 24 * 60 * 60); // 30 days
        await redis.expire(`payment:count:daily:${dateKey}`, 30 * 24 * 60 * 60); // 30 days
        
        // Track monthly payment metrics
        await redis.incrby(`payment:fees:monthly:${monthKey}`, processingFee);
        await redis.incrby(`payment:revenue:monthly:${monthKey}`, amount);
        await redis.incr(`payment:count:monthly:${monthKey}`); // Increment payment count
        await redis.expire(`payment:fees:monthly:${monthKey}`, 90 * 24 * 60 * 60); // 90 days
        await redis.expire(`payment:revenue:monthly:${monthKey}`, 90 * 24 * 60 * 60); // 90 days
        await redis.expire(`payment:count:monthly:${monthKey}`, 90 * 24 * 60 * 60); // 90 days

        if (paymentType === "one_time") {
          // One-time subscription purchase
          const subscriptionTier = tier || AMOUNT_TO_TIER[amount];
          if (subscriptionTier && ["weekly", "monthly", "yearly"].includes(subscriptionTier)) {
            const expiry = calculateExpiry(subscriptionTier);
            if (expiry) {
              await updateSubscription(
                userId,
                subscriptionTier as "weekly" | "monthly" | "yearly",
                expiry,
                false // one-time payment, no auto-renew
              );
              logger.info(`User ${userId} purchased ${subscriptionTier} subscription (one-time)`);
            }
          }
        }
        break;

      case "subscription.created":
        // Subscription was created (user will be charged on activation)
        const createdSub = event.payload.subscription.entity;
        const createdNotes = createdSub.notes || {};
        const createdUserId = createdNotes.user_id as string;
        const customerId = createdSub.customer_id;

        if (createdUserId) {
          const metadata = await getUserMetadata(createdUserId);
          if (metadata) {
            metadata.razorpay_subscription_id = createdSub.id;
            if (customerId) {
              metadata.razorpay_customer_id = customerId;
            }
            metadata.subscription_auto_renew = true;
            await setUserMetadata(createdUserId, metadata);
          }
        }
        break;

      case "subscription.activated":
        // Subscription activated (first payment successful)
        const activatedSub = event.payload.subscription.entity;
        const activatedNotes = activatedSub.notes || {};
        const activatedUserId = activatedNotes.user_id as string;
        const planId = activatedSub.plan_id;
        const currentEnd = activatedSub.current_end;

        if (activatedUserId) {
          const subscriptionTier = PLAN_TO_TIER[planId] || "monthly";
          const expiry = currentEnd 
            ? new Date(currentEnd * 1000).toISOString() 
            : calculateExpiry(subscriptionTier);

          if (expiry) {
            await updateSubscription(
              activatedUserId,
              subscriptionTier as "weekly" | "monthly" | "yearly",
              expiry,
              true, // auto-renew enabled
              activatedSub.id,
              activatedSub.customer_id
            );
            logger.info(`User ${activatedUserId} subscription activated: ${subscriptionTier}`);
          }
        }
        break;

      case "subscription.charged":
        // Subscription renewal payment charged
        const chargedSub = event.payload.subscription.entity;
        const chargedNotes = chargedSub.notes || {};
        const chargedUserId = chargedNotes.user_id as string;
        const currentEndCharged = chargedSub.current_end;
        const chargedAmount = chargedSub.amount || 0; // in paise

        // Track payment processing fee for subscription renewal
        if (chargedAmount > 0) {
          const processingFee = Math.floor(chargedAmount * 0.02); // 2% fee in paise
          const { getRedisClient } = await import("@/lib/reframe/redis");
          const redis = getRedisClient();
          const now = new Date();
          const dateKey = now.toISOString().split('T')[0];
          const monthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
          
          // Track daily payment metrics (same structure as payment.captured)
          await redis.incrby(`payment:fees:daily:${dateKey}`, processingFee);
          await redis.incrby(`payment:revenue:daily:${dateKey}`, chargedAmount);
          await redis.incr(`payment:count:daily:${dateKey}`); // Increment payment count
          await redis.expire(`payment:fees:daily:${dateKey}`, 30 * 24 * 60 * 60);
          await redis.expire(`payment:revenue:daily:${dateKey}`, 30 * 24 * 60 * 60);
          await redis.expire(`payment:count:daily:${dateKey}`, 30 * 24 * 60 * 60);
          
          // Track monthly payment metrics
          await redis.incrby(`payment:fees:monthly:${monthKey}`, processingFee);
          await redis.incrby(`payment:revenue:monthly:${monthKey}`, chargedAmount);
          await redis.incr(`payment:count:monthly:${monthKey}`); // Increment payment count
          await redis.expire(`payment:fees:monthly:${monthKey}`, 90 * 24 * 60 * 60);
          await redis.expire(`payment:revenue:monthly:${monthKey}`, 90 * 24 * 60 * 60);
          await redis.expire(`payment:count:monthly:${monthKey}`, 90 * 24 * 60 * 60);
        }

        if (chargedUserId && currentEndCharged) {
          const metadata = await getUserMetadata(chargedUserId);
          if (metadata) {
            metadata.subscription_expires_at = new Date(currentEndCharged * 1000).toISOString();
            metadata.subscription_status = "active";
            await setUserMetadata(chargedUserId, metadata);
            logger.info(`User ${chargedUserId} subscription renewed until ${metadata.subscription_expires_at}`);
          }
        }
        break;

      case "subscription.cancelled":
      case "subscription.paused":
        // Subscription cancelled or paused
        const cancelledSub = event.payload.subscription.entity;
        const cancelledNotes = cancelledSub.notes || {};
        const cancelledUserId = cancelledNotes.user_id as string;

        if (cancelledUserId) {
          const metadata = await getUserMetadata(cancelledUserId);
          if (metadata) {
            // Don't remove subscription immediately - let them use until period ends
            metadata.subscription_auto_renew = false;
            metadata.subscription_status = "cancelled";
            // Keep subscription_expires_at as is - they paid for the period
            await setUserMetadata(cancelledUserId, metadata);
            logger.info(`User ${cancelledUserId} subscription cancelled (will expire at ${metadata.subscription_expires_at})`);
          }
        }
        break;

      default:
        logger.info(`Unhandled Razorpay event type: ${eventType}`);
    }
  } catch (err: any) {
    logger.error(`Error processing Razorpay webhook:`, err);
    return new NextResponse(`Webhook handler error: ${err.message}`, { status: 500 });
  }

  return new NextResponse("OK", { status: 200 });
}

