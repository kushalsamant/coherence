# PowerShell script to add OAuth credentials to each app's .env.production file
# Run this from the kushalsamant.github.io directory
# Note: App-specific .env.production files are at the repository root

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

# 1. ASK - needs OAuth credentials and AUTH_URL
$askEnv = "ask.env.production"
Write-Host "`n1. Updating ASK ($askEnv)..." -ForegroundColor Yellow
Add-Or-Update-EnvVar -FilePath $askEnv -Key "ASK_GOOGLE_CLIENT_ID" -Value $GOOGLE_CLIENT_ID -Comment "Google OAuth Client ID"
Add-Or-Update-EnvVar -FilePath $askEnv -Key "ASK_GOOGLE_SECRET" -Value $GOOGLE_CLIENT_SECRET -Comment "Google OAuth Client Secret"
Add-Or-Update-EnvVar -FilePath $askEnv -Key "ASK_AUTH_URL" -Value $AUTH_URL -Comment "Centralized authentication URL"

# 2. Reframe - needs OAuth credentials and AUTH_URL
$reframeEnv = "reframe.env.production"
Write-Host "`n2. Updating Reframe ($reframeEnv)..." -ForegroundColor Yellow
Add-Or-Update-EnvVar -FilePath $reframeEnv -Key "REFRAME_GOOGLE_CLIENT_ID" -Value $GOOGLE_CLIENT_ID -Comment "Google OAuth Client ID"
Add-Or-Update-EnvVar -FilePath $reframeEnv -Key "REFRAME_GOOGLE_CLIENT_SECRET" -Value $GOOGLE_CLIENT_SECRET -Comment "Google OAuth Client Secret"
Add-Or-Update-EnvVar -FilePath $reframeEnv -Key "REFRAME_AUTH_URL" -Value $AUTH_URL -Comment "Centralized authentication URL"

# 3. Sketch2BIM - needs OAuth credentials and AUTH_URL
$sketch2bimEnv = "sketch2bim.env.production"
Write-Host "`n3. Updating Sketch2BIM ($sketch2bimEnv)..." -ForegroundColor Yellow
Add-Or-Update-EnvVar -FilePath $sketch2bimEnv -Key "SKETCH2BIM_GOOGLE_CLIENT_ID" -Value $GOOGLE_CLIENT_ID -Comment "Google OAuth Client ID"
Add-Or-Update-EnvVar -FilePath $sketch2bimEnv -Key "SKETCH2BIM_GOOGLE_SECRET" -Value $GOOGLE_CLIENT_SECRET -Comment "Google OAuth Client Secret"
Add-Or-Update-EnvVar -FilePath $sketch2bimEnv -Key "SKETCH2BIM_AUTH_URL" -Value $AUTH_URL -Comment "Centralized authentication URL"

Write-Host "`n✅ OAuth credentials added to all app .env.production files!" -ForegroundColor Green
Write-Host "`nNote: These files may be gitignored. Make sure to add the same variables to:" -ForegroundColor Yellow
Write-Host "  - Vercel environment variables (for frontend projects)" -ForegroundColor Yellow
Write-Host "  - Render environment variables (for backend projects)" -ForegroundColor Yellow

