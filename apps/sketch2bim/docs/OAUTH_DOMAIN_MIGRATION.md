# OAuth Domain Migration Guide

## Overview

This document outlines the steps required to migrate OAuth authentication from `https://sketch2bim.vercel.app` to `https://sketch2bim.kvshvl.in`.

## Status

✅ **Completed (Code/Config Updates)**:
- Documentation files updated
- Configuration files updated
- All code references updated

⚠️ **Manual Steps Required**:
- Google Cloud Console OAuth credentials
- Vercel environment variables
- Backend environment variables (if needed)

## Manual Steps Required

### Step 1: Google Cloud Console OAuth Credentials

**Location**: https://console.cloud.google.com/apis/credentials

**Action Required**:
1. Navigate to Google Cloud Console → APIs & Services → Credentials
2. Find the OAuth 2.0 Client ID used for Sketch2BIM
3. Click "Edit" on the OAuth client
4. Update **Authorized redirect URIs**:
   - **Remove**: `https://sketch2bim.vercel.app/api/auth/callback/google`
   - **Add**: `https://sketch2bim.kvshvl.in/api/auth/callback/google`
5. Update **Authorized JavaScript origins** (if configured):
   - **Remove**: `https://sketch2bim.vercel.app`
   - **Add**: `https://sketch2bim.kvshvl.in`
6. Save changes

**Important**: Changes may take 5-10 minutes to propagate.

### Step 2: Vercel Environment Variables

**Location**: Vercel Dashboard → Project Settings → Environment Variables

**Action Required**:
1. Navigate to your Vercel project settings
2. Go to Environment Variables section
3. Update `AUTH_URL`:
   - **Old**: `https://sketch2bim.vercel.app`
   - **New**: `https://sketch2bim.kvshvl.in`
4. Ensure no trailing slash
5. Apply to all environments (Production, Preview, Development)
6. Redeploy the application after updating

**Other variables to check**:
- `NEXTAUTH_URL` (if exists) - should match `AUTH_URL`
- `FRONTEND_URL` (if exists) - should be `https://sketch2bim.kvshvl.in`

### Step 3: Backend Environment Variables (Render)

**Location**: Render Dashboard → Service Settings → Environment

**Action Required**:
1. Navigate to your Render backend service
2. Go to Environment section
3. Update `FRONTEND_URL`:
   - **Old**: `https://sketch2bim.vercel.app`
   - **New**: `https://sketch2bim.kvshvl.in`
4. Update `ALLOWED_ORIGINS`:
   - **Old**: `https://sketch2bim.vercel.app` or `https://sketch2bim.com`
   - **New**: `https://sketch2bim.kvshvl.in`
5. Save changes (Render will automatically redeploy)

## Verification Steps

After completing all manual steps:

1. **Clear browser cache and cookies**
2. Visit `https://sketch2bim.kvshvl.in`
3. Click "Sign In with Google"
4. Verify redirect to Google OAuth consent screen
5. Complete OAuth flow
6. Verify redirect back to `https://sketch2bim.kvshvl.in` after authentication
7. Verify user is logged in and can access dashboard

## Expected Behavior

- ✅ OAuth flow completes successfully
- ✅ User is redirected back to application
- ✅ Session is established
- ✅ No redirect loops or errors

## Troubleshooting

If sign-in still doesn't work after updates:

1. **Check Google Console**: Verify redirect URI is exactly `https://sketch2bim.kvshvl.in/api/auth/callback/google`
2. **Check Vercel env vars**: Verify `AUTH_URL=https://sketch2bim.kvshvl.in` (no trailing slash)
3. **Check Render env vars**: Verify `FRONTEND_URL` and `ALLOWED_ORIGINS` are updated
4. **Check browser console**: Look for OAuth errors
5. **Check NextAuth logs**: Enable debug mode if needed (`debug: true` in auth.ts)
6. **Verify SSL**: Ensure new domain has valid SSL certificate
7. **Wait for propagation**: Google OAuth changes may take 5-10 minutes

## Files Updated

### Documentation
- ✅ `README.md` - Updated domain references
- ✅ `docs/DEPLOYMENT_CHECKLIST.md` - Updated example URLs
- ✅ `docs/PRODUCTION_VERIFICATION.md` - Updated verification steps
- ✅ `docs/TROUBLESHOOTING.md` - Updated OAuth troubleshooting section
- ✅ `frontend/app/docs/quickstart/page.tsx` - Updated example URL

### Configuration
- ✅ `infra/render.yaml` - Updated `FRONTEND_URL` and `ALLOWED_ORIGINS`

## Important Notes

1. **OAuth Redirect URI must match exactly**: The redirect URI in Google Console must exactly match what NextAuth expects: `https://sketch2bim.kvshvl.in/api/auth/callback/google`

2. **AUTH_URL must match frontend domain**: The `AUTH_URL` environment variable must exactly match the frontend domain (no trailing slash)

3. **Propagation time**: Google OAuth changes may take 5-10 minutes to propagate. Vercel deployments are usually instant.

4. **Cache clearing**: Users may need to clear browser cache/cookies if they previously signed in with the old domain

5. **HTTPS required**: OAuth requires HTTPS - ensure the new domain has valid SSL certificate

## Support

If you encounter issues after completing all steps, check:
- Browser console for errors
- Vercel deployment logs
- Render service logs
- NextAuth debug logs (if enabled)

