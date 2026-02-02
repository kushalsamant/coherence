# Deployment Verification Script
# Verifies that all services are deployed and accessible

param(
    [switch]$SkipAuth,
    [switch]$Verbose
)

$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Deployment Verification Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$results = @{
    "Health Checks" = @{}
    "Environment Variables" = @{}
    "Authentication" = @{}
}

# Health check endpoints
$healthEndpoints = @{
    "Sketch2BIM Backend" = "https://sketch2bim-backend.onrender.com/health"
}

Write-Host "[1/3] Health Checks" -ForegroundColor Yellow
Write-Host ""

foreach ($service in $healthEndpoints.Keys) {
    $url = $healthEndpoints[$service]
    Write-Host "  Checking $service..." -ForegroundColor Gray -NoNewline
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 10 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            $content = $response.Content | ConvertFrom-Json
            Write-Host " ✓" -ForegroundColor Green
            if ($Verbose) {
                Write-Host "    Status: $($content.status)" -ForegroundColor Gray
                Write-Host "    Service: $($content.service)" -ForegroundColor Gray
                Write-Host "    Version: $($content.version)" -ForegroundColor Gray
            }
            $results["Health Checks"][$service] = @{
                "Status" = "Healthy"
                "Details" = $content
            }
        } else {
            Write-Host " ✗ (Status: $($response.StatusCode))" -ForegroundColor Red
            $results["Health Checks"][$service] = @{
                "Status" = "Unhealthy"
                "Error" = "HTTP $($response.StatusCode)"
            }
        }
    } catch {
        Write-Host " ✗ (Error: $($_.Exception.Message))" -ForegroundColor Red
        $results["Health Checks"][$service] = @{
            "Status" = "Unreachable"
            "Error" = $_.Exception.Message
        }
    }
}

Write-Host ""
Write-Host "[2/3] Environment Variables" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Note: Environment variable verification requires manual check in Vercel/Render dashboards" -ForegroundColor Gray
Write-Host "  Refer to DEPLOYMENT_CONFIGURATION_GUIDE.md for required variables" -ForegroundColor Gray

# Check if .env.production files exist
$envFiles = @(
    "sketch2bim.env.production"
)

foreach ($envFile in $envFiles) {
    if (Test-Path $envFile) {
        Write-Host "  ✓ $envFile exists" -ForegroundColor Green
        $results["Environment Variables"][$envFile] = "Exists"
    } else {
        Write-Host "  ✗ $envFile not found" -ForegroundColor Red
        $results["Environment Variables"][$envFile] = "Missing"
    }
}

Write-Host ""
Write-Host "[3/3] Authentication" -ForegroundColor Yellow
Write-Host ""

if ($SkipAuth) {
    Write-Host "  Skipping authentication tests (use -SkipAuth to skip)" -ForegroundColor Gray
} else {
    Write-Host "  Note: Authentication flow testing requires:" -ForegroundColor Gray
    Write-Host "    - Manual testing in browser" -ForegroundColor Gray
    Write-Host "    - Valid OAuth credentials" -ForegroundColor Gray
    Write-Host "    - Access to kvshvl.in" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Test URLs:" -ForegroundColor Gray
    Write-Host "    - Sketch2BIM: https://sketch2bim.kvshvl.in" -ForegroundColor Gray
    Write-Host "    - Main Auth: https://kvshvl.in/api/auth/signin" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allHealthy = $true
foreach ($service in $results["Health Checks"].Keys) {
    $status = $results["Health Checks"][$service]["Status"]
    $color = if ($status -eq "Healthy") { "Green" } else { "Red" }
    Write-Host "  $service : $status" -ForegroundColor $color
    if ($status -ne "Healthy") {
        $allHealthy = $false
    }
}

Write-Host ""
if ($allHealthy) {
    Write-Host "✓ All health checks passed!" -ForegroundColor Green
} else {
    Write-Host "✗ Some health checks failed. Check the errors above." -ForegroundColor Red
}

Write-Host ""
Write-Host "For detailed deployment steps, see:" -ForegroundColor Gray
Write-Host "  - DEPLOYMENT_CONFIGURATION_GUIDE.md" -ForegroundColor Gray
Write-Host "  - DEPLOYMENT_CHECKLIST.md" -ForegroundColor Gray
Write-Host ""

