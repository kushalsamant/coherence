/**
 * Shared checkout utilities for Razorpay integration
 */

import type { SubscriptionTier, PaymentType, CheckoutSessionResponse, RazorpayCheckoutOptions } from "./PricingTier";

declare global {
  interface Window {
    Razorpay: any;
  }
}

/**
 * Load Razorpay checkout script dynamically
 */
export function loadRazorpayScript(): Promise<void> {
  return new Promise((resolve, reject) => {
    if (typeof window === "undefined") {
      reject(new Error("Window is not available"));
      return;
    }

    // Check if already loaded
    if (window.Razorpay) {
      resolve();
      return;
    }

    // Check if script is already being loaded
    const existingScript = document.querySelector('script[src="https://checkout.razorpay.com/v1/checkout.js"]');
    if (existingScript) {
      existingScript.addEventListener("load", () => resolve());
      existingScript.addEventListener("error", () => reject(new Error("Failed to load Razorpay script")));
      return;
    }

    // Load script
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.async = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load Razorpay script"));
    document.body.appendChild(script);
  });
}

/**
 * Create Razorpay checkout options from session response
 */
export function createRazorpayOptions(
  sessionData: CheckoutSessionResponse,
  paymentType: PaymentType,
  onSuccess: (response: any) => void,
  onCancel: () => void
): RazorpayCheckoutOptions {
  const options: RazorpayCheckoutOptions = {
    key: sessionData.key_id,
    amount: sessionData.amount,
    currency: sessionData.currency,
    name: sessionData.name,
    description: sessionData.description,
    prefill: sessionData.prefill,
    theme: sessionData.theme,
    handler: onSuccess,
    modal: {
      ondismiss: onCancel,
    },
  };

  // Add order_id or subscription_id based on payment type
  if (paymentType === "one_time" && sessionData.order_id) {
    options.order_id = sessionData.order_id;
  } else if (paymentType === "subscription" && sessionData.subscription_id) {
    options.subscription_id = sessionData.subscription_id;
  }

  return options;
}

/**
 * Open Razorpay checkout modal
 */
export async function openRazorpayCheckout(
  options: RazorpayCheckoutOptions,
  onPaymentFailed?: (response: any) => void
): Promise<void> {
  await loadRazorpayScript();

  if (!window.Razorpay) {
    throw new Error("Razorpay checkout script not loaded. Please refresh the page.");
  }

  const rzp = new window.Razorpay(options);

  if (onPaymentFailed) {
    rzp.on("payment.failed", onPaymentFailed);
  }

  rzp.open();
}

/**
 * Create checkout session by calling backend API
 */
export async function createCheckoutSession(
  tier: SubscriptionTier,
  paymentType: PaymentType,
  apiEndpoint: string = "/api/payments/checkout"
): Promise<CheckoutSessionResponse> {
  const response = await fetch(`${apiEndpoint}?price_id=${tier}&payment_type=${paymentType}`);
  
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: "Failed to create checkout session" }));
    throw new Error(error.error || "Failed to create checkout session");
  }

  const data = await response.json();
  
  if (data.error) {
    throw new Error(data.error);
  }

  return data;
}

