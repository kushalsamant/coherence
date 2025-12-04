'use client'

import { Suspense } from 'react'
import { createCheckoutSession, openRazorpayCheckout, createRazorpayOptions } from "@kvshvl/shared-frontend/payments";
import type { SubscriptionTier, PaymentType } from "@kvshvl/shared-frontend/payments";
import { useRouter } from 'next/navigation'
import { Card, Button } from '@kushalsamant/design-template'

function PricingContent() {
  const router = useRouter()

  const handleSubscribe = async (tier: SubscriptionTier, paymentType: PaymentType = 'one_time') => {
    if (tier === 'trial') {
      router.push('/')
      return
    }

    try {
      const sessionData = await createCheckoutSession(tier, paymentType, '/api/payments/checkout')
      
      const options = createRazorpayOptions(
        sessionData,
        paymentType,
        (response) => {
          router.push('/?checkout=success')
        },
        () => {
          // Payment cancelled
        }
      )

      await openRazorpayCheckout(options, (response) => {
        alert(`Payment failed: ${response.error?.description || 'Unknown error'}`)
      })
    } catch (err: any) {
      alert('Failed to create checkout session. Please try again.')
      logger.error('Checkout error:', err)
    }
  }

  const pricingPlans = [
    {
      name: 'Trial',
      price: 'Free',
      period: '7 days',
      description: 'Try every feature with unlimited access.',
      features: [
        'Unlimited access during trial',
        'All features unlocked',
        '7-day access window'
      ],
      tier: 'trial' as SubscriptionTier,
      cta: 'Start Free Trial',
      variant: 'secondary' as const
    },
    {
      name: 'Week',
      price: '₹1,299',
      period: 'per week',
      description: 'Perfect for short-term projects.',
      features: [
        'Unlimited access',
        'All features',
        '7-day access'
      ],
      tier: 'weekly' as SubscriptionTier,
      cta: 'Subscribe',
      variant: 'primary' as const
    },
    {
      name: 'Monthly',
      price: '₹3,499',
      period: 'per month',
      description: 'Best value for regular users.',
      features: [
        'Unlimited access',
        'All features',
        '30-day access',
        'Priority support'
      ],
      tier: 'monthly' as SubscriptionTier,
      cta: 'Subscribe',
      variant: 'primary' as const
    },
    {
      name: 'Yearly',
      price: '₹29,999',
      period: 'per year',
      description: 'Maximum savings for long-term users.',
      features: [
        'Unlimited access',
        'All features',
        '365-day access',
        'Priority support',
        'Save 33% vs monthly'
      ],
      tier: 'yearly' as SubscriptionTier,
      cta: 'Subscribe',
      variant: 'primary' as const
    }
  ]

  return (
    <div style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)' }}>
        <h1 style={{ fontSize: 'var(--font-size-4xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-lg)' }}>
          {{APP_DISPLAY_NAME}} Pricing
        </h1>
        <p style={{ fontSize: 'var(--font-size-lg)', color: 'var(--color-text-secondary)' }}>
          Choose a plan that works for you
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
              >
                {plan.cta}
              </Button>
            </div>
          </Card>
        ))}
      </div>

      <div style={{ marginTop: 'var(--space-2xl)', textAlign: 'center', color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-sm)' }}>
        <p>All plans include unlimited access. Cancel anytime.</p>
        <p style={{ marginTop: 'var(--space-sm)' }}>
          We accept all major credit cards, debit cards, UPI, and netbanking through Razorpay.
        </p>
      </div>
    </div>
  )
}

export default function PricingPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <PricingContent />
    </Suspense>
  )
}

