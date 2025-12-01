# All Phases - Remaining Tasks

This file consolidates all remaining tasks across all phases. For detailed information, see individual phase files.

---

# Phase 0: Pre-Implementation Verification

**Status**: 🟡 Partial (95% Complete)

**Remaining**: Build verification fixes for Vercel deployment.

## Action Items

- [ ] Update `packages/design-system/package.json` peer dependency: `"next": "^14.0.0 || ^15.0.0"`
- [ ] Verify `packages/design-system` is committed as normal source (not a submodule)
- [ ] Configure Vercel build settings:
  - [ ] Set Install Command to: `npm install --legacy-peer-deps`
  - [ ] Set Build Command to: `npm run build` (or custom `vercel-build` script)
- [ ] Test deployment on Vercel
- [ ] Verify subdomain routing works after successful build

---

# Phase 1: Platform Consolidation

**Status**: 🟡 Partial (90% Complete)  
**Priority**: **CRITICAL**

## Remaining Tasks

### 1.5 Import Path Fixes ⚠️ **CRITICAL**

- [ ] Update all Reframe app routes (`app/reframe/*.tsx`) import paths
- [ ] Remove duplicate `app/reframe/api/` directory (use `app/api/reframe/` instead)
- [ ] Update all Sketch2BIM app routes import paths
- [ ] Verify ASK app routes import paths
- [ ] Verify all component files use correct internal imports

### 1.6 Auth Configuration Updates

- [ ] Verify auth.ts files work with current configuration
- [ ] Test authentication flow from each app route
- [ ] Verify centralized auth at `kvshvl.in/api/auth/*` works for all apps

### 1.7 API Call Updates

- [ ] Update all API client files to use unified backend
- [ ] Add `NEXT_PUBLIC_PLATFORM_API_URL` to Vercel environment variables
- [ ] Update all API calls in components and pages
- [ ] Test API endpoints work correctly

### 1.8 Backend Route Migration

- [ ] Verify all ASK backend routes work in unified backend
- [ ] Verify all Reframe backend routes work in unified backend
- [ ] Verify all Sketch2BIM backend routes work in unified backend
- [ ] Test each router works correctly

### 1.9 Subscription System Implementation

- [ ] Implement subscription checking logic in middleware
- [ ] Test subscription checkout flow
- [ ] Test subscription status checking
- [ ] Verify subscription utilities work with unified model

### 1.10 Environment Variables & Configuration

- [ ] Verify all required frontend variables set in Vercel
- [ ] Verify all required backend variables set in Render
- [ ] Document all required environment variables

### 1.11 Testing & Migration

- [ ] Local testing (all routes, auth, API calls, subscriptions)
- [ ] Staging deployment and testing
- [ ] Production migration
- [ ] Update Razorpay webhook URLs
- [ ] Monitor for 1-2 weeks

### 1.12 Cleanup (After 1-2 weeks of successful operation)

- [ ] Remove old Vercel projects
- [ ] Remove old Render services
- [ ] Archive old code directories
- [ ] Clean up dependencies
- [ ] Update documentation

---

# Phase 1: Database & Infrastructure (Legacy)

**Status**: ⏳ Pending (0%)

## Remaining Tasks

### 1.1 Stripe to Razorpay Database Migrations

- [ ] Create ASK Alembic migration to rename `stripe_*` columns to `razorpay_*`
- [ ] Create Sketch2BIM Alembic migration to rename `stripe_*` columns to `razorpay_*`
- [ ] Check if Reframe has any `stripe_*` database fields and create migration if needed
- [ ] Test migrations on staging database first
- [ ] Verify data integrity after migration

### 1.2 Upstash Postgres Migration

- [ ] Export Supabase backups (ASK and Sketch2BIM schemas and data)
- [ ] Create two Upstash Postgres databases
- [ ] Run schema migrations on Upstash databases
- [ ] Import data from Supabase backups
- [ ] Update environment variables with Upstash connection strings
- [ ] Test locally with Upstash databases
- [ ] Deploy to production
- [ ] Monitor for 1 week before deprovisioning Supabase

---

# Phase 2: Code Standardization & Cleanup

**Status**: 🟡 Partial (50%)

## Remaining Tasks

### 2.3 Backend Migration to Shared Components

- [ ] Migrate `apps/ask/api/main.py` to use `shared_backend.api.factory.create_app`
- [ ] Migrate `apps/ask/api/models_db.py` to extend `BaseUser` and `BasePayment`
- [ ] Migrate `apps/sketch2bim/backend/app/main.py` to use FastAPI factory
- [ ] Preserve custom middleware (correlation, timeout, security headers)
- [ ] Migrate models to extend base models
- [ ] Test all routes work correctly

### 2.4 Frontend Migration to Shared Components

- [ ] Migrate ASK settings page to use shared components
- [ ] Migrate Sketch2BIM settings page to use shared components
- [ ] Migrate Reframe settings page to use shared components
- [ ] Preserve app-specific features (data export, account deletion, etc.)
- [ ] Migrate all pricing pages to use shared payment utilities
- [ ] Replace inline Razorpay script loading with shared utilities
- [ ] Test all payment flows and subscription management

---

# Phase 3: Environment Variables & Configuration

**Status**: 🟡 Partial (66%)

## Remaining Tasks

### 3.1 Environment Variable Verification

- [ ] Verify Render services have all prefixed variables
- [ ] Verify Vercel projects have all prefixed variables
- [ ] Remove any unprefixed variables
- [ ] Verify no `STRIPE_*` variables exist
- [ ] Verify no `*_GROQ_DAILY_COST_THRESHOLD` variables exist
- [ ] Update `.env.example` template file to match `.env.local` structure
- [ ] Update developer documentation

### 3.2 Backward Compatibility Removal

- [ ] Remove `/add-credits` endpoints (if not needed for admin)
- [ ] Remove legacy generate endpoint models (if not used)
- [ ] Remove "backward compatibility" comments from env templates
- [ ] Update config file comments
- [ ] Update route comments

---

# Phase 4: Documentation Updates

**Status**: ⏳ Pending (0%)

## Remaining Tasks

### 4.1 Stripe → Razorpay Documentation

- [ ] Update `docs/DATABASE_MIGRATION_GUIDE.md` - Update SQL examples
- [ ] Update `docs/repo-skills-CV.md` - Replace Stripe mentions
- [ ] Update `docs/migrate-to-self-hosted-oracle.md` - Update env var examples
- [ ] Update `docs/competitive-analysis-HONEST.md` - Update payment processor mentions
- [ ] Update `docs/termsofservice.md` - Update payment processor references
- [ ] Update `docs/privacypolicy.md` - Replace Stripe section with Razorpay
- [ ] Update `docs/cancellationrefund.md` - Update processing timelines

### 4.2 Cost Monitoring Documentation

- [ ] Update `docs/COST_ANALYSIS.md` - Remove daily threshold references
- [ ] Update `docs/ENVIRONMENT_VARIABLES_REFERENCE.md` - Remove daily threshold entries
- [ ] Update `apps/ask/docs/COST_MONITORING_SETUP.md` - Remove daily threshold examples

### 4.3 Migration Guides

- [ ] Create `docs/migrations/ASK_MIGRATION_GUIDE.md`
- [ ] Create `docs/migrations/SKETCH2BIM_MIGRATION_GUIDE.md`
- [ ] Create `docs/migrations/REFRAME_MIGRATION_GUIDE.md`

---

# Phase 5: Testing & Verification

**Status**: ⏳ Pending (0%)

## Remaining Tasks

### 5.1 Pricing Unification Verification

- [ ] Verify checkout routes support all tiers (week/monthly/yearly)
- [ ] Verify webhook handlers correctly identify all tiers
- [ ] Verify subscription duration logic includes weekly
- [ ] Verify Razorpay dashboard shows unified plan IDs
- [ ] Test end-to-end payment flows for all tiers

### 5.2 Comprehensive Codebase Scans

- [ ] Search for remaining Stripe references (excluding node_modules, .git, lockfiles)
- [ ] Categorize: Code, Documentation, Comments, Config
- [ ] Fix all functional code references
- [ ] Update documentation
- [ ] Search for `GROQ_DAILY_COST_THRESHOLD` or `DAILY_COST_THRESHOLD`
- [ ] Remove from code, update documentation

### 5.3 Conceptual Verification

**Payment Flow Tests**:
- [ ] Create subscription for each tier (week/monthly/yearly)
- [ ] Verify webhook receives correct tier information
- [ ] Verify database records use `razorpay_*` fields (not `stripe_*`)
- [ ] Verify subscription duration matches tier (7/30/365 days)
- [ ] Test payment failure scenarios
- [ ] Test subscription cancellation

**Cost Monitoring Tests**:
- [ ] Verify monthly cost threshold alerts trigger correctly
- [ ] Verify daily cost threshold alerts do NOT exist
- [ ] Test cost aggregation across all apps
- [ ] Verify cost dashboard displays correctly

**Database Migration Tests**:
- [ ] Test migration on fresh database
- [ ] Test migration on database with existing `stripe_*` columns
- [ ] Test migration on database already using `razorpay_*` columns
- [ ] Test rollback (downgrade) procedure
- [ ] Verify data integrity after migration

**Infrastructure Tests**:
- [ ] Verify all health endpoints respond (`/health`)
- [ ] Test authentication flow (sign in, sign out)
- [ ] Verify OAuth redirects work correctly
- [ ] Test API endpoints with new configuration
- [ ] Verify environment variables are correctly loaded

---

# Phase 6: Dependency & Script Cleanup

**Status**: ✅ Complete (100%)

**Nothing left to do in this phase.**
