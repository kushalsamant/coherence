'use client'

import { Suspense, useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { createCheckoutSession } from '@/lib/ask/api'
import { Card, Button } from '@kushalsamant/design-template'
import Link from 'next/link'
import { logger } from '@/lib/logger'
import { loadRazorpayScript, openRazorpayCheckout } from '@/lib/shared/razorpay'

function PricingContent() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [checkoutLoading, setCheckoutLoading] = useState<string | null>(null)

  useEffect(() => {
    // Load Razorpay script using shared utility
    loadRazorpayScript().catch((err) => {
      logger.error('Failed to load Razorpay script:', err)
    })
    
    // Check for checkout success/cancel
    const checkoutStatus = searchParams?.get('checkout')
    if (checkoutStatus === 'success') {
      alert('Payment successful! Your subscription is now active.')
      router.push('/')
    } else if (checkoutStatus === 'canceled') {
      alert('Payment canceled.')
    }
  }, [searchParams, router])

  const handleSubscribe = async (tier: string, paymentType: 'one_time' | 'subscription' = 'one_time') => {
    if (tier === 'trial') {
      router.push('/')
      return
    }

    const paidTiers = ['weekly', 'monthly', 'yearly']
    if (!paidTiers.includes(tier)) {
      alert('Invalid subscription tier')
      return
    }

    setCheckoutLoading(`${tier}_${paymentType}`)
    try {
      // Get Razorpay order/subscription details from backend
      const orderData = await createCheckoutSession(tier, paymentType)
      
      // Open Razorpay checkout using shared utility
      await openRazorpayCheckout(
        orderData,
        (response: any) => {
          // Payment successful
          setCheckoutLoading(null)
          router.push('/?checkout=success')
        },
        (response: any) => {
          // Payment failed
          setCheckoutLoading(null)
          alert(`Payment failed: ${response.error.description || 'Unknown error'}`)
        },
        () => {
          // Payment dismissed
          setCheckoutLoading(null)
        }
      )
    } catch (err: any) {
      logger.error('Checkout error:', err)
      alert('Failed to create checkout session. Please try again.')
      setCheckoutLoading(null)
    }
  }

  const pricingPlans = [
    {
      name: 'Trial',
      price: 'Free',
      period: '7 days',
      description: 'Try every feature with unlimited research sessions.',
      features: [
        'Unlimited research sessions during trial',
        'All research tools',
        '7-day access window'
      ],
      tier: 'trial',
      cta: 'Start Free Trial',
      variant: 'secondary' as const
    },
    {
      name: 'Week',
      price: '₹1,299',
      period: 'per week',
      description: 'Perfect for short-term research projects.',
      features: [
        'Unlimited research sessions',
        'All research tools',
        '7-day access'
      ],
      tier: 'weekly',
      cta: 'Subscribe',
      variant: 'primary' as const
    },
    {
      name: 'Month',
      price: '₹3,499',
      period: 'per month',
      description: 'Best value for regular researchers.',
      features: [
        'Unlimited research sessions',
        'All research tools',
        '30-day access',
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
      description: 'Maximum savings for long-term research.',
      features: [
        'Unlimited research sessions',
        'All research tools',
        '365-day access',
        'Priority support',
        'Save 33% vs monthly'
      ],
      tier: 'yearly',
      cta: 'Subscribe',
      variant: 'primary' as const
    }
  ]

  return (
    <div style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-2xl)' }}>
        <h1 style={{ fontSize: 'var(--font-size-4xl)', fontWeight: 'var(--font-weight-bold)', marginBottom: 'var(--space-lg)' }}>
          ASK Pricing
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
              <div style={{ width: '100%', marginTop: 'var(--space-md)' }}>
                <Button 
                  variant={plan.variant} 
                  onClick={() => handleSubscribe(plan.tier)}
                  disabled={checkoutLoading === `${plan.tier}_one_time` || checkoutLoading === `${plan.tier}_subscription`}
                >
                  {checkoutLoading === `${plan.tier}_one_time` || checkoutLoading === `${plan.tier}_subscription` 
                    ? 'Processing...' 
                    : plan.cta}
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div style={{ marginTop: 'var(--space-2xl)', textAlign: 'center', color: 'var(--color-text-secondary)', fontSize: 'var(--font-size-sm)' }}>
        <p>All plans include unlimited research sessions. Cancel anytime.</p>
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
