# PowerShell script to remove old app-specific OAuth variables from all .env files
# Run this from the kushalsamant.github.io directory

$ErrorActionPreference = "Stop"

# Old OAuth variables to remove
$oldOAuthVars = @(
    "ASK_GOOGLE_CLIENT_ID",
    "ASK_GOOGLE_SECRET",
    "REFRAME_GOOGLE_CLIENT_ID",
    "REFRAME_GOOGLE_SECRET",
    "SKETCH2BIM_GOOGLE_CLIENT_ID",
    "SKETCH2BIM_GOOGLE_SECRET"
)

Write-Host "Removing old app-specific OAuth variables from .env files..." -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan

# Find all .env files (excluding node_modules and .git)
$envFiles = Get-ChildItem -Recurse -Filter ".env*" -File | Where-Object {
    $_.FullName -notlike "*node_modules*" -and 
    $_.FullName -notlike "*.git*" -and
    $_.Name -notlike "*.template*" -and
    $_.Name -notlike "*.example*"
}

$totalRemoved = 0

foreach ($file in $envFiles) {
    $filePath = $file.FullName
    $relativePath = $file.FullName.Replace((Get-Location).Path + "\", "")
    
    Write-Host "`nProcessing: $relativePath" -ForegroundColor Yellow
    
    if (-not (Test-Path $filePath)) {
        Write-Host "  ⚠️  File not found, skipping" -ForegroundColor Yellow
        continue
    }
    
    $content = Get-Content $filePath -Raw
    if ($null -eq $content) {
        Write-Host "  ⚠️  File is empty, skipping" -ForegroundColor Yellow
        continue
    }
    
    $originalContent = $content
    $removedCount = 0
    
    foreach ($varName in $oldOAuthVars) {
        # Pattern to match the variable line (with or without comment, with or without value)
        # Matches: VAR_NAME=value, # VAR_NAME=value, VAR_NAME=, etc.
        $pattern = "(?m)^\s*#?\s*$([regex]::Escape($varName))\s*=.*$"
        
        if ($content -match $pattern) {
            # Remove the line (including any comment lines before it if they're related)
            $content = $content -replace $pattern, ""
            $removedCount++
            Write-Host "  ✅ Removed: $varName" -ForegroundColor Green
        }
    }
    
    # Clean up multiple consecutive newlines (more than 2)
    $content = $content -replace "(\r?\n){3,}", "`r`n`r`n"
    
    # Only write if something was removed
    if ($removedCount -gt 0) {
        Set-Content -Path $filePath -Value $content -NoNewline
        Write-Host "  📝 Removed $removedCount variable(s) from this file" -ForegroundColor Cyan
        $totalRemoved += $removedCount
    } else {
        Write-Host "  ✓ No old OAuth variables found" -ForegroundColor Gray
    }
}

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "✅ Cleanup complete! Removed $totalRemoved old OAuth variable(s) from $($envFiles.Count) .env file(s)" -ForegroundColor Green

