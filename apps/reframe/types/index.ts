// User Metadata
export interface UserMetadata {
  subscription_tier?: 'trial' | 'week' | 'monthly' | 'yearly';
  subscription_status?: 'inactive' | 'active' | 'cancelled' | 'expired';
  subscription_expires_at?: string; // ISO timestamp
  subscription_auto_renew?: boolean;
  razorpay_subscription_id?: string;
  razorpay_customer_id?: string;
  email?: string;
}

// Consent Data
export interface ConsentData {
  acceptedAt: string;
  termsVersion: string;
  privacyVersion: string;
  ipAddress?: string;
}

// Razorpay Checkout Metadata
export interface RazorpayCheckoutMetadata {
  userId: string;
  type?: 'one_time' | 'subscription';
  plan?: string;
}

// Error with message
export interface ErrorWithMessage {
  message: string;
}

export function isErrorWithMessage(error: unknown): error is ErrorWithMessage {
  return (
    typeof error === 'object' &&
    error !== null &&
    'message' in error &&
    typeof (error as Record<string, unknown>).message === 'string'
  );
}

export function toErrorWithMessage(maybeError: unknown): ErrorWithMessage {
  if (isErrorWithMessage(maybeError)) return maybeError;
  
  try {
    return { message: JSON.stringify(maybeError) };
  } catch {
    return { message: String(maybeError) };
  }
}
