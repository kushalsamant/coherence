# Phase 3: Environment Variables & Configuration

> **Navigation**: [README](../README.md) | [Progress Status](../01_PROGRESS_STATUS.md)

**Status**: 🟡 Partial (66%)  
**Priority**: Medium  
**Time Estimate**: 2-3 hours remaining  
**Dependencies**: None

**Completed**:
- ✅ 3.3: Script references cleanup
- ✅ 3.2: Backward compatibility removal

**Remaining**:
- ⏳ 3.1: Environment variable verification

## 3.1 Environment Variable Verification

**Status**: ⏳ Pending  
**Time Estimate**: 2-3 hours

**Production Environments**
- [ ] Verify Render services have all prefixed variables
- [ ] Verify Vercel projects have all prefixed variables
- [ ] Remove any unprefixed variables
- [ ] Verify no `STRIPE_*` variables exist
- [ ] Verify no `*_GROQ_DAILY_COST_THRESHOLD` variables exist

**Local Development**
- ✅ Single unified `.env.local` file at repo root (organized by prefix sections)
- ✅ Backend configs updated to load root `.env.local`
- [ ] Update `.env.example` template file (if exists) to match `.env.local` structure
- [ ] Update developer documentation

**Reference**: See [Environment Variables Reference](../reference/environment-variables-reference.md)

## 3.2 Backward Compatibility Removal

**Status**: ✅ **COMPLETE**  
**Time Estimate**: 2-3 hours (completed)

**Code Cleanup** ✅ (Completed 2024-12-19)
- ✅ Removed `LIVE_KEY_ID`/`LIVE_KEY_SECRET` fallbacks from ASK config (`apps/platform-api/api/config.py`)
- ✅ Removed `LIVE_KEY_ID`/`LIVE_KEY_SECRET` fallbacks from Sketch2BIM config (`apps/sketch2bim/backend/app/config.py`)
- ✅ Updated `razorpay_key_id` and `razorpay_key_secret` properties to use only prefixed variables
- ⏳ Remove `/add-credits` endpoints (if not needed for admin) - Pending review
- ⏳ Remove legacy generate endpoint models (if not used) - Pending review

**Documentation Cleanup**
- ⏳ Remove "backward compatibility" comments from env templates
- ⏳ Update config file comments
- ⏳ Update route comments

## 3.3 Script References Cleanup

**Status**: ✅ **COMPLETE**

**Reframe package.json**
- ✅ Removed `"setup": "tsx scripts/setup.ts"` script (file doesn't exist)
- ✅ OR created the missing setup.ts file if needed

---

**Related Files**:
- [Environment Variables Reference](../reference/environment-variables-reference.md) - Complete env var list
- [Phase 0: Verification](./phase-0-verification.md) - Issue that was fixed
- [README](../README.md) - Navigation and overview

