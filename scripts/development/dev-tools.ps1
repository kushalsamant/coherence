# dev-tools.ps1
# Consolidated development utilities for the KVSHVL platform
# Usage: .\dev-tools.ps1 <command> [arguments]

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

$ErrorActionPreference = "Continue"

# ============================================================================
# Git Operations
# ============================================================================

function Sync-Repo {
    Write-Host "🔄 Syncing repository..." -ForegroundColor Cyan
    Write-Host ""
    
    $rootDir = Get-Location
    
    # Check if there are uncommitted changes
    $status = git status --porcelain
    $hasChanges = ($status -ne $null) -and ($status.Length -gt 0)
    
    # Pull changes
    Write-Host "   ⬇️  Pulling changes..." -ForegroundColor Cyan
    try {
        $pullOutput = git pull 2>&1 | Out-String
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ Pull successful" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  Pull completed with warnings/conflicts" -ForegroundColor Yellow
            Write-Host $pullOutput -ForegroundColor Gray
        }
    } catch {
        Write-Host "   ❌ Pull failed: $_" -ForegroundColor Red
    }
    
    # Push changes (only if there are commits to push)
    $currentBranch = git branch --show-current
    $localCommits = git log "origin/$currentBranch"..HEAD 2>&1 | Out-String
    $hasCommitsToPush = ($localCommits -ne $null) -and ($localCommits.Length -gt 0) -and ($localCommits -notmatch "fatal")
    
    if ($hasCommitsToPush) {
        Write-Host "   ⬆️  Pushing changes..." -ForegroundColor Cyan
        try {
            $pushOutput = git push 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) {
                Write-Host "   ✅ Push successful" -ForegroundColor Green
            } else {
                Write-Host "   ❌ Push failed: $pushOutput" -ForegroundColor Red
            }
        } catch {
            Write-Host "   ❌ Push failed: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "   ℹ️  No commits to push" -ForegroundColor Gray
    }
    
    if ($hasChanges) {
        Write-Host "   ⚠️  Warning: Uncommitted changes detected" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "✅ Repository synced!" -ForegroundColor Green
}

function Update-Repo {
    param([string]$Message = "Update repo")
    
    Write-Host "Staging all changes..." -ForegroundColor Cyan
    git add .
    
    Write-Host "Committing with message: $Message" -ForegroundColor Cyan
    git commit -m "$Message"
    
    Write-Host "Pushing to origin/main..." -ForegroundColor Cyan
    git push origin main
    
    Write-Host "✅ Repo updated!" -ForegroundColor Green
}

# ============================================================================
# Environment File Management
# ============================================================================

function Check-EnvFiles {
    Write-Host "Checking .env files for correct OAuth configuration..." -ForegroundColor Green
    Write-Host ("=" * 70) -ForegroundColor Cyan
    
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
            Write-Host "     Run '.\dev-tools.ps1 add-oauth' to create it" -ForegroundColor Yellow
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
        Write-Host "❌ Some .env files need updates. Run '.\dev-tools.ps1 add-oauth' to fix them." -ForegroundColor Red
    }
}

function Add-OAuthCredentials {
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
}

function Remove-OldOAuthVars {
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
    Write-Host ("=" * 70) -ForegroundColor Cyan
    
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
            $pattern = "(?m)^\s*#?\s*$([regex]::Escape($varName))\s*=.*$"
            
            if ($content -match $pattern) {
                # Remove the line
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
}

function Cleanup-EnvProduction {
    Write-Host "Analyzing .env files to remove duplicates..." -ForegroundColor Green
    Write-Host ("=" * 70) -ForegroundColor Cyan
    
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
        return
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
}

# ============================================================================
# Help
# ============================================================================

function Show-Help {
    Write-Host ""
    Write-Host "KVSHVL Platform Development Tools" -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\dev-tools.ps1 <command> [arguments]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Git Operations:" -ForegroundColor White
    Write-Host "    sync-repo              Pull and push repository changes"
    Write-Host "    update-repo [message]   Stage, commit, and push all changes"
    Write-Host ""
    Write-Host "  Environment Management:" -ForegroundColor White
    Write-Host "    check-env              Check .env files for correct OAuth configuration"
    Write-Host "    add-oauth              Add OAuth credentials to all app .env files"
    Write-Host "    remove-old-oauth       Remove old app-specific OAuth variables"
    Write-Host "    cleanup-env            Remove duplicate variables from .env.production"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\dev-tools.ps1 sync-repo"
    Write-Host "  .\dev-tools.ps1 update-repo 'Fixed bug in auth'"
    Write-Host "  .\dev-tools.ps1 check-env"
    Write-Host "  .\dev-tools.ps1 add-oauth"
    Write-Host ""
}

# ============================================================================
# Main Command Router
# ============================================================================

switch ($Command.ToLower()) {
    "sync-repo" { Sync-Repo }
    "update-repo" { 
        $msg = if ($Arguments.Count -gt 0) { $Arguments -join " " } else { "Update repo" }
        Update-Repo -Message $msg
    }
    "check-env" { Check-EnvFiles }
    "add-oauth" { Add-OAuthCredentials }
    "remove-old-oauth" { Remove-OldOAuthVars }
    "cleanup-env" { Cleanup-EnvProduction }
    "help" { Show-Help }
    default { 
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}

