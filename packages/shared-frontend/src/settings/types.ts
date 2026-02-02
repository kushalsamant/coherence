/**
 * Settings page type definitions
 */

export interface UserMetadata {
  email?: string;
  name?: string;
  id?: string;
  subscription_tier?: string;
  subscription?: string; // Legacy field
  subscription_status?: string;
  subscription_expires_at?: string;
  subscription_auto_renew?: boolean;
  razorpay_subscription_id?: string;
  razorpay_customer_id?: string;
}

export interface SettingsSectionConfig {
  /** Section title */
  title: string;
  /** Whether to show this section */
  show?: boolean;
  /** Custom render function */
  render?: () => React.ReactNode;
}

export interface SubscriptionDisplayConfig {
  /** How to display subscription tier */
  tierLabel?: (tier: string) => string;
  /** How to display subscription status */
  statusLabel?: (status: string) => string;
  /** Color mapping for tier badges */
  tierColors?: Record<string, string>;
  /** Custom subscription info */
  customInfo?: React.ReactNode;
}

export interface PaymentHistoryItem {
  id: string;
  amount: number;
  currency: string;
  status: string;
  product_type: string;
  created_at: string;
  razorpay_payment_id?: string;
  razorpay_order_id?: string;
}

