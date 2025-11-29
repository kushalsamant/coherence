# Pricing Unification - Verification & Testing Plan

**Status:** ⏳ PENDING VERIFICATION  
**Last Updated:** January 2025  
**Goal:** Verify that pricing unification is complete and working end-to-end across all applications.

---

## ✅ What Has Been Completed

### Configuration & Code Updates
- ✅ Environment variables unified across all apps
- ✅ Frontend pricing pages show unified values (₹1,299 / ₹3,499 / ₹29,999)
- ✅ Backend configs use unified defaults
- ✅ All documentation updated
- ✅ Reframe fully updated with weekly tier support
- ✅ ASK and Sketch2BIM frontends show weekly tier

### Documentation
- ✅ `ENVIRONMENT_VARIABLES_REFERENCE.md` has canonical pricing section
- ✅ All README files mention unified pricing
- ✅ `COST_ANALYSIS.md` updated
- ✅ `COMPETITIVE_ANALYSIS.md` updated

---

## 🔍 Verification Tasks Remaining

### Task 1: Verify Backend Checkout Routes Support All Tiers
**Priority:** High  
**Status:** ⏳ Pending Verification

**ASK Backend:**
- [ ] Verify `apps/ask/api/routes/checkout.py` (or equivalent) handles `week`, `month`, and `year` tiers
- [ ] Verify it uses environment variables (`ASK_RAZORPAY_WEEK_AMOUNT`, `ASK_RAZORPAY_MONTH_AMOUNT`, `ASK_RAZORPAY_YEAR_AMOUNT`)
- [ ] Verify it uses unified plan IDs for subscriptions
- [ ] Check that weekly tier is properly mapped to Razorpay plan ID

**Sketch2BIM Backend:**
- [ ] Verify `apps/sketch2bim/backend/app/routes/payments.py` (or equivalent) handles all three tiers
- [ ] Verify it uses environment variables (`SKETCH2BIM_RAZORPAY_WEEK_AMOUNT`, etc.)
- [ ] Verify it uses unified plan IDs for subscriptions
- [ ] Check that weekly tier is properly mapped to Razorpay plan ID

**Reframe Backend:**
- [x] Already verified - Reframe uses Next.js API routes, all updated

**Action Items:**
1. Read backend checkout/razorpay route files for ASK and Sketch2BIM
2. Verify tier mapping logic includes `week`
3. Verify environment variable usage
4. Verify plan ID usage matches unified values

---

### Task 2: Verify Webhook Handlers Support All Tiers
**Priority:** High  
**Status:** ⏳ Pending Verification

**ASK Backend:**
- [ ] Verify webhook handler correctly identifies `week`, `month`, and `year` tiers from amounts/plan IDs
- [ ] Verify amount-to-tier mapping includes weekly: `129900` → `week`
- [ ] Verify plan-to-tier mapping includes: `plan_Rha5Ikcm5JrGqx` → `week`

**Sketch2BIM Backend:**
- [ ] Verify webhook handler correctly identifies all three tiers
- [ ] Verify amount-to-tier mapping includes weekly
- [ ] Verify plan-to-tier mapping includes unified plan IDs

**Reframe:**
- [x] Already verified - webhook handler updated with weekly support

**Action Items:**
1. Find webhook handler files in ASK and Sketch2BIM backends
2. Verify amount/plan ID mapping dictionaries include all three tiers
3. Ensure mapping uses unified values from environment variables

---

### Task 3: Verify Subscription Duration Logic
**Priority:** Medium  
**Status:** ⏳ Pending Verification

**ASK Backend:**
- [ ] Verify subscription duration calculation includes `week: 7` days
- [ ] Check that subscription expiry logic handles weekly subscriptions correctly

**Sketch2BIM Backend:**
- [ ] Verify subscription duration calculation includes `week: 7` days
- [ ] Check that subscription expiry logic handles weekly subscriptions correctly

**Reframe:**
- [x] Already verified - `subscription.ts` includes weekly duration

**Action Items:**
1. Find subscription service/utility files in ASK and Sketch2BIM
2. Verify duration constants include weekly tier
3. Check expiry calculation logic

---

### Task 4: End-to-End Testing Plan
**Priority:** High  
**Status:** ⏳ Pending

**Test Scenarios:**
- [ ] **ASK App - Weekly Subscription:**
  - [ ] Navigate to pricing page
  - [ ] Click "Subscribe" on Week plan (₹1,299)
  - [ ] Complete Razorpay checkout (test mode)
  - [ ] Verify webhook received and processed
  - [ ] Verify user subscription updated to `week` tier
  - [ ] Verify subscription expires in 7 days

- [ ] **ASK App - Monthly Subscription:**
  - [ ] Test monthly subscription flow (₹3,499)
  - [ ] Verify subscription expires in 30 days

- [ ] **ASK App - Yearly Subscription:**
  - [ ] Test yearly subscription flow (₹29,999)
  - [ ] Verify subscription expires in 365 days

- [ ] **Sketch2BIM App - Weekly Subscription:**
  - [ ] Test all three tiers (week/month/year)
  - [ ] Verify checkout flow works
  - [ ] Verify webhooks process correctly

- [ ] **Sketch2BIM App - Monthly/Yearly:**
  - [ ] Test remaining tiers
  - [ ] Verify subscription durations

- [ ] **Reframe App - All Tiers:**
  - [ ] Verify weekly tier works end-to-end
  - [ ] Test all three tiers

**Action Items:**
1. Set up test Razorpay account (if not already done)
2. Configure test webhook endpoints
3. Execute test scenarios in staging/development environment
4. Document results

---

### Task 5: Verify Plan IDs in Production
**Priority:** Critical  
**Status:** ⏳ Pending

**Production Verification:**
- [ ] Verify Razorpay dashboard shows unified plan IDs:
  - [ ] `plan_Rha5Ikcm5JrGqx` (Week)
  - [ ] `plan_Rha5JNPsk1WmI6` (Month)
  - [ ] `plan_Rha5Jzn1sk8o1X` (Year)
- [ ] Verify all three apps use the SAME plan IDs (not app-specific)
- [ ] Verify plan IDs are active in Razorpay dashboard
- [ ] Verify plan amounts match unified pricing

**Action Items:**
1. Log into Razorpay dashboard
2. Navigate to Plans section
3. Verify the three unified plan IDs exist
4. Verify plan details (amount, interval) match canonical values
5. Confirm no app-specific plan IDs are being used

---

### Task 6: Search for Remaining Old Pricing References
**Priority:** Medium  
**Status:** ⏳ Pending

**Search Areas:**
- [ ] Test files and fixtures
- [ ] Email templates
- [ ] Notification text
- [ ] API response examples in documentation
- [ ] Marketing/landing page copy
- [ ] Blog posts or announcements
- [ ] Error messages
- [ ] Log messages or debug output

**Search Terms:**
- `999` (old monthly)
- `7999` (old yearly)
- `99900` (old monthly in paise)
- `799900` (old yearly in paise)
- `99` (old daily pricing)
- Old plan IDs (if any)

**Known Legacy References:**
- `apps/ask/scripts/setup.ts` - Stripe script with old values (already marked as legacy)

**Action Items:**
1. Run comprehensive grep search across entire codebase
2. Check documentation files not yet reviewed
3. Review email templates (if any)
4. Update or remove old references

---

### Task 7: Verify Environment Variables in Production
**Priority:** Critical  
**Status:** ⏳ Pending

**Production Environment Verification:**
- [ ] **ASK Production (Render/Vercel):**
  - [ ] Verify `ASK_RAZORPAY_WEEK_AMOUNT=129900` is set
  - [ ] Verify `ASK_RAZORPAY_MONTH_AMOUNT=349900` is set
  - [ ] Verify `ASK_RAZORPAY_YEAR_AMOUNT=2999900` is set
  - [ ] Verify plan ID variables are set correctly

- [ ] **Sketch2BIM Production:**
  - [ ] Verify all pricing amount variables are set
  - [ ] Verify plan ID variables are set correctly

- [ ] **Reframe Production:**
  - [ ] Verify all pricing amount variables are set
  - [ ] Verify plan ID variables are set correctly

**Action Items:**
1. Log into production deployment platforms (Render, Vercel)
2. Check environment variables for each service
3. Compare against `*.env.production` files
4. Update if discrepancies found

---

### Task 8: Documentation Verification
**Priority:** Low  
**Status:** ✅ Mostly Complete

**Remaining Checks:**
- [ ] Verify all pricing references in app-specific docs (e.g., `apps/ask/docs/*`, `apps/sketch2bim/docs/*`)
- [ ] Check deployment guides mention unified pricing
- [ ] Verify API documentation (if any) mentions unified pricing
- [ ] Check any onboarding or setup guides

**Action Items:**
1. Search for pricing references in all documentation directories
2. Update any outdated references
3. Add notes about unified pricing where relevant

---

### Task 9: Database Migration Verification (if applicable)
**Priority:** Medium  
**Status:** ⏳ Pending

**Database Checks:**
- [ ] Verify subscription tier enum/constraints include `week` (not just `month` and `year`)
- [ ] Check existing subscriptions - ensure migration path if tier structure changed
- [ ] Verify database schema supports weekly subscriptions

**Action Items:**
1. Check database schema/migration files
2. Verify subscription tier columns/types
3. Plan migration if schema updates needed

---

## 📋 Verification Execution Plan

### Phase 1: Code Verification (No Deployment Required)
1. ✅ Task 1: Verify Backend Checkout Routes
2. ✅ Task 2: Verify Webhook Handlers
3. ✅ Task 3: Verify Subscription Duration Logic
4. ✅ Task 6: Search for Old Pricing References
5. ✅ Task 8: Documentation Verification

**Estimated Time:** 2-3 hours  
**Can be done immediately**

---

### Phase 2: Configuration Verification (Requires Access)
1. ⏳ Task 4: End-to-End Testing
2. ⏳ Task 5: Verify Plan IDs in Production
3. ⏳ Task 7: Verify Environment Variables in Production
4. ⏳ Task 9: Database Migration Verification

**Estimated Time:** 3-4 hours  
**Requires:**
- Access to Razorpay dashboard
- Access to production deployment platforms
- Test/staging environment access

---

## 🎯 Success Criteria

The verification is complete when:

1. ✅ All backend routes support weekly tier
2. ✅ All webhook handlers correctly identify weekly tier
3. ✅ All subscription duration logic includes weekly
4. ✅ End-to-end tests pass for all three tiers in all apps
5. ✅ Production plan IDs match unified values
6. ✅ Production environment variables are correct
7. ✅ No old pricing references remain (except documented legacy code)
8. ✅ All documentation is accurate

---

## 📝 Notes

### Current Status
- **Code Updates:** ✅ Complete
- **Documentation:** ✅ Complete
- **Verification:** ⏳ Pending
- **Testing:** ⏳ Pending

### Risk Areas
1. **Backend Routes:** ASK and Sketch2BIM may need weekly tier support added if not already present
2. **Webhook Handlers:** Must correctly map weekly amounts/plan IDs
3. **Production Config:** Environment variables must be set correctly in production
4. **Plan IDs:** Must verify all apps use the same shared plan IDs (not create app-specific ones)

### Quick Wins
- Task 1-3 can be verified by reading code files (no deployment needed)
- Task 6 can be done with grep searches
- Task 8 is mostly complete, just needs final sweep

### Blockers
- Task 4 requires test/staging environment
- Task 5 requires Razorpay dashboard access
- Task 7 requires production deployment platform access

---

## 🔗 Related Files

**Backend Route Files to Check:**
- `apps/ask/api/routes/checkout.py` (or similar)
- `apps/ask/api/routes/webhook.py` (or similar)
- `apps/sketch2bim/backend/app/routes/payments.py`
- `apps/sketch2bim/backend/app/routes/webhook.py` (or similar)

**Subscription Service Files:**
- `apps/ask/api/services/subscription.py` (or similar)
- `apps/sketch2bim/backend/app/services/cost_service.py`

**Configuration Files:**
- `apps/ask/api/config.py` ✅ (already verified - has correct defaults)
- `apps/sketch2bim/backend/app/config.py` ✅ (already verified - has correct defaults)

---

**Next Steps:** Start with Phase 1 verification tasks (code review) before moving to Phase 2 (production verification).

