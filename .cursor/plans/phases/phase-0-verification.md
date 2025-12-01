# Phase 0: Pre-Implementation Verification

> **Navigation**: [README](../README.md) | [Progress Status](../01_PROGRESS_STATUS.md)

**Status**: ✅ Complete (100%)  
**Priority**: Critical (already done)  
**Time**: 2-3 hours (completed)

## 0.1 Comprehensive Codebase Verification

**Purpose**: Verify all items claimed as "✅ Completed" in plan files are actually complete in the codebase before beginning implementation.

### Verification Results

**✅ VERIFIED COMPLETE**:
1. ✅ Database models use `razorpay_*` fields (no `stripe_*` found)
   - `apps/ask/api/models_db.py` - Uses `razorpay_customer_id`, `razorpay_payment_id`, `razorpay_order_id`
   - `apps/sketch2bim/backend/app/models.py` - Uses `razorpay_*` fields
   - SQL migrations (`database/migrations/02_create_ask_tables.sql`, `03_create_sketch2bim_tables.sql`) - Use `razorpay_*` columns

2. ✅ Payment routes use Razorpay (no Stripe references found)
   - `apps/ask/api/routes/payments.py` - No Stripe references
   - `apps/sketch2bim/backend/app/routes/payments.py` - No Stripe references

3. ✅ Config files have no Stripe fields
   - `render.yaml` - No Stripe references
   - `apps/sketch2bim/backend/app/config.py` - No Stripe references

4. ✅ ASK setup.ts script deleted (not found in codebase)

5. ✅ Shared backend alerts.py - `daily_cost_threshold` parameter removed from function signature

**✅ VERIFIED COMPLETE (Additional)**:
6. ✅ Daily cost threshold removal - COMPLETE
   - `packages/shared-frontend/src/cost-monitoring/groq-monitor.ts` - Only checks monthly threshold (lines 185-203)
   - No `DAILY_COST_THRESHOLD` constant exists or is referenced
   - Code is correct and working

7. ✅ Tier naming standardization - COMPLETE
   - `apps/ask/frontend/app/pricing/page.tsx` - Uses `'monthly'` and `'yearly'` ✅
   - `apps/sketch2bim/frontend/app/pricing/page.tsx` - Uses `'monthly'` and `'yearly'` ✅
   - `apps/sketch2bim/frontend/app/settings/page.tsx` - Uses `'monthly'` and `'yearly'` ✅
   - `apps/sketch2bim/frontend/app/settings/payments/page.tsx` - Uses `'monthly'` and `'yearly'` ✅
   - `apps/sketch2bim/frontend/components/CreditsDisplay.tsx` - Uses `'monthly'` and `'yearly'` ✅
   - `apps/sketch2bim/backend/app/schemas.py` - Defines `MONTHLY = "monthly"` and `YEARLY = "yearly"` ✅
   - `apps/sketch2bim/scripts/create_razorpay_plans.py` - Uses `"monthly"` and `"yearly"` ✅

**⚠️ MINOR ISSUE FOUND**:
1. ⚠️ **Reframe setup.ts Script Reference**:
   - `apps/reframe/package.json` line 12: References `"setup": "tsx scripts/setup.ts"`
   - File `apps/reframe/scripts/setup.ts` does NOT exist
   - **Action Required**: Remove script reference from package.json (covered in [Phase 4.3](../phases/phase-4-configuration.md#33-script-references-cleanup))

---

## Repository Audit Findings

### Critical Issues - ✅ Fixed

1. ✅ **Reframe Backend Subscription Service** - Fixed weekly tier values (1 → 7 days)
2. ✅ **Sketch2BIM Payment Route** - Fixed incorrect Stripe field names (now uses Razorpay fields)

### High Priority Issues

#### Tier Naming Inconsistency
- Reframe uses `"monthly"` and `"yearly"`
- ASK and Sketch2BIM use `"month"` and `"year"`
- **Status**: ✅ Standardized to `"monthly"` and `"yearly"` (Phase 2.1 complete)

### Medium Priority Issues

- ✅ Database schemas use Razorpay field names (verified)
- ✅ Stripe package dependency in Reframe (not in package.json, only in lockfile - safe to ignore)

### Documentation References

- [Documentation Index](../../docs/DOCUMENTATION_INDEX.md) - Complete documentation guide
- [Monorepo Migration Guide](../../docs/MONOREPO_MIGRATION.md) - Migration instructions
- [Cost Analysis](../../docs/COST_ANALYSIS.md) - Infrastructure cost analysis
- [Environment Variables Reference](../../docs/ENVIRONMENT_VARIABLES_REFERENCE.md) - Canonical env var list

---

**Related Files**:
- [Phase 2: Database & Infrastructure](./phase-2-database-infrastructure.md) - Next phase to implement
- [Phase 4: Configuration](./phase-4-configuration.md) - Fixes the minor issue found

