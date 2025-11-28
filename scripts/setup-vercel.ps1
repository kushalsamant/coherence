# =============================================================================
# Vercel Project Setup Automation Script
# =============================================================================
# This script automates the setup of Vercel projects for ASK, Reframe, and Sketch2BIM
# It sets root directories and links projects to Vercel
# =============================================================================

param(
    [string]$VercelToken = "",
    [switch]$SkipLogin = $false
)

$ErrorActionPreference = "Stop"

# Project configurations
$projects = @(
    @{
        Name = "ask"
        RootDirectory = "apps/ask/frontend"
        DisplayName = "ASK"
    },
    @{
        Name = "reframe"
        RootDirectory = "apps/reframe"
        DisplayName = "Reframe"
    },
    @{
        Name = "sketch2bim"
        RootDirectory = "apps/sketch2bim/frontend"
        DisplayName = "Sketch2BIM"
    }
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Vercel Project Setup Automation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Vercel CLI is installed
Write-Host "Checking for Vercel CLI..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version 2>&1
    Write-Host "✓ Vercel CLI found: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Vercel CLI not found. Please install it first:" -ForegroundColor Red
    Write-Host "  npm install -g vercel" -ForegroundColor Yellow
    exit 1
}

# Login to Vercel if needed
if (-not $SkipLogin) {
    Write-Host ""
    Write-Host "Checking Vercel authentication..." -ForegroundColor Yellow
    
    # Check if already logged in
    try {
        $whoami = vercel whoami 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Already authenticated as: $whoami" -ForegroundColor Green
        } else {
            throw "Not authenticated"
        }
    } catch {
        Write-Host "Not authenticated. Logging in..." -ForegroundColor Yellow
        
        if ($VercelToken) {
            # Use token for non-interactive login
            $env:VERCEL_TOKEN = $VercelToken
            Write-Host "Using provided Vercel token..." -ForegroundColor Yellow
        } else {
            # Interactive login
            Write-Host "Please login to Vercel..." -ForegroundColor Yellow
            vercel login
            if ($LASTEXITCODE -ne 0) {
                Write-Host "✗ Login failed" -ForegroundColor Red
                exit 1
            }
        }
    }
}

# Get repository root (parent of scripts directory)
$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $repoRoot) {
    $repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}
$repoRoot = Resolve-Path $repoRoot

Write-Host ""
Write-Host "Repository root: $repoRoot" -ForegroundColor Cyan
Write-Host ""

# Process each project
foreach ($project in $projects) {
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    Write-Host "Setting up: $($project.DisplayName)" -ForegroundColor Cyan
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    
    $projectPath = Join-Path $repoRoot $project.RootDirectory
    
    if (-not (Test-Path $projectPath)) {
        Write-Host "✗ Project directory not found: $projectPath" -ForegroundColor Red
        continue
    }
    
    Write-Host "Project path: $projectPath" -ForegroundColor Yellow
    
    # Check if package.json exists
    $packageJson = Join-Path $projectPath "package.json"
    if (-not (Test-Path $packageJson)) {
        Write-Host "✗ package.json not found in $projectPath" -ForegroundColor Red
        continue
    }
    
    # Change to project directory
    Push-Location $projectPath
    
    try {
        # Check if already linked
        $vercelDir = Join-Path $projectPath ".vercel"
        if (Test-Path $vercelDir) {
            Write-Host "Project already linked to Vercel" -ForegroundColor Yellow
            $linkInfo = Get-Content (Join-Path $vercelDir "project.json") -Raw | ConvertFrom-Json
            Write-Host "  Linked to: $($linkInfo.projectId)" -ForegroundColor Gray
        } else {
            Write-Host "Linking project to Vercel..." -ForegroundColor Yellow
            Write-Host "  (You may be prompted to select/create a project)" -ForegroundColor Gray
            
            # Link project (non-interactive if token provided)
            if ($VercelToken) {
                vercel link --yes --token $VercelToken 2>&1 | Out-Null
            } else {
                vercel link --yes 2>&1 | Out-Null
            }
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Project linked successfully" -ForegroundColor Green
            } else {
                Write-Host "✗ Failed to link project" -ForegroundColor Red
                continue
            }
        }
        
        # Note: Root directory must be set via Vercel dashboard or API
        # CLI doesn't support setting root directory directly
        Write-Host ""
        Write-Host "⚠ IMPORTANT: Set Root Directory in Vercel Dashboard:" -ForegroundColor Yellow
        Write-Host "  1. Go to: https://vercel.com/kvshvl/$($project.Name)/settings" -ForegroundColor Gray
        Write-Host "  2. General → Root Directory: $($project.RootDirectory)" -ForegroundColor Gray
        Write-Host "  3. Save changes" -ForegroundColor Gray
        Write-Host ""
        Write-Host "  Or use the Vercel API/CLI to set it programmatically" -ForegroundColor Gray
        
    } finally {
        Pop-Location
    }
    
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Set Root Directory for each project in Vercel dashboard" -ForegroundColor Gray
Write-Host "2. Run sync-vercel-env.ps1 to sync environment variables" -ForegroundColor Gray
Write-Host ""

