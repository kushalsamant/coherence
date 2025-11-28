# =============================================================================
# Vercel Complete Setup Script
# =============================================================================
# Master script that runs all Vercel setup steps in sequence:
# 1. Prerequisites check
# 2. Authentication
# 3. Link projects
# 4. Set root directories
# 5. Sync environment variables
# 6. Verification
# =============================================================================

param(
    [string]$VercelToken = "",
    [ValidateSet("production", "preview", "development", "all")]
    [string]$Environment = "production",
    [switch]$DryRun = $false,
    [switch]$SkipVerification = $false
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Vercel Complete Setup Automation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# Get repository root (parent of scripts directory)
$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $repoRoot) {
    $repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}
$repoRoot = Resolve-Path $repoRoot

# Get Vercel token from environment if not provided
if (-not $VercelToken) {
    $VercelToken = $env:VERCEL_TOKEN
}

# Step 1: Prerequisites Check
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 1: Prerequisites Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Vercel CLI
Write-Host "Checking for Vercel CLI..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version 2>&1
    Write-Host "✓ Vercel CLI found: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Vercel CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "  npm install -g vercel" -ForegroundColor Yellow
    exit 1
}

# Check for token (required for root directory setup)
if (-not $VercelToken) {
    Write-Host ""
    Write-Host "⚠ Vercel token not provided. Some steps may require manual intervention." -ForegroundColor Yellow
    Write-Host "  Get token from: https://vercel.com/account/tokens" -ForegroundColor Gray
    Write-Host "  Set via: -VercelToken parameter or VERCEL_TOKEN environment variable" -ForegroundColor Gray
    Write-Host ""
    $continue = Read-Host "Continue anyway? (y/N)"
    if ($continue -ne "y" -and $continue -ne "Y") {
        exit 0
    }
}

Write-Host ""

# Step 2: Authentication
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 2: Authentication" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Checking Vercel authentication..." -ForegroundColor Yellow
try {
    if ($VercelToken) {
        $env:VERCEL_TOKEN = $VercelToken
    }
    $whoami = vercel whoami 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Authenticated as: $whoami" -ForegroundColor Green
    } else {
        throw "Not authenticated"
    }
} catch {
    Write-Host "Not authenticated. Logging in..." -ForegroundColor Yellow
    if ($VercelToken) {
        $env:VERCEL_TOKEN = $VercelToken
        Write-Host "Using provided Vercel token..." -ForegroundColor Gray
    } else {
        vercel login
        if ($LASTEXITCODE -ne 0) {
            Write-Host "✗ Login failed" -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host ""

# Step 3: Link Projects
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 3: Link Projects" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$setupScript = Join-Path $repoRoot "scripts\setup-vercel.ps1"
if (Test-Path $setupScript) {
    Write-Host "Running project linking script..." -ForegroundColor Yellow
    try {
        if ($VercelToken) {
            & $setupScript -VercelToken $VercelToken -SkipLogin 2>&1 | Out-Host
        } else {
            & $setupScript -SkipLogin 2>&1 | Out-Host
        }
        
        if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
            Write-Host "⚠ Project linking had issues. Continuing..." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠ Project linking had issues: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Setup script not found: $setupScript" -ForegroundColor Yellow
}

Write-Host ""

# Step 4: Set Root Directories
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 4: Set Root Directories" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$rootDirScript = Join-Path $repoRoot "scripts\setup-vercel-rootdir.ps1"
if (Test-Path $rootDirScript) {
    if ($VercelToken) {
        Write-Host "Setting root directories via API..." -ForegroundColor Yellow
        try {
            if ($DryRun) {
                & $rootDirScript -VercelToken $VercelToken -DryRun 2>&1 | Out-Host
            } else {
                & $rootDirScript -VercelToken $VercelToken 2>&1 | Out-Host
            }
            
            if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
                Write-Host "⚠ Root directory setup had issues. Check output above." -ForegroundColor Yellow
            }
        } catch {
            Write-Host "⚠ Root directory setup had issues: $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠ Vercel token required for root directory setup." -ForegroundColor Yellow
        Write-Host "  Skipping this step. Set root directories manually in dashboard:" -ForegroundColor Yellow
        Write-Host "  - ASK: apps/ask/frontend" -ForegroundColor Gray
        Write-Host "  - Reframe: apps/reframe" -ForegroundColor Gray
        Write-Host "  - Sketch2BIM: apps/sketch2bim/frontend" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠ Root directory script not found: $rootDirScript" -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Sync Environment Variables
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 5: Sync Environment Variables" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$syncScript = Join-Path $repoRoot "scripts\sync-vercel-env.ps1"
if (Test-Path $syncScript) {
    Write-Host "Syncing environment variables..." -ForegroundColor Yellow
    try {
        $syncParams = @{
            Environment = $Environment
        }
        if ($DryRun) {
            $syncParams.DryRun = $true
        }
        if ($VercelToken) {
            $syncParams.VercelToken = $VercelToken
        }
        
        & $syncScript @syncParams 2>&1 | Out-Host
        
        if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne $null) {
            Write-Host "⚠ Environment variable sync had issues. Check output above." -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠ Environment variable sync had issues: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ Sync script not found: $syncScript" -ForegroundColor Yellow
}

Write-Host ""

# Step 6: Verification
if (-not $SkipVerification) {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Step 6: Verification" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $verifyScript = Join-Path $repoRoot "scripts\verify-vercel-setup.ps1"
    if (Test-Path $verifyScript) {
        Write-Host "Running verification..." -ForegroundColor Yellow
        try {
            if ($VercelToken) {
                & $verifyScript -VercelToken $VercelToken -Environment $Environment 2>&1 | Out-Host
            } else {
                & $verifyScript -Environment $Environment 2>&1 | Out-Host
            }
        } catch {
            Write-Host "⚠ Verification had issues: $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠ Verification script not found: $verifyScript" -ForegroundColor Yellow
        Write-Host "  Run it separately when available." -ForegroundColor Gray
    }
    
    Write-Host ""
}

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "This was a dry run. Run without -DryRun to apply changes." -ForegroundColor Yellow
} else {
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Verify deployments in Vercel dashboard" -ForegroundColor Gray
    Write-Host "2. Test deployments for each project" -ForegroundColor Gray
    Write-Host "3. Monitor first deployments for any issues" -ForegroundColor Gray
}

Write-Host ""

