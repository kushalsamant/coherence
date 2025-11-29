#!/bin/bash
# Project Generator Script
# Generates a new KVSHVL platform project from templates

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
TEMPLATES_DIR="$REPO_ROOT/templates"

# Function to print colored messages
print_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

print_info() {
    echo -e "$1"
}

# Function to prompt for input
prompt_input() {
    local prompt=$1
    local var_name=$2
    local default=$3
    
    if [ -n "$default" ]; then
        read -p "$prompt [$default]: " input
        eval "$var_name=\${input:-$default}"
    else
        read -p "$prompt: " input
        eval "$var_name=\$input"
    fi
}

# Function to replace placeholders in file
replace_placeholders() {
    local file=$1
    local app_name=$2
    local app_display_name=$3
    local app_prefix=$4
    local app_description=$5
    
    # Determine if running on macOS or Linux
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/{{APP_NAME}}/$app_name/g" "$file"
        sed -i '' "s/{{APP_DISPLAY_NAME}}/$app_display_name/g" "$file"
        sed -i '' "s/{{APP_PREFIX}}/$app_prefix/g" "$file"
        sed -i '' "s/{{APP_DESCRIPTION}}/$app_description/g" "$file"
    else
        # Linux
        sed -i "s/{{APP_NAME}}/$app_name/g" "$file"
        sed -i "s/{{APP_DISPLAY_NAME}}/$app_display_name/g" "$file"
        sed -i "s/{{APP_PREFIX}}/$app_prefix/g" "$file"
        sed -i "s/{{APP_DESCRIPTION}}/$app_description/g" "$file"
    fi
}

# Function to generate project
generate_project() {
    local app_name=$1
    local app_display_name=$2
    local app_prefix=$3
    local app_description=$4
    local include_frontend=$5
    local include_backend=$6
    
    local project_dir="$REPO_ROOT/apps/$app_name"
    
    print_info "\n=== Generating Project: $app_display_name ==="
    
    # Create project directory
    if [ -d "$project_dir" ]; then
        print_error "Directory $project_dir already exists!"
        exit 1
    fi
    
    mkdir -p "$project_dir"
    
    # Generate frontend
    if [ "$include_frontend" = "y" ] || [ "$include_frontend" = "Y" ]; then
        print_info "\nGenerating frontend..."
        local frontend_dir="$project_dir/frontend"
        cp -r "$TEMPLATES_DIR/nextjs-app" "$frontend_dir"
        
        # Replace placeholders in all files
        find "$frontend_dir" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.json" -o -name "*.md" -o -name "*.template" \) | while read file; do
            replace_placeholders "$file" "$app_name" "$app_display_name" "$app_prefix" "$app_description"
        done
        
        print_success "Frontend generated at $frontend_dir"
    fi
    
    # Generate backend
    if [ "$include_backend" = "y" ] || [ "$include_backend" = "Y" ]; then
        print_info "\nGenerating backend..."
        local backend_dir="$project_dir/backend"
        cp -r "$TEMPLATES_DIR/fastapi-backend" "$backend_dir"
        
        # Replace placeholders in all files
        find "$backend_dir" -type f \( -name "*.py" -o -name "*.txt" -o -name "*.md" -o -name "*.template" \) | while read file; do
            replace_placeholders "$file" "$app_name" "$app_display_name" "$app_prefix" "$app_description"
        done
        
        print_success "Backend generated at $backend_dir"
    fi
    
    # Create environment file template
    print_info "\nCreating environment file template..."
    local env_file="$REPO_ROOT/${app_name}.env.production"
    if [ ! -f "$env_file" ]; then
        cat > "$env_file" << EOF
# ${app_display_name} - Production Environment Variables
# Copy this file and fill in the actual values

# Application
${app_prefix}_APP_NAME=${app_display_name}
${app_prefix}_APP_ENV=production
${app_prefix}_DEBUG=false

# Database
${app_prefix}_DATABASE_URL=postgresql://user:password@localhost/${app_name}

# Frontend
${app_prefix}_FRONTEND_URL=https://${app_name}.kvshvl.in

# CORS
${app_prefix}_CORS_ORIGINS=https://${app_name}.kvshvl.in,https://www.${app_name}.kvshvl.in

# Razorpay Configuration
${app_prefix}_RAZORPAY_KEY_ID=your_key_id
${app_prefix}_RAZORPAY_KEY_SECRET=your_key_secret
${app_prefix}_RAZORPAY_WEBHOOK_SECRET=your_webhook_secret

# Pricing (in paise)
${app_prefix}_RAZORPAY_WEEK_AMOUNT=129900
${app_prefix}_RAZORPAY_MONTH_AMOUNT=349900
${app_prefix}_RAZORPAY_YEAR_AMOUNT=2999900

# Razorpay Plan IDs
${app_prefix}_RAZORPAY_PLAN_WEEK=plan_xxxxx
${app_prefix}_RAZORPAY_PLAN_MONTH=plan_xxxxx
${app_prefix}_RAZORPAY_PLAN_YEAR=plan_xxxxx
EOF
        print_success "Environment file template created at $env_file"
    else
        print_warning "Environment file $env_file already exists, skipping..."
    fi
    
    # Create README
    print_info "\nCreating project README..."
    local readme_file="$project_dir/README.md"
    cat > "$readme_file" << EOF
# ${app_display_name}

${app_description}

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

See \`../../${app_name}.env.production\` for environment variable configuration.

## Documentation

- [Frontend README](frontend/README.md)
- [Backend README](backend/README.md)
EOF
    print_success "README created at $readme_file"
    
    print_success "\n=== Project Generated Successfully ==="
    print_info "\nNext steps:"
    print_info "1. Review and customize the generated code"
    print_info "2. Set up environment variables in ${app_name}.env.production"
    print_info "3. Install dependencies (npm install / pip install)"
    print_info "4. Start development servers"
}

# Main execution
main() {
    print_info "=== KVSHVL Platform Project Generator ==="
    print_info ""
    
    # Collect project information
    prompt_input "App name (lowercase, no spaces)" APP_NAME ""
    if [ -z "$APP_NAME" ]; then
        print_error "App name is required!"
        exit 1
    fi
    
    prompt_input "App display name" APP_DISPLAY_NAME "$(echo $APP_NAME | tr '[:lower:]' '[:upper:]')"
    
    prompt_input "App prefix for env vars (uppercase)" APP_PREFIX "$(echo $APP_NAME | tr '[:lower:]' '[:upper:]')"
    
    prompt_input "App description" APP_DESCRIPTION "A KVSHVL platform application"
    
    prompt_input "Include frontend? (y/n)" INCLUDE_FRONTEND "y"
    
    prompt_input "Include backend? (y/n)" INCLUDE_BACKEND "y"
    
    if [ "$INCLUDE_FRONTEND" != "y" ] && [ "$INCLUDE_FRONTEND" != "Y" ] && \
       [ "$INCLUDE_BACKEND" != "y" ] && [ "$INCLUDE_BACKEND" != "Y" ]; then
        print_error "At least one of frontend or backend must be included!"
        exit 1
    fi
    
    # Confirm
    print_info "\n=== Project Configuration ==="
    print_info "App Name: $APP_NAME"
    print_info "Display Name: $APP_DISPLAY_NAME"
    print_info "Prefix: $APP_PREFIX"
    print_info "Description: $APP_DESCRIPTION"
    print_info "Frontend: $INCLUDE_FRONTEND"
    print_info "Backend: $INCLUDE_BACKEND"
    print_info ""
    
    prompt_input "Continue? (y/n)" CONFIRM "y"
    
    if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
        print_info "Cancelled."
        exit 0
    fi
    
    # Generate project
    generate_project "$APP_NAME" "$APP_DISPLAY_NAME" "$APP_PREFIX" "$APP_DESCRIPTION" "$INCLUDE_FRONTEND" "$INCLUDE_BACKEND"
}

# Run main function
main

