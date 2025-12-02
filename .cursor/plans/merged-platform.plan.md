# KVSHVL Platform - Implementation Plan

**Last Updated**: 2025-12-02  
**Status**: ~98% Complete  
**Priority**: Testing & deployment remaining

---

## Quick Summary

- **Unified Platform**: 1 Vercel + 1 Render (from 4 Vercel + 3 Render)
- **Cost Savings**: ~55% reduction ($101/mo → $45/mo)
- **Recent**: Next.js 16 build fixed, dependabot branches cleaned

---

## Remaining Work

### Phase 1: Testing & Deployment (CRITICAL - 90% done)

- [ ] Local testing (routes, auth, API, subscriptions)
- [ ] Staging deployment
- [ ] Production migration
- [ ] Update Razorpay webhooks
- [ ] Monitor 1-2 weeks
- [ ] Remove old Vercel/Render services
- [ ] Clean up dependencies

### Phase 2: Database Migration (HIGH RISK)

- [ ] Test migrations on staging FIRST
- [ ] Run on production databases
- [ ] Export Supabase backups
- [ ] Create Upstash Postgres databases
- [ ] Import data
- [ ] Update environment variables
- [ ] Monitor 1 week before deprovisioning Supabase

### Phase 3: Frontend Components (50% done)

- [ ] Migrate settings pages (ASK, Sketch2BIM, Reframe)
- [ ] Migrate pricing pages
- [ ] Replace inline Razorpay scripts with shared utilities
- [ ] Test payment flows

### Phase 4: Configuration (33% done)

- [ ] Verify environment variables (Render, Vercel)
- [ ] Remove `STRIPE_*` variables
- [ ] Remove `*_GROQ_DAILY_COST_THRESHOLD` variables
- [ ] Update `.env.example`
- [ ] Remove backward compatibility code

### Phase 5: Documentation

- [ ] Update Stripe → Razorpay references
- [ ] Remove daily cost threshold docs
- [ ] Create migration guides

### Phase 6: Testing & Verification

- [ ] Payment flow tests (all tiers)
- [ ] Cost monitoring tests
- [ ] Database migration tests
- [ ] Infrastructure tests
- [ ] Comprehensive codebase scans

### Phase 7: Final Cleanup

- [ ] Remove Stripe from package.json/requirements.txt
- [ ] Regenerate lockfiles
- [ ] Update script references

---

## Risk Mitigation

**Database Migrations (Phase 2)**:
- Always test staging first
- Full backups before migration
- Have rollback plan ready

**Platform Consolidation (Phase 1)**:
- Test locally before deployment
- Keep old deployments active 1-2 weeks
- Monitor for import errors

**Rollback**:
```bash
# Database
cd apps/platform-api
alembic downgrade -1

# Infrastructure
# Revert env vars in dashboards
# Restore OAuth config
# Git revert code changes
```

---

## Success Criteria

- [ ] All routes work (ASK, Reframe, Sketch2BIM)
- [ ] All payments use Razorpay
- [ ] No Stripe references in code/docs
- [ ] Only monthly cost thresholds (no daily)
- [ ] Production stable for 1 week
- [ ] All databases migrated to Upstash

---

*For detailed phase information, see comprehensive plan file.*
