# PowerShell script to reorganize .env.production into frontend and backend sections
# Handles duplicate keys carefully (test vs live values)
#
# Usage:
#   .\reorganize-env.ps1                         # Uses sketch2bim.env.production
#   .\reorganize-env.ps1 -EnvFile "custom.env"  # Uses custom file
#
# The app-specific .env.production is located at: ../../sketch2bim.env.production

param(
    [string]$EnvFile = ""  # Default: use sketch2bim.env.production
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
    Write-Host "   .\reorganize-env.ps1 -EnvFile `".env.production`"" -ForegroundColor Yellow
    exit 1
}

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
        # Simple approach: split on # and take first part, trim spaces
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
