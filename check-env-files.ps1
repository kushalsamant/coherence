# PowerShell script to check all .env files for correct OAuth configuration
# Run this from the kushalsamant.github.io directory

$ErrorActionPreference = "Continue"

Write-Host "Checking .env files for correct OAuth configuration..." -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan

# Required variables for each project
$requiredVars = @{
    ".env.production" = @(
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET"
    )
    "apps\ask\frontend\.env.production" = @(
        "NEXT_PUBLIC_AUTH_URL"
    )
    "apps\reframe\.env.production" = @(
        "NEXT_PUBLIC_AUTH_URL"
    )
    "apps\sketch2bim\frontend\.env.production" = @(
        "NEXT_PUBLIC_AUTH_URL"
    )
}

# Expected values
$expectedValues = @{
    "GOOGLE_CLIENT_ID" = "620186529337-lrr0bflcuihq2gnsko6vbrnsdv2u3ugu.apps.googleusercontent.com"
    "GOOGLE_CLIENT_SECRET" = "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"
    "NEXT_PUBLIC_AUTH_URL" = "https://kvshvl.in"
}

$allCorrect = $true

foreach ($filePath in $requiredVars.Keys) {
    Write-Host "`nChecking: $filePath" -ForegroundColor Yellow
    
    if (-not (Test-Path $filePath)) {
        Write-Host "  ❌ FILE NOT FOUND" -ForegroundColor Red
        Write-Host "     Run add-oauth-credentials.ps1 to create it" -ForegroundColor Yellow
        $allCorrect = $false
        continue
    }
    
    $content = Get-Content $filePath -Raw -ErrorAction SilentlyContinue
    if ($null -eq $content) {
        Write-Host "  ❌ FILE IS EMPTY" -ForegroundColor Red
        $allCorrect = $false
        continue
    }
    
    $fileCorrect = $true
    foreach ($varName in $requiredVars[$filePath]) {
        # Check if variable exists (with or without value)
        $pattern = "^$([regex]::Escape($varName))\s*="
        if ($content -match $pattern) {
            # Extract the value
            $match = [regex]::Match($content, "$pattern(.+)$", [System.Text.RegularExpressions.RegexOptions]::Multiline)
            if ($match.Success) {
                $value = $match.Groups[1].Value.Trim()
                
                # Check if it matches expected value (if we have one)
                if ($expectedValues.ContainsKey($varName)) {
                    if ($value -eq $expectedValues[$varName]) {
                        Write-Host "  ✅ $varName = $value" -ForegroundColor Green
                    } else {
                        Write-Host "  ⚠️  $varName = $value" -ForegroundColor Yellow
                        Write-Host "     Expected: $($expectedValues[$varName])" -ForegroundColor Yellow
                        $fileCorrect = $false
                    }
                } else {
                    Write-Host "  ✅ $varName = $value" -ForegroundColor Green
                }
            } else {
                Write-Host "  ⚠️  $varName exists but has no value" -ForegroundColor Yellow
                $fileCorrect = $false
            }
        } else {
            Write-Host "  ❌ $varName is MISSING" -ForegroundColor Red
            $fileCorrect = $false
        }
    }
    
    if (-not $fileCorrect) {
        $allCorrect = $false
    }
}

# Check for old OAuth variables that should be removed
Write-Host "`nChecking for old OAuth variables (should be removed/commented):" -ForegroundColor Yellow
$oldVars = @(
    "ASK_GOOGLE_CLIENT_ID",
    "ASK_GOOGLE_SECRET",
    "REFRAME_GOOGLE_CLIENT_ID",
    "REFRAME_GOOGLE_CLIENT_SECRET",
    "SKETCH2BIM_GOOGLE_CLIENT_ID",
    "SKETCH2BIM_GOOGLE_SECRET"
)

foreach ($filePath in @(".env.production", "apps\ask\frontend\.env.production", "apps\reframe\.env.production", "apps\sketch2bim\frontend\.env.production")) {
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw -ErrorAction SilentlyContinue
        foreach ($oldVar in $oldVars) {
            $pattern = "^$([regex]::Escape($oldVar))\s*="
            if ($content -match $pattern -and $content -notmatch "^#.*$pattern") {
                Write-Host "  ⚠️  $filePath contains $oldVar (should be removed or commented)" -ForegroundColor Yellow
                $allCorrect = $false
            }
        }
    }
}

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
if ($allCorrect) {
    Write-Host "✅ All .env files are correctly configured!" -ForegroundColor Green
} else {
    Write-Host "❌ Some .env files need updates. Run add-oauth-credentials.ps1 to fix them." -ForegroundColor Red
}

