import { logger } from '@/lib/logger';

// Detect environment based on Razorpay key ID
const isProduction = (process.env.REFRAME_RAZORPAY_KEY_ID || process.env.RAZORPAY_KEY_ID)?.startsWith('rzp_live_');

logger.debug(`[App Config] Using ${isProduction ? 'PRODUCTION' : 'TEST'} mode`);

export function getInternationalPaymentsEnabled(): boolean {
  const enabled = process.env.REFRAME_INTERNATIONAL_PAYMENTS_ENABLED || process.env.INTERNATIONAL_PAYMENTS_ENABLED || 'false';
  return enabled === 'true';
}

export function getFromEmail(): string {
  return process.env.REFRAME_FROM_EMAIL || process.env.FROM_EMAIL || 'Reframe <noreply@localhost>';
}

// Razorpay pricing amounts in paise (₹1 = 100 paise)
// Unified pricing shared across all apps (ASK, Reframe, Sketch2BIM)
// Week: ₹1,299 = 129900 paise
// Monthly: ₹3,499 = 349900 paise
// Yearly: ₹29,999 = 2999900 paise
export function getRazorpayWeeklyAmount(): number {
  return parseInt(process.env.REFRAME_RAZORPAY_WEEKLY_AMOUNT || process.env.RAZORPAY_WEEKLY_AMOUNT || "129900", 10);
}

export function getRazorpayMonthlyAmount(): number {
  return parseInt(process.env.REFRAME_RAZORPAY_MONTHLY_AMOUNT || process.env.RAZORPAY_MONTHLY_AMOUNT || "349900", 10);
}

export function getRazorpayYearlyAmount(): number {
  return parseInt(process.env.REFRAME_RAZORPAY_YEARLY_AMOUNT || process.env.RAZORPAY_YEARLY_AMOUNT || "2999900", 10);
}

// Razorpay Plan IDs for subscriptions (shared across all apps)
// Plan IDs are unified: same plan IDs used by ASK, Reframe, and Sketch2BIM
export function getRazorpayPlanWeekly(): string {
  return process.env.REFRAME_RAZORPAY_PLAN_WEEKLY || process.env.RAZORPAY_PLAN_WEEKLY || "";
}

export function getRazorpayPlanMonthly(): string {
  return process.env.REFRAME_RAZORPAY_PLAN_MONTHLY || process.env.RAZORPAY_PLAN_MONTHLY || "";
}

export function getRazorpayPlanYearly(): string {
  return process.env.REFRAME_RAZORPAY_PLAN_YEARLY || process.env.RAZORPAY_PLAN_YEARLY || "";
}

