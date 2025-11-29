# Vercel Automation Guide

This guide explains how to automate Vercel configuration for all projects (ASK, Reframe, Sketch2BIM) without manually visiting the Vercel dashboard.

## Overview

The automation consists of:
1. **vercel.json files** - Configuration files for each project
2. **setup-vercel.ps1** - Script to link projects and set up Vercel
3. **sync-vercel-env.ps1** - Script to sync environment variables from `.env.production` files

## Prerequisites

1. **Vercel CLI installed:**
   ```powershell
   npm install -g vercel
   ```

2. **Vercel account** with access to the `kvshvl` team

3. **Vercel token** (optional, for non-interactive setup):
   - Get from: https://vercel.com/account/tokens
   - Store securely (don't commit to git)

## Project Structure

Each project has its own `vercel.json` file:

- **ASK**: `apps/ask/frontend/vercel.json`
- **Reframe**: `apps/reframe/vercel.json`
- **Sketch2BIM**: `apps/sketch2bim/frontend/vercel.json`

## Initial Setup

### Quick Start (Recommended)

Run the master script to complete all setup steps automatically:

```powershell
cd kushalsamant.github.io
.\scripts\setup-vercel-all.ps1 -VercelToken "your-token-here"
```

This will:
1. Check prerequisites
2. Authenticate with Vercel
3. Link all projects
4. Set root directories via API
5. Sync environment variables
6. Verify configuration

**Dry run mode:**
```powershell
.\scripts\setup-vercel-all.ps1 -VercelToken "token" -DryRun
```

### Manual Setup (Step by Step)

If you prefer to run steps individually:

#### Step 1: Link Projects to Vercel

```powershell
.\scripts\setup-vercel.ps1 -VercelToken "your-token-here"
```

This script will:
- Check if Vercel CLI is installed
- Authenticate with Vercel (if needed)
- Link each project to Vercel

#### Step 2: Set Root Directories

**Automated (via API):**
```powershell
.\scripts\setup-vercel-rootdir.ps1 -VercelToken "your-token-here"
```

**Manual (via Dashboard):**
1. **ASK**: 
   - Go to: https://vercel.com/kvshvl/ask/settings
   - General → Root Directory: `apps/ask/frontend`
   - Save

2. **Reframe**:
   - Go to: https://vercel.com/kvshvl/reframe/settings
   - General → Root Directory: `apps/reframe`
   - Save

3. **Sketch2BIM**:
   - Go to: https://vercel.com/kvshvl/sketch2bim/settings
   - General → Root Directory: `apps/sketch2bim/frontend`
   - Save

#### Step 3: Sync Environment Variables

Sync environment variables from `.env.production` files:

```powershell
.\scripts\sync-vercel-env.ps1
```

**Options:**
- `-Environment production` - Sync to production only (default)
- `-Environment all` - Sync to production, preview, and development
- `-DryRun` - Preview changes without applying
- `-Force` - Update existing variables
- `-VercelToken "token"` - Use token for non-interactive mode

**Example:**
```powershell
# Dry run to see what would be synced
.\scripts\sync-vercel-env.ps1 -DryRun

# Sync to production only
.\scripts\sync-vercel-env.ps1 -Environment production

# Sync to all environments
.\scripts\sync-vercel-env.ps1 -Environment all -Force
```

## Environment Variables

The sync script automatically filters and syncs only frontend variables:

### ASK Frontend Variables
- `ASK_API_BASE_URL`
- `ASK_AUTH_SECRET`
- `ASK_AUTH_URL`
- `ASK_BACKEND_URL`
- `ASK_GOOGLE_CLIENT_ID`
- `ASK_GOOGLE_SECRET`
- `ASK_GROQ_API_BASE`
- `ASK_NEXT_PUBLIC_API_URL`
- `ASK_NEXTAUTH_SECRET`
- `ASK_NEXTAUTH_URL`
- `NEXT_PUBLIC_AUTH_URL`
- Any `NEXT_PUBLIC_*` variables

### Reframe Frontend Variables
- `REFRAME_API_URL`
- `REFRAME_AUTH_SECRET`
- `REFRAME_AUTH_URL`
- `REFRAME_GOOGLE_CLIENT_ID`
- `REFRAME_GOOGLE_CLIENT_SECRET`
- `REFRAME_NEXT_PUBLIC_API_URL`
- `REFRAME_NEXT_PUBLIC_FREE_LIMIT`
- `REFRAME_NEXT_PUBLIC_SITE_URL`
- `REFRAME_NEXTAUTH_SECRET`
- `REFRAME_NEXTAUTH_URL`
- `REFRAME_RAZORPAY_KEY_ID`
- `REFRAME_RAZORPAY_KEY_SECRET`
- `REFRAME_RAZORPAY_WEBHOOK_SECRET`
- `REFRAME_RESEND_API_KEY`
- `NEXT_PUBLIC_AUTH_URL`
- Any `NEXT_PUBLIC_*` variables

### Sketch2BIM Frontend Variables
- `SKETCH2BIM_AUTH_SECRET`
- `SKETCH2BIM_AUTH_URL`
- `SKETCH2BIM_GOOGLE_CLIENT_ID`
- `SKETCH2BIM_GOOGLE_SECRET`
- `SKETCH2BIM_NEXT_PUBLIC_API_URL`
- `SKETCH2BIM_NEXT_PUBLIC_FREE_LIMIT`
- `SKETCH2BIM_NEXTAUTH_SECRET`
- `SKETCH2BIM_NEXTAUTH_URL`
- `NEXT_PUBLIC_AUTH_URL`
- Any `NEXT_PUBLIC_*` variables

## vercel.json Configuration

Each `vercel.json` file configures:

- **Framework**: Next.js (auto-detected)
- **Build command**: `npm run build`
- **Output directory**: `.next`
- **Install command**: `npm install`
- **Image optimization**: Domain configurations
- **Function timeouts**: For Sketch2BIM (300s for WebAssembly)

## Updating Environment Variables

### Method 1: Update .env.production and Sync

1. Edit the appropriate `.env.production` file:
   - `ask.env.production`
   - `reframe.env.production`
   - `sketch2bim.env.production`

2. Run the sync script:
   ```powershell
   .\scripts\sync-vercel-env.ps1 -Environment production -Force
   ```

### Method 2: Manual via Vercel CLI

```powershell
# Add a single variable
vercel env add VARIABLE_NAME ask production

# List all variables
vercel env ls ask

# Remove a variable
vercel env rm VARIABLE_NAME ask production
```

### Method 3: Via Vercel Dashboard

1. Go to project settings: https://vercel.com/kvshvl/{project}/settings/environment-variables
2. Add/edit variables manually

## Troubleshooting

### Vercel CLI Not Found

**Error:** `vercel: command not found`

**Solution:**
```powershell
npm install -g vercel
```

### Authentication Failed

**Error:** `Not authenticated`

**Solution:**
```powershell
vercel login
```

Or use a token:
```powershell
$env:VERCEL_TOKEN = "your-token"
```

### Project Not Found

**Error:** `Project not found: ask`

**Solution:**
1. Ensure project exists in Vercel dashboard
2. Check project name matches (case-sensitive)
3. Verify you have access to the `kvshvl` team

### Root Directory Not Set

**Symptom:** Build fails or wrong files are deployed

**Solution:**
Set root directory in Vercel dashboard (see Step 2 above)

### Environment Variables Not Syncing

**Possible causes:**
1. Variable not in frontend variables list
2. Variable value is empty
3. API rate limiting
4. Token permissions

**Solution:**
- Check script output for errors
- Verify variable exists in `.env.production`
- Try syncing manually via CLI
- Check Vercel API rate limits

### Build Failures

**Common issues:**
1. **Wrong root directory** - Set in dashboard
2. **Missing environment variables** - Sync via script
3. **Node version mismatch** - Set in `package.json` or Vercel settings
4. **Build command issues** - Check `vercel.json` buildCommand

## Automation Workflow

### Initial Setup (One-time)

**Option 1: Automated (Recommended)**
```powershell
# 1. Install Vercel CLI
npm install -g vercel

# 2. Get Vercel token from https://vercel.com/account/tokens

# 3. Run master script (does everything)
.\scripts\setup-vercel-all.ps1 -VercelToken "your-token" -Environment all
```

**Option 2: Step by Step**
```powershell
# 1. Install Vercel CLI
npm install -g vercel

# 2. Get Vercel token
# Get from: https://vercel.com/account/tokens

# 3. Link projects
.\scripts\setup-vercel.ps1 -VercelToken "token"

# 4. Set root directories
.\scripts\setup-vercel-rootdir.ps1 -VercelToken "token"

# 5. Sync environment variables
.\scripts\sync-vercel-env.ps1 -VercelToken "token" -Environment all

# 6. Verify setup
.\scripts\verify-vercel-setup.ps1 -VercelToken "token" -Environment all
```

### Regular Updates

```powershell
# After updating .env.production files
.\scripts\sync-vercel-env.ps1 -Environment production -Force
```

## CI/CD Integration

You can integrate these scripts into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Sync Vercel Environment Variables
  run: |
    npm install -g vercel
    vercel login --token ${{ secrets.VERCEL_TOKEN }}
    pwsh scripts/sync-vercel-env.ps1 -VercelToken ${{ secrets.VERCEL_TOKEN }} -Environment production
```

## Limitations

1. **Root Directory**: Cannot be set via CLI or vercel.json (must use dashboard or API)
2. **Interactive Prompts**: Some Vercel CLI commands require interactive input
3. **API Rate Limits**: Vercel API has rate limits (check dashboard)
4. **Secrets**: Sensitive values should be set via dashboard or secure token

## Best Practices

1. **Use tokens for automation**: Store Vercel token securely (environment variable, secret manager)
2. **Dry run first**: Always test with `-DryRun` before applying changes
3. **Version control**: Commit `vercel.json` files but not `.vercel` directories
4. **Document changes**: Update `.env.production` files when adding new variables
5. **Test locally**: Verify builds work locally before deploying

## Related Documentation

- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Vercel API Documentation](https://vercel.com/docs/rest-api)
- [Environment Variables Reference](../apps/ask/docs/ENVIRONMENT_VARIABLES.md)
- [Deployment Configuration Guide](../DEPLOYMENT_CONFIGURATION_GUIDE.md)

## Scripts Reference

### setup-vercel-all.ps1 (Master Script)

**Purpose:** Run all Vercel setup steps in sequence

**Usage:**
```powershell
.\scripts\setup-vercel-all.ps1 [-VercelToken "token"] [-Environment production|preview|development|all] [-DryRun] [-SkipVerification]
```

**Parameters:**
- `-VercelToken`: Vercel API token for non-interactive mode
- `-Environment`: Target environment for env var sync - default: `production`
- `-DryRun`: Preview changes without applying
- `-SkipVerification`: Skip verification step at the end

**Example:**
```powershell
# Complete setup for production
.\scripts\setup-vercel-all.ps1 -VercelToken "token" -Environment production

# Dry run to see what would happen
.\scripts\setup-vercel-all.ps1 -VercelToken "token" -DryRun
```

### setup-vercel.ps1

**Purpose:** Link projects to Vercel and set up basic configuration

**Usage:**
```powershell
.\scripts\setup-vercel.ps1 [-VercelToken "token"] [-SkipLogin]
```

**Parameters:**
- `-VercelToken`: Vercel API token for non-interactive mode
- `-SkipLogin`: Skip authentication check (if already logged in)

### setup-vercel-rootdir.ps1

**Purpose:** Set root directories for all projects via Vercel API

**Usage:**
```powershell
.\scripts\setup-vercel-rootdir.ps1 -VercelToken "token" [-DryRun]
```

**Parameters:**
- `-VercelToken`: Vercel API token (required)
- `-DryRun`: Preview changes without applying

**Note:** Requires Vercel API token with project admin permissions.

### sync-vercel-env.ps1

**Purpose:** Sync environment variables from `.env.production` files to Vercel

**Usage:**
```powershell
.\scripts\sync-vercel-env.ps1 [-Environment production|preview|development|all] [-DryRun] [-Force] [-VercelToken "token"]
```

**Parameters:**
- `-Environment`: Target environment(s) - default: `production`
- `-DryRun`: Preview changes without applying
- `-Force`: Update existing variables
- `-VercelToken`: Vercel API token for non-interactive mode

### verify-vercel-setup.ps1

**Purpose:** Verify Vercel configuration for all projects

**Usage:**
```powershell
.\scripts\verify-vercel-setup.ps1 [-VercelToken "token"] [-Environment production|preview|development|all]
```

**Parameters:**
- `-VercelToken`: Vercel API token (optional, but required for root directory verification)
- `-Environment`: Environment to check - default: `production`

**Checks:**
- Projects are linked
- Root directories are set correctly
- Environment variables are present
- Variables match `.env.production` files

**Example:**
```powershell
# Verify production setup
.\scripts\verify-vercel-setup.ps1 -VercelToken "token" -Environment production

# Verify all environments
.\scripts\verify-vercel-setup.ps1 -VercelToken "token" -Environment all
```

## Support

For issues or questions:
1. Check Vercel dashboard for project status
2. Review script output for error messages
3. Check Vercel CLI version: `vercel --version`
4. Verify environment files are correctly formatted

