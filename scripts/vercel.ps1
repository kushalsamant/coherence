# =============================================================================
# Vercel Management Script - Consolidated
# =============================================================================
# Single script for all Vercel operations:
# - setup: Complete setup (link projects, set root dirs, sync env, verify)
# - deploy: Trigger deployments
# - sync: Sync environment variables
# - verify: Verify configuration
# - link: Link projects only
# - rootdir: Set root directories only
# =============================================================================

param(
    [ValidateSet("setup", "deploy", "sync", "verify", "link", "rootdir")]
    [string]$Action = "setup",
    [string]$VercelToken = "qBiwTlx8W3uA7nhcXT890h0s",
    [ValidateSet("production", "preview", "development", "all")]
    [string]$Environment = "production",
    [ValidateSet("ask", "reframe", "sketch2bim", "kushalsamant-github-io", "all")]
    [string]$Project = "all",
    [ValidateSet("production", "preview")]
    [string]$Target = "production",
    [switch]$DryRun = $false,
    [switch]$Force = $false,
    [switch]$SkipLogin = $false
)

$ErrorActionPreference = "Stop"

# Project configurations
$projects = @(
    @{
        Name = "ask"
        DisplayName = "ASK"
        RootDirectory = "apps/ask/frontend"
        EnvFile = "ask.env.production"
        Prefix = "ASK_"
        FrontendVars = @(
            "ASK_API_BASE_URL", "ASK_AUTH_SECRET", "ASK_AUTH_URL", "ASK_BACKEND_URL",
            "ASK_GOOGLE_CLIENT_ID", "ASK_GOOGLE_SECRET", "ASK_GROQ_API_BASE",
            "ASK_NEXT_PUBLIC_API_URL", "ASK_NEXTAUTH_SECRET", "ASK_NEXTAUTH_URL",
            "NEXT_PUBLIC_AUTH_URL"
        )
    },
    @{
        Name = "reframe"
        DisplayName = "Reframe"
        RootDirectory = "apps/reframe"
        EnvFile = "reframe.env.production"
        Prefix = "REFRAME_"
        FrontendVars = @(
            "REFRAME_API_URL", "REFRAME_AUTH_SECRET", "REFRAME_AUTH_URL",
            "REFRAME_GOOGLE_CLIENT_ID", "REFRAME_GOOGLE_CLIENT_SECRET",
            "REFRAME_NEXT_PUBLIC_API_URL", "REFRAME_NEXT_PUBLIC_FREE_LIMIT",
            "REFRAME_NEXT_PUBLIC_SITE_URL", "REFRAME_NEXTAUTH_SECRET",
            "REFRAME_NEXTAUTH_URL", "REFRAME_RAZORPAY_KEY_ID",
            "REFRAME_RAZORPAY_KEY_SECRET", "REFRAME_RAZORPAY_WEBHOOK_SECRET",
            "REFRAME_RESEND_API_KEY", "NEXT_PUBLIC_AUTH_URL"
        )
    },
    @{
        Name = "sketch2bim"
        DisplayName = "Sketch2BIM"
        RootDirectory = "apps/sketch2bim/frontend"
        EnvFile = "sketch2bim.env.production"
        Prefix = "SKETCH2BIM_"
        FrontendVars = @(
            "SKETCH2BIM_AUTH_SECRET", "SKETCH2BIM_AUTH_URL",
            "SKETCH2BIM_GOOGLE_CLIENT_ID", "SKETCH2BIM_GOOGLE_SECRET",
            "SKETCH2BIM_NEXT_PUBLIC_API_URL", "SKETCH2BIM_NEXT_PUBLIC_FREE_LIMIT",
            "SKETCH2BIM_NEXTAUTH_SECRET", "SKETCH2BIM_NEXTAUTH_URL",
            "NEXT_PUBLIC_AUTH_URL"
        )
    },
    @{
        Name = "kushalsamant-github-io"
        DisplayName = "Portfolio Site"
        RootDirectory = $null
        EnvFile = $null
        Prefix = ""
        FrontendVars = @()
    }
)

# Get Vercel token (fallback to env if not provided, but default is hardcoded)
if (-not $VercelToken -or $VercelToken -eq "") {
    $VercelToken = $env:VERCEL_TOKEN
    if (-not $VercelToken) {
        $VercelToken = "qBiwTlx8W3uA7nhcXT890h0s"  # Hardcoded default
    }
}

# Get repository root
$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $repoRoot) {
    $repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}
$repoRoot = Resolve-Path $repoRoot

# =============================================================================
# Helper Functions
# =============================================================================

function Test-VercelCLI {
    try {
        $vercelVersion = vercel --version 2>&1
        Write-Host "✓ Vercel CLI found: $vercelVersion" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "✗ Vercel CLI not found. Please install: npm install -g vercel" -ForegroundColor Red
        return $false
    }
}

function Test-VercelAuth {
    param([string]$Token, [switch]$SkipLogin)
    
    if ($SkipLogin) {
        return $true
    }
    
    try {
        if ($Token) {
            $env:VERCEL_TOKEN = $Token
        }
        $whoami = vercel whoami 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Authenticated as: $whoami" -ForegroundColor Green
            return $true
        } else {
            throw "Not authenticated"
        }
    } catch {
        Write-Host "Not authenticated. Logging in..." -ForegroundColor Yellow
        if ($Token) {
            $env:VERCEL_TOKEN = $Token
            Write-Host "Using provided Vercel token..." -ForegroundColor Gray
            return $true
        } else {
            vercel login
            if ($LASTEXITCODE -eq 0) {
                return $true
            } else {
                Write-Host "✗ Login failed" -ForegroundColor Red
                return $false
            }
        }
    }
}

function Get-ProjectId {
    param([string]$ProjectName, [string]$Token)
    
    try {
        $headers = @{ "Authorization" = "Bearer $Token" }
        $response = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects" `
            -Method GET -Headers $headers
        $project = $response.projects | Where-Object { $_.name -eq $ProjectName } | Select-Object -First 1
        return $project.id
    } catch {
        Write-Host "  ✗ Failed to get project ID: $_" -ForegroundColor Red
        return $null
    }
}

function Get-RootDirectory {
    param([string]$ProjectId, [string]$Token)
    
    try {
        $headers = @{ "Authorization" = "Bearer $Token" }
        $response = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$ProjectId" `
            -Method GET -Headers $headers
        return $response.rootDirectory
    } catch {
        return $null
    }
}

function Set-RootDirectory {
    param([string]$ProjectId, [string]$RootDirectory, [string]$Token, [switch]$DryRun)
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would set root directory to: $RootDirectory" -ForegroundColor Gray
        return $true
    }
    
    try {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Content-Type" = "application/json"
        }
        $body = @{ rootDirectory = $RootDirectory } | ConvertTo-Json
        Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$ProjectId" `
            -Method PATCH -Headers $headers -Body $body | Out-Null
        return $true
    } catch {
        Write-Host "  ✗ Failed to set root directory: $_" -ForegroundColor Red
        return $false
    }
}

function Parse-EnvFile {
    param([string]$FilePath)
    
    $envVars = @{}
    if (-not (Test-Path $FilePath)) {
        return $envVars
    }
    
    $lines = Get-Content $FilePath
    foreach ($line in $lines) {
        $line = $line.Trim()
        if ($line -eq "" -or $line.StartsWith("#")) { continue }
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
    return $envVars
}

function Sync-EnvVar {
    param(
        [string]$ProjectId, [string]$VarName, [string]$VarValue,
        [string]$EnvType, [string]$Token, [switch]$Force, [switch]$DryRun
    )
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would set: $VarName = $VarValue ($EnvType)" -ForegroundColor Gray
        return $true
    }
    
    try {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Content-Type" = "application/json"
        }
        
        $targets = @()
        switch ($EnvType) {
            "production" { $targets = @("production") }
            "preview" { $targets = @("preview") }
            "development" { $targets = @("development") }
        }
        
        # Check if exists
        try {
            $existing = Invoke-RestMethod -Uri "https://api.vercel.com/v10/projects/$ProjectId/env" `
                -Method GET -Headers $headers
            $existingVar = $existing.envs | Where-Object { $_.key -eq $VarName -and $_.target -contains $EnvType } | Select-Object -First 1
            
            if ($existingVar) {
                if ($Force) {
                    $body = @{ value = $VarValue; target = $targets } | ConvertTo-Json
                    Invoke-RestMethod -Uri "https://api.vercel.com/v10/projects/$ProjectId/env/$($existingVar.id)" `
                        -Method PATCH -Headers $headers -Body $body | Out-Null
                    Write-Host "  ✓ Updated: $VarName" -ForegroundColor Green
                    return $true
                } else {
                    Write-Host "  ⊘ Exists (skip): $VarName (use -Force to update)" -ForegroundColor Gray
                    return $false
                }
            }
        } catch { }
        
        # Create new
        $body = @{
            key = $VarName
            value = $VarValue
            type = "encrypted"
            target = $targets
        } | ConvertTo-Json
        
        Invoke-RestMethod -Uri "https://api.vercel.com/v10/projects/$ProjectId/env" `
            -Method POST -Headers $headers -Body $body | Out-Null
        Write-Host "  ✓ Set: $VarName" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "  ✗ Failed to set $VarName : $_" -ForegroundColor Red
        return $false
    }
}

function Get-ProjectGitInfo {
    param([string]$ProjectId, [string]$Token)
    
    try {
        $headers = @{ "Authorization" = "Bearer $Token" }
        $response = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$ProjectId" `
            -Method GET -Headers $headers
        if ($response.link -and $response.link.type -eq "github") {
            return @{
                Type = "github"
                Repo = $response.link.repo
                Org = $response.link.org
            }
        }
        return $null
    } catch {
        return $null
    }
}

function Trigger-Deployment {
    param([string]$ProjectName, [string]$ProjectId, [string]$TargetEnv, [string]$Token, [switch]$DryRun)
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would trigger $TargetEnv deployment for $ProjectName" -ForegroundColor Gray
        return @{ Success = $true; DeploymentUrl = "https://$ProjectName.vercel.app" }
    }
    
    try {
        $headers = @{
            "Authorization" = "Bearer $Token"
            "Content-Type" = "application/json"
        }
        
        $gitInfo = Get-ProjectGitInfo -ProjectId $ProjectId -Token $Token
        $body = @{
            name = $ProjectName
            project = $ProjectId
            target = $TargetEnv
        }
        
        if ($gitInfo) {
            Write-Host "  Project is connected to Git: $($gitInfo.Org)/$($gitInfo.Repo)" -ForegroundColor Gray
            $body.gitSource = @{
                type = "github"
                repo = $gitInfo.Repo
                ref = "main"
            }
        }
        
        $response = Invoke-RestMethod -Uri "https://api.vercel.com/v13/deployments" `
            -Method POST -Headers $headers -Body ($body | ConvertTo-Json -Depth 10)
        
        Write-Host "  ✓ Deployment triggered successfully" -ForegroundColor Green
        Write-Host "    Deployment ID: $($response.id)" -ForegroundColor Gray
        Write-Host "    URL: https://$($response.url)" -ForegroundColor Gray
        
        return @{
            Success = $true
            DeploymentId = $response.id
            DeploymentUrl = "https://$($response.url)"
            State = $response.readyState
        }
    } catch {
        Write-Host "  ✗ Failed to trigger deployment: $_" -ForegroundColor Red
        return @{ Success = $false; Error = $_.Exception.Message }
    }
}

# =============================================================================
# Action Handlers
# =============================================================================

function Invoke-LinkProjects {
    param([string]$Token, [switch]$SkipLogin, [switch]$DryRun)
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Linking Projects" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    if (-not (Test-VercelCLI)) { exit 1 }
    if (-not (Test-VercelAuth -Token $Token -SkipLogin:$SkipLogin)) { exit 1 }
    
    $projectsToLink = $projects | Where-Object { $_.RootDirectory -ne $null }
    
    foreach ($project in $projectsToLink) {
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        Write-Host "Linking: $($project.DisplayName)" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        
        $projectPath = Join-Path $repoRoot $project.RootDirectory
        if (-not (Test-Path $projectPath)) {
            Write-Host "✗ Directory not found: $projectPath" -ForegroundColor Red
            continue
        }
        
        $vercelDir = Join-Path $projectPath ".vercel"
        if (Test-Path $vercelDir) {
            Write-Host "✓ Already linked" -ForegroundColor Green
            continue
        }
        
        Push-Location $projectPath
        try {
            if ($DryRun) {
                Write-Host "  [DRY RUN] Would link project" -ForegroundColor Gray
            } else {
                vercel link --yes --token $Token 2>&1 | Out-Null
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✓ Linked successfully" -ForegroundColor Green
                } else {
                    Write-Host "✗ Failed to link" -ForegroundColor Red
                }
            }
        } finally {
            Pop-Location
        }
        Write-Host ""
    }
}

function Invoke-SetRootDirectories {
    param([string]$Token, [switch]$DryRun)
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Setting Root Directories" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    if ($DryRun) {
        Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
        Write-Host ""
    }
    
    $projectsToSet = $projects | Where-Object { $_.RootDirectory -ne $null }
    $successCount = 0
    
    foreach ($project in $projectsToSet) {
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        Write-Host "Setting up: $($project.DisplayName)" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        
        $projectId = Get-ProjectId -ProjectName $project.Name -Token $Token
        if (-not $projectId) {
            Write-Host "✗ Skipping - could not get project ID" -ForegroundColor Red
            Write-Host ""
            continue
        }
        
        Write-Host "✓ Project ID: $projectId" -ForegroundColor Green
        
        $currentRootDir = Get-RootDirectory -ProjectId $projectId -Token $Token
        if ($currentRootDir -eq $project.RootDirectory) {
            Write-Host "✓ Root directory already set correctly" -ForegroundColor Green
            $successCount++
        } else {
            if (Set-RootDirectory -ProjectId $projectId -RootDirectory $project.RootDirectory -Token $Token -DryRun:$DryRun) {
                Write-Host "✓ Root directory set successfully" -ForegroundColor Green
                $successCount++
            }
        }
        Write-Host ""
    }
    
    Write-Host "Successfully configured: $successCount / $($projectsToSet.Count) projects" -ForegroundColor $(if ($successCount -eq $projectsToSet.Count) { "Green" } else { "Yellow" })
    Write-Host ""
}

function Invoke-SyncEnvironmentVariables {
    param([string]$Token, [string]$Environment, [switch]$Force, [switch]$DryRun)
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Syncing Environment Variables" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    if ($DryRun) {
        Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
        Write-Host ""
    }
    
    $environments = @()
    switch ($Environment) {
        "all" { $environments = @("production", "preview", "development") }
        default { $environments = @($Environment) }
    }
    
    $projectsToSync = $projects | Where-Object { $_.EnvFile -ne $null }
    $totalVars = 0
    $syncedVars = 0
    
    foreach ($project in $projectsToSync) {
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        Write-Host "Syncing: $($project.DisplayName)" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        
        $envFilePath = Join-Path $repoRoot $project.EnvFile
        $envVars = Parse-EnvFile -FilePath $envFilePath
        
        if ($envVars.Count -eq 0) {
            Write-Host "✗ No environment variables found" -ForegroundColor Red
            continue
        }
        
        # Filter frontend variables
        $frontendVars = @{}
        foreach ($varName in $project.FrontendVars) {
            if ($envVars.ContainsKey($varName)) {
                $frontendVars[$varName] = $envVars[$varName]
            }
        }
        foreach ($key in $envVars.Keys) {
            if ($key -like "NEXT_PUBLIC_*" -or $key -like "$($project.Prefix)NEXT_PUBLIC_*") {
                if (-not $frontendVars.ContainsKey($key)) {
                    $frontendVars[$key] = $envVars[$key]
                }
            }
        }
        
        $projectId = Get-ProjectId -ProjectName $project.Name -Token $Token
        if (-not $projectId) {
            Write-Host "✗ Could not get project ID" -ForegroundColor Red
            continue
        }
        
        foreach ($envType in $environments) {
            Write-Host "Environment: $envType" -ForegroundColor Yellow
            foreach ($varName in $frontendVars.Keys) {
                if ([string]::IsNullOrWhiteSpace($frontendVars[$varName])) { continue }
                $totalVars++
                if (Sync-EnvVar -ProjectId $projectId -VarName $varName -VarValue $frontendVars[$varName] `
                    -EnvType $envType -Token $Token -Force:$Force -DryRun:$DryRun) {
                    $syncedVars++
                }
            }
            Write-Host ""
        }
    }
    
    Write-Host "Total variables processed: $totalVars" -ForegroundColor Gray
    Write-Host "Successfully synced: $syncedVars" -ForegroundColor Gray
    Write-Host ""
}

function Invoke-VerifySetup {
    param([string]$Token, [string]$Environment)
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Verifying Setup" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $environments = @()
    switch ($Environment) {
        "all" { $environments = @("production", "preview", "development") }
        default { $environments = @($Environment) }
    }
    
    $results = @{
        LinkedProjects = 0
        RootDirectoriesCorrect = 0
        EnvVarsChecked = 0
        EnvVarsMissing = 0
    }
    
    foreach ($project in $projects) {
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        Write-Host "Verifying: $($project.DisplayName)" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        Write-Host ""
        
        # Check linking
        if ($project.RootDirectory) {
            $projectPath = Join-Path $repoRoot $project.RootDirectory
            $vercelDir = Join-Path $projectPath ".vercel"
            if (Test-Path $vercelDir) {
                Write-Host "✓ Project is linked" -ForegroundColor Green
                $results.LinkedProjects++
            } else {
                Write-Host "✗ Project is not linked" -ForegroundColor Red
            }
        }
        
        # Check root directory
        if ($project.RootDirectory) {
            $projectId = Get-ProjectId -ProjectName $project.Name -Token $Token
            if ($projectId) {
                $rootDir = Get-RootDirectory -ProjectId $projectId -Token $Token
                if ($rootDir -eq $project.RootDirectory) {
                    Write-Host "✓ Root directory correct: $rootDir" -ForegroundColor Green
                    $results.RootDirectoriesCorrect++
                } else {
                    Write-Host "✗ Root directory mismatch (Expected: $($project.RootDirectory), Actual: $rootDir)" -ForegroundColor Red
                }
            }
        }
        
        # Check environment variables
        if ($project.EnvFile) {
            $envFilePath = Join-Path $repoRoot $project.EnvFile
            $expectedVars = Parse-EnvFile -FilePath $envFilePath
            $expectedFrontendVars = @{}
            foreach ($varName in $project.FrontendVars) {
                if ($expectedVars.ContainsKey($varName)) {
                    $expectedFrontendVars[$varName] = $expectedVars[$varName]
                }
            }
            
            foreach ($envType in $environments) {
                Write-Host "Environment: $envType" -ForegroundColor Yellow
                # Note: Full env var verification would require CLI or additional API calls
                Write-Host "  (Environment variable verification requires CLI)" -ForegroundColor Gray
            }
        }
        Write-Host ""
    }
    
    Write-Host "Summary:" -ForegroundColor Yellow
    Write-Host "  Linked: $($results.LinkedProjects) / $($projects.Count)" -ForegroundColor Gray
    Write-Host "  Root Directories: $($results.RootDirectoriesCorrect) / $($projects.Count)" -ForegroundColor Gray
    Write-Host ""
}

function Invoke-Deploy {
    param([string]$Token, [string]$Project, [string]$Target, [switch]$DryRun)
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Triggering Deployments" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    if ($DryRun) {
        Write-Host "DRY RUN MODE - No deployments will be triggered" -ForegroundColor Yellow
        Write-Host ""
    }
    
    $projectsToDeploy = @()
    if ($Project -eq "all") {
        $projectsToDeploy = $projects
    } else {
        $projectsToDeploy = $projects | Where-Object { $_.Name -eq $Project }
        if ($projectsToDeploy.Count -eq 0) {
            Write-Host "✗ Project not found: $Project" -ForegroundColor Red
            exit 1
        }
    }
    
    $successCount = 0
    $failureCount = 0
    $deployments = @()
    
    foreach ($project in $projectsToDeploy) {
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        Write-Host "Deploying: $($project.DisplayName)" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Cyan
        
        $projectId = Get-ProjectId -ProjectName $project.Name -Token $Token
        if (-not $projectId) {
            Write-Host "✗ Skipping - could not get project ID" -ForegroundColor Red
            $failureCount++
            Write-Host ""
            continue
        }
        
        $result = Trigger-Deployment -ProjectName $project.Name -ProjectId $projectId -TargetEnv $Target -Token $Token -DryRun:$DryRun
        
        if ($result.Success) {
            $successCount++
            $deployments += $result
        } else {
            $failureCount++
        }
        Write-Host ""
    }
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Deployment Summary" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Successful: $successCount" -ForegroundColor $(if ($successCount -gt 0) { "Green" } else { "Gray" })
    Write-Host "Failed: $failureCount" -ForegroundColor $(if ($failureCount -gt 0) { "Red" } else { "Gray" })
    Write-Host ""
    
    if ($deployments.Count -gt 0) {
        Write-Host "Deployment URLs:" -ForegroundColor Yellow
        foreach ($deployment in $deployments) {
            Write-Host "  $($deployment.DeploymentUrl)" -ForegroundColor Gray
        }
    }
    Write-Host ""
}

# =============================================================================
# Main Execution
# =============================================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Vercel Management Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Action: $Action" -ForegroundColor Yellow
Write-Host ""

switch ($Action) {
    "setup" {
        if (-not (Test-VercelCLI)) { exit 1 }
        if (-not (Test-VercelAuth -Token $VercelToken -SkipLogin:$SkipLogin)) { exit 1 }
        
        Invoke-LinkProjects -Token $VercelToken -SkipLogin:$SkipLogin -DryRun:$DryRun
        Invoke-SetRootDirectories -Token $VercelToken -DryRun:$DryRun
        Invoke-SyncEnvironmentVariables -Token $VercelToken -Environment $Environment -Force:$Force -DryRun:$DryRun
        Invoke-VerifySetup -Token $VercelToken -Environment $Environment
    }
    "deploy" {
        Invoke-Deploy -Token $VercelToken -Project $Project -Target $Target -DryRun:$DryRun
    }
    "sync" {
        Invoke-SyncEnvironmentVariables -Token $VercelToken -Environment $Environment -Force:$Force -DryRun:$DryRun
    }
    "verify" {
        Invoke-VerifySetup -Token $VercelToken -Environment $Environment
    }
    "link" {
        if (-not (Test-VercelCLI)) { exit 1 }
        if (-not (Test-VercelAuth -Token $VercelToken -SkipLogin:$SkipLogin)) { exit 1 }
        Invoke-LinkProjects -Token $VercelToken -SkipLogin:$SkipLogin -DryRun:$DryRun
    }
    "rootdir" {
        Invoke-SetRootDirectories -Token $VercelToken -DryRun:$DryRun
    }
}

Write-Host "Complete!" -ForegroundColor Green
Write-Host ""

