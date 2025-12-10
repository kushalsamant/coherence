/**
 * Analytics tracking utilities
 * Provides event tracking for conversion funnel and user actions
 */

// Analytics event types
export type AnalyticsEvent =
  | 'page_view'
  | 'page_exit'
  | 'navigation'
  | 'time_on_page'
  | 'signup'
  | 'trial_start'
  | 'first_upload'
  | 'subscription_start'
  | 'subscription_cancel'
  | 'checkout_start'
  | 'checkout_complete'
  | 'checkout_abandon'
  | 'trial_expired'
  | 'upgrade_prompt'
  | 'error_occurred';

export interface AnalyticsEventData {
  event: AnalyticsEvent;
  properties?: Record<string, any>;
  userId?: string;
  timestamp?: number;
}

/**
 * Track an analytics event
 * Supports multiple analytics providers (Google Analytics, Plausible, etc.)
 */
export function trackEvent(event: AnalyticsEvent, properties?: Record<string, any>) {
  if (typeof window === 'undefined') {
    return; // Server-side rendering
  }

  const eventData: AnalyticsEventData = {
    event,
    properties,
    timestamp: Date.now(),
  };

  // Google Analytics 4 (gtag)
  if (typeof window.gtag !== 'undefined') {
    window.gtag('event', event, {
      ...properties,
      event_category: 'engagement',
    });
  }

  // Plausible Analytics
  if (typeof window.plausible !== 'undefined') {
    window.plausible(event, {
      props: properties,
    });
  }

  // Custom analytics endpoint (if needed)
  if (process.env.NEXT_PUBLIC_ANALYTICS_ENDPOINT) {
    fetch(process.env.NEXT_PUBLIC_ANALYTICS_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(eventData),
    }).catch((err) => {
      console.error('Analytics tracking error:', err);
    });
  }

  // Log in development
  if (process.env.NODE_ENV === 'development') {
    console.log('Analytics Event:', event, properties);
  }
}

// Track page entry time for time-on-page calculation
let pageEntryTime: number | null = null;
let previousPath: string | null = null;

/**
 * Track page view with navigation flow tracking
 */
export function trackPageView(path: string, title?: string) {
  const now = Date.now();
  
  // Track time on previous page if applicable
  if (pageEntryTime !== null && previousPath !== null) {
    const timeOnPage = Math.round((now - pageEntryTime) / 1000); // seconds
    trackEvent('time_on_page', {
      path: previousPath,
      duration: timeOnPage,
    });
  }

  // Track navigation flow
  if (previousPath !== null && previousPath !== path) {
    trackEvent('navigation', {
      from: previousPath,
      to: path,
      timestamp: now,
    });
  }

  // Track page view
  trackEvent('page_view', {
    path,
    title: title || document.title,
    referrer: previousPath || document.referrer,
  });

  // Google Analytics page view
  if (typeof window.gtag !== 'undefined') {
    window.gtag('config', process.env.NEXT_PUBLIC_GA_ID || '', {
      page_path: path,
      page_title: title || document.title,
    });
  }

  // Update tracking state
  pageEntryTime = now;
  previousPath = path;
}

/**
 * Track page exit (for drop-off analysis)
 */
export function trackPageExit(path: string) {
  if (pageEntryTime !== null) {
    const timeOnPage = Math.round((Date.now() - pageEntryTime) / 1000);
    trackEvent('page_exit', {
      path,
      duration: timeOnPage,
      timestamp: Date.now(),
    });
  }
}

/**
 * Track conversion funnel events
 */
export const funnelEvents = {
  landingPageView: () => trackEvent('page_view', { page: 'landing' }),
  signup: (method?: string) => trackEvent('signup', { method }),
  trialStart: (userId?: string) => trackEvent('trial_start', { userId }),
  firstUpload: (userId?: string, jobId?: string) =>
    trackEvent('first_upload', { userId, jobId }),
  subscriptionStart: (tier: string, userId?: string) =>
    trackEvent('subscription_start', { tier, userId }),
  checkoutStart: (tier: string) => trackEvent('checkout_start', { tier }),
  checkoutComplete: (tier: string, amount?: number) =>
    trackEvent('checkout_complete', { tier, amount }),
  checkoutAbandon: (tier: string, step?: string) =>
    trackEvent('checkout_abandon', { tier, step }),
  trialExpired: (userId?: string) => trackEvent('trial_expired', { userId }),
  upgradePrompt: (source: string) => trackEvent('upgrade_prompt', { source }),
};

/**
 * Track user flow through conversion funnel
 * Helps identify drop-off points
 */
export function trackFunnelStep(step: string, properties?: Record<string, any>) {
  trackEvent('navigation', {
    funnel_step: step,
    ...properties,
  });
}

/**
 * Track errors
 */
export function trackError(
  error: Error | string,
  context?: string,
  userId?: string
) {
  const errorMessage = typeof error === 'string' ? error : error.message;
  trackEvent('error_occurred', {
    error_message: errorMessage,
    context,
    userId,
  });
}

// Extend Window interface for analytics
declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
    plausible?: (event: string, options?: { props?: Record<string, any> }) => void;
  }
}
