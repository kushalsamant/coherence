# Documentation Index

## Main Documentation Files

### Migration & Structure
- **[MONOREPO_MIGRATION.md](./MONOREPO_MIGRATION.md)** - ✅ Complete migration status (all migrations finished)
- **[MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)** - Step-by-step guide for migrating applications to use shared packages
- **[APP_MIGRATION_STATUS.md](./APP_MIGRATION_STATUS.md)** - ✅ Detailed status for each application (all migrations complete)
- **[STRUCTURE_CLEANUP.md](./STRUCTURE_CLEANUP.md)** - ✅ Structure cleanup status (cleanup complete)
- **[REPO_CLEANUP_SUMMARY.md](./REPO_CLEANUP_SUMMARY.md)** - ✅ Repository cleanup summary (old repos deleted)

### Infrastructure & Configuration
- **[COST_ANALYSIS.md](./COST_ANALYSIS.md)** - Comprehensive infrastructure cost analysis for all applications
- **[DATABASE_MIGRATION_GUIDE.md](./DATABASE_MIGRATION_GUIDE.md)** - Guide for setting up shared Supabase database with schemas
- **[DATABASE_SETUP_COMPLETE.md](./DATABASE_SETUP_COMPLETE.md)** - Database setup completion status and next steps
- **[ENVIRONMENT_VARIABLES_SYNC.md](./ENVIRONMENT_VARIABLES_SYNC.md)** - Environment variables synchronization status across all codebases
- **[migrate-to-self-hosted-oracle.md](./migrate-to-self-hosted-oracle.md)** - Oracle Cloud migration guide for Reframe

### Design & Development
- **[DESIGN_SYSTEM.md](./DESIGN_SYSTEM.md)** - Design system documentation
- **[README-NEXTJS.md](./README-NEXTJS.md)** - Next.js migration documentation

### Application-Specific Documentation

#### ASK
- **[apps/ask/README.md](../apps/ask/README.md)** - ASK application documentation
- **[apps/ask/DEPLOYMENT.md](../apps/ask/DEPLOYMENT.md)** - ASK deployment guide
- **[apps/ask/TROUBLESHOOTING.md](../apps/ask/TROUBLESHOOTING.md)** - ASK troubleshooting guide
- **[apps/ask/docs/ENVIRONMENT_VARIABLES.md](../apps/ask/docs/ENVIRONMENT_VARIABLES.md)** - ASK environment variables

#### Sketch2BIM
- **[apps/sketch2bim/README.md](../apps/sketch2bim/README.md)** - Sketch2BIM application documentation
- See `apps/sketch2bim/docs/` for additional documentation

#### Reframe
- **[apps/reframe/readme.md](../apps/reframe/readme.md)** - Reframe application documentation

### Content Documentation
- `history.md` - Site history
- `cancellationrefund.md` - Cancellation and refund policy
- `privacypolicy.md` - Privacy policy
- `termsofservice.md` - Terms of service
- `competitive-analysis-HONEST.md` - Competitive analysis
- `repo-skills-CV.md` - Repository skills and CV
- `the-minimal-theme.md` - Theme documentation

## Quick Reference

**New to the monorepo?** → Start with [README.md](../README.md)

**Want to know migration status?** → [MONOREPO_MIGRATION.md](./MONOREPO_MIGRATION.md) (✅ Complete)

**Need app-specific details?** → [APP_MIGRATION_STATUS.md](./APP_MIGRATION_STATUS.md)

**Deploying an app?** → Check app-specific deployment docs:
- ASK: [apps/ask/DEPLOYMENT.md](../apps/ask/DEPLOYMENT.md)
- Sketch2BIM: See `apps/sketch2bim/docs/`
- Reframe: See `apps/reframe/readme.md`

**Environment variables?** → All production env vars are in `.env.production` files at repo root:
- `ask.env.production`
- `sketch2bim.env.production`
- `reframe.env.production`

**Cost analysis?** → [COST_ANALYSIS.md](./COST_ANALYSIS.md)

**Database setup?** → [DATABASE_MIGRATION_GUIDE.md](./DATABASE_MIGRATION_GUIDE.md)

**Troubleshooting?** → Check app-specific troubleshooting docs or [apps/ask/TROUBLESHOOTING.md](../apps/ask/TROUBLESHOOTING.md)

