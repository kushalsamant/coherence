# Environment Variables Update Instructions

> **⚠️ Important:** All production environment variables are centralized in `.env.production` files at the repository root:
> - `ask.env.production`
> - `sketch2bim.env.production`
> - `reframe.env.production`

## Update Shared OAuth Variables

Add the following to the **top** of each `.env.production` file (in the shared section):

```bash
# =============================================================================
# SHARED GOOGLE OAUTH (Used by all apps via kvshvl.in)
# =============================================================================
GOOGLE_CLIENT_ID=620186529337-lrr0bflcuihq2gnsko6vbrnsdv2u3ugu.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=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
```

## Remove or Comment Out Old OAuth Variables

Find and comment out or remove these old app-specific OAuth variables:

```bash
# OLD - Remove or comment out:
# ASK_GOOGLE_CLIENT_ID=...
# ASK_GOOGLE_SECRET=...
# REFRAME_GOOGLE_CLIENT_ID=...
# REFRAME_GOOGLE_SECRET=...
# SKETCH2BIM_GOOGLE_CLIENT_ID=...
# SKETCH2BIM_GOOGLE_SECRET=...
```

## Verification

After updating each `.env.production` file, verify:
1. `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are in the shared section
2. Old app-specific OAuth variables (e.g., `ASK_GOOGLE_CLIENT_ID`) are commented out or removed
3. All other environment variables remain unchanged

## Local Development

For local development, create `.env.local` files in app directories (these are gitignored):
- `apps/ask/api/.env.local`
- `apps/ask/frontend/.env.local`
- `apps/sketch2bim/backend/.env.local`
- `apps/sketch2bim/frontend/.env.local`
- `apps/reframe/.env.local`

These local files will override values from the centralized `.env.production` files.

