# Razorpay Webhook Configuration Guide

## Primary Webhook Endpoint

**Use this URL in Razorpay Dashboard:**

```
https://kvshvl.in/api/platform/razorpay-webhook
```

## Webhook Endpoints Summary

### `/api/platform/razorpay-webhook` ✅ PRIMARY
**File:** `app/api/platform/razorpay-webhook/route.ts`  
**Purpose:** Main webhook handler for all Razorpay events  
**Features:**
- ✅ Signature validation (secure)
- ✅ Handles all subscription events
- ✅ Tracks payment metrics
- ✅ Updates user subscriptions
- ✅ Redis-based user metadata

**Events Handled:**
- `payment.captured` - One-time payments
- `subscription.created` - Subscription created
- `subscription.activated` - First payment successful
- `subscription.charged` - Renewal payment
- `subscription.cancelled` - Subscription cancelled
- `subscription.paused` - Subscription paused

**Use this for:** All production Razorpay webhooks

---

### `/api/subscriptions/webhook` ⚠️ PROXY (Legacy)
**File:** `app/api/subscriptions/webhook/route.ts`  
**Purpose:** Forwards webhooks to backend API  
**Status:** Legacy endpoint, forwards to platform API

**Note:** This endpoint forwards webhooks to the backend Python API. May not be needed if using platform webhook above.

---

## Configuration Steps

### 1. Configure in Razorpay Dashboard

1. Login to https://dashboard.razorpay.com
2. Go to **Settings** → **Webhooks**
3. Click **Add New Webhook** or edit existing
4. Enter webhook URL:
   ```
   https://kvshvl.in/api/platform/razorpay-webhook
   ```
5. Set webhook secret (copy it for environment variables)
6. Select events to listen to:
   - [x] `payment.captured`
   - [x] `subscription.created`
   - [x] `subscription.activated`
   - [x] `subscription.charged`
   - [x] `subscription.cancelled`
   - [x] `subscription.paused`
7. Save webhook

### 2. Set Environment Variables

**In Render dashboard:**
- `PLATFORM_RAZORPAY_WEBHOOK_SECRET` = (webhook secret from step 5)

**In Vercel dashboard:**
- `PLATFORM_RAZORPAY_WEBHOOK_SECRET` = (same webhook secret)

### 3. Test Webhook

Use Razorpay's webhook testing tool:
1. Go to Settings → Webhooks
2. Click "Test Webhook"
3. Select an event type
4. Send test event
5. Verify response is 200 OK

---

## Security

The webhook validates signatures using:
```typescript
verifyWebhookSignature(body, signature)
```

**Implementation:** Uses crypto.createHmac with webhook secret to verify authenticity

**Never skip signature validation** - this prevents unauthorized webhook calls

---

## Monitoring

Webhook events are logged to console. Check logs for:
- `✅ User {userId} purchased {tier} subscription`
- `✅ User {userId} subscription activated`
- `✅ User {userId} subscription renewed`
- `❌ Missing user_id in payment notes`
- `❌ Razorpay webhook signature verification failed`

---

**Last Updated:** December 5, 2025  
**Status:** Configured and ready for production

