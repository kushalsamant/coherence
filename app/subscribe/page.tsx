'use client';

import { Suspense, useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Card, Button } from '@kushalsamant/design-template';
import Link from 'next/link';

function SubscribeContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [checkoutLoading, setCheckoutLoading] = useState<string | null>(null);

  useEffect(() => {
    // Load Razorpay checkout script
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    document.body.appendChild(script);
    
    // Check for checkout success/cancel
    const checkoutStatus = searchParams?.get('checkout');
    if (checkoutStatus === 'success') {
      alert('Payment successful! Your subscription is now active. You now have access to all KVSHVL platform apps.');
      router.push('/');
    } else if (checkoutStatus === 'canceled') {
      alert('Payment canceled.');
    }
    
    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, [searchParams, router]);

  const handleSubscribe = async (tier: string) => {
    const paidTiers = ['week', 'monthly', 'yearly'];
    if (!paidTiers.includes(tier)) {
      alert('Invalid subscription tier');
      return;
    }

    setCheckoutLoading(tier);
    try {
      // Get Razorpay order/subscription details from unified backend
      const response = await fetch('/api/subscriptions/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ tier }),
      });

      if (!response.ok) {
        throw new Error('Failed to create checkout session');
      }

      const orderData = await response.json();
      
      // Check if Razorpay is loaded
      if (typeof (window as any).Razorpay === 'undefined') {
        throw new Error('Razorpay checkout script not loaded. Please refresh the page.');
      }

      // Create Razorpay checkout options
      const options: any = {
        key: orderData.key_id,
        amount: orderData.amount,
        currency: orderData.currency,
        name: orderData.name,
        description: orderData.description,
        subscription_id: orderData.subscription_id,
        prefill: orderData.prefill,
        theme: orderData.theme,
        handler: function (response: any) {
          setCheckoutLoading(null);
          router.push('/subscribe?checkout=success');
        },
        modal: {
          ondismiss: function() {
            setCheckoutLoading(null);
          }
        }
      };

      // Open Razorpay checkout
      const rzp = new (window as any).Razorpay(options);
      rzp.on('payment.failed', function (response: any) {
        setCheckoutLoading(null);
        alert(`Payment failed: ${response.error.description || 'Unknown error'}`);
      });
      rzp.open();
    } catch (err: any) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Checkout error:', err);
      }
      alert('Failed to create checkout session. Please try again.');
      setCheckoutLoading(null);
    }
  };

  const pricingPlans = [
    {
      name: 'Week',
      price: '₹1,299',
      period: 'per week',
      description: 'Perfect for short-term projects.',
      features: [
        'Access to all KVSHVL platform apps',
        'ASK: Daily Research',
        'Reframe',
        'Sketch2BIM',
        '7-day access',
        'All features unlocked'
      ],
      tier: 'week',
      cta: 'Subscribe',
      variant: 'secondary' as const
    },
    {
      name: 'Month',
      price: '₹3,499',
      period: 'per month',
      description: 'Best value for regular users.',
      features: [
        'Access to all KVSHVL platform apps',
        'ASK: Daily Research',
        'Reframe',
        'Sketch2BIM',
        '30-day access',
        'All features unlocked',
        'Priority support'
      ],
      tier: 'monthly',
      cta: 'Subscribe',
      variant: 'primary' as const
    },
    {
      name: 'Year',
      price: '₹29,999',
      period: 'per year',
      description: 'Maximum savings for long-term use.',
      features: [
        'Access to all KVSHVL platform apps',
        'ASK: Daily Research',
        'Reframe',
        'Sketch2BIM',
        '365-day access',
        'All features unlocked',
        'Priority support',
        'Save 33% vs monthly'
      ],
      tier: 'yearly',
      cta: 'Subscribe',
      variant: 'primary' as const
    }
  ];

  return (
    <div style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)' }}>
        <h1 style={{ fontSize: 'var(--font-size-4xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-lg)' }}>
          KVSHVL Platform Subscription
        </h1>
        <p style={{ fontSize: 'var(--font-size-lg)', color: 'var(--color-text-secondary)' }}>
          One subscription. All apps. Unlimited access.
        </p>
      </div>

      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', 
        gap: 'var(--space-lg)',
        marginTop: 'var(--space-2xl)'
      }}>
        {pricingPlans.map((plan) => (
          <Card key={plan.tier} variant="default">
            <div style={{ padding: 'var(--space-xl)' }}>
              <h2 style={{ fontSize: 'var(--font-size-2xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-sm)' }}>
                {plan.name}
              </h2>
              <p style={{ fontSize: 'var(--font-size-3xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-xs)' }}>
                {plan.price}
              </p>
              <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', marginBottom: 'var(--space-md)' }}>
                {plan.period}
              </p>
              <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--color-text-secondary)', marginBottom: 'var(--space-md)' }}>
                {plan.description}
              </p>
              <ul style={{ listStyle: 'none', padding: 0, margin: 'var(--space-md) 0', display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
                {plan.features.map((feature, idx) => (
                  <li key={idx} style={{ fontSize: 'var(--font-size-sm)' }}>✓ {feature}</li>
                ))}
              </ul>
              <Button 
                variant={plan.variant} 
                style={{ width: '100%', marginTop: 'var(--space-md)' }}
                onClick={() => handleSubscribe(plan.tier)}
                disabled={checkoutLoading === plan.tier}
              >
                {checkoutLoading === plan.tier ? 'Processing...' : plan.cta}
              </Button>
            </div>
          </Card>
        ))}
      </div>

      <div style={{ marginTop: 'var(--space-2xl)', textAlign: 'center', color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-sm)' }}>
        <p>All plans include access to all current and future KVSHVL platform apps. Cancel anytime.</p>
        <p style={{ marginTop: 'var(--space-sm)' }}>
          We accept all major credit cards, debit cards, UPI, and netbanking through Razorpay.
        </p>
      </div>
    </div>
  );
}

export default function SubscribePage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SubscribeContent />
    </Suspense>
  );
}

