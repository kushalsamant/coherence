'use client';

import { Suspense, useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { api, User } from '@/lib/sketch2bim/api';
import Link from 'next/link';

function PricingContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [checkoutLoading, setCheckoutLoading] = useState<string | null>(null);

  useEffect(() => {
    loadUser();
    
    // Load Razorpay checkout script
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    document.body.appendChild(script);
    
    // Check for checkout success/cancel
    const checkoutStatus = searchParams?.get('checkout');
    if (checkoutStatus === 'success') {
      alert('Payment successful! Your credits have been added.');
      router.push('/dashboard');
    } else if (checkoutStatus === 'canceled') {
      alert('Payment canceled.');
    }
    
    return () => {
      // Cleanup script on unmount
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, [searchParams, router]);

  const loadUser = async () => {
    try {
      const data = await api.getCurrentUser();
      setUser(data);
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to load user');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSubscribe = async (tier: string, paymentType: 'one_time' | 'subscription' = 'one_time') => {
    if (!user) {
      router.push('/api/auth/signin');
      return;
    }

    if (user.subscription_tier === tier && user.subscription_status === 'active') {
      alert(`You already have a ${tier} subscription!`);
      return;
    }

    if (tier === 'trial') {
      router.push('/dashboard');
      return;
    }

    const paidTiers = ['week', 'monthly', 'yearly'];
    if (!paidTiers.includes(tier)) {
      alert('Invalid subscription tier');
      return;
    }

    setCheckoutLoading(`${tier}_${paymentType}`);
    try {
      // Get Razorpay order/subscription details from backend
      const orderData = await api.createCheckoutSession(tier, paymentType);
      
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
        prefill: orderData.prefill,
        theme: orderData.theme,
        handler: function (response: any) {
          // Payment successful
          setCheckoutLoading(null);
          router.push('/dashboard?checkout=success');
        },
        modal: {
          ondismiss: function() {
            // Payment cancelled
            setCheckoutLoading(null);
          }
        }
      };

      // For one-time payments, use order_id; for subscriptions, use subscription_id
      if (paymentType === 'one_time' && orderData.order_id) {
        options.order_id = orderData.order_id;
      } else if (paymentType === 'subscription' && orderData.subscription_id) {
        options.subscription_id = orderData.subscription_id;
      }

      // Open Razorpay checkout
      const rzp = new (window as any).Razorpay(options);
      rzp.on('payment.failed', function (response: any) {
        setCheckoutLoading(null);
        alert(`Payment failed: ${response.error.description || 'Unknown error'}`);
      });
      rzp.open();
    } catch (err: any) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Checkout error');
      }
      // Never expose internal error details
      alert('Failed to create checkout session. Please try again.');
      setCheckoutLoading(null);
    }
  };

  const sharedFeatures = [
    'Unlimited conversions',
    'IFC (Revit-compatible), DWG, SketchUp exports',
    'Layout variations & iterations',
    'Auto legend detection & QC reports',
    'Priority support'
  ];

  const pricingPlans = [
    {
      name: 'Trial',
      price: 'Free',
      period: '7 days',
      description: 'Try every feature with unlimited conversions.',
      features: [
        'Unlimited conversions during trial',
        'All export formats (single-use)',
        'Auto legend detection',
        '7-day access window'
      ],
      cta: 'Start Trial',
      tier: 'trial',
      popular: false
    },
    {
      name: 'Week Access',
      price: '₹1,299',
      period: '7 days',
      description: 'Perfect for crit week or short sprints.',
      features: sharedFeatures,
      cta: 'Buy Week Access',
      tier: 'week',
      popular: false
    },
    {
      name: 'Monthly Access',
      price: '₹3,499',
      period: '30 days',
      description: 'Ongoing coursework or client production.',
      features: sharedFeatures,
      cta: 'Subscribe Monthly',
      tier: 'monthly',
      popular: true
    },
    {
      name: 'Yearly Access',
      price: '₹29,999',
      period: '365 days',
      description: 'Best value for power users.',
      features: sharedFeatures,
      cta: 'Subscribe Yearly',
      tier: 'yearly',
      popular: false
    }
  ];

  const getCurrentTier = () => {
    if (!user) return null;
    return user.subscription_tier;
  };

  const currentTier = getCurrentTier();

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <nav className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <Link href="/" className="text-2xl font-bold text-primary-600">
              Sketch-to-BIM
            </Link>
            <div className="flex items-center gap-4">
              {user ? (
                <>
                  <Link href="/dashboard" className="text-gray-700 dark:text-gray-300 hover:text-primary-600">
                    Dashboard
                  </Link>
                  <span className="text-gray-500 dark:text-gray-400">{user.email}</span>
                </>
              ) : (
                <Link href="/api/auth/signin" className="btn-primary">
                  Sign In
                </Link>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Header Section */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-gray-100 mb-4">
            Simple, Transparent Pricing
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Choose the plan that fits your workflow. Upgrade or downgrade at any time.
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {pricingPlans.map((plan) => {
            const isCurrentPlan = currentTier === plan.tier;
            const isLoading = checkoutLoading === plan.tier;

            return (
              <div
                key={plan.name}
                className={`card relative ${
                  plan.popular ? 'ring-2 ring-primary-600 shadow-lg' : ''
                }`}
              >
                {plan.popular && (
                  <div className="absolute top-0 right-0 bg-primary-600 text-white px-3 py-1 rounded-bl-lg text-sm font-medium">
                    Most Popular
                  </div>
                )}
                
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-2">{plan.name}</h3>
                  <div className="mb-4">
                    <span className="text-4xl font-bold text-gray-900 dark:text-gray-100">{plan.price}</span>
                    {plan.period && (
                      <span className="text-gray-600 dark:text-gray-400 ml-2">/{plan.period}</span>
                    )}
                  </div>
                  <p className="text-gray-600 dark:text-gray-400">{plan.description}</p>
                </div>

                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                      <svg
                        className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                      <span className="text-gray-700 dark:text-gray-300">{feature}</span>
                    </li>
                  ))}
                </ul>

                {plan.tier === 'trial' ? (
                  <button
                    onClick={() => handleSubscribe('trial')}
                    className="w-full py-3 rounded-lg font-medium border border-primary-600 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 transition-colors"
                  >
                    {plan.cta}
                  </button>
                ) : (
                  // Week, Month, Year: Both one-time and subscription options
                  <div className="space-y-3">
                    <button
                      onClick={() => handleSubscribe(plan.tier, 'one_time')}
                      disabled={isCurrentPlan || checkoutLoading === `${plan.tier}_one_time`}
                      className={`w-full py-2.5 rounded-lg font-medium transition-colors text-sm ${
                        isCurrentPlan
                          ? 'bg-gray-200 dark:bg-gray-800 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                          : 'bg-gray-900 dark:bg-gray-700 text-white hover:bg-gray-800 dark:hover:bg-gray-600'
                      }`}
                    >
                      {checkoutLoading === `${plan.tier}_one_time`
                        ? 'Processing...'
                        : `Buy One-Time (${plan.price})`}
                    </button>
                    <button
                      onClick={() => handleSubscribe(plan.tier, 'subscription')}
                      disabled={isCurrentPlan || checkoutLoading === `${plan.tier}_subscription`}
                      className={`w-full py-2.5 rounded-lg font-medium transition-colors text-sm ${
                        isCurrentPlan
                          ? 'bg-gray-200 dark:bg-gray-800 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                          : plan.popular
                          ? 'bg-primary-600 text-white hover:bg-primary-700'
                          : 'bg-primary-600 text-white hover:bg-primary-700'
                      }`}
                    >
                      {checkoutLoading === `${plan.tier}_subscription`
                        ? 'Processing...'
                        : `Subscribe (${plan.price}/${plan.period}, auto-renews)`}
                    </button>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* FAQ Section */}
        <div className="max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-8 text-center">
            Frequently Asked Questions
          </h2>
          <div className="space-y-6">
            <div className="card">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                What happens if I exceed my monthly limit?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Trial users can upgrade to any paid pass at any time. Week, month, and year passes
                include unlimited conversions for the selected duration.
              </p>
            </div>
            <div className="card">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                Can I change plans later?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Yes! You can upgrade or downgrade at any time. Changes take effect immediately
                for upgrades and at the end of your billing cycle for downgrades.
              </p>
            </div>
            <div className="card">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                Do you offer refunds?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Monthly and yearly plans include a 30-day money-back guarantee.
                Contact support for assistance with refunds.
              </p>
            </div>
            <div className="card">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-2">
                What payment methods do you accept?
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                We accept all major credit cards, debit cards, UPI, and netbanking through Razorpay. 
                Payments are secure and processed instantly.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function PricingPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    }>
      <PricingContent />
    </Suspense>
  );
}
