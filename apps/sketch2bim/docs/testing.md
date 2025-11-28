# Testing Guide

Complete guide for testing Sketch-to-BIM payment flows, webhooks, and functionality before production deployment.

## Table of Contents

1. [Test Mode Setup](#test-mode-setup)
2. [Pre-Testing Checklist](#pre-testing-checklist)
3. [One-Time Payment Tests](#one-time-payment-tests)
4. [Subscription Tests](#subscription-tests)
5. [Webhook Testing](#webhook-testing)
6. [Error Handling Tests](#error-handling-tests)
7. [UI/UX Tests](#uiux-tests)
8. [Database Tests](#database-tests)
9. [Security Tests](#security-tests)
10. [Production Deployment Checklist](#production-deployment-checklist)

---

## Test Mode Setup

### Test Mode vs Production Mode

**Test Mode:**
- Uses test API keys (start with `rzp_test_`)
- No real money is charged
- Test cards available for testing
- Webhooks can be tested with ngrok
- Plans can be created in test mode

**Production Mode:**
- Uses live API keys (start with `rzp_live_`)
- Real money is charged
- Requires production webhook URL
- Plans must be created separately

### Step 1: Get Test Mode Credentials

1. **Log in to Razorpay Dashboard**
   - Go to https://dashboard.razorpay.com
   - Switch to **Test Mode** (toggle in top right)

2. **Get Test API Keys**
   - Go to **Settings** → **API Keys**
   - Copy **Key ID** (starts with `rzp_test_`)
   - Copy **Key Secret** (starts with `rzp_test_`)

3. **Create Test Webhook Secret**
   - Go to **Settings** → **Webhooks**
   - Click **+ Add New Webhook**
   - Use ngrok URL (see Step 2)
   - Copy the **Secret** generated

### Step 2: Set Up Local Testing with ngrok

1. **Install ngrok**
   ```bash
   # Windows (PowerShell)
   choco install ngrok
   # OR download from https://ngrok.com/download
   ```

2. **Start your backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

3. **Expose local server**
   ```bash
   ngrok http 8000
   ```
   - Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

4. **Update webhook URL in Razorpay**
   - Use: `https://abc123.ngrok.io/api/v1/payments/webhook`

### Step 3: Create Test Environment File

Create `.env.test` (or update `.env.local`):

```env
# Razorpay Test Mode Keys
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=rzp_test_xxxxxxxxxxxxx
RAZORPAY_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxx

# Pricing (shared across all projects - same as production)
# Prefixed versions are required (unprefixed versions are deprecated but still supported for backward compatibility)
SKETCH2BIM_RAZORPAY_WEEK_AMOUNT=129900
SKETCH2BIM_RAZORPAY_MONTH_AMOUNT=349900
SKETCH2BIM_RAZORPAY_YEAR_AMOUNT=2999900

# Test Plan IDs (shared across all projects - will be created)
SKETCH2BIM_RAZORPAY_PLAN_WEEK=
SKETCH2BIM_RAZORPAY_PLAN_MONTH=
SKETCH2BIM_RAZORPAY_PLAN_YEAR=
# Or use unprefixed (both work due to backward compatibility):
# RAZORPAY_PLAN_WEEK=
# RAZORPAY_PLAN_MONTH=
# RAZORPAY_PLAN_YEAR=

# Frontend URL (for local testing)
FRONTEND_URL=http://localhost:3000
```

### Step 4: Create Test Plans

**Option A: Use Script (Test Mode)**
```bash
# Load test environment
# Windows PowerShell
$env:RAZORPAY_KEY_ID="rzp_test_xxxxx"
$env:RAZORPAY_KEY_SECRET="rzp_test_xxxxx"

# Run script
python scripts/create_razorpay_plans.py
```

**Option B: Create Manually in Dashboard**
1. Switch to **Test Mode** in Razorpay Dashboard
2. Go to **Subscriptions** → **Plans**
3. Create 3 plans:
   - **Week Pass**: ₹1,299, Weekly, Interval: 1
   - **Month**: ₹3,499, Monthly, Interval: 1
   - **Year**: ₹29,999, Yearly, Interval: 1
4. Copy Plan IDs to `.env.test`

### Step 5: Run Database Migration

```bash
cd backend
alembic upgrade head
```

This adds:
- `razorpay_subscription_id` column
- `subscription_auto_renew` column

### Step 6: Configure Webhook Events

In Razorpay Dashboard → Settings → Webhooks:

Select these events:
- ✅ `payment.captured`
- ✅ `subscription.created`
- ✅ `subscription.activated`
- ✅ `subscription.charged`
- ✅ `subscription.cancelled`
- ✅ `subscription.paused`

---

## Pre-Testing Checklist

- [ ] Razorpay test mode API keys obtained
- [ ] `.env.test` file created with test credentials
- [ ] ngrok installed and configured
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database migration applied (`alembic upgrade head`)
- [ ] Test plans created in Razorpay Dashboard (or via script)
- [ ] Webhook configured in Razorpay Dashboard with ngrok URL
- [ ] Webhook secret added to `.env.test`

---

## One-Time Payment Tests

### Week Pass (₹1,299)
- [ ] Click "Buy One-Time" button
- [ ] Complete payment with test card
- [ ] Payment successful
- [ ] Webhook `payment.captured` received
- [ ] User tier updated to "week"
- [ ] `subscription_auto_renew` is `False`
- [ ] Expiry date set to 7 days from now
- [ ] Credits granted (unlimited)

### Month Pass (₹3,499)
- [ ] Same as Week Pass
- [ ] User tier updated to "month"
- [ ] Expiry date set to 30 days from now

### Year Pass (₹29,999)
- [ ] Same as Week Pass
- [ ] User tier updated to "year"
- [ ] Expiry date set to 365 days from now

### Test Cards Reference

Razorpay Test Cards:
- **Success**: `4111 1111 1111 1111`
- **Failure**: `4000 0000 0000 0002`
- **3D Secure**: `4012 0010 3714 1112`

More test cards: https://razorpay.com/docs/payments/test-cards/

---

## Subscription Tests

### Day Subscription
- [ ] Click "Subscribe" button
- [ ] Complete payment with test card
- [ ] `subscription.created` webhook received
- [ ] `subscription.activated` webhook received
- [ ] `razorpay_subscription_id` stored in database
- [ ] `subscription_auto_renew` is `True`
- [ ] User tier updated correctly
- [ ] Expiry date set correctly

### Week Subscription
- [ ] Same as Day Subscription

### Month Subscription
- [ ] Same as Day Subscription

### Year Subscription
- [ ] Same as Day Subscription

### Subscription Management Tests

**Cancel Subscription:**
- [ ] Go to Settings page
- [ ] Click "Cancel Subscription"
- [ ] Confirm cancellation
- [ ] `subscription.cancelled` webhook received
- [ ] `subscription_auto_renew` set to `False`
- [ ] Access continues (not immediately revoked)
- [ ] Expiry date unchanged

**Resume Subscription (if applicable):**
- [ ] Resume cancelled subscription
- [ ] `subscription_auto_renew` set to `True`
- [ ] Subscription reactivated

---

## Webhook Testing

### Webhook Endpoint
- **URL**: `POST /api/v1/payments/webhook`
- **Headers Required**: `x-razorpay-signature`
- **Content-Type**: `application/json`

### Webhook Events Handled

**One-Time Payments:**
- `payment.captured` - When a one-time payment is successfully captured

**Subscriptions:**
- `subscription.created` - When a subscription is created
- `subscription.activated` - When a subscription is activated (first payment successful)
- `subscription.charged` - When a subscription renews (recurring payment)
- `subscription.cancelled` - When a subscription is cancelled
- `subscription.paused` - When a subscription is paused

### Testing Methods

**Option 1: Use Razorpay Dashboard (Recommended)**
1. Go to Razorpay Dashboard → Settings → Webhooks
2. Click on your webhook
3. Click **Send Test Event**
4. Select event type
5. Check your backend logs for receipt

**Option 2: Use ngrok for Local Testing**
1. Install ngrok: `npm install -g ngrok` or download from https://ngrok.com
2. Start your backend: `uvicorn backend.app.main:app --reload`
3. Expose local server: `ngrok http 8000`
4. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)
5. In Razorpay Dashboard, add webhook URL: `https://abc123.ngrok.io/api/v1/payments/webhook`
6. Test payments - webhooks will be forwarded to your local server

### Webhook Signature Verification Tests
- [ ] Valid webhook signature accepted
- [ ] Invalid webhook signature rejected
- [ ] Missing signature rejected

### Webhook Event Processing Tests
- [ ] `payment.captured` processed correctly
- [ ] `subscription.created` processed correctly
- [ ] `subscription.activated` processed correctly
- [ ] `subscription.charged` processed correctly (renewal)
- [ ] `subscription.cancelled` processed correctly

### Verifying Webhook Works

**Check Webhook Logs:**
The webhook handler logs errors. Check your backend logs for:
- "Webhook signature verification failed" - Invalid signature
- "User not found" - Payment succeeded but user doesn't exist
- Successful processing messages

**Test Scenarios:**

1. **One-Time Payment**
   - Make a one-time purchase
   - Check that `payment.captured` webhook is received
   - Verify user's `subscription_tier` is updated
   - Verify `subscription_auto_renew` is `False`

2. **Subscription Creation**
   - Create a subscription
   - Check that `subscription.created` webhook is received
   - Verify `razorpay_subscription_id` is stored
   - Verify `subscription_auto_renew` is `True`

3. **Subscription Activation**
   - After first payment succeeds
   - Check that `subscription.activated` webhook is received
   - Verify user's tier and expiry are set correctly

4. **Subscription Renewal**
   - Wait for renewal (or trigger manually in Razorpay dashboard)
   - Check that `subscription.charged` webhook is received
   - Verify expiry date is updated

5. **Subscription Cancellation**
   - Cancel subscription via settings page
   - Check that `subscription.cancelled` webhook is received
   - Verify `subscription_auto_renew` is `False`
   - Verify access continues until period ends

### Common Webhook Issues

**Webhook Not Received:**
- Check webhook URL is correct in Razorpay dashboard
- Verify webhook secret is set correctly
- Check firewall/network settings
- Verify backend is running and accessible

**Invalid Signature Error:**
- Ensure `RAZORPAY_WEBHOOK_SECRET` matches the secret from Razorpay dashboard
- Verify the payload is not modified before signature verification
- Check that `x-razorpay-signature` header is present

**User Not Found:**
- Payment succeeded but user lookup failed
- Check that `user_id` is included in order/subscription notes
- Verify user exists in database

---

## Error Handling Tests

### Payment Failures
- [ ] Failed payment handled gracefully
- [ ] User sees appropriate error message
- [ ] No credits/subscription granted on failure
- [ ] Webhook not sent for failed payments

### Invalid Scenarios
- [ ] Invalid tier name rejected
- [ ] Missing user handled correctly
- [ ] Duplicate payment prevented (if applicable)

### Common Test Mode Issues

**Issue: "Invalid API Key"**
- **Solution**: Ensure you're using test mode keys (start with `rzp_test_`)
- **Check**: Toggle in Razorpay Dashboard is set to "Test Mode"

**Issue: Webhook Not Received**
- **Solution**: Verify ngrok is running and URL is correct
- **Check**: Webhook URL in Razorpay matches ngrok URL
- **Check**: Backend is running on port 8000

**Issue: "Plan not found"**
- **Solution**: Create plans in test mode separately
- **Check**: Plan IDs in `.env.test` match test mode plans

**Issue: Signature Verification Failed**
- **Solution**: Ensure webhook secret matches
- **Check**: `RAZORPAY_WEBHOOK_SECRET` in `.env.test` matches dashboard

---

## UI/UX Tests

### Pricing Page
- [ ] Both "Buy One-Time" and "Subscribe" buttons visible
- [ ] Buttons disabled for current plan
- [ ] Loading states work correctly
- [ ] Success redirect works
- [ ] Cancel redirect works

### Settings Page
- [ ] Subscription status displayed correctly
- [ ] Auto-renew status shown
- [ ] Cancel button visible for active subscriptions
- [ ] Resume button visible for cancelled subscriptions
- [ ] Expiry date displayed correctly

---

## Database Tests

### User Model
- [ ] `razorpay_subscription_id` stored correctly
- [ ] `subscription_auto_renew` flag set correctly
- [ ] `subscription_tier` updated correctly
- [ ] `subscription_expires_at` set correctly

### Payment Records
- [ ] Payment records created for one-time payments
- [ ] Payment records created for subscription renewals
- [ ] Payment records linked to correct user
- [ ] Payment amounts correct

---

## Security Tests

- [ ] Webhook signature verification working
- [ ] API keys not exposed in frontend
- [ ] User can only cancel their own subscription
- [ ] Payment amounts validated server-side

---

## Performance Tests

- [ ] Webhook processing time < 2 seconds
- [ ] Checkout page loads quickly
- [ ] Payment flow completes in reasonable time

---

## Final Checks

- [ ] All tests pass
- [ ] No console errors
- [ ] No backend errors in logs
- [ ] Database migrations successful
- [ ] Ready for production deployment

---

## Production Deployment Checklist

After test mode passes:

- [ ] Switch to production API keys
- [ ] Create production plans
- [ ] Update `sketch2bim.env.production` (at repository root) with production values
- [ ] Configure production webhook URL
- [ ] Test production webhook with test event
- [ ] Monitor first few production payments
- [ ] Verify production webhooks are received

### Production Webhook Checklist

- [ ] Webhook URL configured in Razorpay dashboard
- [ ] Webhook secret added to `.env.production`
- [ ] All required events selected in Razorpay dashboard
- [ ] Webhook endpoint is publicly accessible
- [ ] SSL certificate is valid (HTTPS required)
- [ ] Webhook signature verification is working
- [ ] Tested with real payments (test mode first)
- [ ] Monitored webhook logs for errors

---

## Feature Testing

### Batch Upload Testing

**Endpoint**: `POST /api/v1/generate/batch-upload`

**Test Cases**:
1. **Successful batch upload**
   - Upload 3-5 valid image files
   - Verify all jobs are created with status "queued"
   - Verify batch_id is assigned to all jobs
   - Check that processing starts for each job

2. **Partial failure handling**
   - Upload mix of valid and invalid files
   - Verify valid files are processed
   - Verify invalid files are reported in response
   - Check that successful jobs still proceed

3. **File size validation**
   - Upload files exceeding size limit
   - Verify error messages are clear
   - Check that valid files in batch still process

4. **Subscription requirement**
   - Test with free tier user (should fail)
   - Test with subscribed user (should succeed)
   - Verify proper error messages

**Test Command**:
```bash
curl -X POST http://localhost:8000/api/v1/generate/batch-upload \
  -H "Authorization: Bearer <token>" \
  -F "files=@sketch1.png" \
  -F "files=@sketch2.png" \
  -F "files=@sketch3.png" \
  -F "project_type=architecture"
```

**Expected Response**:
```json
{
  "batch_id": "batch_xxx",
  "job_ids": ["job_xxx", "job_yyy", "job_zzz"],
  "total_jobs": 3
}
```

### Layout Variations Testing

**Endpoint**: `POST /api/v1/variations/jobs/{job_id}/variations`

**Prerequisites**:
- Job must be completed (status="completed")
- Job must have plan_data

**Test Cases**:
1. **Generate variations**
   - Create variations from completed job
   - Verify variations are created in database
   - Check that IFC files are generated for each variation
   - Verify variation confidence scores

2. **List variations**
   - Get all variations for a job
   - Verify correct ordering (by variation_number)
   - Check that all variation data is returned

3. **Get single variation**
   - Retrieve specific variation by ID
   - Verify all fields are present
   - Check IFC URL is available

4. **Delete variation**
   - Delete a variation
   - Verify it's removed from database
   - Check that child variations prevent deletion

**Test Command**:
```bash
curl -X POST http://localhost:8000/api/v1/variations/jobs/{job_id}/variations \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"num_variations": 3}'
```

**Known Limitations**:
- Variation quality depends on original sketch complexity
- Simple algorithms may produce similar variations
- Works best with clear room boundaries

### Iterations Testing

**Endpoint**: `POST /api/v1/iterations/jobs/{job_id}/iterations`

**Test Cases**:
1. **Create iteration**
   - Create iteration from completed job
   - Verify iteration record is created
   - Check that IFC URL is copied from parent

2. **Create child iteration**
   - Create iteration with parent_iteration_id
   - Verify parent-child relationship
   - Check that changes can be applied

3. **Apply changes**
   - Create iteration with changes_json
   - Regenerate IFC with changes
   - Verify plan_data is modified correctly
   - Check that new IFC file is generated

4. **List iterations**
   - Get all iterations for a job
   - Verify correct ordering (newest first)
   - Check parent-child relationships

5. **Update iteration**
   - Update iteration name, notes, or changes
   - Verify changes are saved
   - Check that change_summary is updated

6. **Delete iteration**
   - Delete iteration without children (should succeed)
   - Try to delete iteration with children (should fail)
   - Verify proper error messages

**Test Command**:
```bash
curl -X POST http://localhost:8000/api/v1/iterations/jobs/{job_id}/iterations \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Modified Layout",
    "changes_json": {
      "moved_elements": [{
        "element_id": "wall1",
        "element_type": "wall",
        "position": {"start": [0, 0], "end": [100, 0]}
      }],
      "resized_rooms": [{
        "room_id": "room1",
        "size": 6000
      }]
    }
  }'
```

**Known Limitations**:
- Change application logic is simplified
- Complex geometric transformations may not be fully supported
- Room resizing uses proportional scaling
- Element movement updates coordinates but may not validate geometry

### Test Results Documentation

After testing, document:
- [ ] Batch upload handles partial failures correctly
- [ ] Variations generate valid IFC files
- [ ] Iterations apply changes correctly
- [ ] Error messages are clear and helpful
- [ ] Edge cases are handled (empty batches, invalid data, etc.)
- [ ] Performance is acceptable for expected workloads

---

## Moving to Production

Once testing is complete:

1. **Switch to Production Mode**
   - Get production API keys from Razorpay Dashboard
   - Create production plans (separate from test plans)
   - Set up production webhook URL (no ngrok needed)

2. **Update Environment Variables**
   - Use production keys in `.env.production`
   - Update Plan IDs for production
   - Update webhook secret for production

3. **Test Production Webhook**
   - Use Razorpay's test event feature
   - Monitor logs for any issues

---

## Debugging

Enable debug logging in `backend/app/routes/payments.py`:

```python
import logging
logger = logging.getLogger(__name__)

# In webhook handler:
logger.info(f"Webhook received: {event_type}")
logger.debug(f"Payload: {payload_str}")
```

---

## References

- Razorpay Webhook Documentation: https://razorpay.com/docs/webhooks/
- Razorpay API Documentation: https://razorpay.com/docs/api/webhooks/
- Test Cards: https://razorpay.com/docs/payments/test-cards/

