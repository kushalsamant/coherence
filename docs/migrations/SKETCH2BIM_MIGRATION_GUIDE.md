# Sketch2BIM Application Migration Guide

## Overview

This guide covers migrating the Sketch2BIM application from legacy systems to the unified platform.

## Database Migration

### Current Schema

Sketch2BIM uses PostgreSQL with the following main tables:
- `users` - User accounts and subscription information
- `jobs` - Sketch-to-BIM conversion jobs
- `iterations` - Job iterations
- `variations` - Job variations
- `referrals` - Referral tracking

### Key Fields

All payment-related fields use `razorpay_*` naming:
- `razorpay_customer_id`
- `razorpay_subscription_id`
- `razorpay_payment_id`
- `razorpay_order_id`

### Migration System

Sketch2BIM uses **Alembic** for database migrations:
- Location: `database/migrations/sketch2bim/`
- Migrations run automatically on application startup
- Can be run manually via `alembic upgrade head`

### Migration Steps

1. **Backup Database**
   ```bash
   pg_dump -h <host> -U <user> -d <database> > sketch2bim_backup.sql
   ```

2. **Run Schema Migrations**
   ```bash
   cd database/migrations/sketch2bim
   alembic upgrade head
   ```

3. **Verify Data Integrity**
   - Check user counts match
   - Verify job records
   - Confirm subscription statuses
   - Check iteration and variation data

### Creating New Migrations

To add schema changes:
```bash
cd database/migrations/sketch2bim
alembic revision --autogenerate -m "description of change"
```

Then review, test, and commit the generated migration file.

## Code Migration

### Import Paths

All imports have been updated to use the new structure:
- `from auth.sketch2bim import get_current_user`
- `from database.sketch2bim import get_db, SessionLocal`
- `from models.sketch2bim import User, Job`
- `from config.sketch2bim import settings`

### API Endpoints

All Sketch2BIM endpoints are under `/api/sketch2bim/*`:
- `/api/sketch2bim/generate` - Create new job
- `/api/sketch2bim/iterations` - Manage iterations
- `/api/sketch2bim/variations` - Manage variations
- `/api/sketch2bim/referrals` - Referral management
- `/api/sketch2bim/payments` - Payment endpoints
- `/api/sketch2bim/health` - Health check

## Environment Variables

Required environment variables (all prefixed):
- `SKETCH2BIM_DATABASE_URL` - PostgreSQL connection string
- `SKETCH2BIM_RAZORPAY_KEY_ID` - Razorpay key ID
- `SKETCH2BIM_RAZORPAY_KEY_SECRET` - Razorpay key secret
- `SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET` - Razorpay webhook secret
- `SKETCH2BIM_GROQ_API_KEY` - Groq API key
- `SKETCH2BIM_GROQ_MONTHLY_COST_THRESHOLD` - Monthly cost threshold (USD)
- `SKETCH2BIM_BUNNY_STORAGE_ZONE` - BunnyCDN storage zone
- `SKETCH2BIM_BUNNY_API_KEY` - BunnyCDN API key

## Testing Checklist

- [ ] User authentication works
- [ ] Subscription management works
- [ ] Payment processing works
- [ ] Job creation works
- [ ] File upload works
- [ ] Job processing works
- [ ] Iterations and variations work
- [ ] Health endpoints respond
- [ ] Webhook handlers process events correctly

## Rollback Procedure

If migration fails:
1. Restore database backup
2. Revert code changes
3. Update environment variables to previous values
4. Restart services
5. If using Alembic: `alembic downgrade -1`

