# Phase 4: Documentation Updates

> **Navigation**: [README](../README.md) | [Progress Status](../01_PROGRESS_STATUS.md)

**Status**: ⏳ Pending (0%)  
**Priority**: Low (can be done in parallel)  
**Time Estimate**: 6-8 hours  
**Dependencies**: None (can start immediately)

> ⚡ **QUICK WIN** - Can be done in parallel with other phases, no code changes required.  
> **Note**: No Stripe references found in `docs/` directory - may already be updated or documentation files may be located elsewhere.

## 4.1 Stripe → Razorpay Documentation

**Status**: ⏳ Pending  
**Time Estimate**: 3-4 hours

**Files to Update**:
- [ ] `docs/DATABASE_MIGRATION_GUIDE.md` - Update SQL examples
- [ ] `docs/repo-skills-CV.md` - Replace Stripe mentions
- [ ] `docs/migrate-to-self-hosted-oracle.md` - Update env var examples
- [ ] `docs/competitive-analysis-HONEST.md` - Update payment processor mentions
- [ ] `docs/termsofservice.md` - Update payment processor references
- [ ] `docs/privacypolicy.md` - Replace Stripe section with Razorpay
- [ ] `docs/cancellationrefund.md` - Update processing timelines

## 4.2 Cost Monitoring Documentation

**Status**: ⏳ Pending  
**Time Estimate**: 2 hours

**Files to Update**:
- [ ] `docs/COST_ANALYSIS.md` - Remove daily threshold references
- [ ] `docs/ENVIRONMENT_VARIABLES_REFERENCE.md` - Remove daily threshold entries
- [ ] `apps/ask/docs/COST_MONITORING_SETUP.md` - Remove daily threshold examples

## 4.3 Migration Guides

**Status**: ⏳ Pending  
**Time Estimate**: 1-2 hours

**Files to Create**:
- [ ] `docs/migrations/ASK_MIGRATION_GUIDE.md`
- [ ] `docs/migrations/SKETCH2BIM_MIGRATION_GUIDE.md`
- [ ] `docs/migrations/REFRAME_MIGRATION_GUIDE.md`

---

## Documentation Reference

### Documentation Index

See [docs/DOCUMENTATION_INDEX.md](../../docs/DOCUMENTATION_INDEX.md) for the complete documentation guide.

### Application-Specific Documentation

#### ASK Application
- `apps/ask/README.md` - Application overview
- `apps/ask/DEPLOYMENT.md` - Deployment guide
- `apps/ask/docs/ENVIRONMENT_VARIABLES.md` - Environment configuration

#### Sketch2BIM Application
- `apps/sketch2bim/README.md` - Application overview
- `apps/sketch2bim/docs/deployment_checklist.md` - Deployment checklist
- `apps/sketch2bim/docs/testing.md` - Testing guide

#### Reframe Application
- `apps/reframe/readme.md` - Application overview
- `apps/reframe/backend/README.md` - Backend documentation

### Package Documentation

- `packages/shared-backend/README.md` - Shared Python utilities
- `packages/shared-frontend/README.md` - Shared TypeScript utilities
- `packages/design-system/README.md` - Design system overview

### General Documentation

Located in `docs/` directory:
- `docs/DOCUMENTATION_INDEX.md` - Complete documentation index
- `docs/COST_ANALYSIS.md` - Infrastructure cost analysis
- `docs/DEPLOYMENT_CHECKLIST.md` - Deployment steps
- `docs/ENVIRONMENT_VARIABLES_REFERENCE.md` - Environment variables

For complete list, see [docs/DOCUMENTATION_INDEX.md](../../docs/DOCUMENTATION_INDEX.md).

## Documentation Templates and Configuration Files

### Documentation Templates

The platform includes templates for generating consistent documentation for new projects.

#### Template Variables
- `{{APP_NAME}}` - Application name (lowercase)
- `{{APP_DISPLAY_NAME}}` - Display name
- `{{APP_PREFIX}}` - Uppercase prefix for env vars
- `{{APP_DESCRIPTION}}` - Application description
- `{{YEAR}}` - Current year

#### Available Templates

1. **README.md.template** - Project README template
   - Location: `docs/templates/README.md.template

2. **DEPLOYMENT.md.template** - Deployment guide template
   - Location: `docs/templates/DEPLOYMENT.md.template`

3. **ENVIRONMENT_VARIABLES.md.template** - Environment variables reference
   - Location: `docs/templates/ENVIRONMENT_VARIABLES.md.template`

4. **API_DOCUMENTATION.md.template** - API documentation template
   - Location: `docs/templates/API_DOCUMENTATION.md.template`

**Usage**: These templates are used by project generator scripts (`scripts/create-project.ps1`).

### Configuration Files

#### robots.txt
SEO configuration for search engine crawlers. See repository root `robots.txt`.

#### .gitattributes
Git configuration for line endings and binary file handling.

#### .vercel/README.txt
Information about Vercel deployment configuration.

---

**Related Files**:
- [Quick Start Guide](../README.md#-quick-start-guide) - Recommended execution order
- [README](../README.md) - Navigation and overview

