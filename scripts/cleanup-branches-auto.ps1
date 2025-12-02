# Non-interactive cleanup script for old dependabot branches
# This will automatically delete merged dependabot branches

Write-Host "Cleaning up dependabot branches (non-interactive)..." -ForegroundColor Cyan

# Switch to main branch
Write-Host "Switching to main branch..." -ForegroundColor Yellow
git checkout main 2>&1 | Out-Null
git pull origin main 2>&1 | Out-Null

# Fetch and prune
Write-Host "Fetching latest branch information..." -ForegroundColor Yellow
git fetch --prune 2>&1 | Out-Null

# List of dependabot branches to keep (active/important ones)
$keepBranches = @(
    "dependabot/npm_and_yarn/next-16.0.6"  # Active Next.js update
)

# Get all remote dependabot branches
Write-Host "`nFinding dependabot branches..." -ForegroundColor Yellow
$allDependabotBranches = git branch -r | Select-String "dependabot" | ForEach-Object { 
    $branch = $_.Line.Trim() -replace 'origin/', ''
    $branch
}

Write-Host "`nFound $($allDependabotBranches.Count) dependabot branches:" -ForegroundColor Cyan
$allDependabotBranches | ForEach-Object { Write-Host "  $_" }

# Find merged branches (excluding the ones we want to keep)
$branchesToDelete = @()
foreach ($branch in $allDependabotBranches) {
    if ($keepBranches -notcontains $branch) {
        # Check if merged
        $isMerged = git branch -r --merged origin/main | Select-String $branch
        if ($isMerged) {
            $branchesToDelete += $branch
        }
    }
}

if ($branchesToDelete.Count -gt 0) {
    Write-Host "`nBranches to delete (merged into main):" -ForegroundColor Green
    $branchesToDelete | ForEach-Object { Write-Host "  $_" }
    
    Write-Host "`nDeleting branches..." -ForegroundColor Yellow
    foreach ($branch in $branchesToDelete) {
        Write-Host "  Deleting: $branch" -ForegroundColor Yellow
        git push origin --delete $branch 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "    [OK] Deleted" -ForegroundColor Green
        } else {
            Write-Host "    [FAILED] May already be deleted" -ForegroundColor Red
        }
    }
} else {
    Write-Host "`nNo merged branches to delete." -ForegroundColor Yellow
}

# Clean up local branches
Write-Host "`nCleaning up local branches..." -ForegroundColor Yellow
$localBranches = git branch | Select-String "dependabot" | ForEach-Object { 
    $_.Line.Trim() -replace '\* ', ''
}

foreach ($branch in $localBranches) {
    if ($keepBranches -notcontains $branch) {
        $remoteExists = git ls-remote --heads origin $branch 2>&1
        if (-not $remoteExists -or $remoteExists -match "error") {
            Write-Host "  Deleting local branch: $branch" -ForegroundColor Yellow
            git branch -D $branch 2>&1 | Out-Null
        }
    }
}

Write-Host "`nCleanup complete!" -ForegroundColor Green
Write-Host "Kept active branch: dependabot/npm_and_yarn/next-16.0.6" -ForegroundColor Cyan

