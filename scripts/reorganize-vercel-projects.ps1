# =============================================================================
# Vercel Projects Reorganization Script
# =============================================================================
# This script reorganizes Vercel projects to properly separate:
# - Root portfolio site (kushalsamant-github-io)
# - ASK app (ask)
# - Reframe app (reframe) - already correct
# - Sketch2BIM app (sketch2bim)
# =============================================================================

param(
    [string]$VercelToken = $env:VERCEL_TOKEN,
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
Write-Host "Vercel Projects Reorganization" -ForegroundColor Cyan
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
Write-Host ""

# Step 1: Get current projects
Write-Host "Step 1: Getting current projects..." -ForegroundColor Yellow
try {
    $allProjects = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects" -Method GET -Headers $headers
    Write-Host "Found $($allProjects.projects.Count) projects" -ForegroundColor Green
    
    $frontendProject = $allProjects.projects | Where-Object { $_.name -eq "frontend" } | Select-Object -First 1
    $rootProject = $allProjects.projects | Where-Object { $_.name -eq "kushalsamant-github-io" } | Select-Object -First 1
    $reframeProject = $allProjects.projects | Where-Object { $_.name -eq "reframe" } | Select-Object -First 1
    
    if ($frontendProject) {
        Write-Host "  - frontend: $($frontendProject.id)" -ForegroundColor Gray
    }
    if ($rootProject) {
        Write-Host "  - kushalsamant-github-io: $($rootProject.id)" -ForegroundColor Gray
    }
    if ($reframeProject) {
        Write-Host "  - reframe: $($reframeProject.id)" -ForegroundColor Gray
    }
} catch {
    Write-Host "Error getting projects: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Delete old projects
Write-Host "Step 2: Deleting old projects..." -ForegroundColor Yellow

if ($frontendProject) {
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would delete frontend project: $($frontendProject.id)" -ForegroundColor Gray
    } else {
        try {
            Write-Host "  Deleting frontend project..." -ForegroundColor Yellow
            Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$($frontendProject.id)" -Method DELETE -Headers $headers | Out-Null
            Write-Host "  ✓ Deleted frontend project" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Error deleting frontend project: $_" -ForegroundColor Red
        }
    }
}

if ($rootProject) {
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would delete kushalsamant-github-io project: $($rootProject.id)" -ForegroundColor Gray
    } else {
        try {
            Write-Host "  Deleting kushalsamant-github-io project..." -ForegroundColor Yellow
            Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$($rootProject.id)" -Method DELETE -Headers $headers | Out-Null
            Write-Host "  ✓ Deleted kushalsamant-github-io project" -ForegroundColor Green
        } catch {
            Write-Host "  ✗ Error deleting kushalsamant-github-io project: $_" -ForegroundColor Red
        }
    }
}

Write-Host ""

# Step 3: Create new projects
Write-Host "Step 3: Creating new projects..." -ForegroundColor Yellow

# Get team/account ID (needed for project creation)
try {
    $userInfo = Invoke-RestMethod -Uri "https://api.vercel.com/v2/user" -Method GET -Headers $headers
    $accountId = $userInfo.user.username
    Write-Host "  Account: $accountId" -ForegroundColor Gray
} catch {
    Write-Host "  ⚠ Could not get account info, will try with team" -ForegroundColor Yellow
    $accountId = "kvshvl"  # Default team name
}

$projectsToCreate = @(
    @{ Name = "ask"; RootDirectory = "apps/ask/frontend"; Framework = "nextjs" },
    @{ Name = "sketch2bim"; RootDirectory = "apps/sketch2bim/frontend"; Framework = "nextjs" },
    @{ Name = "kushalsamant-github-io"; RootDirectory = ""; Framework = "nextjs" }
)

$createdProjects = @{}

foreach ($projectConfig in $projectsToCreate) {
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would create project: $($projectConfig.Name)" -ForegroundColor Gray
    } else {
        try {
            Write-Host "  Creating project: $($projectConfig.Name)..." -ForegroundColor Yellow
            
            $body = @{
                name = $projectConfig.Name
                framework = $projectConfig.Framework
            } | ConvertTo-Json
            
            $newProject = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects" -Method POST -Headers $headers -Body $body
            $createdProjects[$projectConfig.Name] = $newProject
            
            Write-Host "  ✓ Created project: $($projectConfig.Name) (ID: $($newProject.id))" -ForegroundColor Green
            
            # Set root directory if specified
            if ($projectConfig.RootDirectory) {
                $updateBody = @{
                    rootDirectory = $projectConfig.RootDirectory
                } | ConvertTo-Json
                
                Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$($newProject.id)" -Method PATCH -Headers $headers -Body $updateBody | Out-Null
                Write-Host "    ✓ Set root directory: $($projectConfig.RootDirectory)" -ForegroundColor Green
            }
        } catch {
            Write-Host "  ✗ Error creating project $($projectConfig.Name): $_" -ForegroundColor Red
            if ($_.ErrorDetails.Message) {
                Write-Host "    Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
            }
        }
    }
}

Write-Host ""

# Step 4: Connect projects to GitHub
Write-Host "Step 4: Connecting projects to GitHub..." -ForegroundColor Yellow

$gitRepo = "kushalsamant/kushalsamant.github.io"

foreach ($projectName in $createdProjects.Keys) {
    $project = $createdProjects[$projectName]
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would connect $projectName to GitHub repo: $gitRepo" -ForegroundColor Gray
    } else {
        try {
            Write-Host "  Connecting $projectName to GitHub..." -ForegroundColor Yellow
            
            # Get Git connection info
            $gitConnections = Invoke-RestMethod -Uri "https://api.vercel.com/v1/integrations" -Method GET -Headers $headers
            $githubIntegration = $gitConnections | Where-Object { $_.type -eq "github" } | Select-Object -First 1
            
            if ($githubIntegration) {
                # Link project to Git repository
                $linkBody = @{
                    type = "github"
                    repo = $gitRepo
                } | ConvertTo-Json
                
                # Note: This might require using the Vercel CLI instead of API
                Write-Host "    ⚠ Git linking may need to be done via Vercel CLI or dashboard" -ForegroundColor Yellow
                Write-Host "    Project $projectName created. Link manually or use: vercel link --project=$projectName" -ForegroundColor Gray
            } else {
                Write-Host "    ⚠ GitHub integration not found. Link manually in dashboard." -ForegroundColor Yellow
            }
        } catch {
            Write-Host "    ⚠ Could not auto-link to GitHub: $_" -ForegroundColor Yellow
            Write-Host "    Link manually in Vercel dashboard or use CLI" -ForegroundColor Gray
        }
    }
}

Write-Host ""

# Step 5: Clean up local .vercel directories
Write-Host "Step 5: Cleaning up local .vercel directories..." -ForegroundColor Yellow

$vercelDirsToRemove = @(
    "$repoRoot\apps\ask\frontend\.vercel",
    "$repoRoot\apps\sketch2bim\frontend\.vercel",
    "$repoRoot\.vercel"
)

foreach ($vercelDir in $vercelDirsToRemove) {
    if (Test-Path $vercelDir) {
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would remove: $vercelDir" -ForegroundColor Gray
        } else {
            try {
                Remove-Item -Path $vercelDir -Recurse -Force
                Write-Host "  ✓ Removed: $vercelDir" -ForegroundColor Green
            } catch {
                Write-Host "  ✗ Error removing $vercelDir : $_" -ForegroundColor Red
            }
        }
    }
}

Write-Host ""

# Step 6: Link local directories to projects
Write-Host "Step 6: Linking local directories to projects..." -ForegroundColor Yellow

$linkings = @(
    @{ Directory = "$repoRoot"; ProjectName = "kushalsamant-github-io" },
    @{ Directory = "$repoRoot\apps\ask\frontend"; ProjectName = "ask" },
    @{ Directory = "$repoRoot\apps\sketch2bim\frontend"; ProjectName = "sketch2bim" }
)

foreach ($linking in $linkings) {
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would link $($linking.Directory) to $($linking.ProjectName)" -ForegroundColor Gray
    } else {
        try {
            Write-Host "  Linking $($linking.Directory) to $($linking.ProjectName)..." -ForegroundColor Yellow
            
            Push-Location $linking.Directory
            try {
                # Use Vercel CLI to link
                $linkOutput = vercel link --yes --project=$($linking.ProjectName) --token $VercelToken 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "    ✓ Linked successfully" -ForegroundColor Green
                } else {
                    Write-Host "    ⚠ Link may have issues. Check output." -ForegroundColor Yellow
                }
            } finally {
                Pop-Location
            }
        } catch {
            Write-Host "    ✗ Error linking: $_" -ForegroundColor Red
        }
    }
}

Write-Host ""

# Step 7: Set root directories (verify/update)
Write-Host "Step 7: Verifying root directories..." -ForegroundColor Yellow

$rootDirConfigs = @(
    @{ ProjectName = "ask"; RootDir = "apps/ask/frontend" },
    @{ ProjectName = "sketch2bim"; RootDir = "apps/sketch2bim/frontend" },
    @{ ProjectName = "kushalsamant-github-io"; RootDir = "" }
)

foreach ($config in $rootDirConfigs) {
    if ($createdProjects.ContainsKey($config.ProjectName)) {
        $project = $createdProjects[$config.ProjectName]
        
        if ($DryRun) {
            Write-Host "  [DRY RUN] Would verify root directory for $($config.ProjectName): $($config.RootDir)" -ForegroundColor Gray
        } else {
            try {
                $projectInfo = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$($project.id)" -Method GET -Headers $headers
                
                if ($projectInfo.rootDirectory -ne $config.RootDir) {
                    $updateBody = @{
                        rootDirectory = $config.RootDir
                    } | ConvertTo-Json
                    
                    Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$($project.id)" -Method PATCH -Headers $headers -Body $updateBody | Out-Null
                    Write-Host "  ✓ Updated root directory for $($config.ProjectName): $($config.RootDir)" -ForegroundColor Green
                } else {
                    Write-Host "  ✓ Root directory already correct for $($config.ProjectName)" -ForegroundColor Green
                }
            } catch {
                Write-Host "  ⚠ Could not verify root directory for $($config.ProjectName): $_" -ForegroundColor Yellow
            }
        }
    }
}

Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Reorganization Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Run sync-vercel-env.ps1 to sync environment variables" -ForegroundColor Gray
Write-Host "2. Run verify-vercel-setup.ps1 to verify configuration" -ForegroundColor Gray
Write-Host "3. Connect projects to GitHub in Vercel dashboard if not auto-linked" -ForegroundColor Gray
Write-Host ""

