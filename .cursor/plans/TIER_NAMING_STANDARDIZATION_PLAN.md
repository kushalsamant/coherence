# Tier Naming Standardization Plan - Standardize to "monthly"/"yearly"

## Decision

**Standard:** Use `"monthly"` and `"yearly"` tier names across all applications (matching Reframe's current naming).

**Action Required:** Update ASK and Sketch2BIM to change from `"month"`/`"year"` to `"monthly"`/`"yearly"`.

## Progress Status

### ✅ COMPLETED - Backend Core Logic

1. ✅ **ASK Subscription Utils** (`apps/ask/api/utils/subscription.py`)
   - Updated SUBSCRIPTION_DURATIONS to use "monthly"/"yearly"
   - Added backwards compatibility for "month"/"year"
   - Added normalize_tier() function

2. ✅ **Sketch2BIM Subscription Utils** (`apps/sketch2bim/backend/app/utils/subscription.py`)
   - Updated SUBSCRIPTION_DURATIONS to use "monthly"/"yearly"
   - Added backwards compatibility for "month"/"year"
   - Added normalize_tier() function

3. ✅ **Shared Backend Subscription Utils** (`packages/shared-backend/subscription/utils.py`)
   - Updated SUBSCRIPTION_DURATIONS to use "monthly"/"yearly"
   - Added backwards compatibility for "month"/"year"
   - Added normalize_tier() function

### ✅ COMPLETED - Payment Processing Routes

4. ✅ **ASK Payment Routes** (`apps/ask/api/routes/payments.py`)
   - Updated AMOUNT_TO_TIER to use "monthly"/"yearly"
   - Updated PLAN_TO_TIER to use "monthly"/"yearly"
   - Updated checkout route with backwards compatibility
   - Updated docstrings

5. ✅ **Sketch2BIM Payment Routes** (`apps/sketch2bim/backend/app/routes/payments.py`)
   - Updated AMOUNT_TO_TIER to use "monthly"/"yearly"
   - Updated PLAN_TO_TIER to use "monthly"/"yearly"
   - Updated checkout route with backwards compatibility
   - Updated docstrings

### ✅ COMPLETED - Database Models & Config

6. ✅ **ASK Database Models** (`apps/ask/api/models_db.py`)
   - Updated comments to reflect "monthly"/"yearly" (backwards compatible)

7. ✅ **Sketch2BIM Database Models** (`apps/sketch2bim/backend/app/models.py`)
   - Updated comments to reflect "monthly"/"yearly" (backwards compatible)

8. ✅ **Shared Backend Feasibility Service** (`packages/shared-backend/feasibility/feasibility_service.py`)
   - Updated PRICING_TIERS to use "monthly"/"yearly" with backwards compatibility

9. ✅ **Sketch2BIM Config** (`apps/sketch2bim/backend/app/config.py`)
   - Updated comments to use "Monthly"/"Yearly"

### ⏳ PENDING - Frontend Components

10. ⏳ **ASK Frontend Pricing Page** (`apps/ask/frontend/app/pricing/page.tsx`)
    - Line 44: Change `['week', 'month', 'year']` to `['week', 'monthly', 'yearly']` (with backwards compatibility)
    - Line 145: Change `tier: 'month'` to `tier: 'monthly'`
    - Line 161: Change `tier: 'year'` to `tier: 'yearly'`
    - Update pricing plan display names if needed

11. ⏳ **Sketch2BIM Frontend Pricing Page** (`apps/sketch2bim/frontend/app/pricing/page.tsx`)
    - Line 70: Change `['week', 'month', 'year']` to `['week', 'monthly', 'yearly']` (with backwards compatibility)
    - Line 173: Change `tier: 'month'` to `tier: 'monthly'`
    - Line 183: Change `tier: 'year'` to `tier: 'yearly'`
    - Update pricing plan display names if needed

12. ⏳ **Sketch2BIM Settings Page** (`apps/sketch2bim/frontend/app/settings/page.tsx`)
    - Line 71-72: Update tier color cases from `'month'`/`'year'` to `'monthly'`/`'yearly'` (with backwards compatibility)

13. ⏳ **Sketch2BIM Payment History Page** (`apps/sketch2bim/frontend/app/settings/payments/page.tsx`)
    - Lines 90-93: Update getProductTypeLabel() to handle "monthly"/"yearly" (with backwards compatibility)
    - Line 102: Update getCreditsLabel() check to include "monthly"/"yearly"

14. ⏳ **Sketch2BIM CreditsDisplay Component** (`apps/sketch2bim/frontend/components/CreditsDisplay.tsx`)
    - Lines 42-45: Update getTierColor() cases from `'month'`/`'year'` to `'monthly'`/`'yearly'` (with backwards compatibility)
    - Lines 57-60: Update getTierBadge() cases from `'month'`/`'year'` to `'monthly'`/`'yearly'` (with backwards compatibility)
    - Line 69: Update paid tier check to include "monthly"/"yearly"

### ⏳ PENDING - Backend Schemas & Scripts

15. ⏳ **Sketch2BIM Schemas** (`apps/sketch2bim/backend/app/schemas.py`)
    - Line 26: Change `MONTH = "month"` to `MONTHLY = "monthly"`
    - Line 27: Change `YEAR = "year"` to `YEARLY = "yearly"`
    - Keep backwards compatibility if this enum is used in validation

16. ⏳ **Sketch2BIM Razorpay Plans Script** (`apps/sketch2bim/scripts/create_razorpay_plans.py`)
    - Line 84: Change `"tier": "month"` to `"tier": "monthly"`
    - Line 97: Change `"tier": "year"` to `"tier": "yearly"`
    - Lines 143-146: Update check_existing_plans() to handle both old and new tier names
    - Lines 193-197: Update output to use "monthly"/"yearly" but note backwards compatibility

### ✅ VERIFIED - Reframe (Already Uses "monthly"/"yearly")

- ✅ Reframe subscription utilities
- ✅ Reframe payment routes
- ✅ Reframe frontend components
- ✅ Reframe type definitions
- ✅ Reframe scripts

No changes needed for Reframe - it already uses the correct naming.

## Remaining Files That Need Updates

### Critical Frontend Files (Payment Flow)

1. **ASK Frontend Pricing Page** (`apps/ask/frontend/app/pricing/page.tsx`)
   - Update tier validation array
   - Update pricing plan tier values

2. **Sketch2BIM Frontend Pricing Page** (`apps/sketch2bim/frontend/app/pricing/page.tsx`)
   - Update tier validation array
   - Update pricing plan tier values

### Frontend Display Components

3. **Sketch2BIM Settings Page** (`apps/sketch2bim/frontend/app/settings/page.tsx`)
   - Update tier color/styling logic

4. **Sketch2BIM Payment History** (`apps/sketch2bim/frontend/app/settings/payments/page.tsx`)
   - Update product type label display
   - Update credits label logic

5. **Sketch2BIM CreditsDisplay** (`apps/sketch2bim/frontend/components/CreditsDisplay.tsx`)
   - Update tier badge display
   - Update tier color logic

### Backend Schemas

6. **Sketch2BIM Schemas Enum** (`apps/sketch2bim/backend/app/schemas.py`)
   - Update SubscriptionTier enum values
   - Ensure backwards compatibility if used in validation

### Scripts

7. **Sketch2BIM Razorpay Plans Script** (`apps/sketch2bim/scripts/create_razorpay_plans.py`)
   - Update tier values in plan notes
   - Update plan checking logic

## Backwards Compatibility Strategy

**Implemented in Backend:**
- All SUBSCRIPTION_DURATIONS dictionaries include both old and new formats
- normalize_tier() functions convert old to new format when needed
- Payment routes accept both formats in their tier mappings

**Required in Frontend:**
- Frontend validation should accept both formats OR normalize before sending
- Display components should handle both formats gracefully
- Product type labels should handle both formats

## Important Considerations

### Existing User Data

⚠️ **CRITICAL**: Existing users in production may have `"month"` or `"year"` stored in their subscription_tier field.

**Solution Implemented:**
- Backend normalization functions handle conversion
- Payment routes accept both formats
- Subscription utilities accept both formats

**Frontend Considerations:**
- Frontend should either:
  - Accept both formats in validation
  - Normalize before sending to backend
  - Display both formats correctly

### Environment Variables

**Note:** Environment variable names remain the same (they use MONTH/YEAR in the name, not in the value):
- `RAZORPAY_MONTH_AMOUNT` (amount value, not tier name)
- `RAZORPAY_YEAR_AMOUNT` (amount value, not tier name)

These don't need to change - only the tier name strings used in code need updating.

## Testing Requirements

After completing all changes, test:
1. ✅ Backend: Checkout flows for all three tiers (week/monthly/yearly) - Backend accepts both formats
2. ✅ Backend: Webhook processing for all tiers - Handles both formats
3. ⏳ Frontend: Pricing page tier validation and display
4. ⏳ Frontend: Checkout flow from pricing page
5. ⏳ Frontend: Settings page tier display
6. ⏳ Frontend: Payment history product type labels

## Implementation Priority

### High Priority (Blocks Functionality)

1. ⏳ Frontend pricing pages (tier validation must accept both or normalize)
2. ⏳ Frontend checkout flows (must send correct tier names)

### Medium Priority (Display Only)

3. ⏳ Settings pages (cosmetic tier display)
4. ⏳ Payment history labels (cosmetic)
5. ⏳ CreditsDisplay component (cosmetic)

### Low Priority (Validation/Enums)

6. ⏳ Backend schemas enum (may affect validation if used strictly)
7. ⏳ Script tier notes (for plan creation, not runtime)

## Summary

**Completed:** ✅ Backend core logic, payment routes, database models, shared services
**Remaining:** ⏳ Frontend components, backend schemas enum, scripts

**Total Files Updated:** 9 backend files ✅
**Total Files Remaining:** 7 files (5 frontend, 1 schema, 1 script) ⏳
