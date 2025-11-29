# push-pull-all-repos.ps1
# Script to pull and push the main git repository

Write-Host "🔄 Syncing all repositories..." -ForegroundColor Cyan
Write-Host ""

# Get the root directory of the main repo
$rootDir = Get-Location

# Function to sync a single repo
function Sync-Repo {
    param(
        [string]$RepoPath,
        [string]$RepoName
    )
    
    Push-Location $RepoPath
    
    Write-Host "📁 Processing: $RepoName" -ForegroundColor Yellow
    Write-Host "   Location: $RepoPath" -ForegroundColor Gray
    
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
    Pop-Location
}

# Sync main repository
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "MAIN REPOSITORY" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Sync-Repo -RepoPath $rootDir -RepoName "Main Repository ($(Split-Path -Leaf $rootDir))"

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ All repositories synced!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
