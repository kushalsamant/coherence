# =============================================================================
# Create All Vercel Projects via API
# =============================================================================
# This script creates all Vercel projects from scratch:
# - Root portfolio site (kushalsamant-github-io)
# - ASK app (ask)
# - Reframe app (reframe)
# - Sketch2BIM app (sketch2bim)
# =============================================================================

param(
    [string]$VercelToken = $env:VERCEL_TOKEN,
    [string]$GitHubRepo = "kushalsamant/kushalsamant.github.io",
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

if (-not $VercelToken) {
    Write-Host "Error: Vercel token is required. Set VERCEL_TOKEN environment variable or pass -VercelToken" -ForegroundColor Red
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $VercelToken"
    "Content-Type" = "application/json"
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Create All Vercel Projects" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# Get repository root
$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $repoRoot) {
    $repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}
$repoRoot = Resolve-Path $repoRoot

Write-Host "Repository root: $repoRoot" -ForegroundColor Cyan
Write-Host "GitHub repo: $GitHubRepo" -ForegroundColor Cyan
Write-Host ""

# Project configurations
$projects = @(
    @{
        Name = "ask"
        RootDirectory = "apps/ask/frontend"
        Framework = "nextjs"
        DisplayName = "ASK"
        LocalPath = "$repoRoot\apps\ask\frontend"
    },
    @{
        Name = "reframe"
        RootDirectory = "apps/reframe"
        Framework = "nextjs"
        DisplayName = "Reframe"
        LocalPath = "$repoRoot\apps\reframe"
    },
    @{
        Name = "sketch2bim"
        RootDirectory = "apps/sketch2bim/frontend"
        Framework = "nextjs"
        DisplayName = "Sketch2BIM"
        LocalPath = "$repoRoot\apps\sketch2bim\frontend"
    },
    @{
        Name = "kushalsamant-github-io"
        RootDirectory = $null  # Root of repo, leave empty
        Framework = "nextjs"
        DisplayName = "Portfolio Site"
        LocalPath = $repoRoot
    }
)

# Step 1: Create all projects
Write-Host "Step 1: Creating projects..." -ForegroundColor Yellow
Write-Host ""

$createdProjects = @{}

foreach ($project in $projects) {
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would create project: $($project.Name)" -ForegroundColor Gray
        if ($project.RootDirectory) {
            Write-Host "    Root directory: $($project.RootDirectory)" -ForegroundColor Gray
        } else {
            Write-Host "    Root directory: (root of repo)" -ForegroundColor Gray
        }
    } else {
        try {
            Write-Host "  Creating project: $($project.DisplayName) ($($project.Name))..." -ForegroundColor Yellow
            
            $body = @{
                name = $project.Name
                framework = $project.Framework
            } | ConvertTo-Json
            
            $newProject = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects" -Method POST -Headers $headers -Body $body
            $createdProjects[$project.Name] = $newProject
            
            Write-Host "    ✓ Created project: $($project.Name) (ID: $($newProject.id))" -ForegroundColor Green
            
            # Set root directory if specified
            if ($project.RootDirectory) {
                $updateBody = @{
                    rootDirectory = $project.RootDirectory
                } | ConvertTo-Json
                
                Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$($newProject.id)" -Method PATCH -Headers $headers -Body $updateBody | Out-Null
                Write-Host "    ✓ Set root directory: $($project.RootDirectory)" -ForegroundColor Green
            } else {
                # For root project, ensure rootDirectory is not set (null/empty)
                Write-Host "    ✓ Root directory: (root of repo)" -ForegroundColor Green
            }
        } catch {
            Write-Host "    ✗ Error creating project $($project.Name): $_" -ForegroundColor Red
            if ($_.ErrorDetails.Message) {
                $errorDetails = $_.ErrorDetails.Message | ConvertFrom-Json -ErrorAction SilentlyContinue
                if ($errorDetails) {
                    Write-Host "      Error: $($errorDetails.error.message)" -ForegroundColor Red
                }
            }
        }
    }
    Write-Host ""
}

# Step 2: Link local directories to projects
Write-Host "Step 2: Linking local directories to projects..." -ForegroundColor Yellow
Write-Host ""

foreach ($project in $projects) {
    if (-not $createdProjects.ContainsKey($project.Name)) {
        Write-Host "  ⚠ Skipping $($project.Name) - project not created" -ForegroundColor Yellow
        continue
    }
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would link $($project.LocalPath) to $($project.Name)" -ForegroundColor Gray
    } else {
        try {
            Write-Host "  Linking $($project.DisplayName)..." -ForegroundColor Yellow
            
            if (-not (Test-Path $project.LocalPath)) {
                Write-Host "    ⚠ Directory not found: $($project.LocalPath)" -ForegroundColor Yellow
                continue
            }
            
            # Remove existing .vercel directory if it exists
            $vercelDir = Join-Path $project.LocalPath ".vercel"
            if (Test-Path $vercelDir) {
                Remove-Item -Path $vercelDir -Recurse -Force -ErrorAction SilentlyContinue
            }
            
            Push-Location $project.LocalPath
            try {
                # Use Vercel CLI to link
                $linkOutput = vercel link --yes --project=$($project.Name) --token $VercelToken 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "    ✓ Linked successfully" -ForegroundColor Green
                } else {
                    Write-Host "    ⚠ Link may have issues. Output:" -ForegroundColor Yellow
                    Write-Host $linkOutput -ForegroundColor Gray
                }
            } finally {
                Pop-Location
            }
        } catch {
            Write-Host "    ✗ Error linking $($project.Name): $_" -ForegroundColor Red
        }
    }
    Write-Host ""
}

# Step 3: Connect projects to GitHub (via Vercel CLI)
Write-Host "Step 3: Connecting projects to GitHub..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Note: GitHub connection may need to be done manually in Vercel dashboard" -ForegroundColor Gray
Write-Host "  or via Vercel CLI after projects are created." -ForegroundColor Gray
Write-Host ""

foreach ($project in $projects) {
    if (-not $createdProjects.ContainsKey($project.Name)) {
        continue
    }
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would connect $($project.Name) to GitHub repo: $GitHubRepo" -ForegroundColor Gray
    } else {
        Write-Host "  Project $($project.Name) created. Connect to GitHub:" -ForegroundColor Yellow
        Write-Host "    1. Go to: https://vercel.com/kvshvl/$($project.Name)/settings/git" -ForegroundColor Gray
        Write-Host "    2. Connect to repository: $GitHubRepo" -ForegroundColor Gray
        Write-Host "    3. Or use: vercel git connect --project=$($project.Name)" -ForegroundColor Gray
    }
    Write-Host ""
}

# Step 4: Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN - No projects were created" -ForegroundColor Yellow
} else {
    Write-Host "Created projects:" -ForegroundColor Green
    foreach ($projectName in $createdProjects.Keys) {
        $project = $createdProjects[$projectName]
        Write-Host "  - $projectName : $($project.id)" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Connect projects to GitHub in Vercel dashboard" -ForegroundColor Gray
    Write-Host "2. Run: .\scripts\sync-vercel-env.ps1 -VercelToken `"$VercelToken`" -Environment all -Force" -ForegroundColor Gray
    Write-Host "3. Run: .\scripts\verify-vercel-setup.ps1 -VercelToken `"$VercelToken`" -Environment all" -ForegroundColor Gray
}

Write-Host ""

