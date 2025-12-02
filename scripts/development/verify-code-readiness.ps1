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

# Check 2: Verify .env.local file exists and has required variables
Write-Host "Checking .env.local file..." -ForegroundColor Yellow
if (Test-Path ".env.local") {
    $content = Get-Content ".env.local" -Raw
    if ($content -match "NEXT_PUBLIC_AUTH_URL=https://kvshvl.in") {
        $success += "[OK] .env.local has NEXT_PUBLIC_AUTH_URL set"
    } else {
        $warnings += "[WARN] .env.local missing NEXT_PUBLIC_AUTH_URL (may be set in Vercel dashboard)"
    }
    if ($content -match "NEXT_PUBLIC_PLATFORM_API_URL") {
        $success += "[OK] .env.local has NEXT_PUBLIC_PLATFORM_API_URL set"
    } else {
        $warnings += "[WARN] .env.local missing NEXT_PUBLIC_PLATFORM_API_URL"
    }
} else {
    $warnings += "[WARN] .env.local not found (may use Vercel dashboard for production)"
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

# Check 5: Verify unified app routes exist
Write-Host "Checking unified app routes..." -ForegroundColor Yellow
$appRoutes = @(
    "app/ask/page.tsx",
    "app/reframe/page.tsx",
    "app/sketch2bim/page.tsx"
)
foreach ($file in $appRoutes) {
    if (Test-Path $file) {
        $success += "[OK] $file exists (unified route)"
    } else {
        $errors += "[ERROR] $file not found (required for unified platform)"
    }
}

# Check 6: Verify platform API exists
Write-Host "Checking platform API..." -ForegroundColor Yellow
if (Test-Path "apps/platform-api/main.py") {
    $success += "[OK] apps/platform-api/main.py exists (unified backend)"
} else {
    $errors += "[ERROR] apps/platform-api/main.py not found (required for unified backend)"
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

