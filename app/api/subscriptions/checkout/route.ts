import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@/lib/auth';
import { logger } from '@/lib/logger';
import Razorpay from 'razorpay';

// Unified subscription checkout endpoint
export const dynamic = 'force-dynamic';

// Initialize Razorpay
const razorpay = new Razorpay({
  key_id: process.env.RAZORPAY_KEY_ID || process.env.PLATFORM_RAZORPAY_KEY_ID || '',
  key_secret: process.env.RAZORPAY_KEY_SECRET || process.env.PLATFORM_RAZORPAY_KEY_SECRET || '',
});

// Plan configuration
const PLANS = {
  weekly: {
    plan_id: process.env.RAZORPAY_PLAN_WEEKLY || process.env.PLATFORM_RAZORPAY_PLAN_WEEKLY,
    amount: 129900, // ₹1,299 in paise
    name: 'Week',
  },
  monthly: {
    plan_id: process.env.RAZORPAY_PLAN_MONTHLY || process.env.PLATFORM_RAZORPAY_PLAN_MONTHLY,
    amount: 349900, // ₹3,499 in paise
    name: 'Month',
  },
  yearly: {
    plan_id: process.env.RAZORPAY_PLAN_YEARLY || process.env.PLATFORM_RAZORPAY_PLAN_YEARLY,
    amount: 2999900, // ₹29,999 in paise
    name: 'Year',
  },
};

export async function POST(req: NextRequest) {
  try {
    // Get session to verify authentication
    // In NextAuth v5 API routes, auth() should work automatically with cookies
    const session = await auth();
    
    logger.info('Session check:', { hasSession: !!session, userEmail: session?.user?.email });
    
    if (!session?.user?.email) {
      logger.error('Checkout failed: No authenticated user');
      return NextResponse.json({ 
        error: 'Please sign in to subscribe',
        details: 'Authentication required. Please sign in first.'
      }, { status: 401 });
    }

    logger.info(`Checkout initiated by: ${session.user.email}`);

    const body = await req.json();
    const { tier } = body;

    if (!tier || !['weekly', 'monthly', 'yearly'].includes(tier)) {
      return NextResponse.json({ error: 'Invalid tier' }, { status: 400 });
    }

    const plan = PLANS[tier as keyof typeof PLANS];
    
    if (!plan.plan_id) {
      logger.error(`Missing plan ID for tier: ${tier}`);
      return NextResponse.json(
        { error: 'Plan configuration missing' },
        { status: 500 }
      );
    }

    // Create Razorpay subscription
    const subscription = await razorpay.subscriptions.create({
      plan_id: plan.plan_id,
      customer_notify: 1,
      total_count: 1,
      notes: {
        email: session.user.email,
        name: session.user.name || 'Unknown',
        tier: tier,
      },
    });

    logger.info(`Created subscription for ${session.user.email}: ${subscription.id}`);

    // Return data for Razorpay checkout
    return NextResponse.json({
      subscription_id: subscription.id,
      key_id: process.env.RAZORPAY_KEY_ID || process.env.PLATFORM_RAZORPAY_KEY_ID,
      amount: plan.amount,
      currency: 'INR',
      name: 'KVSHVL Platform',
      description: `${plan.name} Subscription`,
      prefill: {
        email: session.user.email,
        name: session.user.name || '',
      },
    });
  } catch (error: any) {
    logger.error('Checkout error:', error);
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}

