# =============================================================================
# Delete and Recreate All Vercel Projects
# =============================================================================
# This script deletes all existing projects and recreates them from scratch
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
Write-Host "Delete and Recreate All Vercel Projects" -ForegroundColor Cyan
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

# Step 1: Get all existing projects
Write-Host "Step 1: Getting existing projects..." -ForegroundColor Yellow
try {
    $allProjects = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects" -Method GET -Headers $headers
    Write-Host "Found $($allProjects.projects.Count) existing projects" -ForegroundColor Green
    
    $projectsToDelete = $allProjects.projects | Where-Object { 
        $_.name -in @("ask", "reframe", "sketch2bim", "kushalsamant-github-io", "frontend")
    }
    
    if ($projectsToDelete.Count -gt 0) {
        Write-Host "Projects to delete:" -ForegroundColor Yellow
        $projectsToDelete | ForEach-Object {
            Write-Host "  - $($_.name) : $($_.id)" -ForegroundColor Gray
        }
    } else {
        Write-Host "No projects found to delete" -ForegroundColor Green
    }
} catch {
    Write-Host "Error getting projects: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Delete existing projects
Write-Host "Step 2: Deleting existing projects..." -ForegroundColor Yellow

foreach ($project in $projectsToDelete) {
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would delete: $($project.name) ($($project.id))" -ForegroundColor Gray
    } else {
        try {
            Write-Host "  Deleting $($project.name)..." -ForegroundColor Yellow
            Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$($project.id)" -Method DELETE -Headers $headers | Out-Null
            Write-Host "    ✓ Deleted $($project.name)" -ForegroundColor Green
        } catch {
            Write-Host "    ✗ Error deleting $($project.name): $_" -ForegroundColor Red
        }
    }
}

Write-Host ""

# Step 3: Wait a moment for deletions to complete
if (-not $DryRun) {
    Write-Host "Waiting for deletions to complete..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
    Write-Host ""
}

# Step 4: Create all projects
Write-Host "Step 4: Creating new projects..." -ForegroundColor Yellow
Write-Host ""

$projects = @(
    @{
        Name = "ask"
        RootDirectory = "apps/ask/frontend"
        Framework = "nextjs"
        DisplayName = "ASK"
        LocalPath = "$repoRoot\apps\ask\frontend"
        Domain = "ask.kvshvl.in"
    },
    @{
        Name = "reframe"
        RootDirectory = "apps/reframe"
        Framework = "nextjs"
        DisplayName = "Reframe"
        LocalPath = "$repoRoot\apps\reframe"
        Domain = "reframe.kvshvl.in"
    },
    @{
        Name = "sketch2bim"
        RootDirectory = "apps/sketch2bim/frontend"
        Framework = "nextjs"
        DisplayName = "Sketch2BIM"
        LocalPath = "$repoRoot\apps\sketch2bim\frontend"
        Domain = "sketch2bim.kvshvl.in"
    },
    @{
        Name = "kushalsamant-github-io"
        RootDirectory = $null
        Framework = "nextjs"
        DisplayName = "Portfolio Site"
        LocalPath = $repoRoot
        Domain = "kvshvl.in"
    }
)

$createdProjects = @{}

foreach ($project in $projects) {
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would create project: $($project.Name)" -ForegroundColor Gray
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
                Write-Host "    ✓ Root directory: (root of repo)" -ForegroundColor Green
            }
            
            # Add domain if specified
            if ($project.Domain) {
                try {
                    $domainBody = @{
                        name = $project.Domain
                    } | ConvertTo-Json
                    
                    Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$($newProject.id)/domains" -Method POST -Headers $headers -Body $domainBody | Out-Null
                    Write-Host "    ✓ Added domain: $($project.Domain)" -ForegroundColor Green
                } catch {
                    Write-Host "    ⚠ Could not add domain $($project.Domain): $_" -ForegroundColor Yellow
                    Write-Host "      Add manually in Vercel dashboard" -ForegroundColor Gray
                }
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

# Step 5: Link local directories
Write-Host "Step 5: Linking local directories to projects..." -ForegroundColor Yellow
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
                $linkOutput = vercel link --yes --project=$($project.Name) --token $VercelToken 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "    ✓ Linked successfully" -ForegroundColor Green
                } else {
                    Write-Host "    ⚠ Link may have issues" -ForegroundColor Yellow
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

# Step 6: Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN - No changes were made" -ForegroundColor Yellow
} else {
    Write-Host "Created projects:" -ForegroundColor Green
    foreach ($projectName in $createdProjects.Keys) {
        $project = $createdProjects[$projectName]
        Write-Host "  - $projectName : $($project.id)" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Connect projects to GitHub in Vercel dashboard:" -ForegroundColor Gray
    foreach ($projectName in $createdProjects.Keys) {
        Write-Host "   https://vercel.com/kvshvl/$projectName/settings/git" -ForegroundColor DarkGray
    }
    Write-Host ""
    Write-Host "2. Sync environment variables:" -ForegroundColor Gray
    Write-Host "   .\scripts\sync-vercel-env.ps1 -VercelToken `"$VercelToken`" -Environment all -Force" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "3. Verify setup:" -ForegroundColor Gray
    Write-Host "   .\scripts\verify-vercel-setup.ps1 -VercelToken `"$VercelToken`" -Environment all" -ForegroundColor DarkGray
}

Write-Host ""

