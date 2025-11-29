# Stripe Removal & Daily-Cost Deprecation - Remaining Implementation Plan

## Overview

This document outlines the **remaining work** to complete the platform-wide removal of Stripe references and deprecation of daily-cost monitoring across all three applications (ASK, Sketch2BIM, Reframe) and shared packages.

## Status Summary

### ✅ Completed Work

1. **Database Models & Code**
   - ✅ All database models updated (`apps/ask/api/models_db.py`, `apps/sketch2bim/backend/app/models.py`, `packages/shared-backend/database/models.py`, `packages/shared-backend/payments/models.py`)
   - ✅ All payment routes updated to use `razorpay_*` field names (`apps/ask/api/routes/payments.py`, `apps/sketch2bim/backend/app/routes/payments.py`)
   - ✅ SQL migrations and schema files updated (`database/migrations/*.sql`, `database/schemas/*.sql`)
   - ✅ Alembic initial migration updated for Sketch2BIM (`apps/sketch2bim/backend/alembic/versions/001_initial_schema.py`)

2. **Configuration & Infrastructure**
   - ✅ Config files updated (`apps/sketch2bim/backend/app/config.py` - removed Stripe fields)
   - ✅ `render.yaml` updated (removed Stripe environment variables)
   - ✅ Stripe setup script deleted (`apps/ask/scripts/setup.ts`)
   - ✅ Scripts updated (`apps/sketch2bim/scripts/reorganize-env-production.ps1`)

3. **Monitoring Code**
   - ✅ Backend monitoring updated (`apps/ask/api/utils/groq_monitor.py`, `apps/reframe/backend/app/services/groq_monitor.py`, `packages/shared-backend/cost-monitoring/alerts.py`)
   - ✅ Frontend monitoring updated (`packages/shared-frontend/src/cost-monitoring/groq-monitor.ts`)

### ⏳ Remaining Work

## Phase 1: Runtime Database Migrations

### 1.1 Create Alembic Migration for ASK

**File**: `apps/ask/alembic/versions/XXX_rename_stripe_to_razorpay.py` (new file)

**Purpose**: Rename existing database columns and indexes from `stripe_*` to `razorpay_*` for ASK application in production databases.

**Actions Required**:
1. Check if ASK has Alembic setup (may need to initialize if missing)
2. Create new migration file with:
   - Rename `users.stripe_customer_id` → `razorpay_customer_id`
   - Rename index `idx_users_stripe_customer_id` → `idx_users_razorpay_customer_id`
   - Rename `payments.stripe_payment_intent_id` → `razorpay_payment_id`
   - Rename index `idx_payments_stripe_payment_intent_id` → `idx_payments_razorpay_payment_id`
   - Rename `payments.stripe_checkout_session_id` → `razorpay_order_id`
   - Rename index `idx_payments_stripe_checkout_session_id` → `idx_payments_razorpay_order_id`

**SQL Operations**:
```sql
-- For ASK schema
SET search_path TO ask_schema, public;

-- Rename columns
ALTER TABLE users RENAME COLUMN stripe_customer_id TO razorpay_customer_id;
ALTER TABLE payments RENAME COLUMN stripe_payment_intent_id TO razorpay_payment_id;
ALTER TABLE payments RENAME COLUMN stripe_checkout_session_id TO razorpay_order_id;

-- Drop old indexes
DROP INDEX IF EXISTS idx_users_stripe_customer_id;
DROP INDEX IF EXISTS idx_payments_stripe_payment_intent_id;
DROP INDEX IF EXISTS idx_payments_stripe_checkout_session_id;

-- Create new indexes
CREATE INDEX IF NOT EXISTS idx_users_razorpay_customer_id ON users(razorpay_customer_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_payment_id ON payments(razorpay_payment_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_order_id ON payments(razorpay_order_id);
```

**Verification**:
- Test migration on staging database first
- Ensure data integrity (no data loss)
- Verify indexes are recreated correctly

### 1.2 Create Alembic Migration for Sketch2BIM

**File**: `apps/sketch2bim/backend/alembic/versions/011_rename_stripe_to_razorpay.py` (new file)

**Purpose**: Rename existing database columns and indexes from `stripe_*` to `razorpay_*` for Sketch2BIM application.

**Actions Required**:
1. Create new migration file (next in sequence after `010_remove_reader_type_column.py`)
2. Use same SQL operations as ASK but for `sketch2bim_schema`

**SQL Operations**:
```sql
-- For Sketch2BIM schema
SET search_path TO sketch2bim_schema, public;

-- Rename columns
ALTER TABLE users RENAME COLUMN stripe_customer_id TO razorpay_customer_id;
ALTER TABLE payments RENAME COLUMN stripe_payment_intent_id TO razorpay_payment_id;
ALTER TABLE payments RENAME COLUMN stripe_checkout_session_id TO razorpay_order_id;

-- Drop old indexes
DROP INDEX IF EXISTS idx_users_stripe_customer_id;
DROP INDEX IF EXISTS idx_payments_stripe_payment_intent_id;
DROP INDEX IF EXISTS idx_payments_stripe_checkout_session_id;

-- Create new indexes
CREATE INDEX IF NOT EXISTS idx_users_razorpay_customer_id ON users(razorpay_customer_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_payment_id ON payments(razorpay_payment_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_order_id ON payments(razorpay_order_id);
```

**Verification**:
- Test migration on staging database first
- Ensure data integrity
- Verify indexes are recreated correctly

### 1.3 Verify Reframe Database

**Purpose**: Confirm Reframe has no `stripe_*` database columns that need migration.

**Actions Required**:
1. Check Reframe database schema (if it has a database)
2. If `stripe_*` columns exist:
   - Create migration to rename them (similar to ASK/Sketch2BIM)
   - Or drop them if confirmed unused
3. If no database or no `stripe_*` columns:
   - Document that no migration needed

**Verification**:
- Query database schema to confirm no `stripe_*` columns exist
- Document findings

---

## Phase 2: Documentation Updates

### 2.1 Update DATABASE_MIGRATION_GUIDE.md

**File**: `.cursor/plans/docs/DATABASE_MIGRATION_GUIDE.md`

**Current Issues**:
- Lines 70, 99: Still show `stripe_customer_id` in SQL examples
- Schema examples need to be updated to show `razorpay_*` field names

**Actions Required**:
1. Update all SQL schema examples to use:
   - `razorpay_customer_id` instead of `stripe_customer_id`
   - `razorpay_payment_id` instead of `stripe_payment_intent_id`
   - `razorpay_order_id` instead of `stripe_checkout_session_id`
2. Update index names in examples:
   - `idx_users_razorpay_customer_id`
   - `idx_payments_razorpay_payment_id`
   - `idx_payments_razorpay_order_id`
3. Add section about runtime migrations for existing deployments
4. Update any narrative text that mentions "Stripe columns" to "Razorpay columns"

**Specific Changes**:
- Line 70: Change `stripe_customer_id VARCHAR UNIQUE,` → `razorpay_customer_id VARCHAR UNIQUE,`
- Line 99: Change `stripe_customer_id VARCHAR UNIQUE,` → `razorpay_customer_id VARCHAR UNIQUE,`
- Add migration instructions for existing databases

### 2.2 Update repo-skills-CV.md

**File**: `.cursor/plans/docs/repo-skills-CV.md`

**Current Issues**:
- Line 56: "✅ Stripe integration (subscriptions + one-time payments)"
- Line 63: "`reframe/lib/stripe.ts` - Complete payment implementation"
- Line 109: "✅ Automated setup scripts (Stripe product creation)"
- Line 115: "Config files: `stripe.test.json`, `stripe.production.json`"
- Line 163: "**Stack:** Next.js 15, TypeScript, NextAuth, Stripe, Redis, Groq"
- Line 223: "| Stripe | ⭐⭐⭐⭐⭐ | Full implementation (subs + webhooks) |"

**Actions Required**:
1. Replace all Stripe mentions with Razorpay:
   - "Stripe integration" → "Razorpay integration"
   - "Stripe product creation" → "Razorpay plan creation"
   - "stripe.test.json" → Remove or replace with "Razorpay configuration"
   - Update stack to show "Razorpay" instead of "Stripe"
2. Update evidence references:
   - Remove `reframe/lib/stripe.ts` reference (file doesn't exist or has been replaced)
   - Update to reflect Razorpay implementation files
3. Keep skill level ratings but update descriptions

**Specific Changes**:
- Line 56: "✅ Razorpay integration (subscriptions + one-time payments)"
- Line 63: Update to reference actual Razorpay implementation files
- Line 109: "✅ Automated setup scripts (Razorpay plan creation)"
- Line 115: Remove or update config file references
- Line 163: "**Stack:** Next.js 15, TypeScript, NextAuth, Razorpay, Redis, Groq"
- Line 223: "| Razorpay | ⭐⭐⭐⭐⭐ | Full implementation (subs + webhooks) |"

### 2.3 Update migrate-to-self-hosted-oracle.md

**File**: `.cursor/plans/docs/migrate-to-self-hosted-oracle.md`

**Current Issues**:
- Lines 137-139: Stripe environment variable examples
- Line 391-393: Stripe env var examples in configuration section
- Line 448: "Stripe checkout works" checklist item
- Line 495: "Stripe payments working" checklist item

**Actions Required**:
1. Remove all Stripe environment variable examples
2. Replace with Razorpay equivalents where relevant:
   - `RAZORPAY_KEY_ID`
   - `RAZORPAY_KEY_SECRET`
   - `RAZORPAY_WEBHOOK_SECRET`
3. Update checklist items:
   - "Stripe checkout works" → "Razorpay checkout works"
   - "Stripe payments working" → "Razorpay payments working"
4. Or remove payment-related checklist items if not relevant to Oracle migration

**Specific Changes**:
- Remove lines 137-139 (Stripe env vars in docker-compose)
- Remove or update lines 391-393 (Stripe env vars in .env example)
- Update line 448: "- [ ] Razorpay checkout works"
- Update line 495: "- [ ] Razorpay payments working"

### 2.4 Update competitive-analysis-HONEST.md

**File**: `.cursor/plans/docs/competitive-analysis-HONEST.md`

**Current Issues**:
- Line 543: "Reframe: 6-tone system, Groq integration, Stripe payments"

**Actions Required**:
1. Update to reflect Razorpay:
   - "Stripe payments" → "Razorpay payments" or "online payments via Razorpay"

**Specific Changes**:
- Line 543: "Reframe: 6-tone system, Groq integration, Razorpay payments"

### 2.5 Update Legal Documentation

#### 2.5.1 termsofservice.md

**File**: `.cursor/plans/docs/termsofservice.md`

**Current Issues**:
- Line 229: "Credit and debit cards (processed via Stripe)"

**Actions Required**:
1. Replace with Razorpay wording:
   - "Credit and debit cards (processed via Razorpay)" or generic "secure payment processor"

**Specific Changes**:
- Line 229: "Credit and debit cards (processed via Razorpay)"

#### 2.5.2 privacypolicy.md

**File**: `.cursor/plans/docs/privacypolicy.md`

**Current Issues**:
- Line 60: "Payment details are processed securely by Stripe"
- Line 107: "**Payment Processors (Stripe):**" section header
- Line 221: "Stripe (payment processing and fraud detection)"
- Line 314: "**Transaction Details:** Via Stripe per their retention policy"
- Line 476-478: Stripe section with privacy policy link
- Line 653: "Our use of third-party service providers (e.g., Stripe, Setmore, Google Analytics)"

**Actions Required**:
1. Replace all Stripe mentions with Razorpay:
   - Update payment processor section to reference Razorpay
   - Remove Stripe privacy policy link
   - Add Razorpay privacy policy link if available
   - Update third-party providers list

**Specific Changes**:
- Line 60: "Payment details are processed securely by Razorpay"
- Line 107: "**Payment Processors (Razorpay):**"
- Line 221: "Razorpay (payment processing and fraud detection)"
- Line 314: "**Transaction Details:** Via Razorpay per their retention policy"
- Line 476-478: Replace with Razorpay section and privacy policy link
- Line 653: "Our use of third-party service providers (e.g., Razorpay, Setmore, Google Analytics)"

#### 2.5.3 cancellationrefund.md

**File**: `.cursor/plans/docs/cancellationrefund.md`

**Current Issues**:
- Line 249: "**Stripe Processing:** 5-10 business days"
- Line 250: "**Bank Processing:** 5-7 business days after Stripe processes"
- Line 262: "Stripe Balance: Credited to Stripe account"
- Line 307: "Payment processing fees (Stripe, bank charges)"
- Line 391: "Stripe processing fees: Non-refundable"

**Actions Required**:
1. Replace all Stripe references with Razorpay:
   - Update processing timelines to reflect Razorpay's actual processing times
   - Update balance/account references
   - Update fee descriptions

**Specific Changes**:
- Line 249: "**Razorpay Processing:** 5-10 business days" (verify actual Razorpay timeline)
- Line 250: "**Bank Processing:** 5-7 business days after Razorpay processes"
- Line 262: "Razorpay Balance: Credited to Razorpay account"
- Line 307: "Payment processing fees (Razorpay, bank charges)"
- Line 391: "Razorpay processing fees: Non-refundable"

---

## Phase 3: Daily-Cost Removal & Monitoring Alignment

### 3.1 Backend Monitoring - Comments & Docstrings

#### 3.1.1 apps/ask/api/utils/groq_monitor.py

**Current Status**: Daily threshold logic removed, but need to verify comments/docstrings

**Actions Required**:
1. Review all function docstrings
2. Remove any mentions of "daily threshold" or "daily cost alerts"
3. Update to clearly describe **monthly-only** thresholds
4. Update usage spike detection to clarify it's based on request count, not daily cost

**Specific Areas to Check**:
- `check_groq_usage_alerts()` function docstring
- `get_daily_usage()` function docstring (may need to clarify this is for reporting, not alerts)
- Any inline comments about daily monitoring

#### 3.1.2 apps/reframe/backend/app/services/groq_monitor.py

**Current Status**: Daily threshold logic removed

**Actions Required**:
1. Review all log messages and comments
2. Ensure all references talk only about monthly costs
3. Remove any "daily cost limit" or "daily threshold" language
4. Update `_check_and_alert()` function comments

**Specific Areas to Check**:
- `track_groq_usage()` function comments
- `_check_and_alert()` function comments
- Print/log statements (line 97, 107)

#### 3.1.3 packages/shared-backend/cost-monitoring/alerts.py

**Current Status**: Daily threshold parameter removed from function signature

**Actions Required**:
1. Review public API docstrings
2. Ensure no mention of daily threshold parameter
3. Clearly document monthly-only behavior
4. Update function signature documentation

**Specific Areas to Check**:
- `check_groq_usage_alerts()` function docstring
- Module-level comments about thresholds
- Any examples or usage documentation

### 3.2 Frontend Monitoring

#### 3.2.1 packages/shared-frontend/src/cost-monitoring/groq-monitor.ts

**Current Status**: Daily threshold logic partially removed, but still has `DAILY_COST_THRESHOLD` usage

**Current Issues**:
- Line 19: Still references `GROQ_DAILY_COST_THRESHOLD` in comments (may be removed already)
- Line 194-199: Still has daily cost alert logic using `DAILY_COST_THRESHOLD`

**Actions Required**:
1. Remove `DAILY_COST_THRESHOLD` constant completely
2. Remove daily cost alert logic from `checkAndAlert()` function (lines 194-206)
3. Update header comments to remove `GROQ_DAILY_COST_THRESHOLD` references
4. Position module as "monthly-cost monitoring with daily breakdowns for charts"
5. Keep daily breakdown functions (for charting) but remove alert logic

**Specific Changes**:
- Remove line 19: `const DAILY_COST_THRESHOLD = ...`
- Remove lines 194-206: Daily cost alert check in `checkAndAlert()`
- Update header comment to clarify monthly-only alerts
- Keep `getDailyUsageRedis()` and daily breakdown functions (for UI charts)

#### 3.2.2 UI Components Review

**Purpose**: Check ASK, Reframe, and platform dashboard components for daily cost threshold/alerts UI

**Files to Check**:
- `apps/ask/frontend/components/platform-dashboard/*.tsx`
- `apps/reframe/app/*.tsx` (if has cost dashboard)
- Any admin/cost monitoring pages

**Actions Required**:
1. Search for strings like:
   - "daily cost threshold"
   - "daily budget"
   - "daily alert"
   - "daily limit"
2. Update UI copy to:
   - Monthly thresholds only
   - Generic "usage monitoring" or "cost monitoring"
   - "Recent daily breakdown" (for charts, not alerts)

**Specific Areas**:
- Tooltips
- Labels
- Error messages
- Help text
- Dashboard cards/tiles

### 3.3 Cost Monitoring Documentation

#### 3.3.1 COST_ANALYSIS.md

**File**: `.cursor/plans/docs/COST_ANALYSIS.md`

**Current Issues**:
- Line 510: "**Configurable**: Via `GROQ_DAILY_COST_THRESHOLD` and `GROQ_MONTHLY_COST_THRESHOLD` env vars"

**Actions Required**:
1. Remove `GROQ_DAILY_COST_THRESHOLD` from the list
2. Update to only mention monthly thresholds
3. Update narrative text about "daily alerts" to "monthly monitoring"

**Specific Changes**:
- Line 510: "**Configurable**: Via `GROQ_MONTHLY_COST_THRESHOLD` env var"
- Update any other mentions of daily alerts in the document

#### 3.3.2 ENVIRONMENT_VARIABLES_REFERENCE.md

**File**: `.cursor/plans/docs/ENVIRONMENT_VARIABLES_REFERENCE.md`

**Current Issues**:
- Line 117: `ASK_GROQ_DAILY_COST_THRESHOLD` entry in table
- Line 276: `REFRAME_GROQ_DAILY_COST_THRESHOLD` entry in table

**Actions Required**:
1. Remove both `*_GROQ_DAILY_COST_THRESHOLD` rows from tables
2. Ensure monthly threshold rows are clearly documented
3. Add note that daily thresholds are no longer supported

**Specific Changes**:
- Remove line 117: `| ASK_GROQ_DAILY_COST_THRESHOLD | Daily cost threshold | 10.0 |`
- Remove line 276: `| REFRAME_GROQ_DAILY_COST_THRESHOLD | Daily cost threshold | 10.0 |`
- Keep monthly threshold rows

#### 3.3.3 apps/ask/docs/COST_MONITORING_SETUP.md

**File**: `.cursor/plans/apps/ask/docs/COST_MONITORING_SETUP.md`

**Current Issues**:
- Line 92: `GROQ_DAILY_COST_THRESHOLD=10.0    # Alert if daily cost > $10`
- Line 156: "Adjust `GROQ_DAILY_COST_THRESHOLD` and `GROQ_MONTHLY_COST_THRESHOLD`"

**Actions Required**:
1. Remove `GROQ_DAILY_COST_THRESHOLD` from environment variable examples
2. Update instructions to only mention monthly thresholds
3. Rewrite narrative about "daily alerts" to "monthly monitoring"

**Specific Changes**:
- Remove line 92: `GROQ_DAILY_COST_THRESHOLD=10.0    # Alert if daily cost > $10`
- Line 156: "Adjust `GROQ_MONTHLY_COST_THRESHOLD` based on your expected usage"
- Update any other mentions of daily thresholds

---

## Phase 4: Environment & Dependency Consistency

### 4.1 Environment Variable Verification

**Files to Check**:
- `ask.env.production`
- `sketch2bim.env.production`
- `reframe.env.production`
- `render.yaml`

**Actions Required**:
1. Verify no `STRIPE_*` environment variables exist in any file
2. Verify no `*_GROQ_DAILY_COST_THRESHOLD` variables exist
3. Ensure all Razorpay variables are present:
   - `*_RAZORPAY_KEY_ID`
   - `*_RAZORPAY_KEY_SECRET`
   - `*_RAZORPAY_WEBHOOK_SECRET`
   - `*_RAZORPAY_*_AMOUNT` (week, month, year)
   - `*_RAZORPAY_PLAN_*` (week, month, year)
4. Ensure all monthly Groq thresholds are present:
   - `*_GROQ_MONTHLY_COST_THRESHOLD`
5. Cross-reference `render.yaml` with `.env.production` files to ensure consistency

**Verification Checklist**:
- [ ] No `STRIPE_*` vars in `ask.env.production`
- [ ] No `STRIPE_*` vars in `sketch2bim.env.production`
- [ ] No `STRIPE_*` vars in `reframe.env.production`
- [ ] No `STRIPE_*` vars in `render.yaml`
- [ ] No `*_GROQ_DAILY_COST_THRESHOLD` in any env file
- [ ] All Razorpay vars present in all files
- [ ] All monthly Groq thresholds present
- [ ] `render.yaml` matches `.env.production` files

### 4.2 Dependency Checks

**Files to Check**:
- `apps/ask/frontend/package.json`
- `apps/reframe/package.json`
- `apps/sketch2bim/backend/requirements.txt`
- `apps/ask/requirements*.txt`
- `apps/reframe/backend/requirements.txt` (if exists)
- Any other `package.json` or `requirements*.txt` files

**Actions Required**:
1. Search for `stripe` dependency in all package.json files
2. Search for `stripe` in all requirements.txt files
3. Remove any active `stripe` dependencies
4. Note: `node_modules` and `package-lock.json` will be regenerated on next `npm install`

**Verification Checklist**:
- [ ] No `stripe` in `apps/ask/frontend/package.json`
- [ ] No `stripe` in `apps/reframe/package.json`
- [ ] No `stripe` in any `requirements*.txt` files
- [ ] Document any found dependencies for removal

### 4.3 Script References Check

**Purpose**: Ensure deleted `apps/ask/scripts/setup.ts` is not referenced anywhere

**Files to Check**:
- All `package.json` files for `"setup"` script
- Documentation files that mention setup scripts
- Any automation/CI files

**Actions Required**:
1. Search for references to `setup.ts` or `scripts/setup`
2. Search for `npm run setup` or similar commands
3. Remove or update references:
   - Remove script from `package.json` if exists
   - Update documentation
   - Update CI/automation if needed

**Verification Checklist**:
- [ ] No `"setup"` script in any `package.json` pointing to deleted file
- [ ] No documentation references to `setup.ts`
- [ ] No CI/automation references

---

## Phase 5: Final Verification & Testing

### 5.1 Codebase Scans

**Purpose**: Final verification that no Stripe or daily-cost references remain

**Scans to Run**:
1. **Stripe references**:
   ```bash
   grep -r "stripe\|Stripe\|STRIPE" --exclude-dir=node_modules --exclude="*.lock" .
   ```
2. **Daily cost threshold references**:
   ```bash
   grep -r "GROQ_DAILY_COST_THRESHOLD\|DAILY_COST_THRESHOLD" --exclude-dir=node_modules --exclude="*.lock" .
   ```

**Actions Required**:
1. Run both grep commands
2. Review all matches
3. Categorize matches:
   - **Acceptable**: Historical/audit reports, vendored code, false positives (e.g., "Pinstripe" font)
   - **Needs Fix**: Functional code, active documentation, configuration
4. Fix all "Needs Fix" matches

**Verification Checklist**:
- [ ] No functional code uses Stripe
- [ ] No active documentation mentions Stripe (except historical context)
- [ ] No configuration files reference Stripe
- [ ] No daily cost threshold logic remains
- [ ] All matches reviewed and categorized

### 5.2 Conceptual Smoke Tests

**Purpose**: Verify system behavior after all changes

**For Each App (ASK, Sketch2BIM, Reframe)**:

#### 5.2.1 Payment Flow Verification

**Test**: New Razorpay subscriptions and one-time payments

**Expected Behavior**:
- Payments are recorded with `razorpay_customer_id` in `users` table
- Payments are recorded with `razorpay_payment_id` and `razorpay_order_id` in `payments` table
- No errors related to missing `stripe_*` columns
- Webhooks process correctly

**Verification Checklist**:
- [ ] ASK: Test one-time payment → verify `razorpay_*` columns populated
- [ ] ASK: Test subscription → verify `razorpay_*` columns populated
- [ ] Sketch2BIM: Test one-time payment → verify `razorpay_*` columns populated
- [ ] Sketch2BIM: Test subscription → verify `razorpay_*` columns populated
- [ ] Reframe: Test payment flow (if applicable) → verify correct behavior

#### 5.2.2 Dashboard Verification

**Test**: Admin and cost dashboards render correctly

**Expected Behavior**:
- Dashboards show monthly cost and usage data
- No UI references to "daily cost threshold" or "daily alerts"
- Charts may show daily breakdowns (for visualization) but no daily limits/alerts
- Monthly threshold alerts work correctly

**Verification Checklist**:
- [ ] ASK platform dashboard loads correctly
- [ ] ASK platform dashboard shows monthly costs only
- [ ] ASK platform dashboard has no "daily threshold" UI elements
- [ ] Sketch2BIM admin dashboard (if exists) shows monthly costs
- [ ] Reframe dashboard (if exists) shows monthly costs
- [ ] All dashboards render without errors

#### 5.2.3 Database Migration Verification

**Test**: Migrations work on fresh and existing databases

**Fresh Database Test**:
- Run SQL migrations (`database/migrations/*.sql`)
- Verify tables created with `razorpay_*` columns
- Verify indexes created correctly
- No `stripe_*` columns exist

**Existing Database Test**:
- Database has `stripe_*` columns with data
- Run Alembic migrations (ASK and Sketch2BIM)
- Verify columns renamed correctly
- Verify data preserved (no data loss)
- Verify indexes recreated correctly
- Verify application still works after migration

**Verification Checklist**:
- [ ] Fresh DB: SQL migrations create `razorpay_*` columns
- [ ] Fresh DB: No `stripe_*` columns exist
- [ ] Existing DB: Alembic migration renames columns
- [ ] Existing DB: Data preserved (spot check sample records)
- [ ] Existing DB: Indexes recreated correctly
- [ ] Existing DB: Application works after migration

---

## Implementation Order

### Recommended Sequence

1. **Phase 1: Runtime DB Migrations** (Critical - affects production)
   - Create and test migrations on staging first
   - Deploy to production after verification

2. **Phase 2: Documentation Updates** (Can be done in parallel)
   - Update all docs to reflect Razorpay
   - Update legal docs

3. **Phase 3: Daily-Cost Removal** (Code cleanup)
   - Backend monitoring comments/docstrings
   - Frontend monitoring code
   - Cost monitoring docs

4. **Phase 4: Environment & Dependency Checks** (Configuration)
   - Verify env files
   - Remove dependencies
   - Check script references

5. **Phase 5: Final Verification** (Quality assurance)
   - Run scans
   - Conceptual testing
   - Document completion

---

## Success Criteria

### Completion Checklist

- [ ] All runtime DB migrations created and tested
- [ ] All documentation updated (no Stripe references, no daily-cost thresholds)
- [ ] All monitoring code updated (monthly-only, no daily threshold logic)
- [ ] All environment files verified (no Stripe, no daily-cost vars)
- [ ] All dependencies removed (no Stripe packages)
- [ ] All script references updated (no deleted setup.ts references)
- [ ] Final scans show no functional Stripe/daily-cost usage
- [ ] Conceptual tests pass (payments, dashboards, migrations)

### Definition of Done

The Stripe removal and daily-cost deprecation is complete when:

1. **Code**: No functional code uses Stripe or daily-cost thresholds
2. **Database**: All columns/indexes use `razorpay_*` naming, migrations tested
3. **Documentation**: All docs reflect Razorpay-only and monthly-only monitoring
4. **Configuration**: All env files and configs use Razorpay, no Stripe vars
5. **Dependencies**: No Stripe packages in dependencies
6. **Testing**: All conceptual tests pass, migrations work on fresh and existing DBs

---

## Notes

- **Backward Compatibility**: Runtime migrations must preserve existing data
- **Testing**: Always test migrations on staging before production
- **Documentation**: Keep historical context where appropriate (e.g., audit reports)
- **False Positives**: Some matches may be false positives (e.g., "Pinstripe" font name)
- **Vendored Code**: Ignore `node_modules` and lockfiles in scans
- **Platform-Wide**: All changes apply to ASK, Sketch2BIM, and Reframe equally

---

## Estimated Effort

- **Phase 1 (DB Migrations)**: 2-3 hours (including testing)
- **Phase 2 (Documentation)**: 2-3 hours
- **Phase 3 (Monitoring Cleanup)**: 1-2 hours
- **Phase 4 (Env/Dependencies)**: 1 hour
- **Phase 5 (Verification)**: 1-2 hours

**Total Estimated Time**: 7-11 hours

---

## Risk Assessment

### Low Risk
- Documentation updates
- Comment/docstring updates
- Environment variable verification

### Medium Risk
- Frontend monitoring code changes (may affect UI)
- UI component updates (may affect user experience)

### High Risk
- Runtime database migrations (data loss risk)
- Production deployment of migrations

### Mitigation
- Test all migrations on staging first
- Backup databases before migration
- Have rollback plan for migrations
- Test payment flows thoroughly after changes

