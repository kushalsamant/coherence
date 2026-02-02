import { NextResponse } from "next/server";
import { logger } from "@/lib/logger";
import { API_CONFIG } from "@/lib/config";

export const runtime = "nodejs";
export const dynamic = 'force-dynamic';

export async function POST(req: Request) {
  const body = await req.text();
  const signature = req.headers.get("x-razorpay-signature");

  if (!signature) {
    return new NextResponse("Missing signature", { status: 400 });
  }

  // Forward webhook to backend API for processing
  // The backend handles signature verification and database updates
  try {
    const API_URL = API_CONFIG.PLATFORM_API_URL;
    const response = await fetch(`${API_URL}/api/subscriptions/webhook`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-razorpay-signature': signature,
      },
      body: body,
    });

    if (!response.ok) {
      logger.error(`Backend webhook handler returned ${response.status}`);
      return new NextResponse("Webhook processing failed", { status: response.status });
    }

    return new NextResponse("OK", { status: 200 });
  } catch (err: any) {
    logger.error(`Error forwarding webhook to backend:`, err);
    return new NextResponse(`Webhook handler error: ${err.message}`, { status: 500 });
  }
}
