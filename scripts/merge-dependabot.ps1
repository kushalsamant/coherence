# Merge dependabot branches into main
Write-Host "Merging dependabot branches..." -ForegroundColor Cyan

# Ensure we're on main and up to date
Write-Host "`n1. Updating main branch..." -ForegroundColor Yellow
git checkout main
git pull origin main

# Merge Next.js 16.0.6 (priority - already fixed)
Write-Host "`n2. Merging Next.js 16.0.6..." -ForegroundColor Yellow
git merge origin/dependabot/npm_and_yarn/next-16.0.6 --no-ff -m "Merge dependabot: Next.js 16.0.6 with build fixes"
if ($LASTEXITCODE -eq 0) {
    Write-Host "   [OK] Merged successfully" -ForegroundColor Green
    git push origin main
} else {
    Write-Host "   [FAILED] Merge conflict or error" -ForegroundColor Red
    Write-Host "   Please resolve manually" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nMerge complete!" -ForegroundColor Green
Write-Host "Next.js 16.0.6 has been merged into main" -ForegroundColor Cyan

