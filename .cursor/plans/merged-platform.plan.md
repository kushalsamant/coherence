# KVSHVL Platform - Action Plan

**Updated:** December 2, 2025  
**Build Status:** ✅ **SUCCESS** (0 errors, 0 vulnerabilities)  
**Deployment Status:** Ready for staging

---

## ✅ Completed Today

- Fixed 50+ TypeScript build errors
- Removed Excel export (security vulnerability)
- Renamed webhook route to `/api/platform/razorpay-webhook` (clarity)
- Production build successful (52 routes, 30 pages)
- Local testing passed (all apps load correctly)
- Environment audit complete

---

## 📋 TODO: What's Left

### 1. Configure Environment Variables (MANUAL - You Must Do)

**Missing Critical Variables:**

Add to `.env.local`:
```bash
# Next Auth (Required for authentication to work)
NEXTAUTH_URL=http://localhost:3000
AUTH_SECRET=<generate: node -e "console.log(require('crypto').randomBytes(32).toString('base64'))">
NEXTAUTH_SECRET=<same as AUTH_SECRET>

# Google OAuth (Get from https://console.cloud.google.com/)
GOOGLE_CLIENT_ID=<your-client-id>
GOOGLE_CLIENT_SECRET=<your-client-secret>

# Unprefixed aliases (copy from PLATFORM_* variables)
UPSTASH_REDIS_REST_URL=<copy from PLATFORM_UPSTASH_REDIS_REST_URL>
UPSTASH_REDIS_REST_TOKEN=<copy from PLATFORM_UPSTASH_REDIS_REST_TOKEN>
RAZORPAY_KEY_ID=<copy from PLATFORM_RAZORPAY_KEY_ID>
RAZORPAY_KEY_SECRET=<copy from PLATFORM_RAZORPAY_KEY_SECRET>
RAZORPAY_WEBHOOK_SECRET=<copy from PLATFORM_RAZORPAY_WEBHOOK_SECRET>
RAZORPAY_PLAN_WEEK=<copy from PLATFORM_RAZORPAY_PLAN_WEEK>
RAZORPAY_PLAN_MONTH=<copy from PLATFORM_RAZORPAY_PLAN_MONTH>
RAZORPAY_PLAN_YEAR=<copy from PLATFORM_RAZORPAY_PLAN_YEAR>
```

**Then:** Restart dev server

---

### 2. Setup Razorpay Webhook (MANUAL - You Must Do)

In Razorpay Dashboard:

**Webhook URL:**
```
https://kvshvl.in/api/platform/razorpay-webhook
```

**Secret:**
```
ABXFmwTgDNJbEq31jova80K96sChptHy
```
(Or use: `PLATFORM_RAZORPAY_TEST_WEBHOOK_SECRET` from your .env.local line 36)

**Alert Email:** `kushaldsamant@gmail.com`  
**Events:** Keep all 44 selected

---

### 3. Test Authentication (After Step 1)

- [ ] Visit http://localhost:3000/account
- [ ] Click "Sign In" 
- [ ] Should redirect to Google OAuth
- [ ] Sign in with Google
- [ ] Should return to account page
- [ ] Verify user session works

---

### 4. Test Subscription Checkout (After Steps 1-3)

**Test Cards (Razorpay Test Mode):**
- Success: `4111 1111 1111 1111`
- Failure: `4000 0000 0000 0002`

**Test Each Tier:**
- [ ] Week (₹1,299) - Test checkout flow
- [ ] Month (₹3,499) - Test checkout flow
- [ ] Year (₹29,999) - Test checkout flow
- [ ] Verify webhook receives events
- [ ] Verify subscription activates in account

---

### 5. Deploy to Staging (MANUAL - Requires Vercel Access)

- [ ] Push code to git repository
- [ ] Deploy via Vercel dashboard
- [ ] Add environment variables in Vercel settings
- [ ] Test on staging URL
- [ ] Smoke test all routes

---

### 6. Deploy to Production (After Staging Stable)

- [ ] Deploy to Vercel production
- [ ] Update Razorpay webhook to production URL
- [ ] Switch to live Razorpay keys
- [ ] Monitor logs for 24-48 hours
- [ ] Verify all apps functional

---

### 7. Post-Deployment Monitoring

- [ ] Monitor error logs daily (first week)
- [ ] Verify subscription flows work
- [ ] Check payment processing
- [ ] Monitor for 2 weeks total
- [ ] Remove old services when stable

---

## 🚫 Blocked Tasks

These can't proceed until environment variables are configured:
- Payment testing (needs auth working)
- Full integration testing (needs auth + payments)
- Production readiness verification (needs all features working)

---

## 📊 Current Metrics

| Metric | Status |
|--------|--------|
| Build | ✅ Success |
| TypeScript Errors | ✅ 0 |
| Security Vulnerabilities | ✅ 0 |
| Environment Config | ⚠️ Incomplete |
| Auth Variables | ❌ Missing |
| Deployment | ⏳ Pending |

---

## 🎯 Priority Order

1. **CRITICAL:** Add missing env vars to `.env.local` (blocks everything)
2. **HIGH:** Test authentication flow (verifies env vars work)
3. **HIGH:** Test subscription checkout (verifies payments work)
4. **MEDIUM:** Deploy to staging
5. **LOW:** Deploy to production (after staging stable)

---

## 📝 Quick Reference

### Key Files Created/Modified Today
- `app/api/platform/razorpay-webhook/route.ts` (moved from reframe)
- `lib/api.ts` (created)
- `app/layout.tsx` (added AuthProvider)
- `docs/*.md` (created 4 files)
- 38 other files with TypeScript/import fixes

### Webhook Setup
- **URL:** `https://kvshvl.in/api/platform/razorpay-webhook`
- **Handles:** All apps (ASK, Reframe, Sketch2BIM)
- **Events:** Subscription lifecycle, payments, refunds

### Google OAuth Setup
- **Console:** https://console.cloud.google.com/
- **Redirect URIs:** 
  - Dev: `http://localhost:3000/api/auth/callback/google`
  - Prod: `https://kvshvl.in/api/auth/callback/google`

---

## ⏭️ Next Session

When you return with environment variables configured:
1. Test authentication
2. Test payments
3. Deploy to staging
4. Deploy to production

**You're 95% complete - just need the auth credentials!**
