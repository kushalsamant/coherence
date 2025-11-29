# Complete Platform Implementation Plan

## 📑 Table of Contents

**Quick Navigation**:
- [Platform Overview](#platform-overview) - Architecture and structure
- [Progress Summary](#progress-summary--remaining-tasks) - Current status and completed work
- [Quick Start Execution Guide](#quick-start-execution-guide) - ⚡ **START HERE** for immediate actions
- [Implementation Phases](#implementation-phases-detailed) - Detailed phase breakdown
- [Success Criteria](#success-criteria) - Definition of done
- [Reference Material](#reference-material-appendices) - Deployment guides, templates, and documentation

**Phase Quick Links**:
- [Phase 0: Verification](#phase-0-pre-implementation-verification--complete) ✅
- [Phase 1: Database & Infrastructure](#phase-1-critical-database--infrastructure--pending) ⏳
- [Phase 2: Code Standardization](#phase-2-code-standardization--cleanup--partial) 🟡
- [Phase 3: Configuration](#phase-3-environment-variables--configuration--partial) 🟡
- [Phase 4: Documentation](#phase-4-documentation-updates--pending) ⏳
- [Phase 5: Testing](#phase-5-testing--verification--pending) ⏳
- [Phase 6: Cleanup](#phase-6-dependency--script-cleanup--pending) ⏳

---

## Platform Overview

### KVSHVL Platform Monorepo

Unified monorepo for KVSHVL platform applications: ASK, Sketch2BIM, and Reframe.

#### Repository Structure

```
kushalsamant.github.io/
├── packages/              # Shared packages
│   ├── shared-backend/    # Python shared code (auth, payments, database, etc.)
│   ├── shared-frontend/   # TypeScript shared code (auth, payments, etc.)
│   └── design-system/     # Design template component library
├── apps/                  # Applications
│   ├── ask/               # ASK
│   ├── sketch2bim/        # Sketch2BIM
│   └── reframe/           # Reframe
└── database/              # Database migrations and schemas
```

#### Platform Architecture

**Applications**:
- `apps/ask`: *ASK: Daily Research* – content Q&A + platform admin dashboard
- `apps/sketch2bim`: Sketch-to-BIM conversion backend + Next.js frontend
- `apps/reframe`: Text reframing service (backend + frontend)

**Shared Code**:
- `packages/shared-backend`: auth, payments (Razorpay), subscription helpers, cost tracking, and configuration utilities
- `packages/shared-frontend`: shared auth/payment helpers for the frontends
- `packages/design-system`: UI component library used by the Next.js apps

**Cost Tracking**:
- **ASK / Sketch2BIM**: Store detailed cost data in Postgres (Supabase or Upstash Postgres) using app-specific schemas (`ask_schema`, `sketch2bim_schema`) or separate databases
- **Reframe**: Tracks Groq usage and cost aggregates in Upstash Redis
- Shared Razorpay plan IDs and pricing are documented in `docs/ENVIRONMENT_VARIABLES_REFERENCE.md` and wired via `render.yaml`
- **Database Migration**: See Phase 1.2 for migrating from Supabase to Upstash Postgres

**Admin Dashboard**:
- Implemented in `apps/ask/frontend` under `/admin/platform-dashboard`
- Talks to ASK backend feasibility and monitoring endpoints:
  - `/api/feasibility/platform/*` for platform-wide economics
  - `/api/monitoring/*` for cost, usage, and alert summaries

#### Database Architecture

The platform uses PostgreSQL databases. Two deployment options are supported:

**Option 1: Supabase (Current)**:
- Shared PostgreSQL database with separate schemas:
  - `ask_schema`: ASK application tables
  - `sketch2bim_schema`: Sketch2BIM application tables

**Option 2: Upstash Postgres (Recommended for consolidation)**:
- Separate databases (one per application):
  - ASK database: All ASK tables in `public` schema
  - Sketch2BIM database: All Sketch2BIM tables in `public` schema
- See Phase 1.2 for migration instructions

#### Deployment Architecture

Each application deploys independently:
- **ASK**: Frontend on Vercel, Backend on Render
- **Sketch2BIM**: Frontend on Vercel, Backend on Render
- **Reframe**: Next.js app on Vercel

#### Shared Packages

**Backend Packages**:
- `shared-backend/auth`: Authentication utilities (JWT, user dependencies)
- `shared-backend/payments`: Razorpay integration and webhook handling
- `shared-backend/database`: Database models and schema utilities
- `shared-backend/subscription`: Subscription management
- `shared-backend/cost-monitoring`: Cost tracking and alerts
- `shared-backend/config`: Shared configuration

**Frontend Packages**:
- `shared-frontend/auth`: NextAuth configuration
- `shared-frontend/payments`: Razorpay client utilities
- `shared-frontend/cost-monitoring`: Cost monitoring UI components
- `design-system`: Component library (@kushalsamant/design-template)

#### Getting Started

**Prerequisites**:
- Node.js 18+
- Python 3.11+
- PostgreSQL (for shared database)
- Redis (for caching)

**Installation**:
```bash
# Install all dependencies
npm install

# Install Python dependencies (if using Poetry)
poetry install
```

**Development**:
```bash
# Run all apps in development mode
npm run dev

# Run specific app
cd apps/ask/frontend && npm run dev
cd apps/ask/api && uvicorn main:app --reload
```

---

## Implementation Plan Overview

This plan consolidates all remaining platform-wide implementation tasks across ASK, Sketch2BIM, Reframe, and shared packages. It includes database migrations, code standardization, infrastructure consolidation, documentation updates, and comprehensive verification.

**Last Updated**: 2025-01-XX - Comprehensive codebase verification complete
**Status**: Ready for implementation - Verification found most claimed issues are already resolved

**⚠️ Important**: Phase 0 verification has been completed. Most issues claimed in the original plan were already fixed:
- ✅ Daily cost threshold removal - COMPLETE (code is correct)
- ✅ Tier naming standardization - COMPLETE (all files use `monthly`/`yearly`)
- ⚠️ Only minor issue: Reframe setup.ts script reference (covered in Phase 3.3)

---

## Progress Summary & Remaining Tasks

### ✅ Completed Phases

**Phase 0: Verification** - ✅ Complete (100%)
- All codebase verification tasks done
- Most issues were already fixed in codebase
- Plan updated to reflect actual state

**Phase 2.1: Tier Naming Standardization** - ✅ Complete (100%)
- All apps use `'monthly'` and `'yearly'` consistently
- Fixed in: ASK, Sketch2BIM, Reframe frontend/backend
- Verified across all pricing, settings, and payment pages

**Phase 2.2: Daily Cost Threshold Removal** - ✅ Complete (100%)
- Removed from all frontend and backend code
- Only monthly thresholds remain
- Code verified and working correctly

**Phase 3.3: Script References Cleanup** - ✅ Complete (100%)
- Removed non-existent `setup.ts` script reference from Reframe package.json
- Consolidated all .ps1 scripts into unified tools

### ⏳ Remaining Phases

**Phase 1: Database & Infrastructure** - ⏳ Pending (0%)
- 1.1: Stripe to Razorpay database migrations (Alembic)
- 1.2: Upstash Postgres migration
- 1.3: Infrastructure consolidation (manual Render/Vercel setup)

**Phase 2: Code Standardization** - 🟡 Partial (50%)
- 2.1: Tier naming - ✅ Complete
- 2.2: Daily cost threshold - ✅ Complete
- 2.3: Backend migration to shared components - ⏳ Pending
- 2.4: Frontend migration to shared components - ⏳ Pending

**Phase 3: Configuration** - 🟡 Partial (33%)
- 3.1: Environment variable verification - ⏳ Pending
- 3.2: Backward compatibility removal - ⏳ Pending
- 3.3: Script references cleanup - ✅ Complete

**Phase 4: Documentation** - ⏳ Pending (0%)
- 4.1: Stripe → Razorpay documentation updates
- 4.2: Cost monitoring documentation updates
- 4.3: Migration guides creation

**Phase 5: Testing & Verification** - ⏳ Pending (0%)
- 5.1: Pricing unification verification
- 5.2: Comprehensive codebase scans
- 5.3: Conceptual verification

**Phase 6: Dependency & Script Cleanup** - ⏳ Pending (0%)
- 6.1: Dependency cleanup (remove Stripe)
- 6.2: Script references verification

**Overall Progress**: ~25% Complete

### 📌 Quick Reference

**Status Legend**:
- ✅ Complete
- 🟡 Partial (in progress)
- ⏳ Pending
- ⚠️ Blocked (requires prerequisite)

**Time Estimates**:
- Quick Wins: 2-4 hours each
- Infrastructure: 8-12 hours
- Code Standardization: 15-25 hours
- Documentation: 6-8 hours (can parallelize)
- Testing: 8-12 hours

**Dependencies**:
- Phase 1.1 → Phase 1.2 (database migrations must be done in order)
- Phase 1.3 can be done independently
- Phase 2.3-2.4 can be done in parallel
- Phase 4 can be done anytime (documentation)
- Phase 5 requires all code changes to be complete
- Phase 6 can be done anytime (cleanup)

### 🎯 Recommended Next Steps

1. **Immediate (Before Investor Meeting)**:
   - ✅ Project structure documentation (DONE)
   - Review remaining tasks to prioritize

2. **Short Term (1-2 weeks)**:
   - Phase 1.3: Infrastructure consolidation (manual Render/Vercel setup)
   - Phase 3.1: Environment variable verification
   - Phase 4: Documentation updates (can be done in parallel)

3. **Medium Term (2-4 weeks)**:
   - Phase 1.1-1.2: Database migrations (requires staging testing)
   - Phase 2.3-2.4: Platform standardization (code refactoring)

4. **Long Term (1-2 months)**:
   - Phase 5: Comprehensive testing
   - Phase 6: Final cleanup

### 📊 Critical Path (Must Do in Order)

1. Phase 1.1: Database migrations (test on staging)
2. Phase 1.2: Upstash migration (if moving from Supabase)
3. Phase 1.3: Infrastructure setup (manual)
4. Phase 2.3-2.4: Code standardization
5. Phase 5: Testing & verification

### 🔄 Can Do in Parallel

- Phase 4: Documentation updates
- Phase 3.2: Backward compatibility removal (if approved)
- Phase 6: Dependency cleanup

---

## 🚀 Quick Start Execution Guide

### Immediate Actions (Can Start Now)

**Quick Wins** (Low effort, high value):
1. ✅ **Phase 3.3** - Script references cleanup (DONE)
2. ⏳ **Phase 4** - Documentation updates (can be done in parallel, no code changes)
3. ⏳ **Phase 3.1** - Environment variable verification (audit only)
4. ⏳ **Phase 6.1** - Remove Stripe dependencies (simple cleanup)

**Before Starting Any Phase**:
- ✅ Phase 0 verification is complete
- Review the specific phase details below
- Check dependencies (some phases require others to complete first)

### Execution Checklist Format

For each phase, use this checklist:
- [ ] Read phase details and understand requirements
- [ ] Check prerequisites and dependencies
- [ ] Review related files mentioned in phase
- [ ] Implement changes
- [ ] Test changes (locally first, then staging)
- [ ] Update progress in this document
- [ ] Mark phase as complete

### Recommended Execution Order

**Week 1 (Quick Wins)**:
1. Phase 4: Documentation updates (parallel work)
2. Phase 3.1: Environment variable verification
3. Phase 6.1: Dependency cleanup

**Week 2-3 (Infrastructure)**:
1. Phase 1.1: Database migrations (if needed, test on staging first)
2. Phase 1.2: Upstash Postgres migration (depends on Phase 1.1)
3. Phase 1.3: Infrastructure consolidation (manual setup - can be done in parallel with 1.1)

**Week 4-6 (Code Standardization)**:
1. Phase 2.3: Backend migration to shared components
2. Phase 2.4: Frontend migration to shared components

**Week 7-8 (Testing & Cleanup)**:
1. Phase 5: Testing & verification
2. Phase 6.2: Script references verification
3. Phase 3.2: Backward compatibility removal (if approved)

---

## 📋 Implementation Phases (Detailed)

### Phase Summary Table

| Phase | Status | Priority | Time Est. | Dependencies | Can Parallelize? |
|-------|--------|----------|-----------|--------------|-------------------|
| Phase 0: Verification | ✅ Complete | - | 2-3h | None | - |
| Phase 1.1: DB Migrations | ⏳ Pending | High | 4-6h | None | No |
| Phase 1.2: Upstash Migration | ⏳ Pending | High | 4-6h | Phase 1.1 | No |
| Phase 1.3: Infrastructure | ⏳ Pending | High | 2-4h | None | Yes (with 1.1) |
| Phase 2.1: Tier Naming | ✅ Complete | - | - | - | - |
| Phase 2.2: Cost Threshold | ✅ Complete | - | - | - | - |
| Phase 2.3: Backend Migration | ⏳ Pending | Medium | 8-12h | None | Yes (with 2.4) |
| Phase 2.4: Frontend Migration | ⏳ Pending | Medium | 7-13h | None | Yes (with 2.3) |
| Phase 3.1: Env Verification | ⏳ Pending | Medium | 2-3h | None | Yes |
| Phase 3.2: Backward Compat | ⏳ Pending | Low | 2-3h | None | Yes |
| Phase 3.3: Script Cleanup | ✅ Complete | - | - | - | - |
| Phase 4: Documentation | ⏳ Pending | Low | 6-8h | None | Yes |
| Phase 5: Testing | ⏳ Pending | High | 8-12h | All code phases | No |
| Phase 6.1: Dependency Cleanup | ⏳ Pending | Low | 1-2h | None | Yes |
| Phase 6.2: Script Verification | ⏳ Pending | Low | 1h | None | Yes |

### Phase Execution Order

1. **Phase 0** (Verification) - ✅ **COMPLETE** - Already done
2. **Phase 1** (Critical) - Database migrations and infrastructure setup
3. **Phase 2** (Standardization) - Code updates and cleanup
4. **Phase 3** (Configuration) - Environment variables and backward compatibility
5. **Phase 4** (Documentation) - ⚡ Can be done in parallel with Phase 2-3
6. **Phase 5** (Verification) - Final testing and validation
7. **Phase 6** (Cleanup) - Dependency and script cleanup

---

## Phase 0: Pre-Implementation Verification ✅ COMPLETE

**Status**: ✅ Complete (100%)  
**Priority**: Critical (already done)  
**Time**: 2-3 hours (completed)

### 0.1 Comprehensive Codebase Verification

**Purpose**: Verify all items claimed as "✅ Completed" in plan files are actually complete in the codebase before beginning implementation.

**Verification Results** (from codebase scan):

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
   - **Action Required**: Remove script reference from package.json (covered in Phase 3.3)

---

## Phase 1: Critical Database & Infrastructure ⏳ PENDING

**Status**: ⏳ Pending (0%)  
**Priority**: High  
**Time Estimate**: 8-12 hours total  
**Dependencies**: None (can start immediately)

### 1.1 Stripe to Razorpay Database Migrations

**ASK Alembic Migration**
- **File**: `apps/ask/alembic/versions/001_rename_stripe_to_razorpay.py` (new)
- **Status**: Alembic initialized, migration file needs to be created
- **Actions**:
  - Create migration to rename columns (if they exist in production):
    - `users.stripe_customer_id` → `razorpay_customer_id`
    - `payments.stripe_payment_intent_id` → `razorpay_payment_id`
    - `payments.stripe_checkout_session_id` → `razorpay_order_id`
  - Update indexes accordingly
  - Include downgrade function for rollback
- **Note**: Models already use `razorpay_*`, but production databases may still have `stripe_*` columns

**Sketch2BIM Alembic Migration**
- **File**: `apps/sketch2bim/backend/alembic/versions/011_rename_stripe_to_razorpay.py` (new)
- **Actions**: Same column/index renames as ASK migration
- **Dependencies**: Migration numbered `011_` (next after `010_remove_reader_type_column.py`)

**Reframe Database Verification**
- Check if Reframe has any `stripe_*` database fields
- If yes, create equivalent migration; if no, document

**Testing**: Test migrations on staging before production deployment

### 1.2 Upstash Postgres Migration

**Pre-Migration Preparation**
- Export Supabase backups (ASK and Sketch2BIM schemas and data)
- Document current database state (row counts, table sizes)

**Upstash Setup**
- Create two Upstash Postgres databases (one for ASK, one for Sketch2BIM)
- Run schema migrations on Upstash databases
- Import data from Supabase backups
- Verify data integrity

**Environment Configuration**
- Update `ask.env.production` with Upstash connection string
- Update `sketch2bim.env.production` with Upstash connection string
- Update Render environment variables
- Remove `DATABASE_SCHEMA` variables (Upstash uses separate databases)

**Testing & Deployment**
- Test locally with Upstash databases
- Deploy to production
- Monitor for 1 week before deprovisioning Supabase

### 1.3 Infrastructure Consolidation - Render Services

**Manual Configuration Required**
- Create three Render Web Services manually (not using Blueprint):
  - `ask` (root: `apps/ask`)
  - `reframe` (root: `apps/reframe/backend`)
  - `sketch2bim` (root: `apps/sketch2bim/backend`)
- Set environment variables from respective `.env.production` files
- Configure build/start commands
- Verify health endpoints

**Vercel Configuration**
- Update main site with Google OAuth credentials
- Update all apps with `NEXT_PUBLIC_AUTH_URL=https://kvshvl.in`
- Remove app-specific OAuth variables

---

## Phase 2: Code Standardization & Cleanup 🟡 PARTIAL

**Status**: 🟡 Partial (50% - 2.1 and 2.2 complete)  
**Priority**: Medium  
**Time Estimate**: 15-25 hours remaining  
**Dependencies**: None (can start immediately)

### 2.1 Tier Naming Standardization

**Status**: ✅ **COMPLETE** - Verified in codebase verification (Phase 0)

All tier naming is already standardized to `'monthly'` and `'yearly'` across:
- ✅ ASK frontend pricing page
- ✅ Sketch2BIM frontend pricing, settings, and payments pages
- ✅ Sketch2BIM frontend components (CreditsDisplay)
- ✅ Sketch2BIM backend schemas
- ✅ Sketch2BIM Razorpay plan creation script

**No action required** - This phase is complete.

### 2.2 Daily Cost Threshold Removal

**Status**: ✅ **COMPLETE** - Verified in codebase verification (Phase 0)

**Frontend**: ✅ Complete
- `packages/shared-frontend/src/cost-monitoring/groq-monitor.ts` - Only checks monthly threshold (lines 185-203)
- No `DAILY_COST_THRESHOLD` constant exists or is referenced
- Code is correct and working

**Backend**: ✅ Complete
- `packages/shared-backend/cost-monitoring/alerts.py` - No daily threshold parameter ✅
- `apps/ask/api/utils/groq_monitor.py` - Uses monthly threshold only ✅
- `apps/reframe/backend/app/services/groq_monitor.py` - Uses monthly threshold only ✅

**UI Component Review** (Optional):
- Search for "daily cost threshold", "daily budget", "daily alert" text in documentation
- Update documentation to reflect monthly-only monitoring
- Keep daily breakdown charts (visualization only, no alerts)

### 2.3 Platform Standardization - Backend Migration

**ASK Backend**
- Migrate `apps/ask/api/main.py` to use `shared_backend.api.factory.create_app`
- Migrate `apps/ask/api/models_db.py` to extend `BaseUser` and `BasePayment`

**Sketch2BIM Backend**
- Migrate `apps/sketch2bim/backend/app/main.py` to use FastAPI factory
- Preserve custom middleware (correlation, timeout, security headers)
- Migrate models to extend base models

**Testing**: Ensure all routes, middleware, and database operations work correctly

### 2.4 Platform Standardization - Frontend Migration

**Settings Pages**
- Migrate ASK, Sketch2BIM, and Reframe settings pages to use shared components
- Preserve app-specific features (data export, account deletion, etc.)

**Pricing Pages**
- Migrate all pricing pages to use shared payment utilities
- Replace inline Razorpay script loading with shared utilities

---

## Phase 3: Environment Variables & Configuration 🟡 PARTIAL

**Status**: 🟡 Partial (33% - 3.3 complete)  
**Priority**: Medium  
**Time Estimate**: 4-6 hours remaining  
**Dependencies**: None (can start immediately)

### 3.1 Environment Variable Verification

**Production Environments**
- Verify Render services have all prefixed variables
- Verify Vercel projects have all prefixed variables
- Remove any unprefixed variables
- Verify no `STRIPE_*` variables exist
- Verify no `*_GROQ_DAILY_COST_THRESHOLD` variables exist

**Local Development**
- Update `.env.example` files to show only prefixed variables
- Update developer documentation

### 3.2 Backward Compatibility Removal

**Code Cleanup** (if user approves)
- Remove `LIVE_KEY_ID`/`LIVE_KEY_SECRET` fallbacks from ASK and Sketch2BIM configs
- Remove `/add-credits` endpoints (if not needed for admin)
- Remove legacy generate endpoint models (if not used)

**Documentation Cleanup**
- Remove "backward compatibility" comments from env templates
- Update config file comments
- Update route comments

### 3.3 Script References Cleanup

**Reframe package.json**
- Remove `"setup": "tsx scripts/setup.ts"` script (file doesn't exist)
- OR create the missing setup.ts file if needed

---

## Phase 4: Documentation Updates ⏳ PENDING

**Status**: ⏳ Pending (0%)  
**Priority**: Low (can be done in parallel)  
**Time Estimate**: 6-8 hours  
**Dependencies**: None (can start immediately)

### 4.1 Stripe → Razorpay Documentation

**Files to Update**:
- `docs/DATABASE_MIGRATION_GUIDE.md` - Update SQL examples
- `docs/repo-skills-CV.md` - Replace Stripe mentions
- `docs/migrate-to-self-hosted-oracle.md` - Update env var examples
- `docs/competitive-analysis-HONEST.md` - Update payment processor mentions
- `docs/termsofservice.md` - Update payment processor references
- `docs/privacypolicy.md` - Replace Stripe section with Razorpay
- `docs/cancellationrefund.md` - Update processing timelines

### 4.2 Cost Monitoring Documentation

**Files to Update**:
- `docs/COST_ANALYSIS.md` - Remove daily threshold references
- `docs/ENVIRONMENT_VARIABLES_REFERENCE.md` - Remove daily threshold entries
- `apps/ask/docs/COST_MONITORING_SETUP.md` - Remove daily threshold examples

### 4.3 Migration Guides

**Create App-Specific Migration Guides**:
- `docs/migrations/ASK_MIGRATION_GUIDE.md`
- `docs/migrations/SKETCH2BIM_MIGRATION_GUIDE.md`
- `docs/migrations/REFRAME_MIGRATION_GUIDE.md`

---

## Phase 5: Testing & Verification ⏳ PENDING

**Status**: ⏳ Pending (0%)  
**Priority**: High (must be done after code changes)  
**Time Estimate**: 8-12 hours  
**Dependencies**: Phases 1, 2, 3 must be complete

### 5.1 Pricing Unification Verification

**Backend Verification**
- Verify checkout routes support all tiers (week/monthly/yearly)
- Verify webhook handlers correctly identify all tiers
- Verify subscription duration logic includes weekly

**Production Verification**
- Verify Razorpay dashboard shows unified plan IDs
- Verify all apps use same plan IDs
- Test end-to-end payment flows for all tiers

### 5.2 Comprehensive Codebase Scans

**Stripe References**
- Search for remaining Stripe references (excluding node_modules, .git, lockfiles)
- Categorize: Code, Documentation, Comments, Config
- Fix all functional code references
- Update documentation

**Daily Cost Threshold References**
- Search for `GROQ_DAILY_COST_THRESHOLD` or `DAILY_COST_THRESHOLD`
- Remove from code, update documentation

### 5.3 Conceptual Verification

**For Each App**:
- Payment flow: Verify Razorpay payments write to correct fields
- Dashboard: Verify monthly-only cost monitoring
- Migration: Test on fresh and existing databases

---

## Phase 6: Dependency & Script Cleanup ⏳ PENDING

**Status**: ⏳ Pending (0%)  
**Priority**: Low (cleanup task)  
**Time Estimate**: 2-3 hours  
**Dependencies**: None (can start immediately)

### 6.1 Dependency Cleanup

**Package Files**
- Remove `stripe` from all `package.json` files
- Remove `stripe` from all `requirements.txt` files
- Regenerate lockfiles on next install

### 6.2 Script References

**Check for**:
- References to deleted `setup.ts` scripts
- Update `package.json` scripts if needed
- Update documentation references

---

## Success Criteria

✅ All database columns use `razorpay_*` naming (no `stripe_*`)
✅ All code references use `razorpay_*` field names
✅ All documentation mentions Razorpay (not Stripe)
✅ All legal docs reference Razorpay
✅ No daily cost threshold configuration or alerts
✅ Only monthly cost thresholds documented and used
✅ Tier naming standardized to "monthly"/"yearly" across all apps
✅ All apps migrated to shared components
✅ No Stripe dependencies in package files
✅ Environment variables consistent across all environments
✅ All migrations tested and working
✅ Production deployments stable

---

## Notes

- **Database Migrations**: Must be tested on staging before production
- **Breaking Changes**: Removing daily cost thresholds and backward compatibility are breaking changes
- **Reframe**: May not have database payment fields - verify before creating migrations
- **Manual Steps**: Infrastructure consolidation requires Render/Vercel dashboard access
- **Testing**: Comprehensive testing required after each phase
- **Verification**: Phase 0 verification found issues that must be fixed before proceeding

---

## Estimated Timeline

- **Phase 0**: 2-3 hours (verification and fixing found issues)
- **Phase 1**: 8-12 hours (database migrations + infrastructure)
- **Phase 2**: 15-25 hours (code standardization)
- **Phase 3**: 4-6 hours (configuration cleanup)
- **Phase 4**: 6-8 hours (documentation)
- **Phase 5**: 8-12 hours (verification)
- **Phase 6**: 2-3 hours (cleanup)

**Total**: 45-67 hours (~6-8 weeks part-time)

---

## 📚 Reference Material (Appendices)

> **Note**: The sections below contain reference information, deployment guides, and documentation templates. These are for consultation during implementation but are not actionable tasks themselves.

---

### Appendix A: Deployment Configuration Guide

**Reference**: See detailed guide in `DEPLOYMENT_CONFIGURATION_GUIDE.md` for complete step-by-step instructions.

#### Vercel Configuration

**Main Site (kushalsamant-github-io)**:
- Add `GOOGLE_CLIENT_ID` = `620186529337-lrr0bflcuihq2gnsko6vbrnsdv2u3ugu.apps.googleusercontent.com`
- Add `GOOGLE_CLIENT_SECRET` = `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`
- Add `NEXTAUTH_SECRET` and `AUTH_SECRET` (generate with `openssl rand -base64 32`)
- Remove old app-specific OAuth variables
- Redeploy

**All Apps (ASK, Reframe, Sketch2BIM)**:
- Add/Update `NEXT_PUBLIC_AUTH_URL=https://kvshvl.in`
- Remove old app-specific OAuth variables (`ASK_GOOGLE_*`, `REFRAME_GOOGLE_*`, `SKETCH2BIM_GOOGLE_*`)
- Verify other environment variables from respective `.env.production` files
- Redeploy

#### Render Configuration

**Backend Services**:
- Connect repository to Render (if not already)
- Point to `render.yaml` at root
- Apply blueprint or create services manually:
  - `ask` (root: `apps/ask`)
  - `reframe` (root: `apps/reframe/backend`)
  - `sketch2bim` (root: `apps/sketch2bim/backend`)

**Environment Variables** (set in Render dashboard):
- ASK Backend: Set `ASK_DATABASE_URL`, `ASK_GROQ_API_KEY`, Razorpay variables
- Reframe Backend: Set `REFRAME_GROQ_API_KEY`, `REFRAME_UPSTASH_REDIS_*`, `REFRAME_NEXTAUTH_SECRET`
- Sketch2BIM Backend: **IMPORTANT** - Remove `SKETCH2BIM_REDIS_URL` (old Render Redis), set `SKETCH2BIM_UPSTASH_REDIS_*`, `SKETCH2BIM_DATABASE_URL`, Razorpay variables, BunnyCDN variables

#### Google OAuth Console

- Verify Authorized JavaScript Origins: `https://kvshvl.in`, `http://localhost:3000`
- Verify Authorized Redirect URIs: `https://kvshvl.in/api/auth/callback/google`, `http://localhost:3000/api/auth/callback/google`

#### Upstash Redis

- Get credentials from Upstash console
- Add to Reframe and Sketch2BIM backend services in Render

---

### Appendix B: Environment Variables Update Instructions

**Important**: All production environment variables are centralized in `.env.production` files at repository root:
- `ask.env.production`
- `sketch2bim.env.production`
- `reframe.env.production`

#### Update Shared OAuth Variables

Add to the **top** of each `.env.production` file (in the shared section):

```bash
# =============================================================================
# SHARED GOOGLE OAUTH (Used by all apps via kvshvl.in)
# =============================================================================
GOOGLE_CLIENT_ID=620186529337-lrr0bflcuihq2gnsko6vbrnsdv2u3ugu.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
```

#### Remove Old OAuth Variables

Comment out or remove:
```bash
# OLD - Remove or comment out:
# ASK_GOOGLE_CLIENT_ID=...
# ASK_GOOGLE_SECRET=...
# REFRAME_GOOGLE_CLIENT_ID=...
# REFRAME_GOOGLE_SECRET=...
# SKETCH2BIM_GOOGLE_CLIENT_ID=...
# SKETCH2BIM_GOOGLE_SECRET=...
```

#### Local Development

Create `.env.local` files in app directories (gitignored):
- `apps/ask/api/.env.local`
- `apps/ask/frontend/.env.local`
- `apps/sketch2bim/backend/.env.local`
- `apps/sketch2bim/frontend/.env.local`
- `apps/reframe/.env.local`

---

### Appendix C: Infrastructure Consolidation Status

#### ✅ Code Changes - COMPLETE

- ✅ `render.yaml` - Updated to use Upstash Redis for Sketch2BIM
- ✅ Environment files - Removed old OAuth, added `NEXT_PUBLIC_AUTH_URL=https://kvshvl.in`
- ✅ Authentication files - Main site NextAuth config, app redirects
- ✅ Documentation - Deployment guides and verification scripts

#### ⏳ Manual Configuration Steps - PENDING

1. **Commit and Push Code Changes**
2. **Vercel Configuration** - Set OAuth variables, update all apps
3. **Render Configuration** - Set up backend services, environment variables
4. **Google OAuth Console** - Verify authorized origins and redirect URIs
5. **Upstash Redis** - Get credentials and add to backend services
6. **Testing & Verification** - Test authentication flows, verify health endpoints

**Reference**: See `DEPLOYMENT_CONFIGURATION_GUIDE.md` for detailed steps.

---

### Appendix D: Backend Verification Results

#### Pricing Unification - ✅ Verified Complete

**Status**: All backend code verification tasks completed. The codebase fully supports unified pricing structure with weekly tier across all three applications.

**Key Findings**:
- ✅ Environment variables reference correct settings
- ✅ Unified plan IDs in production configuration (all apps use same plan IDs)
- ✅ Backend checkout routes support all tiers (week/month/year)
- ✅ Webhook handlers map weekly tier correctly
- ✅ Subscription duration logic includes weekly (7 days)
- ✅ All hardcoded tier lists include `week`
- ✅ No old pricing references found

**Unified Plan IDs**:
- Week: `plan_Rha5Ikcm5JrGqx`
- Month: `plan_Rha5JNPsk1WmI6`
- Year: `plan_Rha5Jzn1sk8o1X`

**Note**: Reframe backend Python service has minor inconsistencies but is not used for payments (Reframe uses Next.js API routes).

---

### Appendix E: Repository Audit Findings

#### Critical Issues - ✅ Fixed

1. ✅ **Reframe Backend Subscription Service** - Fixed weekly tier values (1 → 7 days)
2. ✅ **Sketch2BIM Payment Route** - Fixed incorrect Stripe field names (now uses Razorpay fields)

#### High Priority Issues

**Tier Naming Inconsistency**:
- Reframe uses `"monthly"` and `"yearly"`
- ASK and Sketch2BIM use `"month"` and `"year"`
- **Recommendation**: Standardize to `"monthly"` and `"yearly"` (covered in Phase 2.1)

#### Medium Priority Issues

- ✅ Database schemas use Razorpay field names (verified)
- ✅ Stripe package dependency in Reframe (not in package.json, only in lockfile - safe to ignore)

---

#### Documentation

- [Documentation Index](./docs/DOCUMENTATION_INDEX.md) - Complete documentation guide
- [Monorepo Migration Guide](./docs/MIGRATION_GUIDE.md) - Migration instructions
- [Migration Status](./docs/MONOREPO_MIGRATION.md) - Current migration status
- [Cost Analysis](./docs/COST_ANALYSIS.md) - Infrastructure cost analysis
- [Deployment Checklist](./docs/DEPLOYMENT_CHECKLIST.md) - End-to-end deployment steps
- [Environment Variables Reference](./docs/ENVIRONMENT_VARIABLES_REFERENCE.md) - Canonical env var list
- [API Versioning Strategy](./docs/API_VERSIONING.md) - How APIs are versioned across apps
- [SLOs](./docs/SLOs.md) - Service-level objectives and alerting hooks

---

### Appendix F: Complete Documentation Reference

This section provides a comprehensive reference to all documentation files that were merged into this plan. These files contain detailed information about specific aspects of the platform.

#### Application-Specific Documentation

**ASK Application**:
- `apps/ask/README.md` - ASK: Daily Research application overview, features, and architecture
- `apps/ask/DEPLOYMENT.md` - ASK deployment guide for Render (backend) and Vercel (frontend)
- `apps/ask/TROUBLESHOOTING.md` - ASK troubleshooting guide and common issues
- `apps/ask/README_FRONTEND.md` - ASK frontend-specific documentation
- `apps/ask/ENV_VARIABLES.md` - ASK environment variables reference
- `apps/ask/docs/ENVIRONMENT_VARIABLES.md` - Detailed ASK environment configuration
- `apps/ask/docs/COST_MONITORING_SETUP.md` - ASK cost monitoring setup guide
- `apps/ask/frontend/README.md` - ASK frontend development guide

**Sketch2BIM Application**:
- `apps/sketch2bim/README.md` - Sketch-to-BIM application overview, quick start, and tech stack
- `apps/sketch2bim/docs/deployment_checklist.md` - Production deployment checklist
- `apps/sketch2bim/docs/production_verification.md` - Production verification checklist
- `apps/sketch2bim/docs/testing.md` - Complete testing guide for payments and webhooks
- `apps/sketch2bim/docs/troubleshooting.md` - Common issues and solutions
- `apps/sketch2bim/docs/migrations.md` - Database migration documentation
- `apps/sketch2bim/docs/FEATURE_FLAGS.md` - Experimental features and optional capabilities
- `apps/sketch2bim/docs/ENVIRONMENT_VARIABLES.md` - Sketch2BIM environment variables
- `apps/sketch2bim/docs/OAUTH_DOMAIN_MIGRATION.md` - OAuth domain migration guide
- `apps/sketch2bim/docs/symbol_recognition.md` - Symbol recognition documentation
- `apps/sketch2bim/docs/HONEST_REVIEW.md` - Honest review and analysis
- `apps/sketch2bim/infra/digitalocean/README.md` - DigitalOcean deployment guide
- `apps/sketch2bim/infra/fly.io/README.md` - Fly.io deployment guide
- `apps/sketch2bim/infra/hetzner/README.md` - Hetzner deployment guide
- `apps/sketch2bim/infra/k8s/README.md` - Kubernetes deployment guide
- `apps/sketch2bim/infra/vps/README.md` - VPS deployment guide
- `apps/sketch2bim/scripts/README.md` - Scripts documentation
- `apps/sketch2bim/train/README.md` - Training documentation
- `apps/sketch2bim/train/annotations/README.md` - Training annotations guide
- `apps/sketch2bim/data/symbols/README.md` - Symbol data documentation

**Reframe Application**:
- `apps/reframe/readme.md` - Reframe application overview, features, and tech stack
- `apps/reframe/backend/README.md` - Reframe backend documentation

#### Package Documentation

**Shared Backend Package**:
- `packages/shared-backend/README.md` - Shared Python utilities documentation (auth, payments, database, subscription, cost-monitoring, config)

**Shared Frontend Package**:
- `packages/shared-frontend/README.md` - Shared TypeScript/Next.js utilities documentation (auth, payments, cost-monitoring)

**Design System Package**:
- `packages/design-system/README.md` - KVSHVL Design Template overview and features
- `packages/design-system/SETUP.md` - Design system setup guide
- `packages/design-system/docs/DESIGN_SYSTEM.md` - Design system documentation
- `packages/design-system/docs/COMPONENTS.md` - Component library reference
- `packages/design-system/docs/MIGRATION.md` - Migration guide for design system

#### General Documentation

**Migration & Structure**:
- `docs/MONOREPO_MIGRATION.md` - Monorepo migration status (✅ Complete)
- `docs/MIGRATION_GUIDE.md` - Step-by-step guide for migrating applications to use shared packages
- `docs/APP_MIGRATION_STATUS.md` - Detailed status for each application (✅ All migrations complete)
- `docs/STRUCTURE_CLEANUP.md` - Structure cleanup status (✅ Cleanup complete)
- `docs/REPO_CLEANUP_SUMMARY.md` - Repository cleanup summary (✅ Old repos deleted)
- `docs/DELETE_OLD_REPOS.md` - Guide for deleting old repositories

**Infrastructure & Configuration**:
- `docs/COST_ANALYSIS.md` - Comprehensive infrastructure cost analysis for all applications
- `docs/DATABASE_MIGRATION_GUIDE.md` - Guide for setting up shared Supabase database with schemas
- `docs/DATABASE_SETUP_COMPLETE.md` - Database setup completion status and next steps
- `docs/ENVIRONMENT_VARIABLES_REFERENCE.md` - Canonical environment variables list
- `docs/ENVIRONMENT_VARIABLES_SYNC.md` - Environment variables synchronization status
- `docs/ENV_PREFIX_MIGRATION_COMPLETE.md` - Environment variable prefix migration completion
- `docs/ENV_PREFIX_MIGRATION_TESTING.md` - Environment variable prefix migration testing
- `docs/migrate-to-self-hosted-oracle.md` - Oracle Cloud migration guide for Reframe

**Deployment & Operations**:
- `docs/DEPLOYMENT_CHECKLIST.md` - End-to-end deployment steps
- `docs/VERCEL_AUTOMATION.md` - Vercel automation and deployment scripts
- `docs/TESTING_CHECKLIST.md` - Testing checklist for all applications

**Design & Development**:
- `docs/DESIGN_SYSTEM.md` - Design system documentation
- `docs/README-NEXTJS.md` - Next.js migration documentation
- `docs/STANDARDIZATION_ANALYSIS.md` - Platform standardization analysis

**API & Architecture**:
- `docs/API_VERSIONING.md` - API versioning strategy across apps
- `docs/ADMIN_DASHBOARD_SETUP.md` - Admin dashboard setup guide
- `docs/SLOs.md` - Service-level objectives and alerting hooks
- `docs/CONSISTENCY_AUDIT_REPORT.md` - Consistency audit report

**Content & Legal**:
- `docs/termsofservice.md` - Terms of service
- `docs/privacypolicy.md` - Privacy policy
- `docs/cancellationrefund.md` - Cancellation and refund policy
- `docs/competitive-analysis-HONEST.md` - Competitive analysis
- `docs/COMPETITIVE_ANALYSIS.md` - Competitive analysis (alternative)
- `docs/repo-skills-CV.md` - Repository skills and CV
- `docs/history.md` - Site history
- `docs/the-minimal-theme.md` - Theme documentation

**Database**:
- `database/migrations/README.md` - Database migrations documentation

**Documentation Index**:
- `docs/DOCUMENTATION_INDEX.md` - Complete documentation index and quick reference guide

---

## Files Merged Into This Plan

This consolidated plan includes content from all implementation plans, documentation files, and reference materials:

**Implementation Plans** (merged into main phases):
- STRIPE_REMOVAL_IMPLEMENTATION_PLAN.md
- STRIPE_REMOVAL_REMAINING_WORK.md
- TIER_NAMING_STANDARDIZATION_PLAN.md
- PRICING_UNIFICATION_PLAN.md
- PRICING_UNIFICATION_VERIFICATION_PLAN.md
- UPSTASH_MIGRATION_IMPLEMENTATION_PLAN.md
- VERCEL_SCRIPT_CONSOLIDATION_IMPLEMENTATION_PLAN.md
- INFRASTRUCTURE_CONSOLIDATION_REMAINING_TASKS.md
- INFRASTRUCTURE_CONSOLIDATION_STATUS.md
- PLATFORM_STANDARDIZATION_REMAINING_TASKS.md
- BACKWARD_COMPATIBILITY_REMOVAL_REMAINING_TASKS.md
- Environment-Variable-Prefix-Migration-Remaining-Tasks.md
- reframe-naming-and-env-cleanup.plan.md
- cross-repository-consistency-audit-and-fix-b0928a3f.plan.md

**Verification & Audit Reports** (merged into appendices):
- BACKEND_VERIFICATION_RESULTS.md
- REPOSITORY_AUDIT_REPORT.md
- DEPLOYMENT_CONFIGURATION_GUIDE.md
- ENV_UPDATE_INSTRUCTIONS.md
- README.md
- README (2).md

**Application Documentation** (referenced in Appendix F):
- All files from `apps/ask/`, `apps/sketch2bim/`, `apps/reframe/` subdirectories

**Package Documentation** (referenced in Appendix F):
- All files from `packages/shared-backend/`, `packages/shared-frontend/`, `packages/design-system/` subdirectories

**General Documentation** (referenced in Appendix F):
- All files from `docs/` subdirectory
- `database/migrations/README.md`

**Total Files Merged**: 
- 71+ markdown files from `.cursor/plans/`
- 200+ repository documentation files (.md)
- 4 documentation template files (.md.template)
- 3 configuration/documentation files (.txt: robots.txt, .gitattributes.txt, .vercel/README.txt)
- **Total: 275+ files** consolidated into this single comprehensive plan

**Note**: Requirements files (requirements.txt), node_modules files, virtual environment files (.venv), and build output files (out/) were excluded as they are not documentation.

### Additional Repository Documentation Files

The following documentation files exist in the repository and are referenced here for completeness. These files contain detailed information about specific aspects of the platform and should be consulted when working on related tasks:

**Root Level Documentation**:
- (No root README.md - content merged into Platform Overview section above)

**Application Documentation**:
- `apps/ask/README.md` - ASK application overview and features
- `apps/ask/DEPLOYMENT.md` - ASK deployment guide
- `apps/ask/TROUBLESHOOTING.md` - ASK troubleshooting guide
- `apps/ask/README_FRONTEND.md` - ASK frontend documentation
- `apps/sketch2bim/README.md` - Sketch2BIM application overview
- `apps/sketch2bim/docs/troubleshooting.md` - Sketch2BIM troubleshooting guide

**General Documentation** (`docs/`):
- `docs/DOCUMENTATION_INDEX.md` - Complete documentation index
- `docs/ADMIN_DASHBOARD_SETUP.md` - Admin dashboard setup guide
- `docs/APP_MIGRATION_STATUS.md` - Application migration status
- `docs/COMPETITIVE_ANALYSIS.md` - Competitive analysis
- `docs/MONOREPO_MIGRATION.md` - Monorepo migration status
- `docs/PROJECT_STARTER_GUIDE.md` - Guide for creating new projects
- `docs/REPO_CLEANUP_SUMMARY.md` - Repository cleanup summary
- `docs/SHARED_COMPONENTS_REFERENCE.md` - Shared components reference
- `docs/STRUCTURE_CLEANUP.md` - Structure cleanup status
- `docs/UPSTASH_MIGRATION_GUIDE.md` - Upstash Postgres migration guide

**Database Documentation**:
- `database/migrations/upstash/README.md` - Upstash migration documentation

**Template Documentation**:
- `templates/fastapi-backend/README.md` - FastAPI backend template guide
- `templates/nextjs-app/README.md` - Next.js app template guide

**Additional Plan Files Merged**:
- `reframe-fastapi-migration-plan.md` - Reframe FastAPI migration plan (content referenced in Phase 2.3)

**Template Files** (merged into Appendix G):
- `docs/templates/DEPLOYMENT.md.template` - Template for generating deployment documentation
- `docs/templates/ENVIRONMENT_VARIABLES.md.template` - Template for generating environment variables documentation
- `docs/templates/API_DOCUMENTATION.md.template` - Template for generating API documentation
- `docs/templates/README.md.template` - Template for generating project README files

**Configuration Files** (merged into Appendix G):
- `robots.txt` - SEO robots configuration
- `.gitattributes.txt` - Git attributes configuration
- `.vercel/README.txt` - Vercel deployment information

**Note**: All these files have been merged into this plan and removed to maintain a single source of truth. The implementation plan now serves as the complete reference for all platform documentation and implementation tasks.

---

### Appendix G: Documentation Templates and Configuration Files

#### Documentation Templates

The platform includes templates for generating consistent documentation for new projects. These templates use placeholder variables that are replaced during project creation:

**Template Variables**:
- `{{APP_NAME}}` - Application name (lowercase, e.g., "myapp")
- `{{APP_DISPLAY_NAME}}` - Display name (e.g., "My App")
- `{{APP_PREFIX}}` - Uppercase prefix for env vars (e.g., "MYAPP")
- `{{APP_DESCRIPTION}}` - Application description
- `{{YEAR}}` - Current year

**Available Templates**:

1. **README.md.template** - Project README template
   - Includes: Overview, Features, Tech Stack, Quick Start, Environment Variables, Project Structure, Development, Deployment, Documentation links
   - Location: `docs/templates/README.md.template`

2. **DEPLOYMENT.md.template** - Deployment guide template
   - Includes: Prerequisites, Database Setup, Environment Variables (Application, Database, Frontend, CORS, Razorpay, Pricing, Plan IDs), Deployment Steps (Render, Vercel), Health Checks, Monitoring
   - Location: `docs/templates/DEPLOYMENT.md.template`

3. **ENVIRONMENT_VARIABLES.md.template** - Environment variables reference template
   - Includes: Application Variables, Database Variables, Frontend Variables, CORS Variables, Razorpay Variables (API Credentials, Pricing, Plan IDs), Groq Variables, Monitoring Variables
   - Location: `docs/templates/ENVIRONMENT_VARIABLES.md.template`

4. **API_DOCUMENTATION.md.template** - API documentation template
   - Includes: Base URL, Authentication, Response Format, Error Handling, Endpoints documentation structure
   - Location: `docs/templates/API_DOCUMENTATION.md.template`

**Usage**: These templates are used by the project generator scripts (`scripts/create-project.sh` or `scripts/create-project.ps1`) to generate consistent documentation for new projects.

#### Configuration Files

**robots.txt**:
```
User-agent: *
Allow: /

# Sitemaps
Sitemap: https://kushalsamant.github.io/sitemap.xml

# Crawl-delay (be respectful)
Crawl-delay: 1

# Directories
Allow: /projects/
Allow: /anthology/
Allow: /assets/

# Files to skip
Disallow: /script/
Disallow: /Gemfile
Disallow: /LICENSE
Disallow: /readme.md
Disallow: /export.xml
```

**Purpose**: SEO configuration for search engine crawlers. Allows access to main content, projects, anthology, and assets while blocking certain directories and files.

**.gitattributes.txt**:
```
* text=auto eol=lf

*.jpg binary
*.png binary
```

**Purpose**: Git configuration for line endings and binary file handling. Ensures consistent line endings (LF) across platforms and marks image files as binary.

**.vercel/README.txt**:
```
> Why do I have a folder named ".vercel" in my project?
The ".vercel" folder is created when you link a directory to a Vercel project.

> What does the "project.json" file contain?
The "project.json" file contains:
- The ID of the Vercel project that you linked ("projectId")
- The ID of the user or team your Vercel project is owned by ("orgId")

> Should I commit the ".vercel" folder?
No, you should not share the ".vercel" folder with anyone.
Upon creation, it will be automatically added to your ".gitignore" file.
```

**Purpose**: Information about Vercel deployment configuration. The `.vercel` folder contains project linking information and should not be committed to version control.

---

### Appendix H: Project Structure Reference

This section provides a comprehensive reference to the repository structure, application organization, and deployment architecture. This content is merged from `PROJECT_STRUCTURE.md` and references `PROJECT_TREE.txt` for the complete directory listing.

---

# KVSHVL Platform - Project Structure

## Repository Overview
```
kushalsamant.github.io/
│
├── 📱 APPS (3 Production Applications)
│   ├── apps/ask/              → ASK: Daily Architectural Research Q&A
│   ├── apps/reframe/          → Reframe: AI Tone Reframing Tool
│   └── apps/sketch2bim/       → Sketch2BIM: Automated Sketch-to-BIM Conversion
│
├── 📦 SHARED PACKAGES
│   ├── packages/design-system/     → Shared UI components
│   ├── packages/shared-backend/    → Shared Python utilities
│   └── packages/shared-frontend/  → Shared TypeScript utilities
│
├── 🌐 MAIN WEBSITE
│   └── app/                    → Portfolio/Company website (Next.js)
│
├── 🔧 DEVELOPMENT TOOLS
│   ├── dev-tools.ps1          → Consolidated development utilities
│   ├── scripts/               → Project generation & deployment scripts
│   └── templates/             → Project templates (FastAPI & Next.js)
│
├── 📚 DOCUMENTATION & CONFIG
│   ├── docs/                   → Documentation templates
│   ├── database/              → Database schemas & migrations
│   ├── .cursor/plans/          → Implementation plans
│   └── render.yaml             → Render.com deployment config
│
└── 📁 OTHER DIRECTORIES
    ├── anthology/              → Personal blog posts (296 markdown files)
    ├── projects/                → Project showcase documentation
    └── assets/                  → Static assets (fonts, images)
```

---

## Detailed Structure

### 🎯 APPS DIRECTORY

#### 1. ASK (apps/ask/)
**Purpose:** Daily Architectural Research Q&A Platform
**Tech Stack:** FastAPI (Backend) + Next.js (Frontend)

```
apps/ask/
├── api/                       # FastAPI Backend
│   ├── routes/               # API endpoints
│   │   ├── generate.py       # Q&A generation
│   │   ├── payments.py       # Payment processing (Razorpay)
│   │   ├── feasibility.py    # Business analytics
│   │   ├── monitoring.py     # Cost monitoring
│   │   ├── qa_pairs.py       # Q&A management
│   │   ├── stats.py          # Statistics
│   │   └── themes.py         # Theme management
│   ├── services/            # Business logic
│   │   ├── groq_service.py  # AI model integration
│   │   ├── cost_service.py  # Cost tracking
│   │   ├── generation_service.py
│   │   ├── chained_generation_service.py
│   │   └── csv_service.py
│   ├── utils/               # Utilities
│   │   ├── groq_monitor.py  # Cost monitoring
│   │   └── subscription.py  # Subscription management
│   ├── models_db.py         # Database models (SQLAlchemy)
│   ├── models.py            # Pydantic schemas
│   ├── config.py            # Configuration
│   ├── database.py          # Database connection
│   ├── auth.py              # Authentication
│   └── main.py              # FastAPI app
│
├── frontend/                 # Next.js Frontend
│   ├── app/                 # Next.js app router
│   │   ├── page.tsx         # Home page
│   │   ├── generate/        # Q&A generation UI
│   │   │   ├── page.tsx
│   │   │   └── flow/page.tsx
│   │   ├── browse/          # Browse Q&A pairs
│   │   ├── pricing/        # Pricing page
│   │   ├── settings/        # User settings
│   │   ├── sign-in/         # Authentication
│   │   └── admin/           # Admin dashboard
│   │       └── platform-dashboard/  # Platform analytics
│   ├── components/          # React components
│   │   ├── GenerationForm.tsx
│   │   ├── QAItem.tsx
│   │   ├── ThemeFilter.tsx
│   │   └── platform-dashboard/  # Dashboard components
│   ├── lib/                 # Utilities
│   │   ├── api.ts           # API client
│   │   └── platform-api.ts  # Platform API
│   └── auth.ts              # NextAuth configuration
│
├── alembic/                  # Database migrations (Alembic)
│   ├── env.py
│   ├── script.py.mako
│   └── versions/            # Migration scripts
├── scripts/                  # Utility scripts
├── ask-tools.ps1            # ASK-specific PowerShell utilities
├── ask.env.template         # Environment variable template
└── requirements.txt         # Python dependencies
```

**Deployment:**
- Frontend: Vercel (Next.js) → `ask.kvshvl.in`
- Backend: Render.com (FastAPI) → `ask.onrender.com`
- Database: PostgreSQL (Supabase or Upstash Postgres)
- Authentication: Centralized at `kvshvl.in`

---

#### 2. REFRAME (apps/reframe/)
**Purpose:** AI-Powered Tone Reframing Tool
**Tech Stack:** Next.js (Full-stack) + Python Backend API

```
apps/reframe/
├── app/                      # Next.js App Router
│   ├── page.tsx             # Main reframe interface
│   ├── pricing/             # Pricing page
│   ├── settings/            # User settings
│   ├── sign-in/             # Authentication
│   ├── sign-up/             # Registration
│   ├── accept-terms/         # Terms acceptance
│   ├── privacy/             # Privacy policy
│   ├── terms/               # Terms of service
│   └── api/                 # API routes (Next.js API routes)
│       ├── razorpay/        # Payment processing
│       │   ├── checkout/    # Checkout creation
│       │   └── subscriptions/  # Subscription management
│       ├── razorpay-webhook/ # Webhook handler
│       ├── reframe-proxy/   # AI generation proxy
│       ├── user-metadata/   # User data
│       ├── account/         # Account management
│       │   ├── delete/      # Account deletion
│       │   └── export/     # Data export
│       ├── usage/           # Usage tracking
│       ├── consent/          # Consent management
│       └── exchange-rates/  # Currency conversion
│
├── backend/                  # Python FastAPI Backend
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   │   └── reframe.py   # Main reframe endpoint
│   │   ├── services/        # Business logic
│   │   │   ├── groq_service.py      # AI integration
│   │   │   ├── tone_service.py      # Tone reframing
│   │   │   ├── cost_service.py     # Cost tracking
│   │   │   ├── groq_monitor.py      # Cost monitoring
│   │   │   ├── subscription_service.py
│   │   │   ├── redis_service.py
│   │   │   └── user_metadata_service.py
│   │   ├── models.py        # Database models
│   │   ├── config.py        # Configuration
│   │   ├── auth.py          # Authentication
│   │   └── main.py          # FastAPI app
│   └── requirements.txt
│
├── components/              # React components
│   ├── ui/                  # UI primitives (shadcn/ui)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── textarea.tsx
│   │   ├── toast.tsx
│   │   ├── dual-price-display.tsx
│   │   └── price-display.tsx
│   ├── HeaderWrapper.tsx
│   ├── export-data-modal.tsx
│   ├── delete-account-modal.tsx
│   └── cookie-banner.tsx
│
├── lib/                     # Utilities
│   ├── groq.ts             # AI integration
│   ├── groq-monitor.ts     # Cost monitoring
│   ├── razorpay.ts         # Payment integration
│   ├── subscription.ts     # Subscription management
│   ├── redis.ts            # Redis client
│   ├── user-metadata.ts    # User data
│   ├── consent.ts          # Consent management
│   ├── app-config.ts       # App configuration
│   └── api-client.ts       # API client
│
├── config/                  # Configuration files
│   ├── app.production.json
│   └── app.test.json
│
├── scripts/
│   └── create_razorpay_plans.ts
│
├── middleware.ts            # Next.js middleware
├── auth.ts                  # NextAuth configuration
└── types/                   # TypeScript types
```

**Deployment:**
- Frontend: Vercel (Next.js) → `reframe.kvshvl.in`
- Backend: Render.com (FastAPI) → `reframe.onrender.com`
- Database: Upstash Redis (for user metadata and caching)
- Authentication: Centralized at `kvshvl.in`

---

#### 3. SKETCH2BIM (apps/sketch2bim/)
**Purpose:** Automated Sketch-to-BIM Conversion
**Tech Stack:** FastAPI (Backend) + Next.js (Frontend) + ML Models

```
apps/sketch2bim/
├── backend/                  # FastAPI Backend
│   ├── app/
│   │   ├── routes/          # API endpoints (11 route files)
│   │   │   ├── jobs.py      # Job management
│   │   │   ├── payments.py  # Payment processing (Razorpay)
│   │   │   ├── projects.py  # Project management
│   │   │   └── ...
│   │   ├── services/        # Business logic
│   │   │   ├── cost_service.py
│   │   │   └── redis_service.py
│   │   ├── ai/              # AI/ML processing
│   │   │   ├── sketch_reader.py
│   │   │   ├── symbol_detector.py
│   │   │   ├── model_generator.py
│   │   │   ├── ifc_generator.py
│   │   │   ├── layout_generator.py
│   │   │   ├── quality_assessor.py
│   │   │   └── processing_agent.py
│   │   ├── extraction/      # IFC extraction
│   │   ├── monitoring/      # System monitoring
│   │   │   ├── alerts.py
│   │   │   ├── database_monitor.py
│   │   │   ├── redis_monitor.py
│   │   │   └── storage_monitor.py
│   │   ├── middleware/      # Custom middleware
│   │   │   ├── correlation.py
│   │   │   ├── security.py
│   │   │   └── timeout.py
│   │   ├── worker/          # Background workers
│   │   ├── utils/           # Utilities (10 files)
│   │   ├── models.py        # Database models (SQLAlchemy)
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database connection
│   │   ├── auth.py          # Authentication
│   │   └── main.py          # FastAPI app
│   ├── alembic/             # Database migrations
│   │   └── versions/        # Migration scripts (10 migrations)
│   ├── tests/               # Unit tests
│   │   ├── integration/
│   │   └── test_*.py        # Test files
│   └── scripts/             # Utility scripts
│
├── frontend/                # Next.js Frontend
│   ├── app/                 # Next.js app router
│   │   ├── page.tsx         # Home page
│   │   ├── dashboard/       # User dashboard
│   │   ├── pricing/         # Pricing page
│   │   ├── settings/        # User settings
│   │   │   └── payments/    # Payment history
│   │   ├── contact/         # Contact page
│   │   ├── privacy/         # Privacy policy
│   │   ├── terms/           # Terms of service
│   │   ├── refund/          # Refund policy
│   │   └── shipping/        # Shipping info
│   ├── components/          # React components
│   │   ├── JobCard.tsx
│   │   ├── JobList.tsx
│   │   ├── IfcViewer.tsx
│   │   ├── IfcEditor.tsx
│   │   ├── CreditsDisplay.tsx
│   │   ├── PaymentHistory.tsx
│   │   ├── ReferralLink.tsx
│   │   └── ...
│   ├── lib/                 # Utilities
│   │   ├── api.ts           # API client
│   │   ├── ifcExport.ts
│   │   └── errorLogger.ts
│   └── auth.ts              # NextAuth configuration
│
├── data/                    # Data files
│   └── symbols/             # Symbol catalog
│
├── models/                  # ML Models
│   └── symbols/             # Symbol detection models
│
├── train/                   # Model training scripts
│   ├── dataset.py
│   ├── models.py
│   ├── symbol_detector.py
│   └── configs/             # Training configurations
│
├── infra/                   # Infrastructure configs
│   ├── k8s/                 # Kubernetes configs
│   ├── fly.io/              # Fly.io deployment
│   ├── grafana/             # Monitoring dashboards
│   ├── digitalocean/        # DigitalOcean setup
│   ├── hetzner/             # Hetzner setup
│   └── vps/                 # VPS bootstrap
│
├── docs/                    # Documentation
│   └── api/                 # API documentation
│       └── openapi.yaml
│
└── scripts/
    ├── sketch2bim-tools.ps1
    ├── create_razorpay_plans.py
    └── delete_razorpay_plan.py
```

**Deployment:**
- Frontend: Vercel (Next.js) → `sketch2bim.kvshvl.in`
- Backend: Render.com (FastAPI) → `sketch2bim.onrender.com`
- Database: PostgreSQL (Supabase or Upstash Postgres)
- Storage: Bunny CDN (for file storage)
- Redis: Upstash Redis (for caching and rate limiting)
- Authentication: Centralized at `kvshvl.in`

---

### 📦 SHARED PACKAGES

#### packages/design-system/
**Purpose:** Shared React/Next.js UI components
```
packages/design-system/
├── src/
│   ├── components/          # Reusable components
│   │   ├── AppHeader.tsx
│   │   ├── AppFooter.tsx
│   │   ├── Button.tsx
│   │   └── ...
│   └── lib/                 # Utilities
└── dist/                    # Compiled output
```

#### packages/shared-backend/
**Purpose:** Shared Python utilities
```
packages/shared-backend/
├── auth/                    # Authentication utilities
├── payments/                # Payment processing
├── feasibility/             # Business analytics
├── cost-monitoring/         # Cost tracking
└── database/                # Database utilities
```

#### packages/shared-frontend/
**Purpose:** Shared TypeScript utilities
```
packages/shared-frontend/
├── src/
│   ├── auth/                # Auth types & utilities
│   ├── payments/            # Payment utilities
│   ├── cost-monitoring/     # Cost tracking
│   └── settings/             # Settings components
```

---

### 🌐 MAIN WEBSITE (app/)

**Purpose:** Portfolio/Company website and authentication hub
```
app/
├── page.tsx                 # Home page
├── projects/                # Project showcase
├── admin/                   # Admin dashboard
├── history/                 # Site history
├── links/                   # Links page
├── getintouch/              # Contact page
├── termsofservice/          # Terms of service (loads from docs/)
├── privacypolicy/           # Privacy policy (loads from docs/)
├── cancellationrefund/      # Refund policy (loads from docs/)
└── api/                     # API routes
    └── auth/                # Authentication routes
        └── signin/          # Sign-in handler
```

**Deployment:**
- Platform: Vercel (Next.js)
- Domain: `kvshvl.in` (main domain)
- Authentication: Centralized OAuth provider for all apps

---

### 🔧 CONFIGURATION FILES

#### Environment Files (Root Level)
```
├── ask.env.production       # ASK app environment variables
├── reframe.env.production   # Reframe app environment variables
└── sketch2bim.env.production # Sketch2BIM app environment variables
```

#### Deployment Configs
```
├── render.yaml              # Render.com deployment config
├── vercel.json              # Vercel deployment config (root)
└── apps/*/vercel.json       # App-specific Vercel configs
```

#### Development Tools
```
├── dev-tools.ps1           # Consolidated dev utilities
├── scripts/
│   ├── create-project.ps1  # Project generator
│   ├── verify-deployment.ps1
│   └── ...
└── templates/              # Project templates
```

---

### 📊 DATABASE STRUCTURE

**Current Setup:**
- **Option 1 (Current):** Supabase PostgreSQL with separate schemas
  - `ask_schema`: ASK application tables
  - `sketch2bim_schema`: Sketch2BIM application tables
- **Option 2 (Recommended):** Upstash Postgres with separate databases
  - One database per application (ASK, Sketch2BIM)
  - All tables in `public` schema

**Migration Files:**
```
database/
├── migrations/             # SQL migration scripts
│   ├── 01_create_schemas.sql
│   ├── 02_create_ask_tables.sql
│   ├── 03_create_sketch2bim_tables.sql
│   ├── RUN_ALL_MIGRATIONS.sql
│   └── upstash/           # Upstash-specific migrations
│       ├── ask_upstash.sql
│       └── sketch2bim_upstash.sql
└── schemas/                # Database schemas
    ├── ask_schema.sql
    └── sketch2bim_schema.sql
```

**Alembic Migrations:**
- **ASK:** `apps/ask/alembic/versions/` (Alembic migrations)
- **Sketch2BIM:** `apps/sketch2bim/backend/alembic/versions/` (10+ migrations)

**Redis:**
- **Reframe:** Uses Upstash Redis for user metadata and caching
- **Sketch2BIM:** Uses Upstash Redis for caching and rate limiting

---

## 🚀 DEPLOYMENT OVERVIEW

### Frontend Deployments (Vercel)
- **Main Website:** `kvshvl.in` (authentication hub)
- **ASK Frontend:** `ask.kvshvl.in`
- **Reframe:** `reframe.kvshvl.in`
- **Sketch2BIM Frontend:** `sketch2bim.kvshvl.in`

### Backend Deployments (Render.com)
- **ASK Backend:** `ask.onrender.com` (from `apps/ask`)
- **Reframe Backend:** `reframe.onrender.com` (from `apps/reframe/backend`)
- **Sketch2BIM Backend:** `sketch2bim.onrender.com` (from `apps/sketch2bim/backend`)

**Deployment Configuration:**
- Unified `render.yaml` at root for all backend services
- Environment variables from `*.env.production` files
- Health check endpoints: `/health`

### Databases
- **PostgreSQL (ASK & Sketch2BIM):**
  - Current: Supabase PostgreSQL (shared database, separate schemas)
  - Recommended: Upstash Postgres (separate databases per app)
- **Redis (Reframe & Sketch2BIM):**
  - Upstash Redis for caching, sessions, and user metadata

### Storage
- **Bunny CDN:** File storage for Sketch2BIM (sketches, IFC files)
- **Vercel Blob:** Static assets and public files

### Authentication
- **Centralized OAuth:** All apps use `kvshvl.in` as authentication provider
- **NextAuth.js:** Used across all Next.js frontends
- **JWT:** Backend services use JWT tokens from centralized auth

---

## 💰 PRICING STRUCTURE (Unified Across All Apps)

**Subscription Tiers:**
- **Week Pass:** ₹1,299 (7 days)
- **Monthly:** ₹3,499 (30 days)
- **Yearly:** ₹29,999 (365 days, ~33% savings)

**Payment Gateway:** Razorpay (India)
- Unified Razorpay plan IDs across all apps
- Environment variables: `*_RAZORPAY_PLAN_ID_WEEK`, `*_RAZORPAY_PLAN_ID_MONTHLY`, `*_RAZORPAY_PLAN_ID_YEARLY`
- Webhook handling for subscription events

**Tier Naming:** Standardized to `'week'`, `'monthly'`, `'yearly'` (not `'month'`/`'year'`)

---

## 🔑 KEY TECHNOLOGIES

### Frontend
- **Next.js 15** (React framework with App Router)
- **TypeScript** (Type-safe development)
- **Tailwind CSS** (Styling)
- **NextAuth.js** (Authentication)
- **shadcn/ui** (UI component library for Reframe)

### Backend
- **FastAPI** (Python web framework)
- **SQLAlchemy** (ORM for database models)
- **Alembic** (Database migrations)
- **Pydantic** (Data validation and schemas)
- **PostgreSQL** (Primary database - Supabase or Upstash Postgres)
- **Redis/Upstash** (Caching and session storage)

### AI/ML
- **Groq API** (LLM inference for all apps)
- **Custom ML models** (Sketch2BIM symbol detection)
- **Cost Monitoring** (Monthly cost thresholds, usage tracking)

### Infrastructure
- **Vercel** (Frontend hosting and serverless functions)
- **Render.com** (Backend hosting - FastAPI services)
- **Bunny CDN** (File storage for Sketch2BIM)
- **Upstash** (Redis and PostgreSQL services)
- **Supabase** (PostgreSQL alternative, being migrated from)

### Development Tools
- **PowerShell** (Windows automation scripts)
- **Poetry/pip** (Python dependency management)
- **npm/pnpm** (Node.js package management)
- **GitHub Actions** (CI/CD workflows)

---

## 📈 BUSINESS METRICS & ANALYTICS

**Cost Monitoring:**
- Monthly cost thresholds (daily thresholds removed)
- Groq API usage tracking
- Cost alerts and notifications
- Shared cost monitoring utilities in `packages/shared-backend/cost-monitoring/`

**Analytics:**
- Revenue tracking (Razorpay webhooks)
- User analytics and subscription management
- Feasibility analysis (ASK platform dashboard)
- Platform-wide dashboard (`/admin/platform-dashboard` in ASK)

**Monitoring:**
- Database monitoring (size, connections)
- Redis monitoring (command usage)
- Storage monitoring (Bunny CDN usage)
- System health checks (`/health` endpoints)

---

## 📝 NOTES FOR INVESTOR MEETING

1. **Monorepo Structure:** Single repository for all products enables code sharing and unified deployment
2. **Shared Infrastructure:** Common packages reduce development time and maintenance costs
3. **Unified Pricing:** Consistent pricing model across all products simplifies billing
4. **Scalable Architecture:** Each app can scale independently
5. **Cost Tracking:** Built-in monitoring for AI costs (Groq API)
6. **Revenue Analytics:** Platform-wide business feasibility analysis

---

## 📝 ADDITIONAL NOTES

### Environment Variables
- All environment variables use app-specific prefixes:
  - `ASK_*` for ASK application
  - `REFRAME_*` for Reframe application
  - `SKETCH2BIM_*` for Sketch2BIM application
- Production environment files: `ask.env.production`, `reframe.env.production`, `sketch2bim.env.production`
- Templates available: `apps/*/ask.env.template` (where applicable)

### Shared Packages Usage
- **shared-backend**: Used by ASK and Sketch2BIM backends for auth, payments, database models
- **shared-frontend**: Used by all Next.js frontends for auth, payments, cost monitoring
- **design-system**: Used by main website and can be used by apps

### Project Templates
- `templates/fastapi-backend/`: Template for new FastAPI backends
- `templates/nextjs-app/`: Template for new Next.js applications

### Scripts
- `dev-tools.ps1`: Consolidated development utilities
- `scripts/vercel.ps1`: Unified Vercel management script
- `scripts/create-project.ps1`: Project generator script

---

## Complete Directory Tree

For a complete file-by-file directory tree listing, see `PROJECT_TREE.txt` in the repository root. This file contains a clean, curated directory tree (2,481 lines) that excludes build artifacts and gitignored directories.

**File Details:**
- **Location:** `PROJECT_TREE.txt` (repository root)
- **Size:** ~101 KB (2,481 lines)
- **Last Generated:** 2025-11-29
- **Exclusions:** Build artifacts (.next, node_modules, __pycache__, dist, build, out, .git, .venv, etc.)
- **Format:** Clean tree structure with Unicode box-drawing characters

**Note:** The PROJECT_TREE.txt file has been regenerated and cleaned to exclude build artifacts, cache files, and gitignored directories. It provides a clean view of the actual source code and documentation structure. For the most up-to-date structure, refer to this file directly.

---

*Last Updated: 2025-11-29*

---

## Files Merged Into This Plan

This consolidated plan includes content from all implementation plans, documentation files, and reference materials:

**Implementation Plans** (merged into main phases):
- STRIPE_REMOVAL_IMPLEMENTATION_PLAN.md
- STRIPE_REMOVAL_REMAINING_WORK.md
- TIER_NAMING_STANDARDIZATION_PLAN.md
- PRICING_UNIFICATION_PLAN.md
- PRICING_UNIFICATION_VERIFICATION_PLAN.md
- UPSTASH_MIGRATION_IMPLEMENTATION_PLAN.md
- VERCEL_SCRIPT_CONSOLIDATION_IMPLEMENTATION_PLAN.md
- INFRASTRUCTURE_CONSOLIDATION_REMAINING_TASKS.md
- INFRASTRUCTURE_CONSOLIDATION_STATUS.md
- PLATFORM_STANDARDIZATION_REMAINING_TASKS.md
- BACKWARD_COMPATIBILITY_REMOVAL_REMAINING_TASKS.md
- Environment-Variable-Prefix-Migration-Remaining-Tasks.md
- reframe-naming-and-env-cleanup.plan.md
- cross-repository-consistency-audit-and-fix-b0928a3f.plan.md

**Verification & Audit Reports** (merged into appendices and Progress Summary):
- BACKEND_VERIFICATION_RESULTS.md
- REPOSITORY_AUDIT_REPORT.md
- DEPLOYMENT_CONFIGURATION_GUIDE.md
- ENV_UPDATE_INSTRUCTIONS.md
- README.md
- README (2).md
- VERIFICATION_REPORT.md - Detailed verification results (merged into Phase 0 and Progress Summary)
- REMAINING_TASKS_SUMMARY.md - Task status and progress tracking (merged into Progress Summary section)

**Project Structure Documentation** (fully merged into Appendix H):
- PROJECT_STRUCTURE.md - Complete project structure reference (fully merged)
- PROJECT_TREE.txt - Clean directory tree reference (2,481 lines, excludes build artifacts)

**Application Documentation** (referenced in Appendix F):
- All files from `apps/ask/`, `apps/sketch2bim/`, `apps/reframe/` subdirectories

**Package Documentation** (referenced in Appendix F):
- All files from `packages/shared-backend/`, `packages/shared-frontend/`, `packages/design-system/` subdirectories

**General Documentation** (referenced in Appendix F):
- All files from `docs/` subdirectory
- `database/migrations/README.md`

**Total Files Merged**: 
- 73+ markdown files from `.cursor/plans/` (including VERIFICATION_REPORT.md and REMAINING_TASKS_SUMMARY.md)
- 200+ repository documentation files (.md)
- 4 documentation template files (.md.template)
- 3 configuration/documentation files (.txt: robots.txt, .gitattributes.txt, .vercel/README.txt)
- 2 project structure files (PROJECT_STRUCTURE.md fully merged, PROJECT_TREE.txt referenced)
- **Total: 282+ files** consolidated into this single comprehensive plan

**Note**: Requirements files (requirements.txt), node_modules files, virtual environment files (.venv), and build output files (out/) were excluded as they are not documentation.

