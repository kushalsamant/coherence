import { NextRequest, NextResponse } from 'next/server';
import { authFunction as auth } from '@/app/ask/auth';
import { logger } from '@/lib/logger';

export const dynamic = 'force-dynamic';

export async function GET(req: NextRequest) {
  try {
    const session = await auth();
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const API_URL = process.env.NEXT_PUBLIC_PLATFORM_API_URL || 'http://localhost:8000';
    
    const response = await fetch(`${API_URL}/api/subscriptions/status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.user.id}`, // Will need proper JWT token
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to get subscription status' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    logger.error('Subscription status error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

