# Merge remaining safe dependabot updates
Write-Host "Merging safe dependabot updates..." -ForegroundColor Cyan

# Ensure we're on main and up to date
git checkout main
git pull origin main

$safeBranches = @(
    @{Name = "dependabot/npm_and_yarn/eslint-config-next-16.0.6"; Message = "ESLint config for Next.js 16"},
    @{Name = "dependabot/npm_and_yarn/types/node-24.10.1"; Message = "Node.js type definitions"},
    @{Name = "dependabot/npm_and_yarn/dotenv-17.2.3"; Message = "Dotenv update"},
    @{Name = "dependabot/npm_and_yarn/groq-sdk-0.37.0"; Message = "Groq SDK update"},
    @{Name = "dependabot/npm_and_yarn/lucide-react-0.555.0"; Message = "Lucide React icons"}
)

$successCount = 0
$failCount = 0
$skippedCount = 0

foreach ($branch in $safeBranches) {
    Write-Host "`nProcessing: $($branch.Message)..." -ForegroundColor Yellow
    Write-Host "  Branch: $($branch.Name)" -ForegroundColor Gray
    
    # Check if branch exists
    $exists = git ls-remote --heads origin $($branch.Name) 2>&1
    if (-not $exists -or $exists -match "error") {
        Write-Host "  [SKIPPED] Branch doesn't exist" -ForegroundColor Gray
        $skippedCount++
        continue
    }
    
    # Try to merge
    git merge "origin/$($branch.Name)" --no-ff -m "Merge dependabot: $($branch.Message)" 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Merged successfully" -ForegroundColor Green
        $successCount++
        
        # Push to remote
        git push origin main 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  [WARNING] Push failed, may need manual push" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [FAILED] Merge conflict - needs manual resolution" -ForegroundColor Red
        $failCount++
        # Abort the failed merge
        git merge --abort 2>&1 | Out-Null
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Successfully merged: $successCount" -ForegroundColor Green
Write-Host "  Failed (conflicts): $failCount" -ForegroundColor Red
Write-Host "  Skipped (not found): $skippedCount" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan

if ($failCount -gt 0) {
    Write-Host "`nSome branches had conflicts and need manual resolution." -ForegroundColor Yellow
}

