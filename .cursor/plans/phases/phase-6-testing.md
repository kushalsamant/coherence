# Phase 5: Testing & Verification

> **Navigation**: [README](../README.md) | [Progress Status](../01_PROGRESS_STATUS.md)

**Status**: ⏳ Pending (0%)  
**Priority**: High (must be done after code changes)  
**Time Estimate**: 8-12 hours  
**Dependencies**: Phases 1, 2, 3 must be complete

> ⚠️ **BLOCKING PHASE** - Cannot start until Phases 1, 2, and 3 are complete.  
> **Note**: Phase 1 is 90% complete (subscription backend done), Phase 3 is 66% complete. Phase 2 is 50% complete. Testing can begin after remaining Phase 1 tasks (testing/deployment) are done.

## 5.1 Pricing Unification Verification

**Status**: ⏳ Pending  
**Time Estimate**: 2-3 hours

- [ ] Verify checkout routes support all tiers (week/monthly/yearly)
- [ ] Verify webhook handlers correctly identify all tiers
- [ ] Verify subscription duration logic includes weekly
- [ ] Verify Razorpay dashboard shows unified plan IDs
- [ ] Test end-to-end payment flows for all tiers

**Unified Plan IDs**:
- Week: `plan_Rha5Ikcm5JrGqx`
- Month: `plan_Rha5JNPsk1WmI6`
- Year: `plan_Rha5Jzn1sk8o1X`

## 5.2 Comprehensive Codebase Scans

**Status**: ⏳ Pending  
**Time Estimate**: 2-3 hours

- [ ] Search for remaining Stripe references (excluding node_modules, .git, lockfiles)
- [ ] Categorize: Code, Documentation, Comments, Config
- [ ] Fix all functional code references
- [ ] Update documentation
- [ ] Search for `GROQ_DAILY_COST_THRESHOLD` or `DAILY_COST_THRESHOLD`
- [ ] Remove from code, update documentation

## 5.3 Conceptual Verification

**Status**: ⏳ Pending  
**Time Estimate**: 4-6 hours

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

## Backend Verification Results

### Pricing Unification - ✅ Verified Complete

**Status**: All backend code verification tasks completed. The codebase fully supports unified pricing structure with weekly tier across all three applications.

#### Key Findings

- ✅ Environment variables reference correct settings
- ✅ Unified plan IDs in production configuration (all apps use same plan IDs)
- ✅ Backend checkout routes support all tiers (week/month/year)
- ✅ Webhook handlers map weekly tier correctly
- ✅ Subscription duration logic includes weekly (7 days)
- ✅ All hardcoded tier lists include `week`
- ✅ No old pricing references found

#### Unified Plan IDs

- **Week**: `plan_Rha5Ikcm5JrGqx`
- **Month**: `plan_Rha5JNPsk1WmI6`
- **Year**: `plan_Rha5Jzn1sk8o1X`

#### Note

Reframe backend Python service has minor inconsistencies but is not used for payments (Reframe uses Next.js API routes).

---

**Related Files**:
- [Phase 2: Database & Infrastructure](./phase-2-database-infrastructure.md) - Migration testing
- [Phase 3: Code Standardization](./phase-3-code-standardization.md) - Code verification
- [README](../README.md) - Navigation and overview

