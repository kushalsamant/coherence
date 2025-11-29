# Verify Code Readiness for Infrastructure Consolidation
# This script checks if all code changes are complete before manual configuration

Write-Host "=== Infrastructure Consolidation - Code Readiness Check ===" -ForegroundColor Cyan
Write-Host ""

$errors = @()
$warnings = @()
$success = @()

# Check 1: Verify render.yaml exists and has Upstash Redis for Sketch2BIM
Write-Host "Checking render.yaml..." -ForegroundColor Yellow
if (Test-Path "render.yaml") {
    $renderContent = Get-Content "render.yaml" -Raw
    if ($renderContent -match "SKETCH2BIM_UPSTASH_REDIS_REST_URL") {
        $success += "[OK] render.yaml has Upstash Redis configuration for Sketch2BIM"
    } else {
        $errors += "[ERROR] render.yaml missing SKETCH2BIM_UPSTASH_REDIS_REST_URL"
    }
    if ($renderContent -match "SKETCH2BIM_REDIS_URL" -and $renderContent -notmatch "#.*SKETCH2BIM_REDIS_URL") {
        $warnings += "[WARN] render.yaml still contains SKETCH2BIM_REDIS_URL (should be removed)"
    } else {
        $success += "[OK] render.yaml does not use old Render Redis for Sketch2BIM"
    }
} else {
    $errors += "✗ render.yaml file not found"
}

# Check 2: Verify .env.production files have NEXT_PUBLIC_AUTH_URL
Write-Host "Checking .env.production files..." -ForegroundColor Yellow
$envFiles = @("ask.env.production", "reframe.env.production", "sketch2bim.env.production")
foreach ($file in $envFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        if ($content -match "NEXT_PUBLIC_AUTH_URL=https://kvshvl.in") {
            $appName = $file -replace "\.env\.production", ""
            $success += "[OK] $file has NEXT_PUBLIC_AUTH_URL set"
        } else {
            $errors += "[ERROR] $file missing NEXT_PUBLIC_AUTH_URL"
        }
        
        # Check for old OAuth credentials
        if ($content -match "(ASK|REFRAME|SKETCH2BIM)_GOOGLE_CLIENT_ID" -or $content -match "(ASK|REFRAME|SKETCH2BIM)_GOOGLE_SECRET") {
            $warnings += "[WARN] $file still contains old OAuth credentials (should be removed)"
        } else {
            $appName = $file -replace "\.env\.production", ""
            $success += "[OK] $file has no old OAuth credentials"
        }
    } else {
        $errors += "✗ $file not found"
    }
}

# Check 3: Verify DEPLOYMENT_CONFIGURATION_GUIDE.md exists
Write-Host "Checking deployment guide..." -ForegroundColor Yellow
if (Test-Path "DEPLOYMENT_CONFIGURATION_GUIDE.md") {
    $success += "[OK] DEPLOYMENT_CONFIGURATION_GUIDE.md exists"
} else {
    $errors += "[ERROR] DEPLOYMENT_CONFIGURATION_GUIDE.md not found"
}

# Check 4: Verify main site auth files exist
Write-Host "Checking main site authentication files..." -ForegroundColor Yellow
if (Test-Path "auth.ts") {
    $success += "[OK] auth.ts exists"
} else {
    $errors += "[ERROR] auth.ts not found (required for centralized auth)"
}

# Check for NextAuth route (handle brackets in folder name)
$nextAuthRoute = Get-ChildItem -Path "app\api\auth" -Recurse -Filter "route.ts" -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match "nextauth" }
if ($nextAuthRoute) {
    $success += "[OK] app/api/auth/[...nextauth]/route.ts exists"
} else {
    $errors += "[ERROR] app/api/auth/[...nextauth]/route.ts not found (required for centralized auth)"
}

if (Test-Path "app\api\auth\signin\page.tsx") {
    $success += "[OK] app/api/auth/signin/page.tsx exists"
} else {
    $errors += "[ERROR] app/api/auth/signin/page.tsx not found (required for centralized auth)"
}

# Check 5: Verify app auth.ts files redirect to main site
Write-Host "Checking app authentication redirects..." -ForegroundColor Yellow
$appAuthFiles = @(
    "apps/ask/frontend/auth.ts",
    "apps/reframe/auth.ts",
    "apps/sketch2bim/frontend/auth.ts"
)
foreach ($file in $appAuthFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        if ($content -match "NEXT_PUBLIC_AUTH_URL" -or $content -match "kvshvl\.in") {
            $success += "[OK] $file redirects to main site"
        } else {
            $warnings += "[WARN] $file may not be configured for centralized auth"
        }
    } else {
        $warnings += "[WARN] $file not found (may not exist)"
    }
}

# Summary
Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
Write-Host ""

if ($success.Count -gt 0) {
    Write-Host "[SUCCESS] Checks:" -ForegroundColor Green
    foreach ($item in $success) {
        Write-Host "  $item" -ForegroundColor Green
    }
    Write-Host ""
}

if ($warnings.Count -gt 0) {
    Write-Host "[WARNINGS]:" -ForegroundColor Yellow
    foreach ($item in $warnings) {
        Write-Host "  $item" -ForegroundColor Yellow
    }
    Write-Host ""
}

if ($errors.Count -gt 0) {
    Write-Host "[ERRORS]:" -ForegroundColor Red
    foreach ($item in $errors) {
        Write-Host "  $item" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Please fix errors before proceeding with manual configuration." -ForegroundColor Red
    exit 1
} else {
    Write-Host "[OK] All code changes are complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Commit and push code changes" -ForegroundColor White
    Write-Host "  2. Follow DEPLOYMENT_CONFIGURATION_GUIDE.md for manual Vercel/Render configuration" -ForegroundColor White
    Write-Host ""
    exit 0
}

