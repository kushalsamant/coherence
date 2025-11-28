# PowerShell script to add shared OAuth credentials to each project's .env.production file
# Run this from the kushalsamant.github.io directory

$ErrorActionPreference = "Stop"

# OAuth credentials
$GOOGLE_CLIENT_ID = "620186529337-lrr0bflcuihq2gnsko6vbrnsdv2u3ugu.apps.googleusercontent.com"
$GOOGLE_CLIENT_SECRET = "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"
$AUTH_URL = "https://kvshvl.in"

Write-Host "Adding OAuth credentials to project .env.production files..." -ForegroundColor Green

# Function to add or update environment variable in .env file
function Add-Or-Update-EnvVar {
    param(
        [string]$FilePath,
        [string]$Key,
        [string]$Value,
        [string]$Comment = ""
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "Creating $FilePath..." -ForegroundColor Yellow
        New-Item -Path $FilePath -ItemType File -Force | Out-Null
    }
    
    $content = Get-Content $FilePath -Raw -ErrorAction SilentlyContinue
    if ($null -eq $content) {
        $content = ""
    }
    
    # Check if key already exists
    $pattern = "^$([regex]::Escape($Key))\s*="
    if ($content -match $pattern) {
        # Update existing value
        $content = $content -replace "$pattern.*", "$Key=$Value"
        Write-Host "  Updated $Key in $FilePath" -ForegroundColor Cyan
    } else {
        # Add new key-value pair
        $newLine = if ($Comment) { "# $Comment`n$Key=$Value" } else { "$Key=$Value" }
        if ($content -and -not $content.EndsWith("`n")) {
            $content += "`n"
        }
        $content += "$newLine`n"
        Write-Host "  Added $Key to $FilePath" -ForegroundColor Green
    }
    
    Set-Content -Path $FilePath -Value $content -NoNewline
}

# 1. Main site (kushalsamant.github.io) - needs OAuth credentials
$mainSiteEnv = ".env.production"
Write-Host "`n1. Updating main site ($mainSiteEnv)..." -ForegroundColor Yellow
Add-Or-Update-EnvVar -FilePath $mainSiteEnv -Key "GOOGLE_CLIENT_ID" -Value $GOOGLE_CLIENT_ID -Comment "Shared Google OAuth Client ID (used by all apps via kvshvl.in)"
Add-Or-Update-EnvVar -FilePath $mainSiteEnv -Key "GOOGLE_CLIENT_SECRET" -Value $GOOGLE_CLIENT_SECRET -Comment "Shared Google OAuth Client Secret (used by all apps via kvshvl.in)"

# 2. ASK Frontend - needs AUTH_URL
$askFrontendEnv = "apps\ask\frontend\.env.production"
Write-Host "`n2. Updating ASK frontend ($askFrontendEnv)..." -ForegroundColor Yellow
Add-Or-Update-EnvVar -FilePath $askFrontendEnv -Key "NEXT_PUBLIC_AUTH_URL" -Value $AUTH_URL -Comment "Centralized authentication URL"

# 3. Reframe - needs AUTH_URL
$reframeEnv = "apps\reframe\.env.production"
Write-Host "`n3. Updating Reframe ($reframeEnv)..." -ForegroundColor Yellow
Add-Or-Update-EnvVar -FilePath $reframeEnv -Key "NEXT_PUBLIC_AUTH_URL" -Value $AUTH_URL -Comment "Centralized authentication URL"

# 4. Sketch2BIM Frontend - needs AUTH_URL
$sketch2bimFrontendEnv = "apps\sketch2bim\frontend\.env.production"
Write-Host "`n4. Updating Sketch2BIM frontend ($sketch2bimFrontendEnv)..." -ForegroundColor Yellow
Add-Or-Update-EnvVar -FilePath $sketch2bimFrontendEnv -Key "NEXT_PUBLIC_AUTH_URL" -Value $AUTH_URL -Comment "Centralized authentication URL"

Write-Host "`n✅ OAuth credentials added to all project .env.production files!" -ForegroundColor Green
Write-Host "`nNote: These files may be gitignored. Make sure to add the same variables to:" -ForegroundColor Yellow
Write-Host "  - Vercel environment variables (for frontend projects)" -ForegroundColor Yellow
Write-Host "  - Render environment variables (for backend projects)" -ForegroundColor Yellow

