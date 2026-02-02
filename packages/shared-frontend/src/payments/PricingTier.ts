/**
 * Pricing tier type definitions
 */

export type SubscriptionTier = "trial" | "weekly" | "monthly" | "yearly";
export type PaymentType = "one_time" | "subscription";

export interface PricingTier {
  /** Tier identifier */
  tier: SubscriptionTier;
  /** Display name */
  name: string;
  /** Price display string (e.g., "₹1,299" or "Free") */
  price: string;
  /** Period display (e.g., "per week", "7 days") */
  period: string;
  /** Description */
  description: string;
  /** List of features */
  features: string[];
  /** CTA button text */
  cta: string;
  /** Whether this tier is highlighted/popular */
  highlight?: boolean;
  /** Badge text (e.g., "BEST VALUE") */
  badge?: string;
  /** Button variant */
  variant?: "primary" | "secondary" | "outline";
}

export interface CheckoutSessionResponse {
  key_id: string;
  amount: number;
  currency: string;
  name: string;
  description: string;
  order_id?: string;
  subscription_id?: string;
  prefill?: {
    email?: string;
    contact?: string;
    name?: string;
  };
  theme?: {
    color?: string;
  };
  success_url?: string;
  cancel_url?: string;
}

export interface RazorpayCheckoutOptions {
  key: string;
  amount: number;
  currency: string;
  name: string;
  description: string;
  order_id?: string;
  subscription_id?: string;
  prefill?: {
    email?: string;
    contact?: string;
    name?: string;
  };
  theme?: {
    color?: string;
  };
  handler: (response: any) => void;
  modal: {
    ondismiss: () => void;
  };
}

