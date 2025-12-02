# Reframe Application Migration Guide

## Overview

This guide covers migrating the Reframe application from legacy systems to the unified platform.

## Database Migration

### Current Architecture

Reframe uses **Redis** for data storage, not PostgreSQL. No SQL database migration is required.

### Redis Keys Structure

- `user:{email}` - User metadata
- `reframe:{user_id}` - User reframe data
- `subscription:{user_id}` - Subscription information

### Migration Steps

1. **Backup Redis Data**
   ```bash
   redis-cli --rdb /path/to/reframe_backup.rdb
   ```

2. **Verify Redis Connection**
   - Check `REFRAME_REDIS_URL` environment variable
   - Test connection to Redis instance

3. **Verify Data Integrity**
   - Check user counts match
   - Verify subscription data
   - Confirm reframe data exists

## Code Migration

### Import Paths

All imports have been updated to use the new structure:
- `from auth.reframe import get_current_user_id, get_current_user_email`
- `from services.reframe.redis_service import get_redis_client`
- `from config.reframe import settings`

### API Endpoints

All Reframe endpoints are under `/api/reframe/*`:
- `/api/reframe` - Main reframe endpoint
- `/api/reframe/subscription` - Subscription management

## Environment Variables

Required environment variables (all prefixed):
- `REFRAME_REDIS_URL` - Redis connection string
- `REFRAME_RAZORPAY_KEY_ID` - Razorpay key ID
- `REFRAME_RAZORPAY_KEY_SECRET` - Razorpay key secret
- `REFRAME_RAZORPAY_WEBHOOK_SECRET` - Razorpay webhook secret
- `REFRAME_GROQ_API_KEY` - Groq API key
- `REFRAME_GROQ_MONTHLY_COST_THRESHOLD` - Monthly cost threshold (USD)

## Testing Checklist

- [ ] User authentication works
- [ ] Subscription management works
- [ ] Payment processing works
- [ ] Reframe generation works
- [ ] Redis connection works
- [ ] Webhook handlers process events correctly

## Rollback Procedure

If migration fails:
1. Restore Redis backup
2. Revert code changes
3. Update environment variables to previous values
4. Restart services

