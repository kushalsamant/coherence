# PowerShell script to reorganize .env.production into Frontend and Backend sections
# Handles duplicate keys carefully - checks values before removing
#
# Usage:
#   .\reorganize-env-production.ps1                           # Uses sketch2bim.env.production
#   .\reorganize-env-production.ps1 -FilePath "custom.env"   # Uses custom file
#
# The app-specific .env.production is located at: ../../sketch2bim.env.production

param(
    [string]$FilePath = ""  # Default: use sketch2bim.env.production
)

# Determine file path
if ([string]::IsNullOrWhiteSpace($FilePath)) {
    # Use app-specific .env.production from workspace root
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $workspaceRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
    $FilePath = Join-Path $workspaceRoot "sketch2bim.env.production"
    Write-Host "[INFO] Using sketch2bim.env.production: $FilePath" -ForegroundColor Cyan
} else {
    Write-Host "[INFO] Using specified file: $FilePath" -ForegroundColor Cyan
}

if (-not (Test-Path $FilePath)) {
    Write-Host "[ERROR] $FilePath not found" -ForegroundColor Red
    Write-Host "[INFO] If you want to reorganize a local file, specify the path:" -ForegroundColor Yellow
    Write-Host "       .\reorganize-env-production.ps1 -FilePath `".env.production`"" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n[INFO] Reading and analyzing $FilePath..." -ForegroundColor Cyan

# Read the file
$lines = Get-Content $FilePath

# Create backup
$backupFile = "$FilePath.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $FilePath $backupFile
Write-Host "[INFO] Created backup: $backupFile" -ForegroundColor Cyan

# Parse variables
$variables = @{}
$currentSection = ""

foreach ($line in $lines) {
    $trimmed = $line.Trim()
    
    # Skip empty lines and comments for now (we'll handle comments later)
    if ([string]::IsNullOrWhiteSpace($trimmed) -or $trimmed.StartsWith('#')) {
        continue
    }
    
        # Check if it's a key=value pair
        if ($trimmed -match '^([^#=]+?)\s*=\s*(.*)$') {
            $key = $matches[1].Trim()
            $rawValue = $matches[2].Trim()
            
            # Remove inline comments (everything after #)
            $value = $rawValue -replace '\s*#.*$', ''
            $value = $value.Trim()
            
            # Remove quotes if present
            if ($value -match "^[""'](.*)[""']$") {
                $value = $matches[1]
            }
            
            # Skip if value is empty or just comment
            if ([string]::IsNullOrWhiteSpace($value) -or $value -match '^#') {
                continue
            }
        
        # Handle duplicate keys - check if this is test or live
        if ($variables.ContainsKey($key)) {
            $existingValue = $variables[$key]
            
            # If one is test and one is live, prefer live for production
            $isTest = ($key -like '*TEST*' -or $key -like '*test*' -or 
                      $value -like '*sk_test*' -or $value -like '*pk_test*' -or 
                      $value -like '*rzp_test*')
            $existingIsTest = ($existingValue -like '*sk_test*' -or $existingValue -like '*pk_test*' -or 
                              $existingValue -like '*rzp_test*')
            
            if ($isTest -and -not $existingIsTest) {
                Write-Host "[WARN] Keeping LIVE value for $key (skipping test: $value)" -ForegroundColor Yellow
                continue
            } elseif (-not $isTest -and $existingIsTest) {
                Write-Host "[INFO] Replacing test value with LIVE value for $key" -ForegroundColor Yellow
                $variables[$key] = $value
                continue
            } elseif ($existingValue -eq $value) {
                Write-Host "[INFO] Duplicate key $key with same value, keeping one" -ForegroundColor Gray
                continue
            } else {
                Write-Host "[WARN] Duplicate key $key with different values:" -ForegroundColor Yellow
                Write-Host "   Existing: $existingValue" -ForegroundColor Gray
                Write-Host "   New:      $value" -ForegroundColor Gray
                Write-Host "   Keeping existing value" -ForegroundColor Gray
                continue
            }
        }
        
        $variables[$key] = $value
    }
}

Write-Host "`n[SUCCESS] Parsed $($variables.Count) unique variables" -ForegroundColor Green

# Define Frontend and Backend variables
$frontendKeys = @(
    'AUTH_URL',
    'NEXT_PUBLIC_API_URL',
    'AUTH_SECRET',
    'NEXTAUTH_SECRET',
    'SKETCH2BIM_GOOGLE_CLIENT_ID',
    'SKETCH2BIM_GOOGLE_SECRET',
    'NEXT_PUBLIC_FREE_LIMIT'
)

$backendKeys = @(
    'DATABASE_URL',
    'DATABASE_URL_OVERRIDE',
    'DATABASE_PASSWORD_OVERRIDE',
    'REDIS_URL',
    'UPSTASH_REDIS_REST_URL',
    'UPSTASH_REDIS_REST_TOKEN',
    'SECRET_KEY',
    'NEXTAUTH_SECRET',
    'JWT_ALGORITHM',
    'JWT_EXPIRATION_HOURS',
    # Razorpay Payment Gateway (replaced Stripe)
    'RAZORPAY_KEY_ID',
    'RAZORPAY_KEY_SECRET',
    'RAZORPAY_WEBHOOK_SECRET',
    # Razorpay Pricing (one-time payments)
    'RAZORPAY_WEEK_AMOUNT',
    'RAZORPAY_MONTH_AMOUNT',
    'RAZORPAY_YEAR_AMOUNT',
    # Razorpay Plan IDs (subscriptions)
    'RAZORPAY_PLAN_WEEK',
    'RAZORPAY_PLAN_MONTH',
    'RAZORPAY_PLAN_YEAR',
    # Alternative Razorpay key names (LIVE_KEY_ID, LIVE_KEY_SECRET)
    'LIVE_KEY_ID',
    'LIVE_KEY_SECRET',
    # Legacy Stripe (kept for backward compatibility detection)
    'STRIPE_SECRET_KEY',
    'STRIPE_PUBLISHABLE_KEY',
    'STRIPE_WEBHOOK_SECRET',
    'STRIPE_PRICE_PRO',
    'STRIPE_PRICE_STUDIO',
    'STRIPE_PRICE_SINGLE',
    # Storage
    'BUNNY_STORAGE_ZONE',
    'BUNNY_ACCESS_KEY',
    'BUNNY_CDN_HOSTNAME',
    'BUNNY_REGION',
    'BUNNY_SIGNED_URL_KEY',
    'BUNNY_SIGNED_URL_EXPIRY',
    # Application
    'ALLOWED_ORIGINS',
    'APP_ENV',
    'APP_NAME',
    'DEBUG',
    'FRONTEND_URL',
    'LOG_LEVEL',
    'JSON_LOGGING',
    'SKETCH_READER_TYPE',
    # Deprecated (but kept for detection)
    'BLENDER_PATH',
    'ML_AGENT_ENABLED',
    'ML_AGENT_MAX_RETRIES',
    'ML_AGENT_PREPROCESSING_THRESHOLD',
    'ML_AGENT_DETECTION_THRESHOLD',
    'ML_AGENT_POST_IFC_THRESHOLD',
    'ML_AGENT_USE_ML_CLASSIFIER',
    # Rate Limiting
    'RATE_LIMIT_PER_MINUTE',
    'RATE_LIMIT_PER_HOUR',
    # File Upload
    'MAX_UPLOAD_SIZE_MB',
    'ALLOWED_EXTENSIONS',
    # Free Tier
    'FREE_CREDITS_LIMIT',
    # IDS Validation
    'IDS_FILE_PATH'
)

# Separate variables
$frontendVars = @{}
$backendVars = @{}
$otherVars = @{}

foreach ($key in $variables.Keys) {
    $normalizedKey = $key.ToUpper()
    
    if ($frontendKeys -contains $normalizedKey) {
        $frontendVars[$key] = $variables[$key]
    } elseif ($backendKeys -contains $normalizedKey) {
        $backendVars[$key] = $variables[$key]
    } else {
        $otherVars[$key] = $variables[$key]
    }
}

Write-Host "   Frontend: $($frontendVars.Count) variables" -ForegroundColor Cyan
Write-Host "   Backend:  $($backendVars.Count) variables" -ForegroundColor Cyan
if ($otherVars.Count -gt 0) {
    Write-Host "   Other:    $($otherVars.Count) variables" -ForegroundColor Yellow
}

# Build new file content
$newContent = @()

# Frontend section
$newContent += "# ============================================================================="
$newContent += "# FRONTEND VARIABLES (Copy to Vercel Environment Variables)"
$newContent += "# ============================================================================="
$newContent += "# Deploy to: https://vercel.com/kvshvl/sketch2bim/settings/environment-variables"
$newContent += ""

# Sort frontend variables alphabetically
$frontendVars.GetEnumerator() | Sort-Object Name | ForEach-Object {
    $newContent += "$($_.Name)=$($_.Value)"
}

$newContent += ""
$newContent += "# End of Frontend Variables"
$newContent += "# ============================================================================="
$newContent += ""
$newContent += ""

# Backend section
$newContent += "# ============================================================================="
$newContent += "# BACKEND VARIABLES (Copy to Render Environment Variables)"
$newContent += "# ============================================================================="
$newContent += "# Deploy to: https://dashboard.render.com/web/srv-xxx/env"
$newContent += ""

# Sort backend variables alphabetically
$backendVars.GetEnumerator() | Sort-Object Name | ForEach-Object {
    $newContent += "$($_.Name)=$($_.Value)"
}

# Add other variables if any
if ($otherVars.Count -gt 0) {
    $newContent += ""
    $newContent += "# Other variables"
    $otherVars.GetEnumerator() | Sort-Object Name | ForEach-Object {
        $newContent += "$($_.Name)=$($_.Value)"
    }
}

$newContent += ""
$newContent += "# End of Backend Variables"
$newContent += "# ============================================================================="

# Write the new file
$newContent | Set-Content -Path $FilePath -Encoding UTF8

Write-Host "`n[SUCCESS] Successfully reorganized $FilePath!" -ForegroundColor Green
Write-Host "   Frontend variables: $($frontendVars.Count)" -ForegroundColor Cyan
Write-Host "   Backend variables:  $($backendVars.Count)" -ForegroundColor Cyan
if ($otherVars.Count -gt 0) {
    Write-Host "   Other variables:    $($otherVars.Count)" -ForegroundColor Yellow
    Write-Host "`n[WARN] Warning: Found $($otherVars.Count) variables not categorized:" -ForegroundColor Yellow
    $otherVars.Keys | ForEach-Object {
        Write-Host "      $_" -ForegroundColor Gray
    }
}
Write-Host "`n[INFO] Backup saved to: $backupFile" -ForegroundColor Cyan

