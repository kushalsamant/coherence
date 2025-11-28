# Environment Variable Prefix Migration - Testing Checklist

This document provides a comprehensive testing checklist for verifying the environment variable prefix migration is working correctly.

## Migration Summary

- **Code**: Uses unprefixed variables (`RAZORPAY_PLAN_WEEK`, `RAZORPAY_WEEK_AMOUNT`, etc.) with backward compatibility
- **Environment Files**: Use prefixed variables (`ASK_RAZORPAY_*`, `SKETCH2BIM_RAZORPAY_*`, etc.) for organization
- **Shared Values**: All projects (ASK, Sketch2BIM, Reframe) use the same Razorpay plan IDs and amounts
- **Backward Compatibility**: Code checks prefixed first, then unprefixed, then defaults

## Pre-Deployment Testing

### 1. Configuration Loading Tests

#### ASK Backend
- [ ] Verify `apps/ask/api/config.py` loads correctly
- [ ] Test that `ASK_RAZORPAY_WEEK_AMOUNT` is read correctly
- [ ] Test that `RAZORPAY_WEEK_AMOUNT` (unprefixed) still works (backward compatibility)
- [ ] Verify default values (129900, 349900, 2999900) are used when no env vars are set
- [ ] Test plan IDs: `ASK_RAZORPAY_PLAN_WEEK`, `ASK_RAZORPAY_PLAN_MONTH`, `ASK_RAZORPAY_PLAN_YEAR`

#### Sketch2BIM Backend
- [ ] Verify `apps/sketch2bim/backend/app/config.py` loads correctly
- [ ] Test that `SKETCH2BIM_RAZORPAY_WEEK_AMOUNT` is read correctly
- [ ] Test that `RAZORPAY_WEEK_AMOUNT` (unprefixed) still works (backward compatibility)
- [ ] Verify default values are used when no env vars are set
- [ ] Test plan IDs: `SKETCH2BIM_RAZORPAY_PLAN_WEEK`, `SKETCH2BIM_RAZORPAY_PLAN_MONTH`, `SKETCH2BIM_RAZORPAY_PLAN_YEAR`

### 2. Environment File Verification

#### ASK Environment File (`ask.env.production`)
- [ ] Verify `ASK_RAZORPAY_WEEK_AMOUNT=129900` is present
- [ ] Verify `ASK_RAZORPAY_MONTH_AMOUNT=349900` is present
- [ ] Verify `ASK_RAZORPAY_YEAR_AMOUNT=2999900` is present
- [ ] Verify `ASK_RAZORPAY_PLAN_WEEK=plan_Rha5Ikcm5JrGqx` is present
- [ ] Verify `ASK_RAZORPAY_PLAN_MONTH=plan_Rha5JNPsk1WmI6` is present
- [ ] Verify `ASK_RAZORPAY_PLAN_YEAR=plan_Rha5Jzn1sk8o1X` is present

#### Sketch2BIM Environment File (`sketch2bim.env.production`)
- [ ] Verify `SKETCH2BIM_RAZORPAY_WEEK_AMOUNT=129900` is present
- [ ] Verify `SKETCH2BIM_RAZORPAY_MONTH_AMOUNT=349900` is present
- [ ] Verify `SKETCH2BIM_RAZORPAY_YEAR_AMOUNT=2999900` is present
- [ ] Verify `SKETCH2BIM_RAZORPAY_PLAN_WEEK=plan_Rha5Ikcm5JrGqx` is present
- [ ] Verify `SKETCH2BIM_RAZORPAY_PLAN_MONTH=plan_Rha5JNPsk1WmI6` is present
- [ ] Verify `SKETCH2BIM_RAZORPAY_PLAN_YEAR=plan_Rha5Jzn1sk8o1X` is present

#### Reframe Environment File (`reframe.env.production`)
- [ ] Verify `REFRAME_RAZORPAY_WEEK_AMOUNT=129900` is present
- [ ] Verify `REFRAME_RAZORPAY_MONTH_AMOUNT=349900` is present
- [ ] Verify `REFRAME_RAZORPAY_YEAR_AMOUNT=2999900` is present
- [ ] Verify plan IDs are present (if applicable)

### 3. Render.yaml Verification

#### ASK Render.yaml (`apps/ask/render.yaml`)
- [ ] Verify `ASK_RAZORPAY_WEEK_AMOUNT` is set to "129900"
- [ ] Verify `ASK_RAZORPAY_MONTH_AMOUNT` is set to "349900"
- [ ] Verify `ASK_RAZORPAY_YEAR_AMOUNT` is set to "2999900"
- [ ] Verify `ASK_RAZORPAY_PLAN_WEEK` is set to "plan_Rha5Ikcm5JrGqx"
- [ ] Verify `ASK_RAZORPAY_PLAN_MONTH` is set to "plan_Rha5JNPsk1WmI6"
- [ ] Verify `ASK_RAZORPAY_PLAN_YEAR` is set to "plan_Rha5Jzn1sk8o1X"

#### Sketch2BIM Render.yaml (`apps/sketch2bim/infra/render.yaml`)
- [ ] Verify `SKETCH2BIM_RAZORPAY_WEEK_AMOUNT` is set to "129900"
- [ ] Verify `SKETCH2BIM_RAZORPAY_MONTH_AMOUNT` is set to "349900"
- [ ] Verify `SKETCH2BIM_RAZORPAY_YEAR_AMOUNT` is set to "2999900"
- [ ] Verify `SKETCH2BIM_RAZORPAY_PLAN_WEEK` is set to "plan_Rha5Ikcm5JrGqx"
- [ ] Verify `SKETCH2BIM_RAZORPAY_PLAN_MONTH` is set to "plan_Rha5JNPsk1WmI6"
- [ ] Verify `SKETCH2BIM_RAZORPAY_PLAN_YEAR` is set to "plan_Rha5Jzn1sk8o1X"

### 4. Shared Packages Verification

- [ ] Verify `packages/shared-backend/config/razorpay.py` reads from environment variables
- [ ] Verify `packages/shared-backend/payments/razorpay.py` has appropriate comments
- [ ] Verify `packages/shared-frontend/src/payments/razorpay.ts` has appropriate comments

### 5. Docker Compose Verification

#### Sketch2BIM Docker Compose (`apps/sketch2bim/infra/docker-compose.yml`)
- [ ] Verify `RAZORPAY_WEEK_AMOUNT` has default value "129900"
- [ ] Verify `RAZORPAY_MONTH_AMOUNT` has default value "349900"
- [ ] Verify `RAZORPAY_YEAR_AMOUNT` has default value "2999900"
- [ ] Verify `RAZORPAY_PLAN_WEEK` has default value "plan_Rha5Ikcm5JrGqx"
- [ ] Verify `RAZORPAY_PLAN_MONTH` has default value "plan_Rha5JNPsk1WmI6"
- [ ] Verify `RAZORPAY_PLAN_YEAR` has default value "plan_Rha5Jzn1sk8o1X"

#### Sketch2BIM Docker Compose Prod (`apps/sketch2bim/infra/docker-compose.prod.yml`)
- [ ] Verify same variables as above are present

## Runtime Testing

### 6. Application Startup Tests

#### ASK Backend
- [ ] Start ASK backend locally with `ask.env.production` loaded
- [ ] Verify no errors related to Razorpay configuration
- [ ] Check logs for correct Razorpay amounts being loaded
- [ ] Verify plan IDs are loaded correctly

#### Sketch2BIM Backend
- [ ] Start Sketch2BIM backend locally with `sketch2bim.env.production` loaded
- [ ] Verify no errors related to Razorpay configuration
- [ ] Check logs for correct Razorpay amounts being loaded
- [ ] Verify plan IDs are loaded correctly

### 7. Payment Flow Tests

#### ASK Payment Flow
- [ ] Test creating a payment order with week subscription
- [ ] Verify amount is 129900 paise (₹1,299)
- [ ] Test creating a payment order with month subscription
- [ ] Verify amount is 349900 paise (₹3,499)
- [ ] Test creating a payment order with year subscription
- [ ] Verify amount is 2999900 paise (₹29,999)
- [ ] Test subscription creation with plan IDs
- [ ] Verify correct plan IDs are used

#### Sketch2BIM Payment Flow
- [ ] Test creating a payment order with week subscription
- [ ] Verify amount is 129900 paise (₹1,299)
- [ ] Test creating a payment order with month subscription
- [ ] Verify amount is 349900 paise (₹3,499)
- [ ] Test creating a payment order with year subscription
- [ ] Verify amount is 2999900 paise (₹29,999)
- [ ] Test subscription creation with plan IDs
- [ ] Verify correct plan IDs are used

### 8. Backward Compatibility Tests

- [ ] Test ASK backend with only unprefixed variables (`RAZORPAY_WEEK_AMOUNT` instead of `ASK_RAZORPAY_WEEK_AMOUNT`)
- [ ] Verify it still works correctly
- [ ] Test Sketch2BIM backend with only unprefixed variables
- [ ] Verify it still works correctly
- [ ] Test with both prefixed and unprefixed set (prefixed should take precedence)

## Deployment Testing

### 9. Render Dashboard Verification

#### ASK API Service
- [ ] Verify `ASK_RAZORPAY_WEEK_AMOUNT=129900` is set in Render dashboard
- [ ] Verify `ASK_RAZORPAY_MONTH_AMOUNT=349900` is set
- [ ] Verify `ASK_RAZORPAY_YEAR_AMOUNT=2999900` is set
- [ ] Verify `ASK_RAZORPAY_PLAN_WEEK=plan_Rha5Ikcm5JrGqx` is set
- [ ] Verify `ASK_RAZORPAY_PLAN_MONTH=plan_Rha5JNPsk1WmI6` is set
- [ ] Verify `ASK_RAZORPAY_PLAN_YEAR=plan_Rha5Jzn1sk8o1X` is set

#### Sketch2BIM Backend Service
- [ ] Verify `SKETCH2BIM_RAZORPAY_WEEK_AMOUNT=129900` is set in Render dashboard
- [ ] Verify `SKETCH2BIM_RAZORPAY_MONTH_AMOUNT=349900` is set
- [ ] Verify `SKETCH2BIM_RAZORPAY_YEAR_AMOUNT=2999900` is set
- [ ] Verify `SKETCH2BIM_RAZORPAY_PLAN_WEEK=plan_Rha5Ikcm5JrGqx` is set
- [ ] Verify `SKETCH2BIM_RAZORPAY_PLAN_MONTH=plan_Rha5JNPsk1WmI6` is set
- [ ] Verify `SKETCH2BIM_RAZORPAY_PLAN_YEAR=plan_Rha5Jzn1sk8o1X` is set

### 10. Production Deployment Tests

#### ASK Production
- [ ] Deploy ASK backend to Render
- [ ] Verify deployment succeeds without errors
- [ ] Test payment endpoints in production
- [ ] Verify correct amounts are returned
- [ ] Test subscription creation in production
- [ ] Verify correct plan IDs are used

#### Sketch2BIM Production
- [ ] Deploy Sketch2BIM backend to Render
- [ ] Verify deployment succeeds without errors
- [ ] Test payment endpoints in production
- [ ] Verify correct amounts are returned
- [ ] Test subscription creation in production
- [ ] Verify correct plan IDs are used

## Post-Deployment Verification

### 11. Production Smoke Tests

- [ ] Test ASK payment flow in production
- [ ] Test Sketch2BIM payment flow in production
- [ ] Verify webhook handling still works
- [ ] Check application logs for any configuration errors
- [ ] Monitor for any payment-related errors

### 12. Monitoring

- [ ] Monitor application logs for 24 hours after deployment
- [ ] Check for any environment variable related errors
- [ ] Verify payment transactions are processing correctly
- [ ] Monitor error rates for payment endpoints

## Rollback Plan

If issues are discovered:

1. **Immediate Rollback**: Revert to previous deployment
2. **Environment Variables**: Keep both prefixed and unprefixed variables set in Render dashboard during transition
3. **Code Rollback**: Revert config.py changes if needed (though backward compatibility should prevent issues)

## Notes

- All projects share the same Razorpay plan IDs and amounts
- Code maintains backward compatibility with unprefixed variables
- Prefixed variables in .env files are for organization only
- Render.yaml files use prefixed variables for consistency
- Default values are hardcoded in config.py as fallback

## Related Documentation

- [ASK Environment Variables](../apps/ask/docs/ENVIRONMENT_VARIABLES.md)
- [Sketch2BIM Environment Variables](../apps/sketch2bim/docs/ENVIRONMENT_VARIABLES.md)
- [Deployment Checklist](../apps/sketch2bim/docs/deployment_checklist.md)

