import { NextResponse } from "next/server";
import { getRazorpayClient } from "@/lib/reframe/razorpay";
import { authFunction as auth } from "@/app/reframe/auth";
import { getUserMetadata, setUserMetadata } from "@/lib/reframe/user-metadata";
import { logger } from "@/lib/logger";

export const dynamic = 'force-dynamic';

/**
 * Cancel a subscription
 * Cancels at the end of the current billing cycle
 */
export async function POST(req: Request) {
  const session = await auth();
  
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const metadata = await getUserMetadata(session.user.id);
  
  if (!metadata?.razorpay_subscription_id) {
    return NextResponse.json({ error: "No active subscription found" }, { status: 404 });
  }

  const razorpay = getRazorpayClient();
  const subscriptionId = metadata.razorpay_subscription_id;

  try {
    // Cancel subscription at period end
    await razorpay.subscriptions.cancel(subscriptionId, true);

    // Update metadata - keep subscription until period ends
    metadata.subscription_auto_renew = false;
    metadata.subscription_status = "cancelled";
    await setUserMetadata(session.user.id, metadata);

    return NextResponse.json({
      status: "success",
      message: "Subscription will be cancelled at the end of the billing cycle",
    });
  } catch (error: any) {
    logger.error("Failed to cancel subscription:", error);
    return NextResponse.json(
      { error: "Failed to cancel subscription", details: error.message },
      { status: 500 }
    );
  }
}
