# Phase 2: Code Standardization & Cleanup

> **Navigation**: [README](../README.md) | [Progress Status](../01_PROGRESS_STATUS.md)

**Status**: 🟡 Partial (50%)  
**Priority**: Medium  
**Time Estimate**: 15-25 hours remaining  
**Dependencies**: None

**Completed**:
- ✅ 2.1: Tier naming standardization
- ✅ 2.2: Daily cost threshold removal

**Remaining**:
- ⏳ 2.3: Backend migration to shared components
- ⏳ 2.4: Frontend migration to shared components

## 2.1 Tier Naming Standardization

**Status**: ✅ **COMPLETE** - Verified in codebase verification (Phase 0)

All tier naming is already standardized to `'monthly'` and `'yearly'` across:
- ✅ ASK frontend pricing page
- ✅ Sketch2BIM frontend pricing, settings, and payments pages
- ✅ Sketch2BIM frontend components (CreditsDisplay)
- ✅ Sketch2BIM backend schemas
- ✅ Sketch2BIM Razorpay plan creation script

**No action required** - This phase is complete.

## 2.2 Daily Cost Threshold Removal

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

## 2.3 Backend Migration to Shared Components

**Status**: ⏳ Pending  
**Time Estimate**: 8-12 hours

**ASK Backend**
- **Action Items**:
  - [ ] Migrate `apps/ask/api/main.py` to use `shared_backend.api.factory.create_app`
  - [ ] Migrate `apps/ask/api/models_db.py` to extend `BaseUser` and `BasePayment`

**Sketch2BIM Backend**
- **Action Items**:
  - [ ] Migrate `apps/sketch2bim/backend/app/main.py` to use FastAPI factory
  - [ ] Preserve custom middleware (correlation, timeout, security headers)
  - [ ] Migrate models to extend base models

**Testing**
- [ ] Ensure all routes work correctly
- [ ] Test middleware functionality
- [ ] Verify database operations work

**Rollback**: See [Risk Assessment - Code Standardization](../02_RISK_ASSESSMENT.md#3-code-standardization-phase-23-24)

## 2.4 Frontend Migration to Shared Components

**Status**: ⏳ Pending  
**Time Estimate**: 7-13 hours

**Settings Pages**
- **Action Items**:
  - [ ] Migrate ASK settings page to use shared components
  - [ ] Migrate Sketch2BIM settings page to use shared components
  - [ ] Migrate Reframe settings page to use shared components
  - [ ] Preserve app-specific features (data export, account deletion, etc.)

**Pricing Pages**
- **Action Items**:
  - [ ] Migrate all pricing pages to use shared payment utilities
  - [ ] Replace inline Razorpay script loading with shared utilities

**Testing**
- [ ] Test all payment flows
- [ ] Test subscription management
- [ ] Test user settings functionality

---

**Related Files**:
- [Phase 0: Verification](./phase-0-verification.md) - Verification results
- [Progress Status](../01_PROGRESS_STATUS.md) - Current status
- [README](../README.md) - Navigation and overview

