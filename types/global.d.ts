/**
 * Global TypeScript Type Declarations
 * Platform-wide types and interfaces
 */

// Razorpay global types
declare global {
  interface Window {
    Razorpay: RazorpayConstructor;
  }
}

interface RazorpayConstructor {
  new (options: RazorpayOptions): RazorpayInstance;
}

interface RazorpayInstance {
  open(): void;
  on(event: string, handler: (response: unknown) => void): void;
}

interface RazorpayOptions {
  key: string;
  amount?: number;
  currency?: string;
  name: string;
  description?: string;
  order_id?: string;
  subscription_id?: string;
  prefill?: {
    name?: string;
    email?: string;
    contact?: string;
  };
  theme?: {
    color?: string;
  };
  handler?: (response: RazorpayResponse) => void;
  modal?: {
    ondismiss?: () => void;
  };
}

interface RazorpayResponse {
  razorpay_payment_id: string;
  razorpay_order_id?: string;
  razorpay_subscription_id?: string;
  razorpay_signature: string;
}

// User session types
interface UserSession {
  user: {
    id: string;
    email: string;
    name: string;
    image?: string;
  };
  expires: string;
}

// Subscription types
type SubscriptionTier = 'trial' | 'daily' | 'weekly' | 'monthly' | 'yearly';
type SubscriptionStatus = 'inactive' | 'active' | 'cancelled' | 'expired';

// API Response types
interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  has_next: boolean;
  has_prev: boolean;
}

// Error types
interface ValidationError {
  field: string;
  message: string;
}

interface ApiError {
  error: string;
  message: string;
  status: number;
  validation_errors?: ValidationError[];
}

// Export empty object to make this a module
export {};

