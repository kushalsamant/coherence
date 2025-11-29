import { NextResponse } from "next/server";
import { getRazorpayClient } from "@/lib/razorpay";
import { auth } from "@/auth";
import { getUserMetadata, initializeUserTrial } from "@/lib/user-metadata";
import {
  getRazorpayWeekAmount,
  getRazorpayMonthlyAmount,
  getRazorpayYearlyAmount,
  getRazorpayPlanWeek,
  getRazorpayPlanMonthly,
  getRazorpayPlanYearly,
} from "@/lib/app-config";

export const dynamic = 'force-dynamic';

/**
 * Create Razorpay order or subscription for checkout
 * 
 * @param price_id - Tier name ('monthly', 'yearly')
 * @param payment_type - 'one_time' for one-time payment, 'subscription' for recurring
 */
export async function GET(req: Request) {
  try {
    const session = await auth();
    if (!session?.user?.id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Validate Razorpay configuration
    const razorpayKeyId = process.env.REFRAME_RAZORPAY_KEY_ID || process.env.RAZORPAY_KEY_ID;
    const razorpayKeySecret = process.env.REFRAME_RAZORPAY_KEY_SECRET || process.env.RAZORPAY_KEY_SECRET;
    if (!razorpayKeyId || !razorpayKeySecret) {
      console.error("❌ Razorpay credentials not configured");
      return NextResponse.json(
        { error: "Razorpay is not configured. Please check environment variables." },
        { status: 500 }
      );
    }

    const razorpay = getRazorpayClient();
    const userId = session.user.id;

    if (!session.user?.email) {
      return NextResponse.json({ error: "No email" }, { status: 400 });
    }

    const { searchParams } = new URL(req.url);
    const priceId = searchParams.get("price_id") || searchParams.get("plan") || "monthly";
    const paymentType = (searchParams.get("payment_type") || "one_time") as "one_time" | "subscription";
    
    const tierKey = priceId.toLowerCase();
    
    // Validate tier is supported
    const supportedTiers = ["week", "monthly", "yearly"];
    if (!supportedTiers.includes(tierKey)) {
      return NextResponse.json(
        { error: `Invalid tier. Supported tiers: ${supportedTiers.join(", ")}` },
        { status: 400 }
      );
    }
    const baseUrl = process.env.REFRAME_AUTH_URL || process.env.AUTH_URL || process.env.REFRAME_NEXT_PUBLIC_SITE_URL || process.env.NEXT_PUBLIC_SITE_URL || "http://localhost:3000";
    const successUrl = `${baseUrl}/?checkout=success`;
    const cancelUrl = `${baseUrl}/pricing?checkout=canceled`;

    // Initialize user with trial if they don't have metadata yet
    const existingMetadata = await getUserMetadata(userId);
    if (!existingMetadata) {
      await initializeUserTrial(userId, session.user.email);
    }

    if (paymentType === "subscription") {
      // Create subscription using Plan ID
      const planMap: Record<string, string> = {
        week: getRazorpayPlanWeek(),
        monthly: getRazorpayPlanMonthly(),
        yearly: getRazorpayPlanYearly(),
      };

      const planId = planMap[tierKey];
      if (!planId) {
        return NextResponse.json(
          {
            error: `Plan not configured for tier: ${tierKey}. Please create Razorpay plans first.`,
          },
          { status: 400 }
        );
      }

      // Get or create Razorpay customer
      let customerId = existingMetadata?.razorpay_customer_id;
      if (!customerId) {
        try {
          const customer = await razorpay.customers.create({
            name: session.user.name || session.user.email.split("@")[0],
            email: session.user.email,
            contact: null,
          });
          customerId = customer.id;
          
          // Save customer ID to metadata
          const metadata = await getUserMetadata(userId);
          if (metadata) {
            metadata.razorpay_customer_id = customerId;
            await import("@/lib/user-metadata").then(m => m.setUserMetadata(userId, metadata));
          }
        } catch (error: any) {
          console.error("Failed to create Razorpay customer:", error);
          return NextResponse.json(
            { error: "Failed to create customer", details: error.message },
            { status: 500 }
          );
        }
      }

      // Create subscription
      try {
        const subscriptionData = {
          plan_id: planId,
          customer_notify: 1,
          total_count: 0, // 0 = infinite recurring
          notes: {
            user_id: userId,
            user_email: session.user.email,
            tier: tierKey,
          },
        };

        const subscription = await razorpay.subscriptions.create(subscriptionData);

        return NextResponse.json({
          subscription_id: subscription.id,
          plan_id: planId,
          amount: subscription.plan.amount,
          currency: subscription.plan.currency,
          key_id: process.env.RAZORPAY_KEY_ID,
          name: "Reframe",
          description: `${tierKey.charAt(0).toUpperCase() + tierKey.slice(1)} subscription (auto-renews)`,
          prefill: {
            email: session.user.email,
            name: session.user.name || session.user.email.split("@")[0],
          },
          theme: {
            color: "#6366f1",
          },
          success_url: successUrl,
          cancel_url: cancelUrl,
          payment_type: "subscription",
        });
      } catch (error: any) {
        console.error("❌ Razorpay subscription creation failed:", error);
        return NextResponse.json(
          { error: "Failed to create subscription", details: error.message },
          { status: 500 }
        );
      }
    } else {
      // Create one-time order
      const tierMap: Record<string, number> = {
        week: getRazorpayWeekAmount(),
        monthly: getRazorpayMonthlyAmount(),
        yearly: getRazorpayYearlyAmount(),
      };

      const amount = tierMap[tierKey];
      if (!amount) {
        return NextResponse.json(
          {
            error: `Invalid tier. Expected one of ${Object.keys(tierMap).join(", ")}, got: ${priceId}`,
          },
          { status: 400 }
        );
      }

      try {
        const order = await razorpay.orders.create({
          amount: amount, // in paise
          currency: "INR",
          receipt: `order_${userId}_${Date.now()}`,
          notes: {
            user_id: userId,
            user_email: session.user.email,
            tier: tierKey,
            payment_type: "one_time",
          },
        });

        return NextResponse.json({
          order_id: order.id,
          amount: order.amount,
          currency: order.currency,
          key_id: process.env.RAZORPAY_KEY_ID,
          name: "Reframe",
          description: `${tierKey.charAt(0).toUpperCase() + tierKey.slice(1)} access (one-time)`,
          prefill: {
            email: session.user.email,
            name: session.user.name || session.user.email.split("@")[0],
          },
          theme: {
            color: "#6366f1",
          },
          success_url: successUrl,
          cancel_url: cancelUrl,
          payment_type: "one_time",
        });
      } catch (error: any) {
        console.error("❌ Razorpay order creation failed:", error);
        return NextResponse.json(
          { error: "Failed to create checkout session", details: error.message },
          { status: 500 }
        );
      }
    }
  } catch (error: any) {
    console.error("❌ Unexpected error in checkout:", error);
    return NextResponse.json(
      { error: "An unexpected error occurred", details: error.message },
      { status: 500 }
    );
  }
}

