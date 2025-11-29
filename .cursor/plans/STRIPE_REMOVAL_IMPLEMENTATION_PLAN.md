# Complete Stripe Removal & Daily-Cost Deprecation - Implementation Plan

## Overview

This plan details all remaining work to completely remove Stripe references and daily-cost thresholds from the entire monorepo (ASK, Sketch2BIM, Reframe, and shared packages). This is a platform-wide cleanup affecting all three applications.

## Current Status

### ✅ Completed
1. **Database Models**: All `stripe_*` fields renamed to `razorpay_*` in:
   - `apps/ask/api/models_db.py`
   - `apps/sketch2bim/backend/app/models.py`
   - `packages/shared-backend/database/models.py`
   - `packages/shared-backend/payments/models.py`

2. **Payment Routes**: All references updated in:
   - `apps/ask/api/routes/payments.py`
   - `apps/sketch2bim/backend/app/routes/payments.py`

3. **SQL Migrations & Schemas**: Updated to use `razorpay_*` columns:
   - `database/migrations/02_create_ask_tables.sql`
   - `database/migrations/03_create_sketch2bim_tables.sql`
   - `database/migrations/RUN_ALL_MIGRATIONS.sql`
   - `database/schemas/ask_schema.sql`
   - `database/schemas/sketch2bim_schema.sql`

4. **Alembic Initial Migration**: Updated:
   - `apps/sketch2bim/backend/alembic/versions/001_initial_schema.py`

5. **Config Files**: Stripe fields removed:
   - `apps/sketch2bim/backend/app/config.py`
   - `render.yaml`

6. **Stripe Setup Script**: Deleted:
   - `apps/ask/scripts/setup.ts`

7. **Backend Monitoring**: Daily threshold logic removed from:
   - `apps/ask/api/utils/groq_monitor.py` (mostly - needs docstring cleanup)
   - `apps/reframe/backend/app/services/groq_monitor.py` (mostly - needs docstring cleanup)
   - `packages/shared-backend/cost-monitoring/alerts.py` (mostly - needs docstring cleanup)

### ⏳ Remaining Work

---

## Phase 1: Runtime Database Migrations (Critical for Production)

### 1.1 Create Alembic Migration for ASK

**File**: `apps/ask/alembic/versions/XXX_rename_stripe_to_razorpay.py` (new file)

**Purpose**: Rename existing `stripe_*` columns to `razorpay_*` in production databases

**Actions**:
1. Check if ASK has Alembic setup (may need to initialize)
2. Create migration file with:
   ```python
   def upgrade():
       # Rename users.stripe_customer_id → razorpay_customer_id
       op.alter_column('users', 'stripe_customer_id', new_column_name='razorpay_customer_id')
       op.drop_index('ix_users_stripe_customer_id', table_name='users')
       op.create_index('ix_users_razorpay_customer_id', 'users', ['razorpay_customer_id'], unique=True)
       
       # Rename payments.stripe_payment_intent_id → razorpay_payment_id
       op.alter_column('payments', 'stripe_payment_intent_id', new_column_name='razorpay_payment_id')
       op.drop_index('ix_payments_stripe_payment_intent_id', table_name='payments')
       op.create_index('ix_payments_razorpay_payment_id', 'payments', ['razorpay_payment_id'], unique=True)
       
       # Rename payments.stripe_checkout_session_id → razorpay_order_id
       op.alter_column('payments', 'stripe_checkout_session_id', new_column_name='razorpay_order_id')
       op.drop_index('ix_payments_stripe_checkout_session_id', table_name='payments')
       op.create_index('ix_payments_razorpay_order_id', 'payments', ['razorpay_order_id'], unique=True)
   
   def downgrade():
       # Reverse operations
   ```

**Dependencies**: 
- Verify ASK has Alembic configured
- If not, initialize Alembic for ASK backend

### 1.2 Create Alembic Migration for Sketch2BIM

**File**: `apps/sketch2bim/backend/alembic/versions/011_rename_stripe_to_razorpay.py` (new file)

**Purpose**: Rename existing `stripe_*` columns to `razorpay_*` in production databases

**Actions**:
1. Create new migration file (next after `010_remove_reader_type_column.py`)
2. Use same column/index rename logic as ASK migration
3. Ensure it works with existing migration chain

**Dependencies**: 
- Alembic already configured for Sketch2BIM
- Migration should be numbered `011_` (next in sequence)

### 1.3 Verify Reframe Database Schema

**Actions**:
1. Check if Reframe has any database models with `stripe_*` fields
2. If yes, create equivalent Alembic migration for Reframe
3. If no, document that Reframe doesn't use payment database fields

**Files to check**:
- `apps/reframe/backend/app/models.py` (if exists)
- Any Reframe database schema definitions

---

## Phase 2: Documentation Updates (Stripe → Razorpay)

### 2.1 Update DATABASE_MIGRATION_GUIDE.md

**File**: `docs/DATABASE_MIGRATION_GUIDE.md`

**Current Issues**:
- Lines 70, 99: Still show `stripe_customer_id` in SQL examples
- Schema snippets need to be updated to show `razorpay_*` fields

**Actions**:
1. Replace all `stripe_customer_id` → `razorpay_customer_id` in SQL examples
2. Replace all `stripe_payment_intent_id` → `razorpay_payment_id`
3. Replace all `stripe_checkout_session_id` → `razorpay_order_id`
4. Update index names in examples:
   - `idx_users_stripe_customer_id` → `idx_users_razorpay_customer_id`
   - `idx_payments_stripe_payment_intent_id` → `idx_payments_razorpay_payment_id`
   - `idx_payments_stripe_checkout_session_id` → `idx_payments_razorpay_order_id`
5. Add note about runtime migrations for existing deployments

**Specific Changes**:
- Line 70: Update `stripe_customer_id VARCHAR UNIQUE,` → `razorpay_customer_id VARCHAR UNIQUE,`
- Line 99: Update `stripe_customer_id VARCHAR UNIQUE,` → `razorpay_customer_id VARCHAR UNIQUE,`
- Update all index creation statements

### 2.2 Update repo-skills-CV.md

**File**: `docs/repo-skills-CV.md`

**Current Issues**:
- Line 56: "✅ Stripe integration (subscriptions + one-time payments)"
- Line 63: "`reframe/lib/stripe.ts` - Complete payment implementation"
- Line 109: "✅ Automated setup scripts (Stripe product creation)"
- Line 115: "Config files: `stripe.test.json`, `stripe.production.json`"
- Line 116: "Setup automation: `scripts/setup.ts`"
- Line 163: "**Stack:** Next.js 15, TypeScript, NextAuth, Stripe, Redis, Groq"
- Line 223: "| Stripe | ⭐⭐⭐⭐⭐ | Full implementation (subs + webhooks) |"

**Actions**:
1. Line 56: Change to "✅ Razorpay integration (subscriptions + one-time payments)"
2. Line 63: Change to "`reframe/lib/razorpay.ts` or payment routes - Complete payment implementation" (verify actual file location)
3. Line 109: Change to "✅ Automated setup scripts (Razorpay plan creation)"
4. Line 115: Remove or update to "Config files: Razorpay plan IDs configured via environment variables"
5. Line 116: Update to "Setup automation: `scripts/create_razorpay_plans.ts`" (if exists) or remove
6. Line 163: Change "Stripe" → "Razorpay"
7. Line 223: Change "Stripe" → "Razorpay"

### 2.3 Update migrate-to-self-hosted-oracle.md

**File**: `docs/migrate-to-self-hosted-oracle.md`

**Current Issues**:
- Lines 137-139: Stripe environment variable examples
- Lines 391-393: Stripe configuration examples
- Lines 448, 495: Stripe checklist items

**Actions**:
1. Remove or replace Stripe env var examples (lines 137-139) with Razorpay equivalents:
   ```yaml
   - RAZORPAY_KEY_ID=${RAZORPAY_KEY_ID}
   - RAZORPAY_KEY_SECRET=${RAZORPAY_KEY_SECRET}
   - RAZORPAY_WEBHOOK_SECRET=${RAZORPAY_WEBHOOK_SECRET}
   ```
2. Remove or replace Stripe config examples (lines 391-393) with Razorpay:
   ```
   RAZORPAY_KEY_ID=rzp_live_xxx
   RAZORPAY_KEY_SECRET=xxx
   RAZORPAY_WEBHOOK_SECRET=xxx
   ```
3. Update checklist items:
   - Line 448: "Stripe checkout works" → "Razorpay checkout works"
   - Line 495: "Stripe payments working" → "Razorpay payments working"

### 2.4 Update competitive-analysis-HONEST.md

**File**: `docs/competitive-analysis-HONEST.md`

**Current Issues**:
- Line 543: "Reframe: 6-tone system, Groq integration, Stripe payments"

**Actions**:
1. Change "Stripe payments" → "Razorpay payments" or "online payments via Razorpay"

### 2.5 Update Legal Documentation

#### 2.5.1 termsofservice.md

**File**: `docs/termsofservice.md`

**Current Issues**:
- Line 229: "Credit and debit cards (processed via Stripe)"

**Actions**:
1. Change to "Credit and debit cards (processed via Razorpay)" or "Credit and debit cards (processed securely by our payment processor)"

#### 2.5.2 privacypolicy.md

**File**: `docs/privacypolicy.md`

**Current Issues**:
- Line 60: "Payment details are processed securely by Stripe"
- Line 107: "**Payment Processors (Stripe):**" section header
- Line 221: "Stripe (payment processing and fraud detection)"
- Line 314: "**Transaction Details:** Via Stripe per their retention policy"
- Line 476-478: Stripe section with privacy policy link
- Line 653: "Our use of third-party service providers (e.g., Stripe, Setmore, Google Analytics)"

**Actions**:
1. Line 60: Change to "Payment details are processed securely by Razorpay" or "our payment processor"
2. Line 107: Change section header to "**Payment Processors (Razorpay):**"
3. Line 221: Change to "Razorpay (payment processing and fraud detection)"
4. Line 314: Change to "**Transaction Details:** Via Razorpay per their retention policy"
5. Lines 476-478: Replace Stripe section with Razorpay:
   ```
   **Razorpay:**
   - Privacy Policy: https://razorpay.com/privacy
   ```
6. Line 653: Change "Stripe" → "Razorpay"

#### 2.5.3 cancellationrefund.md

**File**: `docs/cancellationrefund.md`

**Current Issues**:
- Line 249: "**Stripe Processing:** 5-10 business days after we initiate refund"
- Line 250: "**Bank Processing:** 5-7 business days after Stripe processes"
- Line 262: "Stripe Balance: Credited to Stripe account"
- Line 307: "Payment processing fees (Stripe, bank charges)"
- Line 391: "Stripe processing fees: Non-refundable"

**Actions**:
1. Line 249: Change to "**Razorpay Processing:** 5-10 business days after we initiate refund"
2. Line 250: Change to "**Bank Processing:** 5-7 business days after Razorpay processes"
3. Line 262: Change to "Razorpay Balance: Credited to Razorpay account"
4. Line 307: Change to "Payment processing fees (Razorpay, bank charges)"
5. Line 391: Change to "Razorpay processing fees: Non-refundable"

---

## Phase 3: Daily-Cost Threshold Removal & Monitoring Alignment

### 3.1 Backend Monitoring Cleanup

#### 3.1.1 apps/ask/api/utils/groq_monitor.py

**Current Issues**:
- Function docstrings may still mention daily thresholds
- Comments may reference daily cost alerts

**Actions**:
1. Review all function docstrings (especially `check_groq_usage_alerts`, `get_daily_usage`, `get_monthly_usage`)
2. Remove any mentions of "daily cost threshold" or "daily alerts"
3. Update to clearly state "monthly cost monitoring" and "usage spike detection (by request count)"
4. Ensure `check_groq_usage_alerts` docstring only mentions monthly thresholds

#### 3.1.2 apps/reframe/backend/app/services/groq_monitor.py

**Current Issues**:
- May still have comments/log messages mentioning daily thresholds
- `_check_and_alert` function may reference daily costs

**Actions**:
1. Review all comments and log messages
2. Remove any "daily cost threshold" references
3. Update to only mention monthly cost monitoring
4. Ensure alert messages only reference monthly thresholds

#### 3.1.3 packages/shared-backend/cost-monitoring/alerts.py

**Current Issues**:
- Function signature and docstring for `check_groq_usage_alerts` may still mention daily threshold parameter
- Comments may reference daily cost monitoring

**Actions**:
1. Verify function signature: `check_groq_usage_alerts(db, GroqUsageModel, daily_cost_threshold=None, monthly_cost_threshold=None)`
2. Remove `daily_cost_threshold` parameter completely
3. Update function signature to: `check_groq_usage_alerts(db, GroqUsageModel, monthly_cost_threshold=None)`
4. Update docstring to remove daily threshold documentation
5. Update function body to remove all daily threshold logic
6. Update comments to describe monthly-only monitoring

### 3.2 Frontend Monitoring Cleanup

#### 3.2.1 packages/shared-frontend/src/cost-monitoring/groq-monitor.ts

**Current Issues**:
- Lines 15-19: Header comments mention `GROQ_DAILY_COST_THRESHOLD`
- Lines 194-202: Still has `DAILY_COST_THRESHOLD` constant and daily alert logic
- `checkAndAlert` function checks daily costs

**Actions**:
1. Remove `DAILY_COST_THRESHOLD` constant (line 19 or nearby)
2. Update header comments (lines 15-19) to:
   ```typescript
   // Alert thresholds (monthly only)
   // Note: This shared package uses unprefixed variables (GROQ_MONTHLY_COST_THRESHOLD) for cross-app compatibility.
   // Apps should set prefixed variables (ASK_GROQ_MONTHLY_COST_THRESHOLD, etc.) in their .env files,
   // but this shared package checks unprefixed variables as a fallback.
   const MONTHLY_COST_THRESHOLD = parseFloat(process.env.GROQ_MONTHLY_COST_THRESHOLD || "50.0"); // $50/month
   ```
3. Remove daily cost check from `checkAndAlert` function (lines 194-202)
4. Keep only monthly cost threshold check
5. Update function to only alert on monthly thresholds
6. Keep daily breakdown tracking for charts (but no alerts)

### 3.3 UI Component Review

**Files to check**:
- `apps/ask/frontend/app/admin/platform-dashboard/page.tsx`
- `apps/ask/frontend/components/platform-dashboard/*.tsx`
- `apps/reframe/app/page.tsx` (if has cost monitoring UI)
- Any other dashboard/cost monitoring UI components

**Actions**:
1. Search for text like "daily cost threshold", "daily budget", "daily alert"
2. Replace with "monthly cost threshold", "monthly budget", or generic "cost monitoring"
3. Update tooltips and labels to reflect monthly-only thresholds
4. Ensure charts still show daily breakdowns (for visualization) but don't reference daily limits

### 3.4 Cost Monitoring Documentation

#### 3.4.1 docs/COST_ANALYSIS.md

**File**: `docs/COST_ANALYSIS.md`

**Current Issues**:
- Line 510: "**Configurable**: Via `GROQ_DAILY_COST_THRESHOLD` and `GROQ_MONTHLY_COST_THRESHOLD` env vars"

**Actions**:
1. Remove `GROQ_DAILY_COST_THRESHOLD` from the list
2. Update to: "**Configurable**: Via `GROQ_MONTHLY_COST_THRESHOLD` env var"
3. Update line 509: "**Alerts**: Daily ($10) and monthly ($50) thresholds" → "**Alerts**: Monthly ($50) threshold and usage spike detection"

#### 3.4.2 docs/ENVIRONMENT_VARIABLES_REFERENCE.md

**File**: `docs/ENVIRONMENT_VARIABLES_REFERENCE.md`

**Current Issues**:
- Line 117: `ASK_GROQ_DAILY_COST_THRESHOLD` entry in table
- Line 276: `REFRAME_GROQ_DAILY_COST_THRESHOLD` entry in table

**Actions**:
1. Remove line 117: Delete the entire row for `ASK_GROQ_DAILY_COST_THRESHOLD`
2. Remove line 276: Delete the entire row for `REFRAME_GROQ_DAILY_COST_THRESHOLD`
3. Ensure only monthly threshold variables remain documented

#### 3.4.3 apps/ask/docs/COST_MONITORING_SETUP.md

**File**: `apps/ask/docs/COST_MONITORING_SETUP.md`

**Current Issues**:
- Line 92: `GROQ_DAILY_COST_THRESHOLD=10.0    # Alert if daily cost > $10`
- Line 156: "Adjust `GROQ_DAILY_COST_THRESHOLD` and `GROQ_MONTHLY_COST_THRESHOLD`"

**Actions**:
1. Remove line 92: Delete the `GROQ_DAILY_COST_THRESHOLD` example
2. Update line 156: Change to "Adjust `GROQ_MONTHLY_COST_THRESHOLD` based on your expected usage"
3. Update any narrative text that mentions "daily alerts" to describe monthly monitoring instead

---

## Phase 4: Script & Config File Cleanup

### 4.1 Verify reorganize-env-production.ps1

**File**: `apps/sketch2bim/scripts/reorganize-env-production.ps1`

**Actions**:
1. Review all comments in the file
2. Ensure no comments suggest Stripe support
3. Add comment if needed: "# Note: This script handles Razorpay-only payment configuration. Stripe is no longer supported."

### 4.2 Check for Stripe Config Files

**Actions**:
1. Search entire repo for files matching patterns:
   - `*stripe*.json`
   - `stripe-test-config.*`
   - `stripe.production.json`
   - `stripe.test.json`
2. For each file found:
   - If obsolete: Delete the file
   - If still needed conceptually: Rename and rewrite for Razorpay (unlikely)

### 4.3 Check Reframe setup.ts Script

**File**: `apps/reframe/scripts/setup.ts` (if exists)

**Actions**:
1. Check if `apps/reframe/scripts/setup.ts` exists
2. If it exists and references Stripe:
   - Either delete it (if obsolete)
   - Or rewrite it for Razorpay plan creation
3. Update `apps/reframe/package.json` line 12:
   - If setup.ts is deleted: Remove `"setup": "tsx scripts/setup.ts"` script
   - If rewritten: Keep script but verify it works with Razorpay

---

## Phase 5: Environment Variables & Dependencies

### 5.1 Environment Variable Consistency Check

**Files to verify**:
- `ask.env.production`
- `sketch2bim.env.production`
- `reframe.env.production`
- `render.yaml`

**Actions**:
1. For each `.env.production` file:
   - Verify no `STRIPE_*` variables exist
   - Verify no `*_GROQ_DAILY_COST_THRESHOLD` variables exist
   - Verify all Razorpay variables are present
   - Verify monthly Groq thresholds are present
2. For `render.yaml`:
   - Verify no Stripe env vars in any service
   - Verify no daily cost threshold vars
   - Cross-reference with `.env.production` files to ensure all needed vars are present
3. Document any discrepancies and fix them

### 5.2 Dependency Cleanup

#### 5.2.1 Check package.json files

**Files to check**:
- `apps/ask/frontend/package.json`
- `apps/reframe/package.json`
- `apps/sketch2bim/frontend/package.json` (if exists)
- Any other `package.json` files in the repo

**Actions**:
1. Search for `"stripe"` in dependencies or devDependencies
2. If found, remove the dependency
3. Note: `package-lock.json` will be regenerated on next `npm install`, so don't manually edit it

#### 5.2.2 Check requirements files

**Files to check**:
- `apps/ask/requirements.txt`
- `apps/ask/requirements-api.txt`
- `apps/sketch2bim/backend/requirements.txt`
- `apps/reframe/backend/requirements.txt` (if exists)
- `packages/shared-backend/requirements.txt` (if exists)

**Actions**:
1. Search for `stripe` package
2. If found, remove it

#### 5.2.3 Check for setup.ts References

**Actions**:
1. Search for references to `setup.ts` in:
   - `package.json` scripts
   - Documentation files
   - Other scripts or automation
2. For each reference:
   - If referring to deleted `apps/ask/scripts/setup.ts`: Remove or update the reference
   - If referring to `apps/reframe/scripts/setup.ts`: Verify it exists and update if needed

---

## Phase 6: Final Verification

### 6.1 Comprehensive Codebase Scans

**Actions**:
1. Run grep searches (excluding `node_modules`, `.git`, lockfiles):
   ```bash
   # Search for Stripe references
   grep -r -i "stripe" --exclude-dir=node_modules --exclude-dir=.git --exclude="*.lock" .
   
   # Search for daily cost threshold references
   grep -r -i "GROQ_DAILY_COST_THRESHOLD\|DAILY_COST_THRESHOLD" --exclude-dir=node_modules --exclude-dir=.git --exclude="*.lock" .
   ```

2. For each match found:
   - Categorize: Code, Documentation, Comments, Config
   - If in code: Fix immediately (shouldn't exist after previous phases)
   - If in docs: Update or remove
   - If in comments: Update to reflect current state
   - If in config: Remove or update

3. Create a report of all remaining references and their locations

### 6.2 Conceptual Verification

**For each app (ASK, Sketch2BIM, Reframe)**:

1. **Payment Flow Verification**:
   - Verify new Razorpay payments write to `razorpay_customer_id`, `razorpay_payment_id`, `razorpay_order_id`
   - Verify webhook handlers use new field names
   - Verify subscription management uses new field names

2. **Dashboard Verification**:
   - Verify cost dashboards show monthly cost data
   - Verify no UI elements reference "daily cost threshold" or "daily budget"
   - Verify charts still show daily breakdowns (for visualization) but don't have daily limits

3. **Migration Verification**:
   - Fresh database: SQL migrations create `razorpay_*` columns correctly
   - Existing database: Alembic migrations rename `stripe_*` → `razorpay_*` without data loss
   - Verify indexes are renamed correctly
   - Test migration rollback (downgrade) works

---

## Implementation Order

1. **Phase 1** (Runtime DB Migrations) - **CRITICAL** - Do first for production safety
2. **Phase 2** (Documentation) - Can be done in parallel with Phase 3
3. **Phase 3** (Daily-Cost Removal) - Can be done in parallel with Phase 2
4. **Phase 4** (Script Cleanup) - Can be done anytime
5. **Phase 5** (Env & Dependencies) - Should be done before Phase 6
6. **Phase 6** (Verification) - Do last to confirm everything is complete

---

## Success Criteria

✅ All database columns use `razorpay_*` naming (no `stripe_*`)
✅ All code references use `razorpay_*` field names
✅ All documentation mentions Razorpay (not Stripe)
✅ All legal docs reference Razorpay (not Stripe)
✅ No daily cost threshold configuration or alerts
✅ Only monthly cost thresholds are documented and used
✅ No Stripe dependencies in package.json or requirements.txt
✅ No references to deleted setup.ts scripts
✅ Environment variables are consistent across .env files and render.yaml
✅ Final grep scan shows no functional Stripe or daily-cost references (except in historical/audit docs if intentionally kept)

---

## Notes

- **Database Migrations**: Must be tested on staging before production deployment
- **Breaking Changes**: Removing daily cost thresholds is a breaking change - ensure all monitoring systems are updated
- **Documentation**: Some historical references may be intentionally kept in audit reports - verify before removing
- **Reframe**: May not have database payment fields - verify before creating migrations

