import { NextResponse } from "next/server";
import { getRazorpayClient } from "@/lib/reframe/razorpay";
import { auth } from "@/app/reframe/auth";
import { getUserMetadata, setUserMetadata } from "@/lib/reframe/user-metadata";

export const dynamic = 'force-dynamic';

/**
 * Resume a paused/cancelled subscription
 */
export async function POST(req: Request) {
  const session = await auth();
  
  if (!session?.user?.id) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const metadata = await getUserMetadata(session.user.id);
  
  if (!metadata?.razorpay_subscription_id) {
    return NextResponse.json({ error: "No subscription found" }, { status: 404 });
  }

  const razorpay = getRazorpayClient();
  const subscriptionId = metadata.razorpay_subscription_id;

  try {
    // Resume subscription
    await razorpay.subscriptions.resume(subscriptionId, {
      resume_at: "now",
    });

    // Update metadata
    metadata.subscription_auto_renew = true;
    metadata.subscription_status = "active";
    await setUserMetadata(session.user.id, metadata);

    return NextResponse.json({
      status: "success",
      message: "Subscription resumed successfully",
    });
  } catch (error: any) {
    console.error("Failed to resume subscription:", error);
    return NextResponse.json(
      { error: "Failed to resume subscription", details: error.message },
      { status: 500 }
    );
  }
}

