# Testing Checklist

Comprehensive testing checklist for all applications in the monorepo after migration to shared packages.

## ASK Application

### Backend Testing

- [ ] **Authentication**
  - [ ] JWT token validation works with shared auth utilities
  - [ ] User authentication flow completes successfully
  - [ ] Session management works correctly

- [ ] **Subscription Management**
  - [ ] Subscription status checks work (`has_active_subscription`)
  - [ ] Subscription expiry calculation works (`calculate_expiry`)
  - [ ] Trial status checks work (`is_active_trial`)
  - [ ] Paid tier checks work (`is_paid_tier`)

- [ ] **Payments**
  - [ ] Razorpay payment creation works
  - [ ] Payment webhook signature verification works
  - [ ] Payment processing fee calculation (2%) works
  - [ ] Payment status updates work correctly

- [ ] **API Endpoints**
  - [ ] `/api/generate` - Content generation works
  - [ ] `/api/qa-pairs` - Q&A pairs retrieval works
  - [ ] `/api/themes` - Themes listing works
  - [ ] `/api/stats` - Statistics endpoint works
  - [ ] `/api/monitoring` - Monitoring endpoint works
  - [ ] `/api/payments` - Payment endpoints work

- [ ] **Database**
  - [ ] Database connection uses `ask_schema`
  - [ ] Schema isolation works (no cross-schema access)
  - [ ] All database operations work correctly

### Frontend Testing

- [ ] **Authentication**
  - [ ] Sign in flow works
  - [ ] Sign out works
  - [ ] Session persistence works

- [ ] **UI Components**
  - [ ] Design template components render correctly
  - [ ] All pages load without errors
  - [ ] Responsive design works

- [ ] **Functionality**
  - [ ] Content generation flow works
  - [ ] Q&A browsing works
  - [ ] Settings page works
  - [ ] Pricing page displays correctly

## Sketch2BIM Application

### Backend Testing

- [ ] **Authentication**
  - [ ] JWT token validation works with shared auth utilities
  - [ ] User authentication flow completes successfully
  - [ ] Session management works correctly

- [ ] **Subscription Management**
  - [ ] Subscription status checks work
  - [ ] Subscription expiry calculation works
  - [ ] Trial status checks work
  - [ ] Paid tier checks work

- [ ] **Payments**
  - [ ] Razorpay payment creation works
  - [ ] Payment webhook signature verification works
  - [ ] Payment processing fee calculation works
  - [ ] Payment status updates work correctly

- [ ] **API Endpoints**
  - [ ] All image processing endpoints work
  - [ ] File upload/download works
  - [ ] Bunny CDN integration works
  - [ ] Health check endpoint works

- [ ] **Database**
  - [ ] Database connection uses `sketch2bim_schema`
  - [ ] Schema isolation works
  - [ ] All database operations work correctly

- [ ] **Redis**
  - [ ] Redis connection works
  - [ ] Caching works correctly
  - [ ] Session storage works

### Frontend Testing

- [ ] **Authentication**
  - [ ] Sign in flow works
  - [ ] Sign out works
  - [ ] Session persistence works

- [ ] **UI Components**
  - [ ] Design template components render correctly
  - [ ] All pages load without errors
  - [ ] Responsive design works

- [ ] **Functionality**
  - [ ] Image upload works
  - [ ] Processing workflow works
  - [ ] Results display correctly
  - [ ] Settings page works

## Reframe Application

### Backend Testing

- [ ] **Authentication**
  - [ ] JWT token validation works with shared auth utilities
  - [ ] User authentication flow completes successfully
  - [ ] No database queries (Redis-only)

- [ ] **Subscription Management**
  - [ ] Redis-based subscription checks work
  - [ ] Usage limits enforced correctly
  - [ ] Free tier limits work (5 reframes)
  - [ ] Premium tier access works

- [ ] **API Endpoints**
  - [ ] `/api/reframe` - Main reframing endpoint works
  - [ ] All tone options work (6 tones)
  - [ ] Generation limits work (9 generations)
  - [ ] Premium tone access works
  - [ ] Health check endpoint works

- [ ] **Redis**
  - [ ] Upstash Redis connection works
  - [ ] User metadata storage works
  - [ ] Usage tracking works
  - [ ] Daily/monthly aggregation works

- [ ] **Groq Integration**
  - [ ] Groq API calls work
  - [ ] Cost monitoring works
  - [ ] Usage tracking works

### Frontend Testing

- [ ] **Authentication**
  - [ ] Sign in flow works
  - [ ] Sign out works
  - [ ] Session persistence works

- [ ] **UI Components**
  - [ ] Design template components render correctly
  - [ ] All pages load without errors
  - [ ] Responsive design works

- [ ] **Functionality**
  - [ ] Text reframing works
  - [ ] All tone options work
  - [ ] Razorpay checkout flow works (shared package)
  - [ ] Usage limits display correctly
  - [ ] Settings page works

## Shared Packages Testing

### Shared Backend

- [ ] **Authentication**
  - [ ] `decode_nextauth_jwt` works correctly
  - [ ] JWT validation handles all edge cases
  - [ ] Auth dependencies work in all apps

- [ ] **Payments**
  - [ ] Razorpay client initialization works
  - [ ] Webhook signature verification works
  - [ ] Processing fee calculation works (2%)

- [ ] **Subscription**
  - [ ] `calculate_expiry` works for all durations
  - [ ] `has_active_subscription` works correctly
  - [ ] `ensure_subscription_status` works
  - [ ] `is_paid_tier` and `is_active_trial` work

- [ ] **Config**
  - [ ] `BaseSettings` loads correctly
  - [ ] Environment variable loading works
  - [ ] App-specific configs extend correctly

### Shared Frontend

- [ ] **Payments**
  - [ ] Razorpay client lazy initialization works
  - [ ] Webhook signature verification works
  - [ ] All imports work correctly

## Integration Testing

- [ ] **Cross-App**
  - [ ] No shared state leaks between apps
  - [ ] Database schema isolation works
  - [ ] Environment variables are properly scoped

- [ ] **Deployment**
  - [ ] All apps build successfully
  - [ ] No missing dependencies
  - [ ] All environment variables are set

## Performance Testing

- [ ] **Response Times**
  - [ ] API endpoints respond within acceptable time
  - [ ] Database queries are optimized
  - [ ] Redis caching improves performance

- [ ] **Load Testing**
  - [ ] Apps handle concurrent requests
  - [ ] Database connection pooling works
  - [ ] No memory leaks

## Security Testing

- [ ] **Authentication**
  - [ ] JWT tokens are properly validated
  - [ ] Unauthorized access is blocked
  - [ ] Session expiration works

- [ ] **Payments**
  - [ ] Webhook signatures are verified
  - [ ] Payment data is secure
  - [ ] No sensitive data in logs

- [ ] **Database**
  - [ ] SQL injection prevention works
  - [ ] Schema isolation prevents cross-access
  - [ ] Connection strings are secure

## Notes

- Test in production-like environment when possible
- Use test payment credentials for Razorpay testing
- Monitor logs for any errors or warnings
- Verify all environment variables are set correctly
- Check database schema isolation manually

## Test Environment Setup

1. Set up local databases with proper schemas
2. Configure Redis (Upstash for Reframe, local for others)
3. Set all required environment variables
4. Install all dependencies
5. Run migrations if needed

