# Close old dependabot branches that have conflicts with updated main
# These will be recreated by Dependabot automatically based on the new main

Write-Host "Closing old dependabot branches..." -ForegroundColor Cyan
Write-Host "Dependabot will recreate PRs automatically if updates are still needed." -ForegroundColor Yellow

# Branches to close (have merge conflicts with updated main)
$branchesToClose = @(
    "dependabot/npm_and_yarn/eslint-config-next-16.0.6",
    "dependabot/npm_and_yarn/types/node-24.10.1",
    "dependabot/npm_and_yarn/dotenv-17.2.3",
    "dependabot/npm_and_yarn/groq-sdk-0.37.0",
    "dependabot/npm_and_yarn/lucide-react-0.555.0",
    "dependabot/npm_and_yarn/postcss-8.5.6",
    "dependabot/npm_and_yarn/tailwindcss-4.1.17",
    "dependabot/npm_and_yarn/multi-d7810531b1"
)

# Keep the Next.js 16.0.3 one if it exists (already superseded)
$branchesToClose += "dependabot/npm_and_yarn/next-16.0.3"

Write-Host "`nBranches to close:" -ForegroundColor Yellow
$branchesToClose | ForEach-Object { Write-Host "  $_" }

$successCount = 0
$failCount = 0

Write-Host "`nDeleting remote branches..." -ForegroundColor Yellow
foreach ($branch in $branchesToClose) {
    Write-Host "  Deleting: $branch" -NoNewline
    $result = git push origin --delete $branch 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " [OK]" -ForegroundColor Green
        $successCount++
    } else {
        if ($result -match "remote ref does not exist") {
            Write-Host " [SKIPPED - already deleted]" -ForegroundColor Gray
        } else {
            Write-Host " [FAILED]" -ForegroundColor Red
            $failCount++
        }
    }
}

# Clean up local branches
Write-Host "`nCleaning up local branches..." -ForegroundColor Yellow
$localBranches = git branch | Select-String "dependabot" | ForEach-Object { 
    $_.Line.Trim() -replace '\* ', ''
}

foreach ($branch in $localBranches) {
    if ($branchesToClose -contains $branch) {
        Write-Host "  Deleting local: $branch" -ForegroundColor Gray
        git branch -D $branch 2>&1 | Out-Null
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Successfully deleted: $successCount" -ForegroundColor Green
Write-Host "  Failed: $failCount" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`nRemaining dependabot branches:" -ForegroundColor Cyan
$remaining = git branch -r | Select-String "dependabot"
if ($remaining) {
    $remaining | ForEach-Object { Write-Host "  $($_.Line.Trim())" }
} else {
    Write-Host "  None - all cleaned up!" -ForegroundColor Green
}

Write-Host "`nNote: Dependabot will automatically create new PRs for any needed updates" -ForegroundColor Yellow
Write-Host "based on the current main branch." -ForegroundColor Yellow

