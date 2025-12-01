# Phase 1: Database & Infrastructure (Legacy)

> **Navigation**: [README](../README.md) | [Progress Status](../01_PROGRESS_STATUS.md) | [Risk Assessment](../02_RISK_ASSESSMENT.md)

**Status**: ⏳ Pending (0%) - Infrastructure consolidation superseded  
**Priority**: High (but mostly superseded by platform consolidation)  
**Time Estimate**: 8-12 hours  
**Dependencies**: Test on staging first

> ⚠️ **NOTE**: Infrastructure consolidation (Phase 1.3) is **✅ COMPLETE** - Superseded by [Phase 1: Platform Consolidation](./phase-1-platform-consolidation.md), which has unified the frontend and backend deployments. This phase now primarily focuses on database migrations.  
> ⚠️ **HIGH RISK PHASE** - See [Risk Assessment](../02_RISK_ASSESSMENT.md) before proceeding. Always test on staging first.

## 1.1 Stripe to Razorpay Database Migrations

**Status**: ⏳ Pending  
**Time Estimate**: 4-6 hours

**ASK Alembic Migration**
- **File**: `apps/ask/alembic/versions/001_rename_stripe_to_razorpay.py` (new)
- **Status**: Alembic initialized, migration file needs to be created
- **Action Items**:
  - Create migration to rename columns (if they exist in production):
    - `users.stripe_customer_id` → `razorpay_customer_id`
    - `payments.stripe_payment_intent_id` → `razorpay_payment_id`
    - `payments.stripe_checkout_session_id` → `razorpay_order_id`
  - Update indexes accordingly
  - Include downgrade function for rollback
- **Note**: Models already use `razorpay_*`, but production databases may still have `stripe_*` columns

**Sketch2BIM Alembic Migration**
- **File**: `apps/sketch2bim/backend/alembic/versions/011_rename_stripe_to_razorpay.py` (new)
- **Action Items**: Same as ASK migration
- **Dependencies**: Migration numbered `011_` (next after `010_remove_reader_type_column.py`)

**Reframe Database Verification**
- [ ] Check if Reframe has any `stripe_*` database fields
- [ ] Create migration if needed, or document if none exist

**Testing**
- [ ] Test migrations on staging database first
- [ ] Verify data integrity after migration

**Rollback**: See [Risk Assessment - Database Migrations](../02_RISK_ASSESSMENT.md#1-database-migrations-phase-11-12)

## 1.2 Upstash Postgres Migration

**Status**: ⏳ Pending  
**Time Estimate**: 4-6 hours  
**Dependencies**: Requires Phase 1.1 complete

**Pre-Migration**
- [ ] Export Supabase backups (ASK and Sketch2BIM schemas and data)
- [ ] Document current database state (row counts, table sizes)

**Migration**
- [ ] Create two Upstash Postgres databases (one for ASK, one for Sketch2BIM)
- [ ] Run schema migrations on Upstash databases
- [ ] Import data from Supabase backups
- [ ] Verify data integrity

**Configuration**
- [ ] Update environment variables with Upstash connection strings
- [ ] Update Render environment variables
- [ ] Remove `DATABASE_SCHEMA` variables (Upstash uses separate databases)

**Deployment**
- [ ] Test locally with Upstash databases
- [ ] Deploy to production
- [ ] Monitor for 1 week before deprovisioning Supabase

## 1.3 Infrastructure Consolidation - Render Services

> ⚠️ **NOTE**: This section is **✅ COMPLETE** - Superseded by [Phase 1: Platform Consolidation](./phase-1-platform-consolidation.md). The platform has been unified into a single Vercel deployment and single Render service. This section is kept for reference only.

**Status**: ✅ **COMPLETE** - Platform consolidation has unified all deployments:
- ✅ Single unified frontend on Vercel (`kvshvl.in`)
- ✅ Single unified backend on Render (`platform-api`)
- ✅ All apps accessible via path-based routes
- ✅ Unified subscription system implemented
- ✅ Subscription backend router fully functional
- See [Phase 1: Platform Consolidation](./phase-1-platform-consolidation.md) for details

**Original Instructions** (kept for reference):
- ~~Create three Render Web Services manually~~ → ✅ Now single unified service
- ~~Update all apps with OAuth~~ → ✅ Already done in platform consolidation
- See [Deployment Configuration Guide](../reference/deployment-configuration.md) for unified deployment details

**Reference**: See [Deployment Configuration Guide](../reference/deployment-configuration.md) for unified deployment steps.

**Rollback**: See [Risk Assessment - Platform Consolidation](../02_RISK_ASSESSMENT.md#2-platform-consolidation-phase-1-platform-consolidation)

---

**Related Files**:
- [Phase 0: Verification](./phase-0-verification.md) - Pre-phase verification
- [Quick Start Guide](../03_QUICK_START_GUIDE.md) - Execution checklist
- [README](../README.md) - Navigation and overview

