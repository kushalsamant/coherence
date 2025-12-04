# sketch2bim-tools.ps1
# Sketch2BIM app development utilities
# Usage: .\sketch2bim-tools.ps1 <command> [arguments]

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ErrorActionPreference = "Continue"

# ============================================================================
# Environment File Management
# ============================================================================

function Reorganize-Env {
    param(
        [string]$EnvFile = "",
        [switch]$Production
    )
    
    # Determine file path
    if ([string]::IsNullOrWhiteSpace($EnvFile)) {
        # Use app-specific .env.production from workspace root
        $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
        $workspaceRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
        $EnvFile = Join-Path $workspaceRoot "sketch2bim.env.production"
        Write-Host "📋 Using sketch2bim.env.production: $EnvFile" -ForegroundColor Cyan
    } else {
        Write-Host "📋 Using specified file: $EnvFile" -ForegroundColor Cyan
    }
    
    if (-not (Test-Path $EnvFile)) {
        Write-Host "❌ Error: $EnvFile not found" -ForegroundColor Red
        Write-Host "💡 If you want to reorganize a local file, specify the path:" -ForegroundColor Yellow
        Write-Host "   .\sketch2bim-tools.ps1 reorganize-env -EnvFile `".env.production`"" -ForegroundColor Yellow
        return
    }
    
    if ($Production) {
        Reorganize-EnvProduction -FilePath $EnvFile
    } else {
        Reorganize-EnvStandard -EnvFile $EnvFile
    }
}

function Reorganize-EnvStandard {
    param([string]$EnvFile)
    
    Write-Host "📋 Reading $EnvFile..." -ForegroundColor Cyan
    
    # Read the file
    $allLines = Get-Content $EnvFile
    
    # Parse all key-value pairs
    $allVars = @{}
    $duplicateGroups = @{}
    
    foreach ($line in $allLines) {
        $trimmedLine = $line.Trim()
        
        # Skip empty lines and comments
        if ([string]::IsNullOrWhiteSpace($trimmedLine) -or $trimmedLine.StartsWith('#')) {
            continue
        }
        
        # Parse key=value pairs
        if ($trimmedLine -match "^([A-Z_][A-Z0-9_]*)\s*=\s*(.*)$") {
            $key = $matches[1]
            $rawValue = $matches[2]
            
            # Remove inline comments (everything after # that's not in quotes)
            $value = $rawValue -replace '\s*#.*$', '' -replace '^\s+|\s+$', ''
            
            # Skip if value is empty or just whitespace
            if ([string]::IsNullOrWhiteSpace($value)) {
                continue
            }
            
            if ($allVars.ContainsKey($key)) {
                # Duplicate found - track all occurrences
                if (-not $duplicateGroups.ContainsKey($key)) {
                    $duplicateGroups[$key] = @()
                    $duplicateGroups[$key] += @{ Value = $allVars[$key]; Source = "First" }
                }
                $duplicateGroups[$key] += @{ Value = $value; Source = "Duplicate" }
            } else {
                $allVars[$key] = $value
            }
        }
    }
    
    # Handle duplicates - prefer live values over test
    Write-Host "`n🔍 Checking for duplicate keys..." -ForegroundColor Cyan
    
    $keysToRemove = @{}
    foreach ($key in $duplicateGroups.Keys) {
        $occurrences = $duplicateGroups[$key]
        Write-Host "`n  Duplicate key: $key" -ForegroundColor Yellow
        $liveValue = $null
        $testValue = $null
        $otherValues = @()
        
        # Check all occurrences
        foreach ($occ in $occurrences) {
            $val = $occ.Value
            Write-Host "    - $val" -ForegroundColor Gray
            
            # Identify live vs test
            if ($val -match "sk_live_" -or $val -match "pk_live_") {
                $liveValue = $val
            } elseif ($val -match "sk_test_" -or $val -match "pk_test_") {
                $testValue = $val
            } else {
                $otherValues += $val
            }
        }
        
        # Decide which value to keep
        if ($liveValue) {
            Write-Host "    ✅ Keeping LIVE value: $liveValue" -ForegroundColor Green
            $allVars[$key] = $liveValue
            $keysToRemove[$key] = "live"
        } elseif ($otherValues.Count -gt 0) {
            # Keep the last non-test value
            $keepValue = $otherValues[-1]
            Write-Host "    ✅ Keeping value: $keepValue" -ForegroundColor Green
            $allVars[$key] = $keepValue
            $keysToRemove[$key] = "other"
        } else {
            # If only test values, still keep one (but warn)
            if ($testValue) {
                Write-Host "    ⚠️  Only test values found, keeping: $testValue" -ForegroundColor Yellow
                $allVars[$key] = $testValue
                $keysToRemove[$key] = "test"
            }
        }
    }
    
    # Categorize variables into frontend and backend
    $frontendKeys = @(
        'AUTH_URL', 'AUTH_SECRET', 'SKETCH2BIM_GOOGLE_CLIENT_ID', 'SKETCH2BIM_GOOGLE_SECRET',
        'NEXT_PUBLIC_API_URL', 'NEXT_PUBLIC_FREE_LIMIT'
    )
    
    $frontendVars = @{}
    $backendVars = @{}
    
    foreach ($key in $allVars.Keys) {
        $value = $allVars[$key]
        
        # Check if it's a known frontend key
        $isFrontend = $false
        foreach ($frontendKey in $frontendKeys) {
            if ($key -eq $frontendKey -or $key.StartsWith("NEXT_PUBLIC_") -or $key.StartsWith("AUTH_")) {
                $isFrontend = $true
                break
            }
        }
        
        if ($isFrontend) {
            $frontendVars[$key] = $value
        } else {
            $backendVars[$key] = $value
        }
    }
    
    Write-Host "`n📊 Summary:" -ForegroundColor Cyan
    Write-Host "   Frontend variables: $($frontendVars.Count)" -ForegroundColor Green
    Write-Host "   Backend variables: $($backendVars.Count)" -ForegroundColor Green
    Write-Host "   Duplicates resolved: $($duplicateGroups.Count)" -ForegroundColor $(if ($duplicateGroups.Count -gt 0) { "Yellow" } else { "Green" })
    
    # Build the reorganized content
    $output = @()
    
    # Frontend section
    $output += "=============================================================================="
    $output += "# FRONTEND VARIABLES (Copy to Vercel Environment Variables)"
    $output += "# Deploy to: https://vercel.com/kvshvl/sketch2bim/settings/environment-variables"
    $output += "# Instructions: Add each variable individually or use `"Add from .env`""
    $output += "=============================================================================="
    $output += ""
    
    # Sort frontend vars alphabetically
    $frontendVars.GetEnumerator() | Sort-Object Name | ForEach-Object {
        $output += "$($_.Key)=$($_.Value)"
    }
    $output += ""
    $output += "# End of Frontend Variables"
    $output += "=============================================================================="
    $output += ""
    $output += ""
    
    # Backend section
    $output += "=============================================================================="
    $output += "# BACKEND VARIABLES (Copy to Render Environment Variables)"
    $output += "# Deploy to: https://dashboard.render.com/web/srv-xxx/env"
    $output += "# Instructions: Add each variable using `"Add Environment Variable`" button"
    $output += "=============================================================================="
    $output += ""
    
    # Sort backend vars alphabetically
    $backendVars.GetEnumerator() | Sort-Object Name | ForEach-Object {
        $output += "$($_.Key)=$($_.Value)"
    }
    $output += ""
    $output += "# End of Backend Variables"
    $output += "=============================================================================="
    
    # Create backup
    $backupFile = "$EnvFile.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $EnvFile $backupFile
    Write-Host "`n📋 Created backup: $backupFile" -ForegroundColor Cyan
    
    # Write the reorganized file
    $output -join "`r`n" | Set-Content -Path $EnvFile -NoNewline
    
    Write-Host "`n✅ Successfully reorganized $EnvFile!" -ForegroundColor Green
    Write-Host "   - Organized into Frontend and Backend sections" -ForegroundColor Cyan
    Write-Host "   - Removed unnecessary comments" -ForegroundColor Cyan
    Write-Host "   - Sorted variables alphabetically" -ForegroundColor Cyan
    Write-Host "   - Resolved duplicate keys (preferred live values)" -ForegroundColor Cyan
    Write-Host "`n📋 Backup saved to: $backupFile" -ForegroundColor Cyan
}

function Reorganize-EnvProduction {
    param([string]$FilePath)
    
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
        # Razorpay Payment Gateway
        'RAZORPAY_KEY_ID',
        'RAZORPAY_KEY_SECRET',
        'RAZORPAY_WEBHOOK_SECRET',
        # Razorpay Pricing (one-time payments)
        'RAZORPAY_WEEK_AMOUNT',
        'RAZORPAY_MONTH_AMOUNT',
        'RAZORPAY_YEAR_AMOUNT',
        # Razorpay Plan IDs (subscriptions)
        'RAZORPAY_PLAN_WEEKLY',
        'RAZORPAY_PLAN_MONTHLY',
        'RAZORPAY_PLAN_YEARLY',
        # Alternative Razorpay key names (LIVE_KEY_ID, LIVE_KEY_SECRET)
        'LIVE_KEY_ID',
        'LIVE_KEY_SECRET',
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
}

# ============================================================================
# Help
# ============================================================================

function Show-Help {
    Write-Host ""
    Write-Host "Sketch2BIM App Development Tools" -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\sketch2bim-tools.ps1 <command> [arguments]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Environment Management:" -ForegroundColor White
    Write-Host "    reorganize-env [file]     Reorganize .env file into Frontend/Backend sections"
    Write-Host "    reorganize-env-prod [file] Reorganize with production-specific logic"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\sketch2bim-tools.ps1 reorganize-env"
    Write-Host "  .\sketch2bim-tools.ps1 reorganize-env -EnvFile `".env.production`""
    Write-Host "  .\sketch2bim-tools.ps1 reorganize-env-prod"
    Write-Host ""
}

# ============================================================================
# Main Command Router
# ============================================================================

switch ($Command.ToLower()) {
    "reorganize-env" { 
        $file = if ($Arguments.Count -gt 0) { $Arguments[0] } else { "" }
        Reorganize-Env -EnvFile $file
    }
    "reorganize-env-prod" { 
        $file = if ($Arguments.Count -gt 0) { $Arguments[0] } else { "" }
        Reorganize-Env -EnvFile $file -Production
    }
    "help" { Show-Help }
    default { 
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}

