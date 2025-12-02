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

### Remaining Tasks

- [ ] Test migrations on staging database first
- [ ] Run migrations on production databases
- [ ] Verify data integrity after migration
- [ ] Export Supabase backups (ASK and Sketch2BIM schemas and data)
- [ ] Create two Upstash Postgres databases
- [ ] Import data from Supabase backups
- [ ] Update environment variables with Upstash connection strings
- [ ] Test locally with Upstash databases
- [ ] Deploy to production
- [ ] Monitor for 1 week before deprovisioning Supabase

**Note**: ⚠️ HIGH RISK - Always test on staging first

---

## Phase 3: Code Standardization

**Status**: 🟡 **50% Complete**

**Priority**: Medium

### Remaining Tasks

#### 3.4 Frontend Migration to Shared Components

- [ ] Migrate ASK settings page to use shared components
- [ ] Migrate Sketch2BIM settings page to use shared components
- [ ] Migrate Reframe settings page to use shared components
- [ ] Preserve app-specific features (data export, account deletion, etc.)
- [ ] Migrate all pricing pages to use shared payment utilities
- [ ] Replace inline Razorpay script loading with shared utilities
- [ ] Test all payment flows and subscription management

---

## Phase 4: Configuration

**Status**: 🟡 **33% Complete**

**Priority**: Medium

### Remaining Tasks

#### 4.1 Environment Variable Verification

- [ ] Verify Render services have all prefixed variables
- [ ] Verify Vercel projects have all prefixed variables
- [ ] Remove any unprefixed variables
- [ ] Verify no `STRIPE_*` variables exist
- [ ] Verify no `*_GROQ_DAILY_COST_THRESHOLD` variables exist
- [ ] Update `.env.example` template file to match `.env.local` structure
- [ ] Update developer documentation

#### 4.2 Backward Compatibility Removal

- [ ] Remove `/add-credits` endpoints (if not needed for admin)
- [ ] Remove legacy generate endpoint models (if not used)
- [ ] Remove "backward compatibility" comments from env templates
- [ ] Update config file comments
- [ ] Update route comments

---

## Phase 5: Documentation

**Status**: ⏳ **PENDING (0%)**

**Priority**: Low

### Remaining Tasks

#### 5.1 Stripe → Razorpay Documentation

- [ ] Update `docs/DATABASE_MIGRATION_GUIDE.md` - Update SQL examples
- [ ] Update `docs/repo-skills-CV.md` - Replace Stripe mentions
- [ ] Update `docs/migrate-to-self-hosted-oracle.md` - Update env var examples
- [ ] Update `docs/competitive-analysis-HONEST.md` - Update payment processor mentions
- [ ] Update `docs/termsofservice.md` - Update payment processor references
- [ ] Update `docs/privacypolicy.md` - Replace Stripe section with Razorpay
- [ ] Update `docs/cancellationrefund.md` - Update processing timelines

#### 5.2 Cost Monitoring Documentation

- [ ] Update `docs/COST_ANALYSIS.md` - Remove daily threshold references
- [ ] Update `docs/ENVIRONMENT_VARIABLES_REFERENCE.md` - Remove daily threshold entries
- [ ] Update `apps/ask/docs/COST_MONITORING_SETUP.md` - Remove daily threshold examples

#### 5.3 Migration Guides

- [ ] Create `docs/migrations/ASK_MIGRATION_GUIDE.md`
- [ ] Create `docs/migrations/SKETCH2BIM_MIGRATION_GUIDE.md`
- [ ] Create `docs/migrations/REFRAME_MIGRATION_GUIDE.md`

---

## Phase 6: Testing & Verification

**Status**: ⏳ **PENDING (0%)**

**Priority**: High (must be done after code changes)

### Remaining Tasks

#### 6.1 Pricing Unification Verification

- [ ] Verify checkout routes support all tiers (week/monthly/yearly)
- [ ] Verify webhook handlers correctly identify all tiers
- [ ] Verify subscription duration logic includes weekly
- [ ] Verify Razorpay dashboard shows unified plan IDs
- [ ] Test end-to-end payment flows for all tiers

#### 6.2 Comprehensive Codebase Scans

- [ ] Search for remaining Stripe references (excluding node_modules, .git, lockfiles)
- [ ] Categorize: Code, Documentation, Comments, Config
- [ ] Fix all functional code references
- [ ] Update documentation
- [ ] Search for `GROQ_DAILY_COST_THRESHOLD` or `DAILY_COST_THRESHOLD`
- [ ] Remove from code, update documentation

#### 6.3 Conceptual Verification

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

## Phase 7: Cleanup

**Status**: ⏳ **PENDING (0%)**

**Priority**: Low (after verification period)

### Remaining Tasks

#### 7.1 Dependency Cleanup

- [ ] Remove stripe from package.json files
- [ ] Remove stripe from requirements.txt files
- [ ] Regenerate lockfiles

#### 7.2 Script References Verification

- [ ] Check for references to deleted setup.ts scripts
- [ ] Update package.json scripts
- [ ] Update documentation

**Note**: Only do this after successful production deployment and verification period

---

## Risk Assessment

**⚠️ Important**: Review this section before starting any phase implementation.

### High-Risk Areas

#### 1. Database Migrations (Phase 2)

**Risk**: Data loss, production downtime, migration failures

**Mitigation**:

- Always test on staging first
- Create full database backups before any migration
- Test rollback procedures on staging
- Schedule during low-traffic periods
- Monitor database connections and query performance
- Have rollback plan ready (downgrade migrations)

#### 2. Platform Consolidation (Phase 1)

**Risk**: Service outages, route conflicts, import path errors, subscription migration issues

**Mitigation**:

- Test all routes locally before deployment
- Keep old deployments active during migration (1-2 weeks)
- Test subdomain rewrites work correctly
- Verify unified subscription checking works across all apps
- Test authentication flow from all app routes
- Monitor for import path errors and fix incrementally
- Test backend route migration thoroughly before production

#### 3. Code Standardization (Phase 3)

**Risk**: Breaking changes, shared component bugs affecting multiple apps

**Mitigation**:

- Migrate one app at a time
- Test thoroughly before moving to next app
- Keep old code as fallback (git branches)
- Run comprehensive test suites

### Rollback Procedures

#### Database Migrations

```bash
# Rollback Alembic migration
cd apps/platform-api
alembic downgrade -1  # Go back one migration

# Or rollback to specific version
alembic downgrade <previous_version>
```

#### Infrastructure Rollback

- Revert environment variables in Render/Vercel dashboards
- Restore old OAuth configuration if needed
- Revert code changes via git if necessary

#### Code Changes

- Use feature branches for all changes
- Keep main branch stable
- Tag releases before major changes
- Use git revert for quick rollbacks

---

## Success Criteria

### Implementation Success Criteria

- [ ] All database columns use `razorpay_*` naming (no `stripe_*`)
- [ ] All code references use `razorpay_*` field names
- [ ] All documentation mentions Razorpay (not Stripe)
- [ ] All legal docs reference Razorpay
- [ ] No daily cost threshold configuration or alerts
- [ ] Only monthly cost thresholds documented and used
- [ ] Tier naming standardized to "monthly"/"yearly" across all apps
- [ ] All apps migrated to shared components
- [ ] No Stripe dependencies in package files
- [ ] Environment variables consistent across all environments
- [ ] All migrations tested and working
- [ ] Production deployments stable

---

## Notes

- **Platform Consolidation**: The platform has been unified from 4 Vercel projects + 3 Render backends into 1 unified Vercel + 1 unified Render service
- **Cost Impact**: ~55% reduction (from ~$101/mo to ~$45/mo)
- **Build Fixed**: Next.js 16 build issues resolved (workspace package + removed submodule command)
- **Branch Cleanup**: All dependabot branches cleaned up (merged Next.js 16, deleted old PRs)
- For questions or clarifications, refer to the specific phase sections above

---

*Last Updated: 2025-12-02 (Build fixes and branch cleanup complete)*
