# Comprehensive Platform Test Script
# Tests all critical functionality

Write-Host "================================" -ForegroundColor Cyan
Write-Host "KVSHVL Platform - Comprehensive Test" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://localhost:3000"
$testsPassed = 0
$testsFailed = 0

function Test-Endpoint {
    param([string]$url, [string]$description)
    
    Write-Host "Testing: $description" -NoNewline
    try {
        $response = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 10 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host " ✓ PASS" -ForegroundColor Green
            $script:testsPassed++
            return $true
        } else {
            Write-Host " ✗ FAIL (Status: $($response.StatusCode))" -ForegroundColor Red
            $script:testsFailed++
            return $false
        }
    } catch {
        Write-Host " ✗ FAIL (Error: $($_.Exception.Message))" -ForegroundColor Red
        $script:testsFailed++
        return $false
    }
}

# Test 1: Homepage
Write-Host "`n1. HOMEPAGE TESTS" -ForegroundColor Yellow
Test-Endpoint "$baseUrl" "Homepage loads"

# Test 2: Authentication Endpoints
Write-Host "`n2. AUTHENTICATION TESTS" -ForegroundColor Yellow
Test-Endpoint "$baseUrl/api/auth/session" "Session endpoint"
Test-Endpoint "$baseUrl/api/auth/signin" "Sign-in page"
Test-Endpoint "$baseUrl/account" "Account page"

# Test 3: Application Pages
Write-Host "`n3. APPLICATION PAGES" -ForegroundColor Yellow
Test-Endpoint "$baseUrl/ask" "ASK application"
Test-Endpoint "$baseUrl/reframe" "Reframe application"
Test-Endpoint "$baseUrl/sketch2bim" "Sketch2BIM application"

# Test 4: Subscription Pages
Write-Host "`n4. SUBSCRIPTION TESTS" -ForegroundColor Yellow
Test-Endpoint "$baseUrl/subscribe" "Subscribe page"

# Test 5: Static Pages
Write-Host "`n5. STATIC PAGES" -ForegroundColor Yellow
Test-Endpoint "$baseUrl/history" "History page"
Test-Endpoint "$baseUrl/projects" "Projects page"
Test-Endpoint "$baseUrl/links" "Links page"
Test-Endpoint "$baseUrl/getintouch" "Get in Touch page"
Test-Endpoint "$baseUrl/privacypolicy" "Privacy Policy"
Test-Endpoint "$baseUrl/termsofservice" "Terms of Service"
Test-Endpoint "$baseUrl/cancellationrefund" "Cancellation & Refund"

# Test 6: Build Check
Write-Host "`n6. BUILD VERIFICATION" -ForegroundColor Yellow
Write-Host "Checking build files..." -NoNewline
if (Test-Path ".next") {
    Write-Host " ✓ PASS" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host " ✗ FAIL" -ForegroundColor Red
    $testsFailed++
}

# Test 7: Environment Variables
Write-Host "`n7. ENVIRONMENT CHECKS" -ForegroundColor Yellow
Write-Host "Checking .env.local..." -NoNewline
if (Test-Path ".env.local") {
    $envContent = Get-Content ".env.local" -Raw
    $requiredVars = @("NEXTAUTH_URL", "AUTH_SECRET", "GOOGLE_CLIENT_ID", "RAZORPAY_KEY_ID")
    $allPresent = $true
    foreach ($var in $requiredVars) {
        if ($envContent -notmatch $var) {
            $allPresent = $false
            break
        }
    }
    if ($allPresent) {
        Write-Host " ✓ PASS" -ForegroundColor Green
        $testsPassed++
    } else {
        Write-Host " ✗ FAIL (Missing variables)" -ForegroundColor Red
        $testsFailed++
    }
} else {
    Write-Host " ✗ FAIL (File not found)" -ForegroundColor Red
    $testsFailed++
}

# Test 8: Package Check
Write-Host "`n8. DEPENDENCY CHECKS" -ForegroundColor Yellow
Write-Host "Checking node_modules..." -NoNewline
if (Test-Path "node_modules") {
    Write-Host " ✓ PASS" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host " ✗ FAIL" -ForegroundColor Red
    $testsFailed++
}

Write-Host "Checking critical packages..." -NoNewline
$criticalPackages = @("next", "react", "next-auth", "razorpay")
$allInstalled = $true
foreach ($pkg in $criticalPackages) {
    if (-not (Test-Path "node_modules/$pkg")) {
        $allInstalled = $false
        break
    }
}
if ($allInstalled) {
    Write-Host " ✓ PASS" -ForegroundColor Green
    $testsPassed++
} else {
    Write-Host " ✗ FAIL" -ForegroundColor Red
    $testsFailed++
}

# Summary
Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Passed: $testsPassed" -ForegroundColor Green
Write-Host "Failed: $testsFailed" -ForegroundColor Red
$total = $testsPassed + $testsFailed
$percentage = [math]::Round(($testsPassed / $total) * 100, 2)
Write-Host "Success Rate: $percentage%" -ForegroundColor $(if ($percentage -ge 90) { "Green" } elseif ($percentage -ge 70) { "Yellow" } else { "Red" })

if ($testsFailed -eq 0) {
    Write-Host "`n✓ ALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "Platform is fully functional and ready for deployment." -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n✗ SOME TESTS FAILED" -ForegroundColor Red
    Write-Host "Please review errors above." -ForegroundColor Red
    exit 1
}

