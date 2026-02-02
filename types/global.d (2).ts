/**
 * Global TypeScript Type Declarations
 * Platform-wide types and interfaces
 * 
 * Note: Razorpay types are defined in @kvshvl/shared-frontend/src/payments/checkout.ts
 */

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

