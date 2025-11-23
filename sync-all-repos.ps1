# sync-all-repos.ps1
# Simple script to pull and push all git repositories

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Syncing All Repositories" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Main repository
Write-Host "[1/2] Main Repository" -ForegroundColor Yellow
Write-Host "Pulling..." -ForegroundColor Gray
git pull
if ($LASTEXITCODE -eq 0) {
    Write-Host "Pull successful!" -ForegroundColor Green
} else {
    Write-Host "Pull completed with warnings" -ForegroundColor Yellow
}

Write-Host "Pushing..." -ForegroundColor Gray
git push
if ($LASTEXITCODE -eq 0) {
    Write-Host "Push successful!" -ForegroundColor Green
} else {
    Write-Host "Push completed or no changes to push" -ForegroundColor Gray
}
Write-Host ""

# Submodules
Write-Host "[2/2] Submodules" -ForegroundColor Yellow
Write-Host "Updating submodules..." -ForegroundColor Gray
git submodule update --remote --merge
if ($LASTEXITCODE -eq 0) {
    Write-Host "Submodules updated!" -ForegroundColor Green
} else {
    Write-Host "Submodule update completed" -ForegroundColor Gray
}

# Push submodule changes if any
$submodules = git config --file .gitmodules --get-regexp path | ForEach-Object { $_ -replace '^submodule\.[^.]*\.path ', '' }
foreach ($submodule in $submodules) {
    if (Test-Path $submodule) {
        Write-Host "Checking submodule: $submodule" -ForegroundColor Gray
        Push-Location $submodule
        $branch = git branch --show-current
        if ($branch) {
            Write-Host "  Pushing $submodule ($branch)..." -ForegroundColor Gray
            git push
        } else {
            Write-Host "  Submodule in detached HEAD state (normal)" -ForegroundColor Gray
        }
        Pop-Location
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "All repositories synced!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

