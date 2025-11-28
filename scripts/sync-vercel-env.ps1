# =============================================================================
# Vercel Environment Variable Sync Script
# =============================================================================
# This script syncs environment variables from .env.production files to Vercel
# Only syncs frontend variables (NEXT_PUBLIC_*, AUTH_*, NEXTAUTH_*, etc.)
# =============================================================================

param(
    [string]$VercelToken = "",
    [ValidateSet("production", "preview", "development", "all")]
    [string]$Environment = "production",
    [switch]$DryRun = $false,
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"

# Project configurations
$projects = @(
    @{
        Name = "ask"
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
Write-Host "Vercel Environment Variable Sync" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

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

# Get Vercel token from environment if not provided
if (-not $VercelToken) {
    $VercelToken = $env:VERCEL_TOKEN
}

# Set token in environment for Vercel CLI
if ($VercelToken) {
    $env:VERCEL_TOKEN = $VercelToken
}

# Check authentication
Write-Host ""
Write-Host "Checking Vercel authentication..." -ForegroundColor Yellow
try {
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
        Write-Host "✗ Not authenticated. Please run: vercel login or provide -VercelToken" -ForegroundColor Red
        exit 1
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

# Function to parse .env file
function Parse-EnvFile {
    param([string]$FilePath)
    
    $envVars = @{}
    
    if (-not (Test-Path $FilePath)) {
        Write-Host "✗ Environment file not found: $FilePath" -ForegroundColor Red
        return $envVars
    }
    
    $lines = Get-Content $FilePath
    foreach ($line in $lines) {
        # Skip comments and empty lines
        $line = $line.Trim()
        if ($line -eq "" -or $line.StartsWith("#")) {
            continue
        }
        
        # Parse KEY=VALUE
        if ($line -match '^([^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            
            # Remove quotes if present
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

# Function to get project ID
function Get-ProjectId {
    param([string]$ProjectName)
    
    if ($VercelToken) {
        try {
            $headers = @{
                "Authorization" = "Bearer $VercelToken"
            }
            $projects = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects" `
                -Method GET `
                -Headers $headers
            $project = $projects.projects | Where-Object { $_.name -eq $ProjectName } | Select-Object -First 1
            return $project.id
        } catch {
            Write-Host "  ✗ Failed to get project ID: $_" -ForegroundColor Red
            return $null
        }
    } else {
        # Use CLI
        try {
            $projectInfo = vercel project ls --json 2>&1 | ConvertFrom-Json
            $project = $projectInfo | Where-Object { $_.name -eq $ProjectName } | Select-Object -First 1
            return $project.id
        } catch {
            return $null
        }
    }
}

# Function to sync environment variable
function Sync-EnvVar {
    param(
        [string]$ProjectName,
        [string]$ProjectId,
        [string]$VarName,
        [string]$VarValue,
        [string]$EnvType
    )
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would set: $VarName = $VarValue ($EnvType)" -ForegroundColor Gray
        return $true
    }
    
    try {
        if ($VercelToken -and $ProjectId) {
            # Use API for non-interactive mode
            $headers = @{
                "Authorization" = "Bearer $VercelToken"
                "Content-Type" = "application/json"
            }
            
            # Map environment type to target array
            $targets = @()
            switch ($EnvType) {
                "production" { $targets = @("production") }
                "preview" { $targets = @("preview") }
                "development" { $targets = @("development") }
            }
            
            # Check if variable exists
            try {
                $existing = Invoke-RestMethod -Uri "https://api.vercel.com/v10/projects/$ProjectId/env" `
                    -Method GET `
                    -Headers $headers
                
                $existingVar = $existing.envs | Where-Object { $_.key -eq $VarName -and $_.target -contains $EnvType } | Select-Object -First 1
                
                if ($existingVar) {
                    if ($Force) {
                        # Update existing variable
                        $body = @{
                            value = $VarValue
                            target = $targets
                        } | ConvertTo-Json
                        
                        Invoke-RestMethod -Uri "https://api.vercel.com/v10/projects/$ProjectId/env/$($existingVar.id)" `
                            -Method PATCH `
                            -Headers $headers `
                            -Body $body | Out-Null
                        
                        Write-Host "  ✓ Updated: $VarName" -ForegroundColor Green
                        return $true
                    } else {
                        Write-Host "  ⊘ Exists (skip): $VarName (use -Force to update)" -ForegroundColor Gray
                        return $false
                    }
                }
            } catch {
                # Variable doesn't exist, continue to create
            }
            
            # Create new variable
            $body = @{
                key = $VarName
                value = $VarValue
                type = "encrypted"
                target = $targets
            } | ConvertTo-Json
            
            Invoke-RestMethod -Uri "https://api.vercel.com/v10/projects/$ProjectId/env" `
                -Method POST `
                -Headers $headers `
                -Body $body | Out-Null
            
            Write-Host "  ✓ Set: $VarName" -ForegroundColor Green
            return $true
        } else {
            # Interactive mode using CLI
            Write-Host "  Setting: $VarName..." -ForegroundColor Yellow
            
            # Use echo to pipe value to vercel env add
            $valueEscaped = $VarValue -replace '"', '\"'
            echo $VarValue | vercel env add $VarName $ProjectName $EnvType 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✓ Set: $VarName" -ForegroundColor Green
                return $true
            } else {
                Write-Host "  ✗ Failed to set: $VarName" -ForegroundColor Red
                Write-Host "  (Try using -VercelToken for automated setup)" -ForegroundColor Gray
                return $false
            }
        }
    } catch {
        Write-Host "  ✗ Failed to set $VarName : $_" -ForegroundColor Red
        return $false
    }
}

# Process each project
$totalVars = 0
$syncedVars = 0

foreach ($project in $projects) {
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    Write-Host "Syncing: $($project.Name)" -ForegroundColor Cyan
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    
    $envFilePath = Join-Path $repoRoot $project.EnvFile
    
    if (-not (Test-Path $envFilePath)) {
        Write-Host "✗ Environment file not found: $envFilePath" -ForegroundColor Red
        continue
    }
    
    Write-Host "Reading: $envFilePath" -ForegroundColor Yellow
    $envVars = Parse-EnvFile -FilePath $envFilePath
    
    if ($envVars.Count -eq 0) {
        Write-Host "✗ No environment variables found" -ForegroundColor Red
        continue
    }
    
    Write-Host "Found $($envVars.Count) variables in file" -ForegroundColor Gray
    
    # Filter for frontend variables
    $frontendVars = @{}
    foreach ($varName in $project.FrontendVars) {
        if ($envVars.ContainsKey($varName)) {
            $frontendVars[$varName] = $envVars[$varName]
        }
    }
    
    # Also include any NEXT_PUBLIC_* variables
    foreach ($key in $envVars.Keys) {
        if ($key -like "NEXT_PUBLIC_*" -or $key -like "$($project.Prefix)NEXT_PUBLIC_*") {
            if (-not $frontendVars.ContainsKey($key)) {
                $frontendVars[$key] = $envVars[$key]
            }
        }
    }
    
    Write-Host "Filtered to $($frontendVars.Count) frontend variables" -ForegroundColor Gray
    Write-Host ""
    
    # Determine which environments to sync
    $environments = @()
    switch ($Environment) {
        "all" { $environments = @("production", "preview", "development") }
        default { $environments = @($Environment) }
    }
    
    # Get project ID once
    Write-Host "Getting project ID..." -ForegroundColor Yellow
    $projectId = Get-ProjectId -ProjectName $project.Name
    if (-not $projectId) {
        Write-Host "✗ Could not get project ID for $($project.Name)" -ForegroundColor Red
        Write-Host "  Make sure the project is linked: vercel link" -ForegroundColor Yellow
        continue
    }
    Write-Host "✓ Project ID: $projectId" -ForegroundColor Green
    Write-Host ""
    
    # Sync variables
    foreach ($envType in $environments) {
        Write-Host "Environment: $envType" -ForegroundColor Yellow
        
        foreach ($varName in $frontendVars.Keys) {
            $varValue = $frontendVars[$varName]
            
            # Skip empty values
            if ([string]::IsNullOrWhiteSpace($varValue)) {
                Write-Host "  ⊘ Skipping empty: $varName" -ForegroundColor Gray
                continue
            }
            
            $totalVars++
            if (Sync-EnvVar -ProjectName $project.Name -ProjectId $projectId -VarName $varName -VarValue $varValue -EnvType $envType) {
                $syncedVars++
            }
        }
        
        Write-Host ""
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Sync Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Total variables processed: $totalVars" -ForegroundColor Gray
Write-Host "Successfully synced: $syncedVars" -ForegroundColor Gray
Write-Host ""

if ($DryRun) {
    Write-Host "This was a dry run. Run without -DryRun to apply changes." -ForegroundColor Yellow
} else {
    Write-Host "Note: Some variables may require manual setup via Vercel dashboard" -ForegroundColor Yellow
    Write-Host "if interactive input is needed or API access is limited." -ForegroundColor Yellow
}
Write-Host ""

