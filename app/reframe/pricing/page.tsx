"use client";

import { Button } from "@/components/reframe/ui/button";
import { Card, CardContent } from "@/components/reframe/ui/card";
import { DualPriceDisplay } from "@/components/reframe/ui/dual-price-display";
import { useSession } from "next-auth/react";
import { Check } from "lucide-react";
import { useEffect, useState } from "react";
import Link from "next/link";
// Pricing configuration - unified across all apps (ASK, Reframe, Sketch2BIM)
// Week: ₹1,299 = 129900 paise
// Monthly: ₹3,499 = 349900 paise
// Yearly: ₹29,999 = 2999900 paise
const PRICING = {
  week: { amount: 1299, currency: "INR", symbol: "₹", interval: "week" },
  monthly: { amount: 3499, currency: "INR", symbol: "₹", interval: "monthly" },
  yearly: { amount: 29999, currency: "INR", symbol: "₹", interval: "yearly" },
};

function getAllDisplayPrices() {
  return PRICING;
}

type PricingTier = {
  name: string;
  priceDetail: string;
  requests: string;
  features: string[];
  cta: string;
  plan: "monthly" | "yearly";
  highlight?: boolean;
  badge?: string;
};

const PRICING_TIERS: PricingTier[] = [
  {
    name: "Free",
    priceDetail: "5 requests total",
    requests: "5 requests to try",
    features: [
      "3 essential tones",
      "Age targeting included",
      "10,000 words per request",
      "Email + Google login",
    ],
    cta: "Start exploring",
    plan: "monthly",
  },
  {
    name: "Week Pro",
    priceDetail: "per week",
    requests: "Unlimited",
    features: [
      "Unlimited requests",
      "All 6 tones unlocked",
      "All character limits unlocked",
      "7-day access",
    ],
    cta: "Perfect for short projects",
    plan: "week",
  },
  {
    name: "Monthly Pro",
    priceDetail: "per month",
    requests: "Unlimited",
    features: [
      "Unlimited requests",
      "All 6 tones unlocked",
      "All character limits unlocked",
      "Maximum limit (250k chars)",
      "Priority support",
    ],
    cta: "For regular creators",
    plan: "monthly",
  },
  {
    name: "Yearly Pro",
    priceDetail: "per year",
    requests: "Unlimited",
    features: [
      "Unlimited requests",
      "All 6 tones unlocked",
      "Save 33% (best value)",
      "Priority support",
      "Early access to new features",
    ],
    cta: "Best for professionals",
    plan: "yearly",
    highlight: true,
    badge: "BEST VALUE",
  },
];


export default function PricingPage() {
  const { data: session } = useSession();
  const isSignedIn = !!session?.user;
  const [userPlan, setUserPlan] = useState<string | undefined>(undefined);
  const [subscriptionTier, setSubscriptionTier] = useState<string | undefined>(undefined);

  // Fetch user metadata
  useEffect(() => {
    const fetchMetadata = async () => {
      if (!isSignedIn) return;
      try {
        const res = await fetch('/api/user-metadata');
        const data = await res.json();
        const tier = data.subscription_tier;
        if (tier) {
          setSubscriptionTier(tier);
          setUserPlan(tier === "trial" ? undefined : tier);
        }
      } catch (e) {
        console.error("Failed to fetch metadata:", e);
      }
    };
    fetchMetadata();
  }, [isSignedIn]);

  const handleSelectPlan = async (plan: string) => {
    if (!isSignedIn) {
      window.location.href = '/';
      return;
    }
    if (plan === userPlan) return;
    
    try {
      // Create Razorpay checkout session
      const res = await fetch(`/api/razorpay/checkout?price_id=${plan}&payment_type=one_time`);
      const data = await res.json();
      
      if (data.error) {
        alert(data.error);
        return;
      }

      // Initialize Razorpay checkout
      const options = {
        key: data.key_id,
        amount: data.amount,
        currency: data.currency,
        name: data.name,
        description: data.description,
        order_id: data.order_id,
        prefill: data.prefill,
        theme: data.theme,
        handler: function(response: any) {
          // Payment successful - redirect to success page
          window.location.href = data.success_url;
        },
        modal: {
          ondismiss: function() {
            // Payment cancelled - redirect to cancel page
            window.location.href = data.cancel_url;
          }
        }
      };

      const razorpay = (window as any).Razorpay;
      if (!razorpay) {
        // Load Razorpay script
        const script = document.createElement('script');
        script.src = 'https://checkout.razorpay.com/v1/checkout.js';
        script.onload = () => {
          const rzp = new (window as any).Razorpay(options);
          rzp.open();
        };
        document.body.appendChild(script);
      } else {
        const rzp = new razorpay(options);
        rzp.open();
      }
    } catch (error) {
      console.error("Failed to create checkout:", error);
      alert("Failed to start checkout. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 to-slate-100 py-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Reframe Pricing</h1>
          <p className="text-xl text-muted-foreground">
            Choose the perfect plan for your content needs
          </p>
          <p className="text-lg text-primary font-medium mt-2">
            6 authentic human tones × 9 generations = 54 unique voices
          </p>
          <p className="text-sm text-muted-foreground mt-3 italic">
            💰 All prices in INR (₹) with live USD, EUR, GBP conversions
          </p>
          <p className="text-sm text-slate-600 mt-2">
            Target any generation: Silent (1928) → Gen Beta (2025+) → Kids (8-12)
          </p>
        </div>

        {/* Subscription Plans Header */}
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold mb-2">Subscription Plans</h2>
          <p className="text-lg text-muted-foreground">
            Recurring plans with unlimited access - monthly or yearly
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {PRICING_TIERS.map((tier) => {
            const isFree = tier.name === "Free";
            const isCurrentPlan = 
              (!userPlan && isFree) ||
              userPlan === tier.plan;

            return (
              <Card
                key={tier.name}
                className={`relative ${
                  tier.highlight
                    ? "border-primary border-2 shadow-xl"
                    : "border-slate-200"
                }`}
              >
                {tier.badge && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2">
                    <span className="bg-primary text-primary-foreground px-4 py-1 rounded-full text-sm font-bold">
                      {tier.badge}
                    </span>
                  </div>
                )}
                <CardContent className="p-6 space-y-4">
                  <div>
                    <h3 className="text-2xl font-bold">{tier.name}</h3>
                    <div className="mt-2">
                      {isFree ? (
                        <div className="flex flex-col items-start">
                          <span className="text-4xl font-bold text-gray-900 dark:text-gray-100">₹0</span>
                          <span className="text-sm text-gray-600 dark:text-gray-400 mt-1">{tier.priceDetail}</span>
                        </div>
                      ) : (
                        <DualPriceDisplay 
                          priceKey={tier.plan}
                          showInterval={false}
                        />
                      )}
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <p className="font-semibold text-sm text-muted-foreground mb-2">
                      {tier.requests}
                    </p>
                    <ul className="space-y-2">
                      {tier.features.map((feature, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-sm">
                          <Check className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  <Button
                    className="w-full"
                    variant={tier.highlight ? "default" : "outline"}
                    onClick={() => handleSelectPlan(tier.plan)}
                    disabled={isCurrentPlan && !isFree}
                  >
                    {isCurrentPlan && !isFree
                      ? "Current Plan"
                      : isFree
                      ? "Sign Up Free"
                      : "Upgrade Now"}
                  </Button>

                  <p className="text-xs text-center text-muted-foreground">
                    {tier.cta}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Feature Comparison Table */}
        <Card className="mb-12">
          <CardContent className="p-6">
            <h2 className="text-2xl font-bold mb-6">Feature Comparison</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3 px-4">Feature</th>
                    <th className="text-center py-3 px-4">Free</th>
                    <th className="text-center py-3 px-4">Week</th>
                    <th className="text-center py-3 px-4">Monthly</th>
                    <th className="text-center py-3 px-4 bg-primary/5">Yearly</th>
                  </tr>
                </thead>
                <tbody className="text-sm">
                  <tr className="border-b">
                    <td className="py-3 px-4">Requests</td>
                    <td className="text-center py-3 px-4">5 total</td>
                    <td className="text-center py-3 px-4">Unlimited</td>
                    <td className="text-center py-3 px-4">Unlimited</td>
                    <td className="text-center py-3 px-4 bg-primary/5">Unlimited</td>
                  </tr>
                  <tr className="border-b">
                    <td className="py-3 px-4">Available Tones</td>
                    <td className="text-center py-3 px-4">3 tones</td>
                    <td className="text-center py-3 px-4">All 6</td>
                    <td className="text-center py-3 px-4">All 6</td>
                    <td className="text-center py-3 px-4 bg-primary/5">All 6</td>
                  </tr>
                  <tr className="border-b">
                    <td className="py-3 px-4">Age Targeting</td>
                    <td className="text-center py-3 px-4">✅</td>
                    <td className="text-center py-3 px-4">✅</td>
                    <td className="text-center py-3 px-4">✅</td>
                    <td className="text-center py-3 px-4 bg-primary/5">✅</td>
                  </tr>
                  <tr className="border-b">
                    <td className="py-3 px-4">Words per Request</td>
                    <td className="text-center py-3 px-4">10,000</td>
                    <td className="text-center py-3 px-4">10,000</td>
                    <td className="text-center py-3 px-4">10,000</td>
                    <td className="text-center py-3 px-4 bg-primary/5">10,000</td>
                  </tr>
                  <tr className="border-b">
                    <td className="py-3 px-4">Priority Support</td>
                    <td className="text-center py-3 px-4">-</td>
                    <td className="text-center py-3 px-4">-</td>
                    <td className="text-center py-3 px-4">✅</td>
                    <td className="text-center py-3 px-4 bg-primary/5">✅</td>
                  </tr>
                  <tr className="border-b">
                    <td className="py-3 px-4">Early Access</td>
                    <td className="text-center py-3 px-4">-</td>
                    <td className="text-center py-3 px-4">-</td>
                    <td className="text-center py-3 px-4">-</td>
                    <td className="text-center py-3 px-4 bg-primary/5">✅</td>
                  </tr>
                  <tr>
                    <td className="py-3 px-4 font-semibold">Cost</td>
                    <td className="text-center py-3 px-4">₹0</td>
                    <td className="text-center py-3 px-4">₹1,299/week</td>
                    <td className="text-center py-3 px-4">₹3,499/mo (₹117/day)</td>
                    <td className="text-center py-3 px-4 bg-primary/5 font-bold text-primary">
                      ₹29,999/yr (₹82/day)
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* FAQ or CTA */}
        <div className="text-center">
          <Button size="lg" asChild>
            <Link href="/">Back to App</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}

