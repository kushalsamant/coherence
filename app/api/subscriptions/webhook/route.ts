import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';
import { API_CONFIG } from "@/lib/config";

export const dynamic = 'force-dynamic';
export const runtime = 'nodejs';

export async function POST(req: NextRequest) {
  try {
    const body = await req.text();
    const signature = req.headers.get('x-razorpay-signature');

    if (!signature) {
      return NextResponse.json(
        { error: 'Missing signature' },
        { status: 400 }
      );
    }

    const API_URL = API_CONFIG.PLATFORM_API_URL;
    
    // Forward webhook to unified backend
    const response = await fetch(`${API_URL}/api/subscriptions/webhook`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Razorpay-Signature': signature,
      },
      body,
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Webhook processing failed' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    logger.error('Webhook error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

