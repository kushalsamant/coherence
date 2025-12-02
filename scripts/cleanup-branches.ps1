# Cleanup script for old dependabot branches
# This script will:
# 1. Delete local dependabot branches that have been merged
# 2. Delete remote dependabot branches that are stale (older than 30 days or merged)

Write-Host "Cleaning up dependabot branches..." -ForegroundColor Cyan

# Switch to main branch first
Write-Host "`nSwitching to main branch..." -ForegroundColor Yellow
git checkout main
git pull origin main

# Get all remote dependabot branches
Write-Host "`nFetching latest branch information..." -ForegroundColor Yellow
git fetch --prune

# List all dependabot branches
Write-Host "`nDependabot branches found:" -ForegroundColor Cyan
$dependabotBranches = git branch -r | Select-String "dependabot" | ForEach-Object { $_.Line.Trim() }
$dependabotBranches | ForEach-Object { Write-Host "  $_" }

# Check which branches are merged into main
Write-Host "`nChecking which branches are merged into main..." -ForegroundColor Yellow
$mergedBranches = git branch -r --merged origin/main | Select-String "dependabot"

if ($mergedBranches) {
    Write-Host "`nMerged dependabot branches (safe to delete):" -ForegroundColor Green
    $mergedBranches | ForEach-Object { Write-Host "  $_" }
    
    # Ask for confirmation
    $confirm = Read-Host "`nDelete these merged branches? (y/n)"
    if ($confirm -eq 'y') {
        $mergedBranches | ForEach-Object {
            $branchName = $_.Line.Trim() -replace 'origin/', ''
            Write-Host "Deleting remote branch: $branchName" -ForegroundColor Yellow
            git push origin --delete $branchName
        }
    }
} else {
    Write-Host "`nNo merged dependabot branches found." -ForegroundColor Yellow
}

# Clean up local branches
Write-Host "`nCleaning up local branches..." -ForegroundColor Yellow
$localDependabotBranches = git branch | Select-String "dependabot" | ForEach-Object { $_.Line.Trim() -replace '\* ', '' }

if ($localDependabotBranches) {
    Write-Host "Local dependabot branches:" -ForegroundColor Cyan
    $localDependabotBranches | ForEach-Object { Write-Host "  $_" }
    
    # Delete local branches that track deleted remote branches
    $localDependabotBranches | ForEach-Object {
        $branchName = $_
        $remoteExists = git ls-remote --heads origin $branchName
        if (-not $remoteExists) {
            Write-Host "Deleting local branch (remote deleted): $branchName" -ForegroundColor Yellow
            git branch -D $branchName
        }
    }
}

# Keep the active Next.js 16.0.6 branch
Write-Host "`nKeeping active branch: dependabot/npm_and_yarn/next-16.0.6" -ForegroundColor Green

Write-Host "`nCleanup complete!" -ForegroundColor Green

