import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/app/ask/auth';

export const dynamic = 'force-dynamic';

export async function POST(req: NextRequest) {
  try {
    const session = await auth();
    
    if (!session?.user?.id) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const API_URL = process.env.NEXT_PUBLIC_PLATFORM_API_URL || 'http://localhost:8000';
    
    const response = await fetch(`${API_URL}/api/subscriptions/cancel`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.user.id}`,
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to cancel subscription' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Cancel subscription error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

