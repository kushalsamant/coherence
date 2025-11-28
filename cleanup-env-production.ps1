# PowerShell script to remove duplicate variables from .env.production
# Removes variables that already exist in ask.env.production, reframe.env.production, and sketch2bim.env.production

$ErrorActionPreference = "Stop"

Write-Host "Analyzing .env files to remove duplicates..." -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan

# Read app-specific .env files
$askEnv = @{}
$reframeEnv = @{}
$sketch2bimEnv = @{}

Write-Host "`nReading app-specific .env files..." -ForegroundColor Yellow

if (Test-Path "ask.env.production") {
    Get-Content "ask.env.production" | ForEach-Object {
        if ($_ -match '^\s*([A-Z_][A-Z0-9_]*)\s*=') {
            $key = $matches[1]
            $askEnv[$key] = $true
        }
    }
    Write-Host "  ✅ ask.env.production: Found $($askEnv.Count) variables" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  ask.env.production not found" -ForegroundColor Yellow
}

if (Test-Path "reframe.env.production") {
    Get-Content "reframe.env.production" | ForEach-Object {
        if ($_ -match '^\s*([A-Z_][A-Z0-9_]*)\s*=') {
            $key = $matches[1]
            $reframeEnv[$key] = $true
        }
    }
    Write-Host "  ✅ reframe.env.production: Found $($reframeEnv.Count) variables" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  reframe.env.production not found" -ForegroundColor Yellow
}

if (Test-Path "sketch2bim.env.production") {
    Get-Content "sketch2bim.env.production" | ForEach-Object {
        if ($_ -match '^\s*([A-Z_][A-Z0-9_]*)\s*=') {
            $key = $matches[1]
            $sketch2bimEnv[$key] = $true
        }
    }
    Write-Host "  ✅ sketch2bim.env.production: Found $($sketch2bimEnv.Count) variables" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  sketch2bim.env.production not found" -ForegroundColor Yellow
}

# Combine all app-specific variables
$allAppVars = @{}
foreach ($key in $askEnv.Keys) { $allAppVars[$key] = $true }
foreach ($key in $reframeEnv.Keys) { $allAppVars[$key] = $true }
foreach ($key in $sketch2bimEnv.Keys) { $allAppVars[$key] = $true }

Write-Host "`nTotal unique variables in app-specific files: $($allAppVars.Count)" -ForegroundColor Cyan

# Variables that should be KEPT in .env.production (needed by root/main site)
$keepVars = @(
    "GOOGLE_CLIENT_ID",
    "GOOGLE_CLIENT_SECRET",
    "NEXTAUTH_SECRET",
    "AUTH_SECRET"
)

Write-Host "`nVariables to KEEP in .env.production (needed by main site):" -ForegroundColor Yellow
foreach ($var in $keepVars) {
    Write-Host "  - $var" -ForegroundColor White
}

# Read .env.production (or .env copy.production)
$envProdFile = if (Test-Path ".env.production") { ".env.production" } elseif (Test-Path ".env copy.production") { ".env copy.production" } else { $null }

if (-not $envProdFile) {
    Write-Host "`n❌ .env.production file not found!" -ForegroundColor Red
    exit 1
}

Write-Host "`nReading $envProdFile..." -ForegroundColor Yellow
$content = Get-Content $envProdFile -Raw
$lines = Get-Content $envProdFile
$originalLineCount = $lines.Count

Write-Host "  Original line count: $originalLineCount" -ForegroundColor Gray

# Process lines and remove duplicates
$newLines = @()
$removedCount = 0
$keptCount = 0

foreach ($line in $lines) {
    $trimmedLine = $line.Trim()
    
    # Skip empty lines and comments
    if ([string]::IsNullOrWhiteSpace($trimmedLine) -or $trimmedLine.StartsWith("#")) {
        $newLines += $line
        continue
    }
    
    # Check if this is a variable assignment
    if ($trimmedLine -match '^\s*([A-Z_][A-Z0-9_]*)\s*=') {
        $varName = $matches[1]
        
        # Keep if it's in the keep list (needed by main site)
        if ($keepVars -contains $varName) {
            $newLines += $line
            $keptCount++
            Write-Host "  ✅ KEPT: $varName (needed by main site)" -ForegroundColor Green
            continue
        }
        
        # Remove if it exists in any app-specific file
        if ($allAppVars.ContainsKey($varName)) {
            Write-Host "  ❌ REMOVED: $varName (exists in app-specific file)" -ForegroundColor Red
            $removedCount++
            continue
        }
        
        # Keep if it's not in app-specific files (might be shared or legacy)
        $newLines += $line
        $keptCount++
    } else {
        # Keep non-variable lines (comments, etc.)
        $newLines += $line
    }
}

# Clean up multiple consecutive newlines
$newContent = ($newLines -join "`r`n") -replace "(\r?\n){3,}", "`r`n`r`n"

# Write back to file
Set-Content -Path $envProdFile -Value $newContent -NoNewline

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host "  Original lines: $originalLineCount" -ForegroundColor Gray
Write-Host "  Variables kept: $keptCount" -ForegroundColor Green
Write-Host "  Variables removed: $removedCount" -ForegroundColor Yellow
Write-Host "  New line count: $($newLines.Count)" -ForegroundColor Gray

Write-Host "`n📝 Updated file: $envProdFile" -ForegroundColor Cyan

