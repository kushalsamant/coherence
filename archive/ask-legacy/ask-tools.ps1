# ask-tools.ps1
# ASK app development utilities
# Usage: .\ask-tools.ps1 <command> [arguments]

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
# Help
# ============================================================================

function Show-Help {
    Write-Host ""
    Write-Host "ASK App Development Tools" -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\ask-tools.ps1 <command> [arguments]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Git Operations:" -ForegroundColor White
    Write-Host "    update-repo [message]   Stage, commit, and push all changes"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\ask-tools.ps1 update-repo"
    Write-Host "  .\ask-tools.ps1 update-repo 'Fixed bug in research feature'"
    Write-Host ""
}

# ============================================================================
# Main Command Router
# ============================================================================

switch ($Command.ToLower()) {
    "update-repo" { 
        $msg = if ($Arguments.Count -gt 0) { $Arguments -join " " } else { "Update repo" }
        Update-Repo -Message $msg
    }
    "help" { Show-Help }
    default { 
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}

