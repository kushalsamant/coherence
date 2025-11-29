# Backward Compatibility Removal - Remaining Tasks

## Overview

This document outlines the remaining tasks after completing the staged removal of backward compatibility across the monorepo. The main stages (1-4) have been completed, but there are cleanup, documentation, migration, and verification tasks remaining.

**Status**: Stages 1-4 completed, cleanup and migration tasks remaining

---

## Completed Stages Summary

### ✅ Stage 1: Environment Variable Cleanup
- Removed unprefixed environment variable fallbacks from all config files
- Updated helper functions to use only prefixed keys
- Updated all service files to use prefixed environment variables only
- Standardized CORS configuration

### ✅ Stage 2: Payments & Stripe Cleanup
- Removed `LIVE_KEY_*` fallbacks from shared-backend packages
- Updated all Razorpay scripts to use only prefixed envs
- Updated frontend Razorpay checkout to use only prefixed envs
- Updated documentation to remove `LIVE_KEY_*` references

### ✅ Stage 3: Legacy API Endpoints & Fields
- Removed legacy `/generate` endpoint from ASK
- Removed credits endpoints from ASK and Sketch2BIM
- Removed legacy subscription field fallbacks from Reframe
- Updated models and schemas to mark deprecated fields as historical

### ✅ Stage 4: Shared Config & Auth Simplification
- Removed `AUTH_SECRET` from shared-backend config
- Updated JWT auth to require only `NEXTAUTH_SECRET`
- Updated Reframe proxy to use only `REFRAME_NEXTAUTH_SECRET`
- Updated documentation and env templates

---

## Remaining Tasks

### Phase 1: Code Cleanup (Items Reverted by User)

#### 1.1 ASK Config - LIVE_KEY Fallbacks
**File**: `apps/ask/api/config.py`
**Status**: User reverted removal
**Current State**: Still has `LIVE_KEY_ID` and `LIVE_KEY_SECRET` fields with fallback logic
**Action Required**:
- [ ] Remove `LIVE_KEY_ID` and `LIVE_KEY_SECRET` fields (lines 84-85)
- [ ] Update `razorpay_key_id` and `razorpay_key_secret` properties to return only `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` (lines 87-95)
- [ ] Remove backward compatibility comments

**Rationale**: These were removed in Stage 2 but user reverted. Should be removed when ready.

#### 1.2 Sketch2BIM Config - LIVE_KEY Fallbacks
**File**: `apps/sketch2bim/backend/app/config.py`
**Status**: User reverted removal
**Current State**: Still has `LIVE_KEY_ID` and `LIVE_KEY_SECRET` fields with fallback logic (lines 124-136)
**Action Required**:
- [ ] Remove `LIVE_KEY_ID` and `LIVE_KEY_SECRET` fields
- [ ] Update `razorpay_key_id` and `razorpay_key_secret` properties to return only prefixed values
- [ ] Remove backward compatibility comments

**Rationale**: These were removed in Stage 2 but user reverted. Should be removed when ready.

#### 1.3 ASK Credits Endpoint
**File**: `apps/ask/api/routes/payments.py`
**Status**: User reverted removal
**Current State**: `/add-credits` endpoint still exists (lines 533-556)
**Action Required**:
- [ ] Remove `/add-credits` endpoint when ready
- [ ] Update any admin tools or scripts that use this endpoint

**Rationale**: Endpoint was removed in Stage 3 but user reverted. Keep for now if needed for admin operations.

#### 1.4 Sketch2BIM Credits Endpoint
**File**: `apps/sketch2bim/backend/app/routes/payments.py`
**Status**: User reverted removal
**Current State**: `/add-credits` endpoint still exists
**Action Required**:
- [ ] Remove `/add-credits` endpoint when ready
- [ ] Update any admin tools or scripts that use this endpoint

**Rationale**: Endpoint was removed in Stage 3 but user reverted. Keep for now if needed for admin operations.

#### 1.5 ASK Legacy Generate Models
**File**: `apps/ask/api/models.py`
**Status**: User reverted removal
**Current State**: `GenerateRequest` and `GenerateResponse` models still exist (lines 74-85)
**Action Required**:
- [ ] Remove `GenerateRequest` and `GenerateResponse` models when legacy endpoint is removed
- [ ] Verify no other code references these models

**Rationale**: Models were removed in Stage 3 but user reverted. Keep if legacy endpoint is still needed.

#### 1.6 ASK answer_image_urls Field
**File**: `apps/ask/api/models.py` and `apps/ask/api/routes/qa_pairs.py`
**Status**: User reverted removal
**Current State**: Field still exists with backward compatibility comment
**Action Required**:
- [ ] Decide if field should be kept (frontend may still use it)
- [ ] If keeping, update comment to indicate it's for frontend compatibility, not backward compatibility
- [ ] If removing, update frontend to use `answer_image_url` instead

**Rationale**: Field was kept for frontend compatibility. Verify frontend usage before removing.

---

### Phase 2: Documentation & Comments Cleanup

#### 2.1 Environment Variable Templates
**Files**: 
- `apps/ask/ask.env.template`
- Other `.env.template` files

**Current State**: Still contain backward compatibility comments
**Action Required**:
- [ ] Remove comments about "backward compatibility" for unprefixed variables (line 17 in ask.env.template)
- [ ] Remove commented-out unprefixed variable examples (lines 32-33 in ask.env.template)
- [ ] Update comments to state that only prefixed variables are supported
- [ ] Check and update other env template files similarly

**Example**:
```diff
- # Note: Code accepts both prefixed (ASK_RAZORPAY_*) and unprefixed (RAZORPAY_*)
- # variables for backward compatibility. Prefixed versions are preferred in .env files.
+ # Note: Only prefixed variables (ASK_RAZORPAY_*) are supported.

- # Unprefixed versions (also work, for backward compatibility)
- # RAZORPAY_KEY_ID=
- # RAZORPAY_KEY_SECRET=
```

#### 2.2 Config File Comments
**Files**:
- `apps/ask/api/config.py` (line 83)
- `apps/sketch2bim/backend/app/config.py` (lines 34, 124, 200)

**Action Required**:
- [ ] Remove or update "Legacy aliases (for backward compatibility)" comments
- [ ] Update "FREE_CREDITS_LIMIT kept for backward compatibility" comment to "Historical field"
- [ ] Update "SKETCH2BIM_ALLOWED_ORIGINS is supported as a legacy alias" comment

#### 2.3 Route Comments
**Files**:
- `apps/ask/api/routes/payments.py` (lines 542-543, 550-551)
- `apps/sketch2bim/backend/app/routes/payments.py` (lines 599-600, 542)

**Action Required**:
- [ ] Update DEPRECATED comments to be more specific about removal timeline
- [ ] Or remove endpoints if no longer needed

#### 2.4 Shared Frontend Types
**File**: `packages/shared-frontend/src/settings/types.ts`
**Current State**: Line 10 has `subscription?: string; // Legacy field`
**Action Required**:
- [ ] Remove legacy `subscription` field from `UserMetadata` interface
- [ ] Verify no frontend code uses this field
- [ ] Update any code that references `metadata.subscription` to use `metadata.subscription_tier`

---

### Phase 3: Legacy Alias Cleanup

#### 3.1 Sketch2BIM CORS Alias
**File**: `apps/sketch2bim/backend/app/config.py`
**Current State**: `SKETCH2BIM_ALLOWED_ORIGINS` is supported as legacy alias for `SKETCH2BIM_CORS_ORIGINS`
**Action Required**:
- [ ] Remove `SKETCH2BIM_ALLOWED_ORIGINS` fallback (line 37)
- [ ] Update `render.yaml` to use `SKETCH2BIM_CORS_ORIGINS` instead of `SKETCH2BIM_ALLOWED_ORIGINS` (line 168)
- [ ] Update `DEPLOYMENT_CONFIGURATION_GUIDE.md` to reference `SKETCH2BIM_CORS_ORIGINS` (line 254)
- [ ] Update any deployment scripts or documentation

#### 3.2 FREE_CREDITS_LIMIT
**File**: `apps/sketch2bim/backend/app/config.py`
**Current State**: Field exists but is set to 0 and marked as "kept for backward compatibility"
**Action Required**:
- [ ] Decide if this field should be removed entirely
- [ ] If keeping, update comment to "Historical field (no longer used)"
- [ ] If removing, remove from config and update `render.yaml` (line 184)
- [ ] Update `reorganize-env-production.ps1` script (line 177)

---

### Phase 4: Production Environment Migration

#### 4.1 Environment Variable Audit
**Action Required**:
- [ ] Audit all production environments (Vercel, Render, etc.) for unprefixed variables
- [ ] Create migration checklist for each environment:
  - ASK production
  - Sketch2BIM production
  - Reframe production
- [ ] Document which unprefixed variables are still in use
- [ ] Create migration timeline

#### 4.2 Vercel Environment Variables
**Action Required**:
- [ ] Review Vercel project settings for all apps
- [ ] Identify any unprefixed environment variables
- [ ] Add prefixed versions
- [ ] Test with prefixed versions
- [ ] Remove unprefixed versions after verification

#### 4.3 Render Environment Variables
**Action Required**:
- [ ] Review `render.yaml` for unprefixed variables
- [ ] Update to use only prefixed variables
- [ ] Update any Render dashboard configurations
- [ ] Test deployment with new variables

#### 4.4 Local Development Setup
**Action Required**:
- [ ] Update all `.env.example` files to show only prefixed variables
- [ ] Update developer documentation
- [ ] Create migration guide for developers

---

### Phase 5: Testing & Verification

#### 5.1 Environment Variable Testing
**Action Required**:
- [ ] Test each app with only prefixed environment variables
- [ ] Verify no fallback to unprefixed variables occurs
- [ ] Test error handling when prefixed variables are missing
- [ ] Verify startup warnings/errors are clear

#### 5.2 API Endpoint Testing
**Action Required**:
- [ ] Test that removed endpoints return 404 (if removed)
- [ ] Test that deprecated endpoints still work (if kept)
- [ ] Verify error messages are clear

#### 5.3 Authentication Testing
**Action Required**:
- [ ] Test JWT authentication with only `NEXTAUTH_SECRET`
- [ ] Verify error when `NEXTAUTH_SECRET` is missing
- [ ] Test that `AUTH_SECRET` is no longer accepted

#### 5.4 Payment Testing
**Action Required**:
- [ ] Test Razorpay integration with only prefixed keys
- [ ] Verify webhook signature validation works
- [ ] Test checkout flow end-to-end

---

### Phase 6: Documentation Updates

#### 6.1 Environment Variables Documentation
**Files**:
- `apps/ask/docs/ENVIRONMENT_VARIABLES.md` (if exists)
- `apps/sketch2bim/docs/ENVIRONMENT_VARIABLES.md`
- Any other env var documentation

**Action Required**:
- [ ] Remove all references to unprefixed variables
- [ ] Remove "backward compatibility" sections
- [ ] Update examples to show only prefixed variables
- [ ] Add migration guide for existing deployments

#### 6.2 API Documentation
**Action Required**:
- [ ] Remove documentation for deprecated endpoints
- [ ] Update API reference to reflect current endpoints only
- [ ] Add deprecation notices if endpoints are kept temporarily

#### 6.3 Deployment Documentation
**Action Required**:
- [ ] Update deployment guides to use only prefixed variables
- [ ] Update troubleshooting guides
- [ ] Remove references to `AUTH_SECRET`
- [ ] Update references to use `SKETCH2BIM_CORS_ORIGINS` instead of `SKETCH2BIM_ALLOWED_ORIGINS`

---

### Phase 7: Script & Tool Updates

#### 7.1 Environment Variable Scripts
**Files**:
- `apps/sketch2bim/scripts/reorganize-env-production.ps1`
- `apps/sketch2bim/scripts/reorganize-env.ps1`

**Action Required**:
- [ ] Remove `AUTH_SECRET` from script variable lists (line 113, 125)
- [ ] Remove `LIVE_KEY_ID` and `LIVE_KEY_SECRET` from scripts (if present)
- [ ] Update scripts to prioritize prefixed variables
- [ ] Add validation to warn about unprefixed variables

#### 7.2 Deployment Scripts
**Action Required**:
- [ ] Review all deployment scripts
- [ ] Update to use only prefixed environment variables
- [ ] Add validation checks
- [ ] Update error messages

---

### Phase 8: Final Verification

#### 8.1 Code Review
**Action Required**:
- [ ] Search codebase for any remaining "backward compatibility" comments
- [ ] Search for any remaining fallback patterns (`or os.getenv("UNPREFIXED")`)
- [ ] Verify all helper functions use only prefixed keys
- [ ] Check for any missed `AUTH_SECRET` references

#### 8.2 Integration Testing
**Action Required**:
- [ ] Full integration test of all apps with prefixed variables only
- [ ] Test authentication flow
- [ ] Test payment flow
- [ ] Test API endpoints
- [ ] Verify no errors in logs related to missing unprefixed variables

#### 8.3 Production Verification
**Action Required**:
- [ ] Deploy to staging with prefixed variables only
- [ ] Run smoke tests
- [ ] Monitor for any issues
- [ ] Deploy to production after verification
- [ ] Monitor production logs for any fallback warnings

---

## Priority Levels

### High Priority (Do First)
1. **Phase 4: Production Environment Migration** - Critical for production stability
2. **Phase 5: Testing & Verification** - Ensure nothing breaks
3. **Phase 6: Documentation Updates** - Keep docs accurate

### Medium Priority (Do Next)
4. **Phase 2: Documentation & Comments Cleanup** - Improve code clarity
5. **Phase 3: Legacy Alias Cleanup** - Remove remaining aliases
6. **Phase 7: Script & Tool Updates** - Keep tools in sync

### Low Priority (Do When Ready)
7. **Phase 1: Code Cleanup (Reverted Items)** - User may want to keep these
8. **Phase 8: Final Verification** - Final polish

---

## Decision Points

### Items Requiring User Decision

1. **LIVE_KEY Fallbacks in ASK/Sketch2BIM Configs**
   - **Question**: Should these be removed now or kept for transition period?
   - **Recommendation**: Remove after production migration is complete

2. **Credits Endpoints**
   - **Question**: Are these still needed for admin operations?
   - **Recommendation**: Keep if needed, but mark clearly as admin-only

3. **Legacy Generate Endpoint**
   - **Question**: Is the legacy `/generate` endpoint still in use?
   - **Recommendation**: Remove if not used, or document as deprecated

4. **answer_image_urls Field**
   - **Question**: Is frontend still using this field?
   - **Recommendation**: Keep if frontend needs it, but update comment

5. **FREE_CREDITS_LIMIT**
   - **Question**: Should this field be removed from config entirely?
   - **Recommendation**: Remove if not used anywhere

---

## Migration Checklist Template

For each production environment:

- [ ] Audit current environment variables
- [ ] Identify unprefixed variables in use
- [ ] Add prefixed versions
- [ ] Test with prefixed versions
- [ ] Update deployment configuration
- [ ] Deploy to staging
- [ ] Verify functionality
- [ ] Deploy to production
- [ ] Remove unprefixed variables
- [ ] Monitor for issues

---

## Notes

- Some items were reverted by the user, indicating they may want to keep certain backward compatibility for now
- Focus on production migration and testing first
- Documentation updates should follow code changes
- Final cleanup can be done incrementally

---

## Timeline Estimate

- **Phase 4 (Production Migration)**: 2-3 days
- **Phase 5 (Testing)**: 1-2 days
- **Phase 6 (Documentation)**: 1 day
- **Phase 2-3 (Cleanup)**: 1-2 days
- **Phase 7 (Scripts)**: 0.5 day
- **Phase 1, 8 (Final cleanup)**: 1-2 days

**Total**: ~7-10 days for complete cleanup

---

## Success Criteria

- [ ] All production environments use only prefixed environment variables
- [ ] No fallback logic remains in codebase
- [ ] All documentation is updated
- [ ] All tests pass with prefixed variables only
- [ ] No backward compatibility comments remain (except for user-kept items)
- [ ] Production deployments are stable

