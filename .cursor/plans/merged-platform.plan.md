# KVSHVL Platform - Implementation Plan

**Last Updated**: 2025-12-02

**Status**: ~98% Complete (All code and infrastructure tasks done, manual testing/deployment required)

## Current Status

**Overall Progress**: ~98% Complete

### Remaining Tasks Summary

- **Phase 1**: Manual testing and deployment (90% code complete)
- **Phase 2**: Manual database migration execution (code and migrations 100% ready)
- **Phase 3**: Frontend migration to shared components (50% complete)

---

## Phase 1: Platform Consolidation

**Status**: 🟡 **90% Complete** (Code ready, manual testing required)

**Priority**: **CRITICAL**

### Remaining Tasks

#### 1.11 Testing & Migration

- [ ] Local testing (all routes, auth, API calls, subscriptions)
- [ ] Staging deployment and testing
- [ ] Production migration
- [ ] Update Razorpay webhook URLs
- [ ] Monitor for 1-2 weeks

#### 1.12 Cleanup (After 1-2 weeks of successful operation)

- [ ] Remove old Vercel projects
- [ ] Remove old Render services
- [ ] Archive old code directories
- [ ] Clean up dependencies
- [ ] Update documentation

**Next Steps**: Set environment variables, test locally, deploy to staging

---

## Phase 2: Database & Infrastructure

**Status**: ✅ **100% Ready** (All migrations created, manual execution required)

**Priority**: High

**Dependencies**: Phase 1 complete, test on staging first

### Remaining Tasks

#### 2.1 Stripe to Razorpay Database Migrations

**Note**: Current models already use `razorpay_*` fields. Only needed if production database has `stripe_*` columns.

- [ ] Check production database for `stripe_*` columns
- [ ] If found, create migration to rename columns
- [ ] Test migrations on staging database first
- [ ] Verify data integrity after migration

#### 2.2 Upstash Postgres Migration

- [ ] Export Supabase backups (ASK and Sketch2BIM schemas and data)
- [ ] Create two Upstash Postgres databases
- [ ] Run schema migrations: `cd database/migrations/ask && alembic upgrade head`
- [ ] Run schema migrations: `cd database/migrations/sketch2bim && alembic upgrade head`
- [ ] Import data from Supabase backups
- [ ] Update environment variables with Upstash connection strings
- [ ] Test locally with Upstash databases
- [ ] Deploy to production
- [ ] Monitor for 1 week before deprovisioning Supabase

**Migration System**: ✅ Complete - Unified Alembic system created at `database/migrations/`

**Note**: ⚠️ HIGH RISK - Always test on staging first

---

## Phase 3: Code Standardization

**Status**: 🟡 **50% Complete**

**Priority**: Medium

**Remaining**: 15-25 hours

### Backend Migration to Shared Components

- [ ] Migrate `apps/platform-api` to use `shared_backend` components consistently
- [ ] Preserve custom middleware (correlation, timeout, security headers)
- [ ] Migrate models to extend base models
- [ ] Test all routes work correctly

### Frontend Migration to Shared Components

- [ ] Migrate ASK settings page to use shared components
- [ ] Migrate Sketch2BIM settings page to use shared components
- [ ] Migrate Reframe settings page to use shared components
- [ ] Preserve app-specific features (data export, account deletion, etc.)
- [ ] Migrate all pricing pages to use shared payment utilities
- [ ] Replace inline Razorpay script loading with shared utilities
- [ ] Test all payment flows and subscription management

---

## Risk Assessment

### High-Risk Areas

#### Database Migrations (Phase 2)

**Risk**: Data loss, production downtime, migration failures

**Mitigation**:

- Always test on staging first
- Create full database backups before any migration
- Test rollback procedures on staging
- Schedule during low-traffic periods
- Monitor database connections and query performance
- Have rollback plan ready

**Rollback**:

```bash
# ASK database
cd database/migrations/ask
alembic downgrade -1

# Sketch2BIM database
cd database/migrations/sketch2bim
alembic downgrade -1
```

#### Platform Consolidation (Phase 1)

**Risk**: Service outages, route conflicts, subscription migration issues

**Mitigation**:

- Test all routes locally before deployment
- Keep old deployments active during migration (1-2 weeks)
- Test subdomain rewrites work correctly
- Verify unified subscription checking works across all apps
- Monitor for errors and fix incrementally

### Safety Checklist

Before starting Phase 2 database migration:

- [ ] Full database backup created (both ASK and Sketch2BIM)
- [ ] Staging environment configured and tested
- [ ] Rollback procedure tested
- [ ] Health monitoring configured
- [ ] Maintenance window scheduled (if needed)

---

## Quick Reference

### Migration Commands

**ASK database**:

```bash
cd database/migrations/ask
alembic upgrade head          # Run migrations
alembic current               # Check current version
alembic downgrade -1          # Rollback one migration
```

**Sketch2BIM database**:

```bash
cd database/migrations/sketch2bim
alembic upgrade head          # Run migrations
alembic current               # Check current version
alembic downgrade -1          # Rollback one migration
```

### Environment Variables Required

```bash
# ASK Database
ASK_DATABASE_URL=postgresql://user:password@host:5432/ask

# Sketch2BIM Database
SKETCH2BIM_DATABASE_URL=postgresql://user:password@host:5432/sketch2bim

# Platform
PLATFORM_RAZORPAY_KEY_ID=...
PLATFORM_RAZORPAY_KEY_SECRET=...
PLATFORM_RAZORPAY_WEBHOOK_SECRET=...
```

---

## Completed Work

- Platform API reorganization (auth/database/config/models consolidated)
- Legacy backward compatibility files removed
- Supabase cleanup complete (all references updated to Upstash Postgres)
- Database system recreated from scratch (unified Alembic migrations at `database/migrations/`)
- All legacy SQL migrations removed
- Migration documentation created
- Design-system package.json updated to support Next 15
- All code verification complete (no Stripe, no daily thresholds, all imports updated)
- No linter errors

---

*Last Updated: 2025-12-02 (Database System Recreated - Ready for Migration Execution)*