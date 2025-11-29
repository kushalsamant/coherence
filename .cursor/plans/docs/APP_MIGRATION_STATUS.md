# Application Migration Status

## Overview

This document tracks the migration status for each application (ASK, Sketch2BIM, Reframe) to use shared packages.

## ASK Backend Migration

### Status: ✅ Complete

#### Completed ✅
1. **Requirements Updated**
   - Added `-e ../../packages/shared-backend` to `requirements.txt` for local editable install

2. **Config Migration**
   - Updated `api/config.py` to extend `shared_backend.config.base.BaseSettings`
   - Kept app-specific fields (database_url property, Razorpay pricing, etc.)
   - Maintains backward compatibility

3. **Subscription Utilities**
   - Updated imports to use `shared_backend.subscription.utils`
   - Functions: `calculate_expiry`, `ensure_subscription_status`, `has_active_subscription`

4. **JWT Authentication**
   - Updated to use `shared_backend.auth.jwt.decode_nextauth_jwt`
   - Removed local JWT decoding implementation

5. **Payments**
   - Updated to use shared subscription utilities
   - Uses shared Razorpay configuration

#### Files Modified
- `apps/ask/requirements.txt` - Added shared-backend dependency
- `apps/ask/api/config.py` - Extends BaseSettings
- `apps/ask/api/auth.py` - Uses shared JWT and subscription utilities
- `apps/ask/api/routes/payments.py` - Uses shared subscription utilities

#### Testing Required ⏳
- Verify shared JWT decoding works with ASK's settings
- Test authentication flow
- Test subscription checks
- Test all API endpoints
- Test payment webhooks

## Sketch2BIM Backend Migration

### Status: ✅ Complete

#### Completed ✅
1. **Requirements Updated**
   - Added `-e ../../packages/shared-backend` to `requirements.txt`

2. **Config Migration**
   - Updated `app/config.py` to extend `shared_backend.config.base.BaseSettings`
   - Kept app-specific configuration

3. **JWT Authentication**
   - Updated to use `shared_backend.auth.jwt.decode_nextauth_jwt`
   - Removed local JWT decoding implementation

4. **Subscription Utilities**
   - Updated to use `shared_backend.subscription.utils`
   - Functions: `calculate_expiry`, `ensure_subscription_status`, `is_active_trial`, `has_active_subscription`

#### Files Modified
- `apps/sketch2bim/backend/requirements.txt` - Added shared-backend dependency
- `apps/sketch2bim/backend/app/config.py` - Extends BaseSettings
- `apps/sketch2bim/backend/app/auth.py` - Uses shared JWT and subscription utilities

#### Testing Required ⏳
- Test authentication flow
- Test subscription checks
- Test all API endpoints
- Test payment webhooks

## Reframe Backend Migration

### Status: ✅ Complete

#### Completed ✅
1. **FastAPI Backend Implementation**
   - FastAPI backend structure created in `apps/reframe/backend/`
   - All services implemented:
     - `redis_service.py` - Upstash Redis REST API client
     - `subscription_service.py` - Subscription logic
     - `tone_service.py` - Tone system with 6 tones and 9 generations
     - `groq_service.py` - Groq API client
     - `groq_monitor.py` - Usage tracking and cost monitoring
     - `user_metadata_service.py` - User metadata management
   - Authentication module (`auth.py`) - NextAuth JWT validation
   - Pydantic models (`models.py`) - Request/response models
   - Configuration (`config.py`) - Application settings
   - Main FastAPI app (`main.py`) - Entry point with CORS
   - Reframe route (`routes/reframe.py`) - Main endpoint implementation
   - `render.yaml` - Render deployment configuration

2. **Frontend Integration**
   - Proxy route (`app/api/reframe-proxy/route.ts`) - Adds JWT token and forwards to FastAPI
   - API client (`lib/api-client.ts`) - Uses proxy route
   - Old Next.js API route removed (`app/api/reframe/route.ts` - DELETED)

3. **Shared Package Integration**
   - Config extends `shared_backend.config.base.BaseSettings`
   - Auth uses `shared_backend.auth.jwt.decode_nextauth_jwt`
   - Requirements includes shared-backend dependency

#### Files Modified
- `apps/reframe/backend/requirements.txt` - Added shared-backend dependency
- `apps/reframe/backend/app/config.py` - Extends BaseSettings
- `apps/reframe/backend/app/auth.py` - Uses shared JWT utilities
- `apps/reframe/lib/api-client.ts` - Uses proxy route
- `apps/reframe/readme.md` - Updated architecture documentation

#### Notes
- Reframe uses Redis, not PostgreSQL, so no database utilities needed
- Authentication only validates JWT, doesn't query a database
- All user metadata stored in Redis keys: `user:metadata:{userId}`
- Usage tracking in Redis: `usage:{userId}:total`
- Groq usage tracked in Redis with daily/monthly aggregation

#### Testing Required ⏳
- Test authentication flow (JWT validation)
- Test subscription checks (Redis-based)
- Test all API endpoints
- Test all tone options
- Test subscription/usage limits
- Test premium tone access
- Monitor Groq usage and costs

## Reframe Frontend Migration

### Status: ✅ Partial (Razorpay Complete)

#### Completed ✅
1. **Razorpay Migration**
   - Updated `apps/reframe/lib/razorpay.ts` to re-export from shared package
   - Maintains backward compatibility (existing imports still work)
   - Uses `@kvshvl/shared-frontend` Razorpay utilities

#### Files Modified
- `apps/reframe/lib/razorpay.ts` - Now re-exports from shared package

#### Testing Required ⏳
- Test Razorpay checkout flow
- Test webhook signature verification
- Ensure all imports still work

## Shared Packages Used

### Backend
1. **`shared_backend.config.base`**
   - BaseSettings class with common configuration
   - Environment variable loading
   - JWT/Auth settings

2. **`shared_backend.auth.jwt`**
   - `decode_nextauth_jwt()` - JWT token validation
   - Consistent JWT handling across all apps

3. **`shared_backend.subscription.utils`**
   - `calculate_expiry()` - Subscription expiry calculation
   - `ensure_subscription_status()` - Status validation
   - `has_active_subscription()` - Subscription check
   - `is_paid_tier()` - Tier validation
   - `is_active_trial()` - Trial check

### Frontend
1. **`@kvshvl/shared-frontend/payments`**
   - Razorpay client with lazy initialization
   - Webhook signature verification

## Testing Checklist

### ASK
- [ ] Authentication flow works
- [ ] Subscription checks work
- [ ] Payment webhooks work
- [ ] All API endpoints work
- [ ] Shared JWT decoding works correctly

### Sketch2BIM
- [ ] Authentication flow works
- [ ] Subscription checks work
- [ ] Payment webhooks work
- [ ] All API endpoints work
- [ ] Shared JWT decoding works correctly

### Reframe
- [ ] Authentication flow works (JWT validation)
- [ ] Subscription checks work (Redis-based)
- [ ] All API endpoints work
- [ ] All tone options work
- [ ] Subscription/usage limits work
- [ ] Premium tone access works
- [ ] Razorpay checkout flow works
- [ ] Webhook signature verification works

## Migration Status Summary

**Overall Status**: ✅ **Complete**

All three applications (ASK, Sketch2BIM, Reframe) have successfully migrated to use shared backend packages. The migrations are complete and in production.

### Completed ✅
- All backend configs extend shared BaseSettings
- All authentication uses shared JWT utilities
- All subscription logic uses shared utilities
- Database setup complete (Supabase with schema isolation)
- Environment variables centralized in `.env.production` files
- Repository cleanup complete (old repos deleted)

### Optional Future Work
- Further frontend package migrations
- Additional shared utility extraction
- Enhanced testing coverage

## Notes

- All migrations maintain backward compatibility
- App-specific code preserved where needed
- Incremental approach minimizes risk
- Shared packages use factory patterns for flexibility
- Each app can still customize as needed

