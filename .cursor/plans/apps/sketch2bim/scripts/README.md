# Utility Scripts

This directory contains utility scripts for deployment, maintenance, and development tasks.

## Scripts Overview

### Payment Management

#### `create_razorpay_plans.py`
**Purpose:** Creates Razorpay subscription plans in your Razorpay account.

**When to use:**
- Initial setup of Razorpay integration
- After creating a new Razorpay account
- When adding new subscription tiers

**Usage:**
```bash
# From project root
python scripts/create_razorpay_plans.py

# Or from backend directory
cd backend
python ../scripts/create_razorpay_plans.py
```

**Requirements:**
- Razorpay API keys in `.env.production` or `.env.test`
- Backend dependencies installed (`pip install -r backend/requirements.txt`)

**What it does:**
- Creates subscription plans for Day, Week, Month, and Year tiers
- Outputs plan IDs that need to be added to environment variables

---

#### `delete_razorpay_plan.py`
**Purpose:** Helper script to identify and delete unused Razorpay plans.

**When to use:**
- When cleaning up unused subscription plans
- After discontinuing a subscription tier

**Usage:**
```bash
python scripts/delete_razorpay_plan.py
```

**Note:** Razorpay doesn't allow deleting plans via API. This script identifies plans that need to be deleted manually from the Razorpay dashboard.

---

### Environment Management

#### `reorganize-env.ps1`
**Purpose:** PowerShell script to reorganize and format environment variable files for development.

**When to use:**
- When `.env` files become messy or unorganized
- Before committing environment variable templates
- When standardizing environment variable format

**Usage:**
```powershell
# From project root
.\scripts\reorganize-env.ps1
```

**What it does:**
- Sorts environment variables alphabetically
- Groups related variables together
- Formats for readability
- Creates backup of original file

---

#### `reorganize-env-production.ps1`
**Purpose:** PowerShell script to reorganize production environment variable files.

**When to use:**
- When organizing production `.env.production` files
- Before deployment
- When standardizing production configuration

**Usage:**
```powershell
.\scripts\reorganize-env-production.ps1
```

**Note:** Be careful when modifying production environment files. Always backup first.

---

### Maintenance

#### `clean_todolist.py`
**Purpose:** Cleans up `todolist.txt` files by removing noise and irrelevant content.

**When to use:**
- When `todolist.txt` becomes cluttered with non-project content
- Before committing todo lists to version control
- Periodic maintenance

**Usage:**
```bash
python scripts/clean_todolist.py
```

**What it does:**
- Filters out non-project related content
- Removes URLs, meeting notes, and other noise
- Keeps only code-related and project-specific todos
- Outputs cleaned file to `todolist.cleaned.txt`

**Requirements:**
- `todolist.txt` file in project root

---

## Script Categories

### Deployment Scripts
- `create_razorpay_plans.py` - Payment gateway setup
- `delete_razorpay_plan.py` - Payment cleanup

### Environment Scripts
- `reorganize-env.ps1` - Development environment organization
- `reorganize-env-production.ps1` - Production environment organization

### Maintenance Scripts
- `clean_todolist.py` - Todo list cleanup

---

## Running Scripts

### Python Scripts
All Python scripts require backend dependencies:

```bash
# Install dependencies first
cd backend
pip install -r requirements.txt

# Then run scripts from project root
python scripts/script_name.py
```

### PowerShell Scripts
PowerShell scripts can be run directly:

```powershell
# From project root
.\scripts\script_name.ps1
```

---

## Adding New Scripts

When adding new utility scripts:

1. **Place in `scripts/` directory**
2. **Add documentation** to this README
3. **Include usage instructions** in script docstring
4. **Add error handling** for missing dependencies
5. **Test on both Windows and Unix** if cross-platform

---

## Best Practices

1. **Always backup** before running scripts that modify files
2. **Test in development** before using in production
3. **Check dependencies** before running scripts
4. **Document changes** made by scripts
5. **Use version control** - commit scripts but not generated files

---

## Troubleshooting

### Python Scripts

**Import errors:**
```bash
# Make sure backend dependencies are installed
cd backend
pip install -r requirements.txt
```

**Environment variable errors:**
- Check that `.env.production` or `.env.test` exists
- Verify required variables are set
- Check file paths are correct

### PowerShell Scripts

**Execution policy errors:**
```powershell
# Allow script execution (one-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**File not found errors:**
- Ensure you're running from project root
- Check file paths in script match your directory structure

