# Tier Naming Standardization Plan - HIGH PRIORITY

## Problem

Reframe uses `"monthly"` and `"yearly"` tier names while ASK and Sketch2BIM use `"month"` and `"year"`. This creates:
- Cross-app integration complexity
- Potential bugs when sharing code
- Confusion in documentation

## Solution

Standardize Reframe to use `"month"` and `"year"` to match ASK/Sketch2BIM pattern.

## Files That Need Changes

### 1. Core Subscription Logic (CRITICAL)

**File:** `apps/reframe/lib/subscription.ts`
- Line 12: Change `monthly: 30,` to `month: 30,`
- Line 13: Change `yearly: 365,` to `year: 365,`
- Line 17: Change `["daily", "week", "monthly", "yearly"]` to `["daily", "week", "month", "year"]`
- Line 21: Update comment to reflect new tier names

### 2. Backend Subscription Service

**File:** `apps/reframe/backend/app/services/subscription_service.py`
- Line 13: Change `"monthly": 30,` to `"month": 30,`
- Line 14: Change `"yearly": 365,` to `"year": 365,`
- Line 18: Change `{"week", "monthly", "yearly"}` to `{"week", "month", "year"}`

### 3. Payment Processing Routes (CRITICAL)

**File:** `apps/reframe/app/api/razorpay/checkout/route.ts`
- Line 19: Update comment to use "month"/"year"
- Line 48: Change default from `"monthly"` to `"month"`
- Line 54: Change `["week", "monthly", "yearly"]` to `["week", "month", "year"]`
- Line 75: Change `monthly: getRazorpayPlanMonthly(),` to `month: getRazorpayPlanMonthly(),`
- Line 76: Change `yearly: getRazorpayPlanYearly(),` to `year: getRazorpayPlanYearly(),`
- Line 160: Change `monthly: getRazorpayMonthlyAmount(),` to `month: getRazorpayMonthlyAmount(),`
- Line 161: Change `yearly: getRazorpayYearlyAmount(),` to `year: getRazorpayYearlyAmount(),`

**File:** `apps/reframe/app/api/razorpay-webhook/route.ts`
- Line 19: Change type from `"week" | "monthly" | "yearly"` to `"week" | "month" | "year"`
- Line 21: Change `"monthly"` to `"month"`
- Line 22: Change `"yearly"` to `"year"`
- Line 26: Change type from `"week" | "monthly" | "yearly"` to `"week" | "month" | "year"`
- Line 28: Change `"monthly"` to `"month"`
- Line 29: Change `"yearly"` to `"year"`
- Line 95: Change `["week", "monthly", "yearly"]` to `["week", "month", "year"]`
- Line 100: Change type annotation to `"week" | "month" | "year"`
- Line 139: Change default from `"monthly"` to `"month"`
- Line 147: Change type annotation to `"week" | "month" | "year"`

### 4. Type Definitions (CRITICAL)

**File:** `apps/reframe/types/index.ts`
- Line 3: Change `'trial' | 'week' | 'monthly' | 'yearly'` to `'trial' | 'week' | 'month' | 'year'`
- Line 11: Update legacy subscription type if still needed

### 5. Frontend Components

**File:** `apps/reframe/components/ui/dual-price-display.tsx`
- Line 6: Change key from `monthly:` to `month:`
- Line 7: Change key from `yearly:` to `year:`

**File:** `apps/reframe/app/pricing/page.tsx`
- Line 16: Change `monthly:` to `month:`
- Line 17: Change `yearly:` to `year:`
- Line 30: Change type from `"monthly" | "yearly"` to `"month" | "year"`
- Update all PRICING_TIERS to use "month"/"year"

**File:** `apps/reframe/app/page.tsx`
- Lines 43-49: Update tier checks from `"monthly"/"yearly"` to `"month"/"year"`

**File:** `apps/reframe/app/settings/page.tsx`
- Update any tier comparisons to use "month"/"year"

### 6. Scripts

**File:** `apps/reframe/scripts/create_razorpay_plans.ts`
- Update tier references from "monthly"/"yearly" to "month"/"year"
- Update environment variable mappings

### 7. Documentation

**File:** `apps/reframe/readme.md`
- Update all references from "monthly"/"yearly" to "month"/"year"

**File:** `apps/reframe/app/terms/page.tsx`
- Update pricing descriptions to use "month"/"year" terminology

### 8. Backend Services

**File:** `apps/reframe/backend/app/services/cost_service.py`
- Update any tier references in comments

**File:** `apps/reframe/backend/app/services/groq_monitor.py`
- Update comments if they reference tiers

## IMPORTANT CONSIDERATIONS

### Database/User Metadata

⚠️ **CRITICAL**: Existing users in production may have `"monthly"` or `"yearly"` stored in their metadata. You need:

1. **Migration Strategy**: Decide how to handle existing user data
   - Option A: Keep both "monthly"/"yearly" and "month"/"year" as valid for backwards compatibility
   - Option B: Migrate all existing user metadata from "monthly"/"yearly" to "month"/"year"
   - Option C: Accept both and normalize on read

2. **Environment Variables**: The environment variable names use "MONTH"/"YEAR":
   - `REFRAME_RAZORPAY_PLAN_MONTH` (already correct)
   - `REFRAME_RAZORPAY_PLAN_YEAR` (already correct)
   - These map to config functions that can be used with either naming

### Testing Requirements

After making changes, you must test:
1. Checkout flows for all three tiers (week/month/year)
2. Webhook processing for all tiers
3. Subscription status checks
4. User metadata reading/writing
5. Pricing page display

## Implementation Order

1. **Phase 1: Core Logic** (Backend subscription utilities)
2. **Phase 2: Payment Routes** (Checkout and webhook handlers)
3. **Phase 3: Type Definitions** (Update TypeScript types)
4. **Phase 4: Frontend Components** (UI updates)
5. **Phase 5: Documentation** (Readmes and user-facing text)
6. **Phase 6: Migration** (Handle existing user data if needed)

## Risk Assessment

**HIGH RISK AREAS:**
- Payment processing routes (could break checkout)
- Webhook handlers (could fail to process payments)
- Subscription status checks (could deny access incorrectly)

**MEDIUM RISK AREAS:**
- Frontend display (cosmetic, won't break functionality)
- Documentation (informational only)

## Recommendation

Given the high priority status, I recommend:
1. Start with core subscription logic (lib/subscription.ts, backend service)
2. Update payment routes carefully with extensive testing
3. Update frontend components
4. Add backwards compatibility layer if needed for existing users
5. Update documentation last

