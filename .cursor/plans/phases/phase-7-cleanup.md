# Phase 6: Dependency & Script Cleanup

> **Navigation**: [README](../README.md) | [Progress Status](../01_PROGRESS_STATUS.md)

**Status**: ✅ Complete (100%)  
**Priority**: Low (cleanup task)  
**Time Estimate**: 2-3 hours (completed)  
**Dependencies**: None (can start immediately)

> ⚡ **QUICK WIN** - Simple cleanup tasks, can be done anytime.

## 6.1 Dependency Cleanup

**Status**: ✅ **COMPLETE** (Completed 2024-12-19)  
**Time Estimate**: 1-2 hours (completed)

- ✅ Verified no `stripe` in root `package.json`
- ✅ Verified no `stripe` in any app `package.json` files
- ✅ Verified no `stripe` in `apps/platform-api/requirements.txt`
- ✅ Verified no `stripe` in `apps/ask/requirements.txt`
- ✅ Verified no `stripe` in `apps/sketch2bim/backend/requirements.txt`
- ✅ Verified no `stripe` in `apps/reframe/backend/requirements.txt`
- ✅ All payment dependencies use Razorpay (`razorpay>=1.4.0` or `razorpay>=2.9.2`)
- ✅ Verified no Stripe dependencies remain in codebase

## 6.2 Script References Verification

**Status**: ✅ **COMPLETE** (Completed 2024-12-19)  
**Time Estimate**: 1 hour (completed)

- ✅ Checked for references to deleted `setup.ts` scripts
- ✅ Verified Reframe `package.json` has no broken script references
- ✅ Searched codebase for `setup.ts` references (only found in node_modules)
- ✅ All script references in `package.json` files are valid
- ✅ No broken references found

**Note**: Reframe setup.ts reference was already fixed in Phase 3.3, and verification confirms no other broken references exist.

---

**Related Files**:
- [Phase 4: Configuration](./phase-4-configuration.md) - Related script cleanup
- [Quick Start Guide](../03_QUICK_START_GUIDE.md) - Execution order
- [README](../README.md) - Navigation and overview

