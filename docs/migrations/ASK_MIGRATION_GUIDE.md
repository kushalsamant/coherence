# ASK Application Migration Guide

## Overview

This guide covers migrating the ASK application from legacy systems to the unified platform.

## Database Migration

### Current Schema

ASK uses PostgreSQL (Upstash Postgres) with the following main tables:
- `users` - User accounts and subscription information
- `payments` - Payment transaction history
- `groq_usage` - Groq API usage tracking

### Key Fields

All payment-related fields use `razorpay_*` naming:
- `razorpay_customer_id`
- `razorpay_subscription_id`
- `razorpay_payment_id`
- `razorpay_order_id`

### Migration System

ASK uses **Alembic** for database migrations:
- Location: `database/migrations/ask/`
- Migrations run automatically on application startup
- Can be run manually via `alembic upgrade head`

### Migration Steps

1. **Backup Database**
   ```bash
   pg_dump -h <host> -U <user> -d <database> > ask_backup.sql
   ```

2. **Run Schema Migrations**
   ```bash
   cd database/migrations/ask
   alembic upgrade head
   ```

3. **Verify Data Integrity**
   - Check user counts match
   - Verify payment records
   - Confirm subscription statuses

### Creating New Migrations

To add schema changes:
```bash
cd database/migrations/ask
alembic revision --autogenerate -m "description of change"
```

Then review, test, and commit the generated migration file.

## Code Migration

### Import Paths

All imports have been updated to use the new structure:
- `from auth.ask import get_current_user`
- `from database.ask import get_db, SessionLocal`
- `from models.ask import User, Payment`
- `from config.base import settings`

### API Endpoints

All ASK endpoints are under `/api/ask/*`:
- `/api/ask/qa-pairs` - Get Q&A pairs
- `/api/ask/generate` - Generate content
- `/api/ask/themes` - Get themes
- `/api/ask/stats` - Get statistics
- `/api/ask/payments` - Payment endpoints

## Environment Variables

Required environment variables (all prefixed):
- `ASK_DATABASE_URL` - PostgreSQL connection string
- `ASK_RAZORPAY_KEY_ID` - Razorpay key ID
- `ASK_RAZORPAY_KEY_SECRET` - Razorpay key secret
- `ASK_RAZORPAY_WEBHOOK_SECRET` - Razorpay webhook secret
- `ASK_GROQ_API_KEY` - Groq API key
- `ASK_GROQ_MONTHLY_COST_THRESHOLD` - Monthly cost threshold (USD)

## Testing Checklist

- [ ] User authentication works
- [ ] Subscription management works
- [ ] Payment processing works
- [ ] Content generation works
- [ ] Q&A pairs can be retrieved
- [ ] Statistics endpoint works
- [ ] Webhook handlers process events correctly

## Rollback Procedure

If migration fails:
1. Restore database backup
2. Revert code changes
3. Update environment variables to previous values
4. Restart services

