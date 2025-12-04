# Project Generator Script (PowerShell)
# Generates a new KVSHVL platform project from templates

param(
    [string]$AppName = "",
    [string]$AppDisplayName = "",
    [string]$AppPrefix = "",
    [string]$AppDescription = "",
    [switch]$IncludeFrontend = $true,
    [switch]$IncludeBackend = $true
)

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir
$TemplatesDir = Join-Path $RepoRoot "templates"
$AppsDir = Join-Path $RepoRoot "apps"

# Function to replace placeholders in file
function Replace-Placeholders {
    param(
        [string]$FilePath,
        [string]$AppName,
        [string]$AppDisplayName,
        [string]$AppPrefix,
        [string]$AppDescription
    )
    
    $content = Get-Content -Path $FilePath -Raw
    $content = $content -replace '{{APP_NAME}}', $AppName
    $content = $content -replace '{{APP_DISPLAY_NAME}}', $AppDisplayName
    $content = $content -replace '{{APP_PREFIX}}', $AppPrefix
    $content = $content -replace '{{APP_DESCRIPTION}}', $AppDescription
    Set-Content -Path $FilePath -Value $content -NoNewline
}

# Function to generate project
function Generate-Project {
    param(
        [string]$AppName,
        [string]$AppDisplayName,
        [string]$AppPrefix,
        [string]$AppDescription,
        [bool]$IncludeFrontend,
        [bool]$IncludeBackend
    )
    
    Write-Host "`n=== Generating Project: $AppDisplayName ===" -ForegroundColor Cyan
    
    $ProjectDir = Join-Path $AppsDir $AppName
    
    # Check if project directory already exists
    if (Test-Path $ProjectDir) {
        Write-Host "ERROR: Directory $ProjectDir already exists!" -ForegroundColor Red
        exit 1
    }
    
    New-Item -ItemType Directory -Path $ProjectDir -Force | Out-Null
    
    # Generate frontend
    if ($IncludeFrontend) {
        Write-Host "`nGenerating frontend..." -ForegroundColor Yellow
        $FrontendTemplateDir = Join-Path $TemplatesDir "nextjs-app"
        $FrontendDir = Join-Path $ProjectDir "frontend"
        
        Copy-Item -Path $FrontendTemplateDir -Destination $FrontendDir -Recurse -Force
        
        # Replace placeholders in all files
        Get-ChildItem -Path $FrontendDir -Recurse -File | Where-Object {
            $_.Extension -in @('.ts', '.tsx', '.json', '.md') -or 
            $_.Name -like '*.template'
        } | ForEach-Object {
            Replace-Placeholders -FilePath $_.FullName -AppName $AppName `
                -AppDisplayName $AppDisplayName -AppPrefix $AppPrefix `
                -AppDescription $AppDescription
        }
        
        Write-Host "Frontend generated at $FrontendDir" -ForegroundColor Green
    }
    
    # Generate backend
    if ($IncludeBackend) {
        Write-Host "`nGenerating backend..." -ForegroundColor Yellow
        $BackendTemplateDir = Join-Path $TemplatesDir "fastapi-backend"
        $BackendDir = Join-Path $ProjectDir "backend"
        
        Copy-Item -Path $BackendTemplateDir -Destination $BackendDir -Recurse -Force
        
        # Replace placeholders in all files
        Get-ChildItem -Path $BackendDir -Recurse -File | Where-Object {
            $_.Extension -in @('.py', '.txt', '.md') -or 
            $_.Name -like '*.template'
        } | ForEach-Object {
            Replace-Placeholders -FilePath $_.FullName -AppName $AppName `
                -AppDisplayName $AppDisplayName -AppPrefix $AppPrefix `
                -AppDescription $AppDescription
        }
        
        Write-Host "Backend generated at $BackendDir" -ForegroundColor Green
    }
    
    # Create environment file template
    Write-Host "`nCreating environment file template..." -ForegroundColor Yellow
    $EnvFile = Join-Path $RepoRoot "$AppName.env.production"
    if (-not (Test-Path $EnvFile)) {
        $EnvContent = @"
# ${AppDisplayName} - Production Environment Variables
# Copy this file and fill in the actual values

# Application
${AppPrefix}_APP_NAME=${AppDisplayName}
${AppPrefix}_APP_ENV=production
${AppPrefix}_DEBUG=false

# Database
${AppPrefix}_DATABASE_URL=postgresql://user:password@localhost/${AppName}

# Frontend
${AppPrefix}_FRONTEND_URL=https://${AppName}.kvshvl.in

# CORS
${AppPrefix}_CORS_ORIGINS=https://${AppName}.kvshvl.in,https://www.${AppName}.kvshvl.in

# Razorpay Configuration
${AppPrefix}_RAZORPAY_KEY_ID=your_key_id
${AppPrefix}_RAZORPAY_KEY_SECRET=your_key_secret
${AppPrefix}_RAZORPAY_WEBHOOK_SECRET=your_webhook_secret

# Pricing (in paise)
${AppPrefix}_RAZORPAY_WEEK_AMOUNT=129900
${AppPrefix}_RAZORPAY_MONTH_AMOUNT=349900
${AppPrefix}_RAZORPAY_YEAR_AMOUNT=2999900

# Razorpay Plan IDs
${AppPrefix}_RAZORPAY_PLAN_WEEKLY=plan_xxxxx
${AppPrefix}_RAZORPAY_PLAN_MONTHLY=plan_xxxxx
${AppPrefix}_RAZORPAY_PLAN_YEARLY=plan_xxxxx
"@
        Set-Content -Path $EnvFile -Value $EnvContent
        Write-Host "Environment file template created at $EnvFile" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Environment file $EnvFile already exists, skipping..." -ForegroundColor Yellow
    }
    
    # Create README
    Write-Host "`nCreating project README..." -ForegroundColor Yellow
    $ReadmeFile = Join-Path $ProjectDir "README.md"
    $ReadmeContent = @"
# ${AppDisplayName}

${AppDescription}

## Quick Start

### Frontend Development

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

### Backend Development

\`\`\`bash
cd backend
pip install -r requirements.txt
python -m app.main
\`\`\`

## Project Structure

- \`frontend/\` - Next.js frontend application
- \`backend/\` - FastAPI backend application

## Environment Variables

See \`../../${AppName}.env.production\` for environment variable configuration.

## Documentation

- [Frontend README](frontend/README.md)
- [Backend README](backend/README.md)
"@
    Set-Content -Path $ReadmeFile -Value $ReadmeContent
    Write-Host "README created at $ReadmeFile" -ForegroundColor Green
    
    Write-Host "`n=== Project Generated Successfully ===" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Review and customize the generated code"
    Write-Host "2. Set up environment variables in ${AppName}.env.production"
    Write-Host "3. Install dependencies (npm install / pip install)"
    Write-Host "4. Start development servers"
}

# Main execution
function Main {
    Write-Host "=== KVSHVL Platform Project Generator ===" -ForegroundColor Cyan
    Write-Host ""
    
    # Collect project information if not provided as parameters
    if ([string]::IsNullOrEmpty($AppName)) {
        $AppName = Read-Host "App name (lowercase, no spaces)"
        if ([string]::IsNullOrEmpty($AppName)) {
            Write-Host "ERROR: App name is required!" -ForegroundColor Red
            exit 1
        }
    }
    
    if ([string]::IsNullOrEmpty($AppDisplayName)) {
        $DefaultDisplayName = $AppName.ToUpper()
        $AppDisplayName = Read-Host "App display name [$DefaultDisplayName]"
        if ([string]::IsNullOrEmpty($AppDisplayName)) {
            $AppDisplayName = $DefaultDisplayName
        }
    }
    
    if ([string]::IsNullOrEmpty($AppPrefix)) {
        $DefaultPrefix = $AppName.ToUpper()
        $AppPrefix = Read-Host "App prefix for env vars (uppercase) [$DefaultPrefix]"
        if ([string]::IsNullOrEmpty($AppPrefix)) {
            $AppPrefix = $DefaultPrefix
        }
    }
    
    if ([string]::IsNullOrEmpty($AppDescription)) {
        $AppDescription = Read-Host "App description [A KVSHVL platform application]"
        if ([string]::IsNullOrEmpty($AppDescription)) {
            $AppDescription = "A KVSHVL platform application"
        }
    }
    
    # Confirm
    Write-Host "`n=== Project Configuration ===" -ForegroundColor Cyan
    Write-Host "App Name: $AppName"
    Write-Host "Display Name: $AppDisplayName"
    Write-Host "Prefix: $AppPrefix"
    Write-Host "Description: $AppDescription"
    Write-Host "Frontend: $IncludeFrontend"
    Write-Host "Backend: $IncludeBackend"
    Write-Host ""
    
    $Confirm = Read-Host "Continue? (y/n) [y]"
    if ([string]::IsNullOrEmpty($Confirm)) {
        $Confirm = "y"
    }
    
    if ($Confirm -ne "y" -and $Confirm -ne "Y") {
        Write-Host "Cancelled." -ForegroundColor Yellow
        exit 0
    }
    
    # Generate project
    Generate-Project -AppName $AppName -AppDisplayName $AppDisplayName `
        -AppPrefix $AppPrefix -AppDescription $AppDescription `
        -IncludeFrontend $IncludeFrontend -IncludeBackend $IncludeBackend
}

# Run main function
Main

