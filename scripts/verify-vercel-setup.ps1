# =============================================================================
# Vercel Setup Verification Script
# =============================================================================
# This script verifies Vercel configuration for all projects:
# - Projects are linked
# - Root directories are set correctly
# - Environment variables are present and match .env.production files
# =============================================================================

param(
    [string]$VercelToken = "",
    [ValidateSet("production", "preview", "development", "all")]
    [string]$Environment = "production"
)

$ErrorActionPreference = "Continue"

# Project configurations
$projects = @(
    @{
        Name = "ask"
        RootDirectory = "apps/ask/frontend"
        DisplayName = "ASK"
        EnvFile = "ask.env.production"
        Prefix = "ASK_"
        FrontendVars = @(
            "ASK_API_BASE_URL",
            "ASK_AUTH_SECRET",
            "ASK_AUTH_URL",
            "ASK_BACKEND_URL",
            "ASK_GOOGLE_CLIENT_ID",
            "ASK_GOOGLE_SECRET",
            "ASK_GROQ_API_BASE",
            "ASK_NEXT_PUBLIC_API_URL",
            "ASK_NEXTAUTH_SECRET",
            "ASK_NEXTAUTH_URL",
            "NEXT_PUBLIC_AUTH_URL"
        )
    },
    @{
        Name = "reframe"
        RootDirectory = "apps/reframe"
        DisplayName = "Reframe"
        EnvFile = "reframe.env.production"
        Prefix = "REFRAME_"
        FrontendVars = @(
            "REFRAME_API_URL",
            "REFRAME_AUTH_SECRET",
            "REFRAME_AUTH_URL",
            "REFRAME_GOOGLE_CLIENT_ID",
            "REFRAME_GOOGLE_CLIENT_SECRET",
            "REFRAME_NEXT_PUBLIC_API_URL",
            "REFRAME_NEXT_PUBLIC_FREE_LIMIT",
            "REFRAME_NEXT_PUBLIC_SITE_URL",
            "REFRAME_NEXTAUTH_SECRET",
            "REFRAME_NEXTAUTH_URL",
            "REFRAME_RAZORPAY_KEY_ID",
            "REFRAME_RAZORPAY_KEY_SECRET",
            "REFRAME_RAZORPAY_WEBHOOK_SECRET",
            "REFRAME_RESEND_API_KEY",
            "NEXT_PUBLIC_AUTH_URL"
        )
    },
    @{
        Name = "sketch2bim"
        RootDirectory = "apps/sketch2bim/frontend"
        DisplayName = "Sketch2BIM"
        EnvFile = "sketch2bim.env.production"
        Prefix = "SKETCH2BIM_"
        FrontendVars = @(
            "SKETCH2BIM_AUTH_SECRET",
            "SKETCH2BIM_AUTH_URL",
            "SKETCH2BIM_GOOGLE_CLIENT_ID",
            "SKETCH2BIM_GOOGLE_SECRET",
            "SKETCH2BIM_NEXT_PUBLIC_API_URL",
            "SKETCH2BIM_NEXT_PUBLIC_FREE_LIMIT",
            "SKETCH2BIM_NEXTAUTH_SECRET",
            "SKETCH2BIM_NEXTAUTH_URL",
            "NEXT_PUBLIC_AUTH_URL"
        )
    }
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Vercel Setup Verification" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get Vercel token
if (-not $VercelToken) {
    $VercelToken = $env:VERCEL_TOKEN
}

# Check Vercel CLI
Write-Host "Checking Vercel CLI..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version 2>&1
    Write-Host "✓ Vercel CLI: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Vercel CLI not found" -ForegroundColor Red
    exit 1
}

# Check authentication
Write-Host "Checking authentication..." -ForegroundColor Yellow
try {
    if ($VercelToken) {
        $env:VERCEL_TOKEN = $VercelToken
    }
    $whoami = vercel whoami 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Authenticated as: $whoami" -ForegroundColor Green
    } else {
        throw "Not authenticated"
    }
} catch {
    if ($VercelToken) {
        Write-Host "⚠ Token provided but authentication check failed. Continuing with API calls..." -ForegroundColor Yellow
    } else {
        Write-Host "✗ Not authenticated. Run: vercel login or provide -VercelToken" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""

# Get repository root (parent of scripts directory)
$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $repoRoot) {
    $repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}
$repoRoot = Resolve-Path $repoRoot

# Function to get project ID
function Get-ProjectId {
    param([string]$ProjectName)
    
    try {
        if ($VercelToken) {
            $headers = @{
                "Authorization" = "Bearer $VercelToken"
            }
            $response = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects" `
                -Method GET `
                -Headers $headers
            $project = $response.projects | Where-Object { $_.name -eq $ProjectName } | Select-Object -First 1
            return $project.id
        } else {
            $projectInfo = vercel project ls --json 2>&1 | ConvertFrom-Json
            $project = $projectInfo | Where-Object { $_.name -eq $ProjectName } | Select-Object -First 1
            return $project.id
        }
    } catch {
        return $null
    }
}

# Function to get root directory
function Get-RootDirectory {
    param([string]$ProjectId)
    
    try {
        if ($VercelToken) {
            $headers = @{
                "Authorization" = "Bearer $VercelToken"
            }
            $response = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$ProjectId" `
                -Method GET `
                -Headers $headers
            return $response.rootDirectory
        }
    } catch {
        return $null
    }
}

# Function to get environment variables
function Get-EnvVars {
    param(
        [string]$ProjectName,
        [string]$EnvType
    )
    
    try {
        $envVars = @{}
        $output = vercel env ls $ProjectName --environment $EnvType --json 2>&1
        if ($LASTEXITCODE -eq 0) {
            $vars = $output | ConvertFrom-Json
            foreach ($var in $vars) {
                $envVars[$var.key] = $var.value
            }
        }
        return $envVars
    } catch {
        return @{}
    }
}

# Function to parse .env file
function Parse-EnvFile {
    param([string]$FilePath)
    
    $envVars = @{}
    if (Test-Path $FilePath) {
        $lines = Get-Content $FilePath
        foreach ($line in $lines) {
            $line = $line.Trim()
            if ($line -eq "" -or $line.StartsWith("#")) {
                continue
            }
            if ($line -match '^([^=]+)=(.*)$') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                if ($value.StartsWith('"') -and $value.EndsWith('"')) {
                    $value = $value.Substring(1, $value.Length - 2)
                }
                if ($value.StartsWith("'") -and $value.EndsWith("'")) {
                    $value = $value.Substring(1, $value.Length - 2)
                }
                $envVars[$key] = $value
            }
        }
    }
    return $envVars
}

# Determine environments to check
$environments = @()
switch ($Environment) {
    "all" { $environments = @("production", "preview", "development") }
    default { $environments = @($Environment) }
}

# Verification results
$results = @{
    TotalProjects = $projects.Count
    LinkedProjects = 0
    RootDirectoriesCorrect = 0
    EnvVarsChecked = 0
    EnvVarsMissing = 0
    EnvVarsMismatched = 0
}

# Verify each project
foreach ($project in $projects) {
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    Write-Host "Verifying: $($project.DisplayName)" -ForegroundColor Cyan
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    Write-Host ""
    
    # Check if project is linked
    Write-Host "1. Project Linking" -ForegroundColor Yellow
    $projectPath = Join-Path $repoRoot $project.RootDirectory
    $vercelDir = Join-Path $projectPath ".vercel"
    
    if (Test-Path $vercelDir) {
        Write-Host "   ✓ Project is linked" -ForegroundColor Green
        $results.LinkedProjects++
        
        try {
            $linkInfo = Get-Content (Join-Path $vercelDir "project.json") -Raw | ConvertFrom-Json
            Write-Host "   Project ID: $($linkInfo.projectId)" -ForegroundColor Gray
        } catch {
            Write-Host "   ⚠ Could not read link info" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ✗ Project is not linked" -ForegroundColor Red
        Write-Host "   Run: cd $($project.RootDirectory) && vercel link" -ForegroundColor Gray
    }
    Write-Host ""
    
    # Check root directory
    Write-Host "2. Root Directory" -ForegroundColor Yellow
    if ($VercelToken) {
        $projectId = Get-ProjectId -ProjectName $project.Name
        if ($projectId) {
            $rootDir = Get-RootDirectory -ProjectId $projectId
            if ($rootDir) {
                if ($rootDir -eq $project.RootDirectory) {
                    Write-Host "   ✓ Root directory correct: $rootDir" -ForegroundColor Green
                    $results.RootDirectoriesCorrect++
                } else {
                    Write-Host "   ✗ Root directory mismatch" -ForegroundColor Red
                    Write-Host "   Expected: $($project.RootDirectory)" -ForegroundColor Gray
                    Write-Host "   Actual: $rootDir" -ForegroundColor Gray
                }
            } else {
                Write-Host "   ✗ Root directory not set" -ForegroundColor Red
            }
        } else {
            Write-Host "   ⚠ Could not get project ID (token may be required)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ⚠ Skipping (Vercel token required for API access)" -ForegroundColor Yellow
    }
    Write-Host ""
    
    # Check environment variables
    Write-Host "3. Environment Variables" -ForegroundColor Yellow
    
    # Parse .env.production file
    $envFilePath = Join-Path $repoRoot $project.EnvFile
    $expectedVars = Parse-EnvFile -FilePath $envFilePath
    
    # Filter for frontend variables
    $expectedFrontendVars = @{}
    foreach ($varName in $project.FrontendVars) {
        if ($expectedVars.ContainsKey($varName)) {
            $expectedFrontendVars[$varName] = $expectedVars[$varName]
        }
    }
    
    # Also include NEXT_PUBLIC_* variables
    foreach ($key in $expectedVars.Keys) {
        if ($key -like "NEXT_PUBLIC_*" -or $key -like "$($project.Prefix)NEXT_PUBLIC_*") {
            if (-not $expectedFrontendVars.ContainsKey($key)) {
                $expectedFrontendVars[$key] = $expectedVars[$key]
            }
        }
    }
    
    Write-Host "   Expected frontend variables: $($expectedFrontendVars.Count)" -ForegroundColor Gray
    
    # Check each environment
    foreach ($envType in $environments) {
        Write-Host "   Environment: $envType" -ForegroundColor Cyan
        
        $actualVars = Get-EnvVars -ProjectName $project.Name -EnvType $envType
        
        $missing = @()
        $mismatched = @()
        
        foreach ($varName in $expectedFrontendVars.Keys) {
            $expectedValue = $expectedFrontendVars[$varName]
            
            # Skip empty expected values
            if ([string]::IsNullOrWhiteSpace($expectedValue)) {
                continue
            }
            
            $results.EnvVarsChecked++
            
            if ($actualVars.ContainsKey($varName)) {
                $actualValue = $actualVars[$varName]
                if ($actualValue -ne $expectedValue) {
                    $mismatched += $varName
                    $results.EnvVarsMismatched++
                }
            } else {
                $missing += $varName
                $results.EnvVarsMissing++
            }
        }
        
        if ($missing.Count -eq 0 -and $mismatched.Count -eq 0) {
            Write-Host "     ✓ All variables present and correct" -ForegroundColor Green
        } else {
            if ($missing.Count -gt 0) {
                Write-Host "     ✗ Missing variables ($($missing.Count)):" -ForegroundColor Red
                foreach ($var in $missing) {
                    Write-Host "       - $var" -ForegroundColor Gray
                }
            }
            if ($mismatched.Count -gt 0) {
                Write-Host "     ⚠ Mismatched variables ($($mismatched.Count)):" -ForegroundColor Yellow
                foreach ($var in $mismatched) {
                    Write-Host "       - $var" -ForegroundColor Gray
                }
            }
        }
    }
    
    Write-Host ""
}

# Summary Report
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Verification Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Projects:" -ForegroundColor Yellow
Write-Host "  Total: $($results.TotalProjects)" -ForegroundColor Gray
Write-Host "  Linked: $($results.LinkedProjects) / $($results.TotalProjects)" -ForegroundColor $(if ($results.LinkedProjects -eq $results.TotalProjects) { "Green" } else { "Yellow" })
Write-Host "  Root Directories Correct: $($results.RootDirectoriesCorrect) / $($results.TotalProjects)" -ForegroundColor $(if ($results.RootDirectoriesCorrect -eq $results.TotalProjects) { "Green" } else { "Yellow" })
Write-Host ""

Write-Host "Environment Variables:" -ForegroundColor Yellow
Write-Host "  Checked: $($results.EnvVarsChecked)" -ForegroundColor Gray
Write-Host "  Missing: $($results.EnvVarsMissing)" -ForegroundColor $(if ($results.EnvVarsMissing -eq 0) { "Green" } else { "Red" })
Write-Host "  Mismatched: $($results.EnvVarsMismatched)" -ForegroundColor $(if ($results.EnvVarsMismatched -eq 0) { "Green" } else { "Yellow" })
Write-Host ""

$allGood = ($results.LinkedProjects -eq $results.TotalProjects) -and 
           ($results.RootDirectoriesCorrect -eq $results.TotalProjects) -and 
           ($results.EnvVarsMissing -eq 0) -and 
           ($results.EnvVarsMismatched -eq 0)

if ($allGood) {
    Write-Host "✓ All checks passed!" -ForegroundColor Green
} else {
    Write-Host "⚠ Some issues found. Review the details above." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To fix issues:" -ForegroundColor Yellow
    Write-Host "  1. Run: .\scripts\setup-vercel-all.ps1" -ForegroundColor Gray
    Write-Host "  2. Or sync env vars: .\scripts\sync-vercel-env.ps1 -Force" -ForegroundColor Gray
}

Write-Host ""

