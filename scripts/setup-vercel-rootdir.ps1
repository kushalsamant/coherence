# =============================================================================
# Vercel Root Directory Setup Script
# =============================================================================
# This script sets root directories for all Vercel projects via API
# Eliminates the need to manually set root directories in the dashboard
# =============================================================================

param(
    [string]$VercelToken = "",
    [switch]$DryRun = $false
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
Write-Host "Vercel Root Directory Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# Check for Vercel token
if (-not $VercelToken) {
    $VercelToken = $env:VERCEL_TOKEN
}

if (-not $VercelToken) {
    Write-Host "✗ Vercel token required. Set -VercelToken parameter or VERCEL_TOKEN environment variable" -ForegroundColor Red
    Write-Host "  Get token from: https://vercel.com/account/tokens" -ForegroundColor Yellow
    exit 1
}

Write-Host "Using Vercel token (ending in ...$($VercelToken.Substring($VercelToken.Length - 4)))" -ForegroundColor Gray
Write-Host ""

# Function to get project ID
function Get-ProjectId {
    param([string]$ProjectName)
    
    try {
        $headers = @{
            "Authorization" = "Bearer $VercelToken"
        }
        
        $response = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects" `
            -Method GET `
            -Headers $headers
        
        $project = $response.projects | Where-Object { $_.name -eq $ProjectName } | Select-Object -First 1
        
        if ($project) {
            return $project.id
        } else {
            Write-Host "  ✗ Project not found: $ProjectName" -ForegroundColor Red
            Write-Host "  Make sure the project exists in Vercel and you have access" -ForegroundColor Yellow
            return $null
        }
    } catch {
        Write-Host "  ✗ Failed to get project ID: $_" -ForegroundColor Red
        return $null
    }
}

# Function to get current root directory
function Get-RootDirectory {
    param(
        [string]$ProjectId
    )
    
    try {
        $headers = @{
            "Authorization" = "Bearer $VercelToken"
        }
        
        $response = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$ProjectId" `
            -Method GET `
            -Headers $headers
        
        return $response.rootDirectory
    } catch {
        return $null
    }
}

# Function to set root directory
function Set-RootDirectory {
    param(
        [string]$ProjectId,
        [string]$ProjectName,
        [string]$RootDirectory
    )
    
    if ($DryRun) {
        Write-Host "  [DRY RUN] Would set root directory to: $RootDirectory" -ForegroundColor Gray
        return $true
    }
    
    try {
        $headers = @{
            "Authorization" = "Bearer $VercelToken"
            "Content-Type" = "application/json"
        }
        
        $body = @{
            rootDirectory = $RootDirectory
        } | ConvertTo-Json
        
        $response = Invoke-RestMethod -Uri "https://api.vercel.com/v9/projects/$ProjectId" `
            -Method PATCH `
            -Headers $headers `
            -Body $body
        
        return $true
    } catch {
        Write-Host "  ✗ Failed to set root directory: $_" -ForegroundColor Red
        if ($_.Exception.Response) {
            $statusCode = $_.Exception.Response.StatusCode.value__
            $errorBody = $_.ErrorDetails.Message
            Write-Host "  Status: $statusCode" -ForegroundColor Red
            Write-Host "  Error: $errorBody" -ForegroundColor Red
        }
        return $false
    }
}

# Process each project
$successCount = 0
$totalCount = $projects.Count

foreach ($project in $projects) {
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    Write-Host "Setting up: $($project.DisplayName)" -ForegroundColor Cyan
    Write-Host "----------------------------------------" -ForegroundColor Cyan
    
    Write-Host "Project: $($project.Name)" -ForegroundColor Yellow
    Write-Host "Target root directory: $($project.RootDirectory)" -ForegroundColor Yellow
    Write-Host ""
    
    # Get project ID
    Write-Host "Getting project ID..." -ForegroundColor Yellow
    $projectId = Get-ProjectId -ProjectName $project.Name
    
    if (-not $projectId) {
        Write-Host "✗ Skipping $($project.Name) - could not get project ID" -ForegroundColor Red
        Write-Host ""
        continue
    }
    
    Write-Host "✓ Project ID: $projectId" -ForegroundColor Green
    Write-Host ""
    
    # Get current root directory
    Write-Host "Checking current root directory..." -ForegroundColor Yellow
    $currentRootDir = Get-RootDirectory -ProjectId $projectId
    
    if ($currentRootDir) {
        Write-Host "Current: $currentRootDir" -ForegroundColor Gray
    } else {
        Write-Host "Current: (not set)" -ForegroundColor Gray
    }
    
    # Check if already set correctly
    if ($currentRootDir -eq $project.RootDirectory) {
        Write-Host "✓ Root directory already set correctly" -ForegroundColor Green
        $successCount++
    } else {
        Write-Host "Setting root directory..." -ForegroundColor Yellow
        
        if (Set-RootDirectory -ProjectId $projectId -ProjectName $project.Name -RootDirectory $project.RootDirectory) {
            Write-Host "✓ Root directory set successfully" -ForegroundColor Green
            
            # Verify it was set
            Start-Sleep -Seconds 1
            $verified = Get-RootDirectory -ProjectId $projectId
            if ($verified -eq $project.RootDirectory) {
                Write-Host "✓ Verified: Root directory is now $verified" -ForegroundColor Green
                $successCount++
            } else {
                Write-Host "⚠ Warning: Root directory may not have been set correctly" -ForegroundColor Yellow
                Write-Host "  Expected: $($project.RootDirectory)" -ForegroundColor Gray
                Write-Host "  Actual: $verified" -ForegroundColor Gray
            }
        } else {
            Write-Host "✗ Failed to set root directory" -ForegroundColor Red
        }
    }
    
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Successfully configured: $successCount / $totalCount projects" -ForegroundColor $(if ($successCount -eq $totalCount) { "Green" } else { "Yellow" })
Write-Host ""

if ($DryRun) {
    Write-Host "This was a dry run. Run without -DryRun to apply changes." -ForegroundColor Yellow
} elseif ($successCount -lt $totalCount) {
    Write-Host "Some projects could not be configured. Check the errors above." -ForegroundColor Yellow
    Write-Host "You may need to:" -ForegroundColor Yellow
    Write-Host "  1. Ensure projects exist in Vercel" -ForegroundColor Gray
    Write-Host "  2. Verify you have admin access to the projects" -ForegroundColor Gray
    Write-Host "  3. Check Vercel API token permissions" -ForegroundColor Gray
}
Write-Host ""

