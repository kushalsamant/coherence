# Admin Dashboard Setup Guide

## Overview

The Platform Dashboard (`/admin`) provides comprehensive business feasibility analysis for the KVSHVL platform (ASK, Sketch2BIM, and Reframe). Access is restricted to admin users only.

## Backend Configuration

### 1. Set Admin Emails

Add the `ADMIN_EMAILS` environment variable to your `ask.env.production` file (or set it in your deployment environment):

```bash
# Comma-separated list of admin email addresses
ASK_ADMIN_EMAILS=admin@example.com,another-admin@example.com

# Or use the shared variable (applies to all apps)
ADMIN_EMAILS=admin@example.com,another-admin@example.com
```

**Important**: 
- Email addresses are case-insensitive
- Multiple admins should be comma-separated
- No spaces around commas (or they will be trimmed)

### 2. Verify Authentication

The dashboard requires:
1. **User Authentication**: User must be signed in via NextAuth
2. **Admin Authorization**: User's email must be in the `ADMIN_EMAILS` list

## Frontend Access

### Accessing the Dashboard

1. Navigate to: `https://kvshvl.in/admin`
2. Sign in if not already authenticated
3. If you're an admin, you'll see the dashboard
4. If you're not an admin, you'll see an "Access Denied" message

### Authentication Flow

1. User signs in via NextAuth (Google OAuth)
2. Frontend checks admin access by calling `/api/feasibility/platform/consolidated`
3. If 403 Forbidden, user is shown access denied message
4. If successful, dashboard loads with all metrics

## API Endpoints

All feasibility endpoints require admin authentication:

- `GET /api/feasibility/platform/unit-economics` - Unit economics analysis
- `GET /api/feasibility/platform/break-even` - Break-even analysis
- `GET /api/feasibility/platform/projections` - Profitability projections
- `GET /api/feasibility/platform/scenarios` - Scenario analysis
- `GET /api/feasibility/platform/margins` - Margin analysis
- `GET /api/feasibility/platform/shared-costs` - Shared infrastructure costs
- `GET /api/feasibility/platform/consolidated` - Consolidated platform view
- `GET /api/feasibility/platform/cross-project` - Cross-project metrics
- `GET /api/feasibility/platform/report` - Generate feasibility report

## Troubleshooting

### "Access Denied" Error

**Possible causes:**
1. Your email is not in the `ADMIN_EMAILS` list
2. `ADMIN_EMAILS` environment variable is not set
3. Email case mismatch (should be handled automatically, but check)

**Solution:**
1. Verify your email is in the `ADMIN_EMAILS` environment variable
2. Check the backend logs for admin access attempts
3. Ensure the environment variable is loaded correctly

### "Admin access not configured" Error

**Cause:** `ADMIN_EMAILS` environment variable is empty or not set

**Solution:**
1. Set `ASK_ADMIN_EMAILS` or `ADMIN_EMAILS` in your environment
2. Restart the backend server
3. Try accessing the dashboard again

### Authentication Issues

**If you can't sign in:**
1. Check that NextAuth is properly configured
2. Verify Google OAuth credentials are set
3. Check browser console for errors

**If you're signed in but still see "Access Denied":**
1. Verify your email matches exactly (case-insensitive) what's in `ADMIN_EMAILS`
2. Check backend logs for the admin check
3. Try signing out and signing back in

## Security Notes

1. **Admin emails are checked on every request** - no caching of admin status
2. **Email comparison is case-insensitive** - `Admin@Example.com` matches `admin@example.com`
3. **Environment variable should be kept secure** - don't commit admin emails to public repos
4. **Consider using environment-specific admin lists** - different admins for dev/staging/prod

## Adding/Removing Admins

To add or remove admin access:

1. Update the `ADMIN_EMAILS` environment variable
2. Restart the backend server
3. Changes take effect immediately (no database migration needed)

## Example Configuration

```bash
# Development
ASK_ADMIN_EMAILS=dev-admin@example.com

# Production
ASK_ADMIN_EMAILS=admin@kvshvl.in,founder@kvshvl.in

# Multiple admins
ASK_ADMIN_EMAILS=admin1@example.com,admin2@example.com,admin3@example.com
```

## Next Steps

After setting up admin access:

1. **Test the dashboard** - Access `/admin` and verify it loads
2. **Review metrics** - Check that cost and revenue data is displaying correctly
3. **Generate reports** - Use the report endpoint to generate feasibility reports
4. **Monitor access** - Check backend logs for any unauthorized access attempts

## Related Documentation

- [Competitive Analysis](./COMPETITIVE_ANALYSIS.md) - Market analysis
- [Deployment Guide](../DEPLOYMENT_CONFIGURATION_GUIDE.md) - Environment setup
- [Monorepo Migration](./MONOREPO_MIGRATION.md) - Platform structure

