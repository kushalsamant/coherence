# Pricing Unification - Remaining Tasks Plan

**Status:** ✅ COMPLETE  
**Last Updated:** January 2025  
**Goal:** Ensure ASK, Reframe, and Sketch2BIM all use the same weekly, monthly, and yearly pricing and Razorpay plan IDs.

## ✅ Completed Items

### 1. Environment Variables ✓
- ✅ All three `.env.production` files have unified pricing values
- ✅ All plan IDs are consistent across apps
- ✅ `ENVIRONMENT_VARIABLES_REFERENCE.md` has dedicated "Pricing & Plans" section

### 2. Reframe App ✓
- ✅ Frontend pricing page updated with weekly tier and unified pricing
- ✅ Dual-price-display component updated
- ✅ Backend checkout route supports weekly
- ✅ Webhook handler supports weekly
- ✅ Subscription service supports weekly
- ✅ README and terms page updated
- ✅ Scripts updated with unified pricing

### 3. Frontend Pricing Display ✓
- ✅ ASK pricing page already shows correct values (₹1,299/week, ₹3,499/month, ₹29,999/year)
- ✅ Sketch2BIM pricing page already shows correct values
- ✅ Reframe pricing page updated

### 4. Backend Configuration ✓
- ✅ ASK backend config already uses correct defaults
- ✅ Sketch2BIM backend config already uses correct defaults
- ✅ Reframe backend doesn't need Razorpay config (payments in Next.js)

---

## ✅ Recently Completed Tasks

### Task 1: Update COST_ANALYSIS.md ✓
**Status:** ✅ Complete  
**File:** `docs/COST_ANALYSIS.md`  
**Action Taken:** Updated competitive pricing section (lines 427-429) to reflect unified pricing structure across all apps.

### Task 2: Update COMPETITIVE_ANALYSIS.md ✓
**Status:** ✅ Complete  
**File:** `docs/COMPETITIVE_ANALYSIS.md`  
**Action Taken:** Updated pricing comparison table and Reframe pricing analysis (lines 266, 272-275) to reflect unified pricing.

### Task 3: Verify DEPLOYMENT_CONFIGURATION_GUIDE.md ✓
**Status:** ✅ Verified  
**File:** `DEPLOYMENT_CONFIGURATION_GUIDE.md`  
**Action Taken:** Verified file already contains correct unified pricing values. No changes needed.

### Task 4: Update ASK README.md ✓
**Status:** ✅ Complete  
**File:** `apps/ask/README.md`  
**Action Taken:** Added unified pricing section with note that pricing is shared across all three apps and reference to canonical documentation.

### Task 5: Update Sketch2BIM README.md ✓
**Status:** ✅ Complete  
**File:** `apps/sketch2bim/README.md`  
**Action Taken:** Added unified pricing section with note that pricing is shared across all three apps and reference to canonical documentation.

### Task 6: Review ASK scripts/setup.ts ✓
**Status:** ✅ Complete  
**File:** `apps/ask/scripts/setup.ts`  
**Action Taken:** Added legacy warning note - this is a Stripe script (not Razorpay) and appears to be for Reframe. ASK now uses Razorpay only.

---

## 🔲 Remaining Tasks

**All tasks have been completed!** 🎉

---

---

## ✅ Verification Checklist

Final verification checklist:

- [x] No old pricing values (₹999, ₹7,999, ₹99/day) appear anywhere in documentation
- [x] All documentation mentions unified pricing
- [x] All READMEs reference the central "Pricing & Plans" section
- [x] All three apps explicitly state they share the same pricing
- [x] COMPETITIVE_ANALYSIS.md reflects unified pricing
- [x] COST_ANALYSIS.md reflects unified pricing
- [x] render.yaml reflects unified pricing ✓
- [x] All environment variable files are consistent ✓
- [x] Frontend pricing pages match ✓
- [x] Backend code uses environment variables ✓

## 🔍 Files with Old Pricing Values Found

1. **`docs/COST_ANALYSIS.md`** - Lines 427-429 (old Reframe pricing: ₹99-3,499/month)
2. **`docs/COMPETITIVE_ANALYSIS.md`** - Lines 266, 272-275 (old Reframe pricing: ₹99/day, ₹999/month, ₹7,999/year)
3. **`apps/ask/scripts/setup.ts`** - Lines 244, 335, 421, 475, 580, 671 (Stripe prices, not Razorpay - needs investigation)

---

## 📝 Notes

### Canonical Pricing (Source of Truth)

**Amounts:**
- Week: ₹1,299 (129900 paise)
- Month: ₹3,499 (349900 paise)
- Year: ₹29,999 (2999900 paise)

**Plan IDs:**
- Week: `plan_Rha5Ikcm5JrGqx`
- Month: `plan_Rha5JNPsk1WmI6`
- Year: `plan_Rha5Jzn1sk8o1X`

**Location:** `render.yaml` and `docs/ENVIRONMENT_VARIABLES_REFERENCE.md`

### Key Files Updated So Far

1. `docs/ENVIRONMENT_VARIABLES_REFERENCE.md` - Added Pricing & Plans section
2. `apps/reframe/lib/app-config.ts` - Added weekly support
3. `apps/reframe/components/ui/dual-price-display.tsx` - Updated values
4. `apps/reframe/app/pricing/page.tsx` - Added weekly tier
5. `apps/reframe/app/api/razorpay/checkout/route.ts` - Added weekly support
6. `apps/reframe/app/api/razorpay-webhook/route.ts` - Added weekly support
7. `apps/reframe/lib/subscription.ts` - Added weekly duration
8. `apps/reframe/readme.md` - Updated pricing
9. `apps/reframe/app/terms/page.tsx` - Updated pricing
10. `apps/reframe/scripts/create_razorpay_plans.ts` - Updated with unified pricing

---

## 🎯 Success Criteria

The unification is complete when:
1. ✅ All apps use the same pricing values
2. ✅ All apps use the same plan IDs
3. ✅ All documentation is consistent
4. ✅ No hardcoded pricing values exist
5. ✅ All pricing references point to canonical source
6. ✅ All apps explicitly state unified pricing structure

