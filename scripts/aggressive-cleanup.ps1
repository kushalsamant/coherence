# Aggressive cleanup - deletes unnecessary dependabot branches
# Strategy:
# 1. Keep only the latest version of each package
# 2. Delete older versions
# 3. Keep active/important branches

Write-Host "Aggressive cleanup of dependabot branches..." -ForegroundColor Cyan
Write-Host "This will delete older versions and keep only the latest." -ForegroundColor Yellow

# Switch to main
git checkout main 2>&1 | Out-Null
git pull origin main 2>&1 | Out-Null
git fetch --prune 2>&1 | Out-Null

# Get all remote dependabot branches
$allBranches = git branch -r | Select-String "dependabot" | ForEach-Object { 
    $_.Line.Trim() -replace 'origin/', ''
}

Write-Host "`nFound $($allBranches.Count) dependabot branches" -ForegroundColor Cyan

# Group branches by package name
$packageGroups = @{}
foreach ($branch in $allBranches) {
    # Extract package name (everything before the version)
    if ($branch -match 'dependabot/npm_and_yarn/(.+?)-(.+)') {
        $packageName = $matches[1]
        $version = $matches[2]
        
        if (-not $packageGroups.ContainsKey($packageName)) {
            $packageGroups[$packageName] = @()
        }
        $packageGroups[$packageName] += @{
            Branch = $branch
            Version = $version
        }
    } elseif ($branch -match 'dependabot/npm_and_yarn/(.+)') {
        # Handle branches without version (like multi-*)
        $packageName = $matches[1]
        if (-not $packageGroups.ContainsKey($packageName)) {
            $packageGroups[$packageName] = @()
        }
        $packageGroups[$packageName] += @{
            Branch = $branch
            Version = "latest"
        }
    }
}

# Determine which branches to keep and delete
$branchesToKeep = @()
$branchesToDelete = @()

foreach ($packageName in $packageGroups.Keys) {
    $branches = $packageGroups[$packageName]
    
    if ($branches.Count -eq 1) {
        # Only one branch for this package - keep it if it's important
        $branch = $branches[0].Branch
        if ($branch -eq "dependabot/npm_and_yarn/next-16.0.6") {
            $branchesToKeep += $branch
            Write-Host "  KEEP: $branch (active Next.js update)" -ForegroundColor Green
        } else {
            # Single branch - could be kept or deleted based on importance
            # For now, keep it but could be reviewed
            $branchesToKeep += $branch
        }
    } else {
        # Multiple branches - keep the latest, delete older ones
        # Sort by version (simple string comparison for most cases)
        $sorted = $branches | Sort-Object { 
            if ($_.Version -eq "latest") { "zzz" } else { $_.Version }
        } -Descending
        
        $latest = $sorted[0]
        $branchesToKeep += $latest.Branch
        Write-Host "  KEEP: $($latest.Branch) (latest version)" -ForegroundColor Green
        
        # Delete older versions
        for ($i = 1; $i -lt $sorted.Count; $i++) {
            $oldBranch = $sorted[$i].Branch
            $branchesToDelete += $oldBranch
            Write-Host "  DELETE: $oldBranch (older version)" -ForegroundColor Yellow
        }
    }
}

# Special handling for known patterns
# Delete next-16.0.3 if next-16.0.6 exists
if ($branchesToKeep -contains "dependabot/npm_and_yarn/next-16.0.6") {
    $oldNext = $allBranches | Where-Object { $_ -eq "dependabot/npm_and_yarn/next-16.0.3" }
    if ($oldNext) {
        $branchesToDelete += $oldNext
        Write-Host "  DELETE: $oldNext (superseded by next-16.0.6)" -ForegroundColor Yellow
    }
}

# Remove duplicates
$branchesToDelete = $branchesToDelete | Select-Object -Unique

Write-Host "`nSummary:" -ForegroundColor Cyan
Write-Host "  Branches to keep: $($branchesToKeep.Count)" -ForegroundColor Green
Write-Host "  Branches to delete: $($branchesToDelete.Count)" -ForegroundColor Yellow

if ($branchesToDelete.Count -gt 0) {
    Write-Host "`nDeleting branches..." -ForegroundColor Yellow
    $successCount = 0
    $failCount = 0
    
    foreach ($branch in $branchesToDelete) {
        Write-Host "  Deleting: $branch" -NoNewline
        $result = git push origin --delete $branch 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host " [OK]" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host " [FAILED - may already be deleted]" -ForegroundColor Red
            $failCount++
        }
    }
    
    Write-Host "`nDeletion complete:" -ForegroundColor Cyan
    Write-Host "  Successfully deleted: $successCount" -ForegroundColor Green
    Write-Host "  Failed/Skipped: $failCount" -ForegroundColor Yellow
} else {
    Write-Host "`nNo branches to delete." -ForegroundColor Green
}

# Clean up local branches
Write-Host "`nCleaning up local branches..." -ForegroundColor Yellow
$localBranches = git branch | Select-String "dependabot" | ForEach-Object { 
    $_.Line.Trim() -replace '\* ', ''
}

foreach ($branch in $localBranches) {
    if ($branchesToDelete -contains $branch) {
        Write-Host "  Deleting local: $branch" -ForegroundColor Yellow
        git branch -D $branch 2>&1 | Out-Null
    }
}

Write-Host "`nCleanup complete!" -ForegroundColor Green
Write-Host "Remaining branches:" -ForegroundColor Cyan
$remaining = git branch -r | Select-String "dependabot"
$remaining | ForEach-Object { Write-Host "  $($_.Line.Trim())" }

