# Manual Test Checklist - Reframe AI

Quick checklist for testing authenticated features that couldn't be tested with automated browser.

---

## ✅ Tests Completed

### Authentication & Session
- [x] OAuth flow initiates correctly
- [x] Checkbox validation works (both required)
- [x] Redirects to Google sign-in
- [x] Session persists on refresh
- [x] Consent tracking recorded

### Free Tier Functionality
- [x] Usage counter increments (1/3, 2/3, 3/3)
- [x] Daily limit banner appears at 3/3
- [x] Premium tone click shows upgrade toast
- [x] Maximum limit click shows Pro feature toast
- [x] Free tones work (Conversational, Professional, Academic)

### Settings Page
- [x] Account overview displays correctly
- [x] Email shown: kushaldsamant@gmail.com
- [x] Usage counter accurate (shows 3/3)
- [x] Data export works (JSON download)
- [x] Consent details visible
- [x] Back to Home button present

### Legal & Compliance
- [x] Terms of Service complete
- [x] Privacy Policy complete
- [x] All external links functional
- [x] Contact emails correct
- [x] GDPR/CCPA language present

### UI/UX
- [x] Responsive design (mobile, tablet, desktop)
- [x] Zero console errors
- [x] All navigation links work
- [x] Cookie banner functional
- [x] Toast notifications work

---

## ⚠️ Tests Blocked

### Payment Testing (Stripe India Restrictions)
- [ ] Weekly Pro subscription ($2.99 or ₹249)
- [ ] Monthly Pro subscription ($9.99 or ₹799)
- [ ] Yearly Pro subscription ($99 or ₹7,999)
- [ ] Starter Pack ($3.99 or ₹299)
- [ ] Standard Pack ($9.99 or ₹799)
- [ ] Premium Pack ($24.99 or ₹1,999)
- [ ] Declined card handling (4000 0000 0000 0002)
- [ ] Webhook verification in Stripe Dashboard

**Reason:** Indian Stripe account requires business verification for accepting payments (even in test mode).

**Solution:** Test in production after Stripe account verification OR use non-Indian Stripe test account.

---

## 📝 Additional Tests (Optional)

### Character Limits
- [ ] Conservative (10k chars) - test at limit
- [ ] Moderate (50k chars) - test at limit  
- [ ] Maximum (250k chars) - test at limit (Pro only)
- [ ] Character counter color changes (green → yellow → orange)

### All 6 Tones
- [ ] Conversational 💬
- [ ] Professional 💼
- [ ] Academic 🎓
- [ ] Enthusiastic ⚡ (Premium)
- [ ] Empathetic 💙 (Premium)
- [ ] Witty 😄 (Premium)

### Edge Cases
- [ ] Empty input validation
- [ ] Less than 10 chars validation
- [ ] Whitespace-only input
- [ ] Copy output button
- [ ] Sign out functionality
- [ ] Back button behavior after auth

### Browser Compatibility
- [ ] Chrome (primary browser)
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile browsers (iOS Safari, Chrome Mobile)

---

## 🚀 Production Testing Checklist

After deployment to production:

### Critical
- [ ] Google OAuth works on production domain
- [ ] Verify `AUTH_URL` set correctly in Vercel
- [ ] Test one complete payment flow (real or test card)
- [ ] Verify webhook returns 200 OK in Stripe Dashboard
- [ ] Check subscription/credits update after payment
- [ ] No console errors in production

### Important
- [ ] Test from real mobile device
- [ ] Verify currency detection works globally
- [ ] Test Indian user sees INR
- [ ] Test US user sees USD
- [ ] Verify Stripe Customer Portal accessible
- [ ] Test session persistence

### Optional
- [ ] Performance testing (Lighthouse score)
- [ ] SEO verification (meta tags)
- [ ] Accessibility audit (WCAG)
- [ ] Load testing
- [ ] Monitor production logs for 24h

---

**Status:** Ready for production deployment after Stripe account verification

