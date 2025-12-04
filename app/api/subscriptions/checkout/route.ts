import { NextRequest, NextResponse } from 'next/server';
import { authFunction as auth } from '@/app/ask/auth'; // Using ASK auth as default - will be unified later
import { logger } from '@/lib/logger';

// Unified subscription checkout endpoint
// This replaces app-specific checkout endpoints
export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    // Get session to verify authentication
    const session = await auth();
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await req.json();
    const { tier } = body;

    if (!tier || !['week', 'monthly', 'yearly'].includes(tier)) {
      return NextResponse.json({ error: 'Invalid tier' }, { status: 400 });
    }

    // TODO: Call unified backend API to create checkout session
    // This will be implemented when backend is consolidated
    // For now, return structure
    const API_URL = process.env.NEXT_PUBLIC_PLATFORM_API_URL || 'http://localhost:8000';
    
    const response = await fetch(`${API_URL}/api/subscriptions/checkout`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: session.user.id,
        tier,
      }),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to create checkout session' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    logger.error('Checkout error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

