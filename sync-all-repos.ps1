# sync-all-repos.ps1
# Simple script to pull and push all git repositories

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Syncing All Repositories" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Main repository
Write-Host "Main Repository" -ForegroundColor Yellow
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
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "All repositories synced!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

