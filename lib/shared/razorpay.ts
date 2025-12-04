/**
 * Shared Razorpay checkout utilities
 * Used across ASK, Reframe, and Sketch2BIM
 */

import { logger } from '@/lib/logger';

interface RazorpayResponse {
  razorpay_payment_id: string;
  razorpay_order_id?: string;
  razorpay_subscription_id?: string;
  razorpay_signature: string;
}

interface RazorpayError {
  code: string;
  description: string;
  source: string;
  step: string;
  reason: string;
  metadata: Record<string, unknown>;
}

interface RazorpayFailureResponse {
  error: RazorpayError;
}

// Note: Window.Razorpay type is declared in packages/shared-frontend/src/payments/checkout.ts
// to avoid duplicate global declarations

interface RazorpayInstance {
  open(): void;
  on(event: string, handler: (response: RazorpayFailureResponse) => void): void;
}

interface RazorpayConstructor {
  new(options: Record<string, unknown>): RazorpayInstance;
}

export interface RazorpayCheckoutOptions {
  key_id: string;
  amount: number;
  currency: string;
  name: string;
  description: string;
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

/**
 * Load Razorpay checkout script dynamically
 * @returns Promise that resolves when script is loaded
 */
export function loadRazorpayScript(): Promise<void> {
  return new Promise((resolve, reject) => {
    // Check if script already exists
    if (typeof window.Razorpay !== 'undefined') {
      resolve();
      return;
    }

    // Check if script is already being loaded
    const existingScript = document.querySelector(
      'script[src="https://checkout.razorpay.com/v1/checkout.js"]'
    );
    
    if (existingScript) {
      existingScript.addEventListener('load', () => resolve());
      existingScript.addEventListener('error', () => 
        reject(new Error('Failed to load Razorpay script'))
      );
      return;
    }

    // Create and load script
    const script = document.createElement('script');
    script.src = 'https://checkout.razorpay.com/v1/checkout.js';
    script.async = true;
    
    script.onload = () => resolve();
    script.onerror = () => reject(new Error('Failed to load Razorpay script'));
    
    document.body.appendChild(script);
  });
}

/**
 * Initialize and open Razorpay checkout
 * @param options Razorpay checkout options
 * @param onSuccess Success callback
 * @param onFailure Failure callback
 * @param onDismiss Dismiss callback
 */
export async function openRazorpayCheckout(
  options: RazorpayCheckoutOptions,
  onSuccess?: (response: RazorpayResponse) => void,
  onFailure?: (response: RazorpayFailureResponse) => void,
  onDismiss?: () => void
): Promise<void> {
  // Ensure Razorpay script is loaded
  await loadRazorpayScript();

  // Create checkout options
  const checkoutOptions: Record<string, unknown> = {
    key: options.key_id,
    amount: options.amount,
    currency: options.currency,
    name: options.name,
    description: options.description,
    prefill: options.prefill || {},
    theme: options.theme || { color: '#9333EA' },
    handler: onSuccess || options.handler || function(response: RazorpayResponse) {
      logger.info('Payment successful:', response);
    },
    modal: {
      ondismiss: onDismiss || options.modal?.ondismiss || function() {
        logger.info('Payment dismissed');
      }
    }
  };

  // Add order_id for one-time payments or subscription_id for subscriptions
  if (options.order_id) {
    checkoutOptions.order_id = options.order_id;
  } else if (options.subscription_id) {
    checkoutOptions.subscription_id = options.subscription_id;
  }

  // Create and open Razorpay instance
  const rzp = new window.Razorpay(checkoutOptions);
  
  // Handle payment failures
  if (onFailure) {
    rzp.on('payment.failed', onFailure as (response: unknown) => void);
  } else {
    rzp.on('payment.failed', function(response: unknown) {
      const failureResponse = response as RazorpayFailureResponse;
      logger.error('Payment failed:', failureResponse.error);
      alert(`Payment failed: ${failureResponse.error.description || 'Unknown error'}`);
    });
  }

  // Open checkout
  rzp.open();
}

/**
 * Create checkout session and open Razorpay
 * Generic function that can be used by any app
 * 
 * @param apiEndpoint API endpoint to create checkout session
 * @param tier Subscription tier (week, monthly, yearly)
 * @param paymentType Payment type (one_time or subscription)
 * @param onSuccess Success callback
 * @param onFailure Failure callback
 * @param onDismiss Dismiss callback
 */
export async function createAndOpenCheckout(
  apiEndpoint: string,
  tier: string,
  paymentType: 'one_time' | 'subscription' = 'one_time',
  onSuccess?: (response: RazorpayResponse) => void,
  onFailure?: (response: RazorpayFailureResponse) => void,
  onDismiss?: () => void
): Promise<void> {
  try {
    // Fetch checkout session from API
    const response = await fetch(apiEndpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tier, paymentType }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    const orderData = await response.json();

    // Open Razorpay checkout
    await openRazorpayCheckout(
      orderData,
      onSuccess,
      onFailure,
      onDismiss
    );
  } catch (error) {
    logger.error('Checkout error:', error instanceof Error ? error : new Error(String(error)));
    throw new Error('Failed to create checkout session. Please try again.');
  }
}

/**
 * Hook to use Razorpay in React components
 * Automatically loads script and provides checkout function
 */
export function useRazorpay() {
  const [isLoaded, setIsLoaded] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(false);
  const [error, setError] = React.useState<Error | null>(null);

  React.useEffect(() => {
    loadRazorpayScript()
      .then(() => setIsLoaded(true))
      .catch((err) => setError(err));
  }, []);

  const openCheckout = React.useCallback(
    async (
      options: RazorpayCheckoutOptions,
      onSuccess?: (response: RazorpayResponse) => void,
      onFailure?: (response: RazorpayFailureResponse) => void,
      onDismiss?: () => void
    ) => {
      if (!isLoaded) {
        throw new Error('Razorpay script not loaded yet');
      }

      setIsLoading(true);
      try {
        await openRazorpayCheckout(options, onSuccess, onFailure, onDismiss);
      } finally {
        setIsLoading(false);
      }
    },
    [isLoaded]
  );

  return {
    isLoaded,
    isLoading,
    error,
    openCheckout,
  };
}

// Note: React import for useRazorpay hook
import React from 'react';

