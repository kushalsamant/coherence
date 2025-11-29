# Vercel Script Consolidation - Implementation Plan

## Overview

This plan documents the consolidation of 9 separate Vercel management scripts into a single unified `scripts/vercel.ps1` script, and outlines all remaining tasks to complete the implementation.

## Context

### What Was Done

1. **Identified Script Redundancy**: Found 9 separate Vercel scripts performing overlapping functions
2. **Created Deployment Script**: Added `deploy-vercel-all.ps1` to trigger deployments via Vercel API
3. **Hardcoded Vercel Token**: Updated all scripts to use hardcoded default token `qBiwTlx8W3uA7nhcXT890h0s`
4. **Consolidated Scripts**: Merged all functionality into single `scripts/vercel.ps1` with 6 action modes
5. **Cleaned Up**: Deleted 9 redundant script files

### Consolidated Script Features

The new `scripts/vercel.ps1` provides:
- **setup**: Complete setup (link projects, set root dirs, sync env, verify)
- **deploy**: Trigger deployments via Vercel API
- **sync**: Sync environment variables from `.env.production` files
- **verify**: Verify Vercel configuration
- **link**: Link projects only
- **rootdir**: Set root directories only

## Remaining Tasks

### 1. Testing & Validation

#### 1.1 Test All Action Modes
**Priority**: High  
**Estimated Time**: 2-3 hours

Test each action mode to ensure functionality:

- [ ] **Test `setup` action**
  - Run: `.\scripts\vercel.ps1 -Action setup -DryRun`
  - Verify: All steps execute without errors
  - Run: `.\scripts\vercel.ps1 -Action setup` (without dry run)
  - Verify: Projects are linked, root dirs set, env vars synced
  - Check: Vercel dashboard confirms changes

- [ ] **Test `deploy` action**
  - Run: `.\scripts\vercel.ps1 -Action deploy -Project ask -DryRun`
  - Verify: Deployment trigger logic works
  - Run: `.\scripts\vercel.ps1 -Action deploy -Project ask`
  - Verify: Deployment is triggered in Vercel
  - Check: Deployment appears in Vercel dashboard
  - Test: Deploy all projects: `.\scripts\vercel.ps1 -Action deploy`

- [ ] **Test `sync` action**
  - Run: `.\scripts\vercel.ps1 -Action sync -Environment production -DryRun`
  - Verify: Shows what would be synced
  - Run: `.\scripts\vercel.ps1 -Action sync -Environment production -Force`
  - Verify: Environment variables are synced to Vercel
  - Check: Vercel dashboard shows updated variables

- [ ] **Test `verify` action**
  - Run: `.\scripts\vercel.ps1 -Action verify`
  - Verify: Correctly reports project status
  - Check: All checks pass for properly configured projects

- [ ] **Test `link` action**
  - Run: `.\scripts\vercel.ps1 -Action link -DryRun`
  - Verify: Shows what would be linked
  - Run: `.\scripts\vercel.ps1 -Action link`
  - Verify: Projects are linked (creates `.vercel` directories)

- [ ] **Test `rootdir` action**
  - Run: `.\scripts\vercel.ps1 -Action rootdir -DryRun`
  - Verify: Shows what would be set
  - Run: `.\scripts\vercel.ps1 -Action rootdir`
  - Verify: Root directories are set in Vercel

#### 1.2 Test Edge Cases
**Priority**: Medium  
**Estimated Time**: 1 hour

- [ ] Test with invalid project name
- [ ] Test with missing Vercel CLI
- [ ] Test with invalid token
- [ ] Test with network errors
- [ ] Test with projects that don't exist in Vercel
- [ ] Test with missing `.env.production` files

#### 1.3 Test Error Handling
**Priority**: Medium  
**Estimated Time**: 30 minutes

- [ ] Verify error messages are clear and actionable
- [ ] Test graceful failure when one project fails
- [ ] Verify dry run mode doesn't make changes
- [ ] Test that script continues on non-critical errors

### 2. Documentation Updates

#### 2.1 Update VERCEL_AUTOMATION.md
**Priority**: High  
**Estimated Time**: 1 hour  
**File**: `.cursor/plans/docs/VERCEL_AUTOMATION.md`

**Current Issues**:
- References old script names (`setup-vercel-all.ps1`, `sync-vercel-env.ps1`, etc.)
- Contains outdated usage examples
- Script reference section lists deleted scripts

**Tasks**:
- [ ] Update all script references to use `vercel.ps1`
- [ ] Update Quick Start section with new command format
- [ ] Update all usage examples:
  ```powershell
  # Old: .\scripts\setup-vercel-all.ps1 -VercelToken "token"
  # New: .\scripts\vercel.ps1 -Action setup
  ```
- [ ] Update Scripts Reference section:
  - Remove references to deleted scripts
  - Document new unified script with all actions
  - Update parameter documentation
- [ ] Add migration guide for users of old scripts
- [ ] Update troubleshooting section with new script paths

#### 2.2 Create Script Usage Documentation
**Priority**: Medium  
**Estimated Time**: 45 minutes  
**File**: `scripts/README.md` or `docs/VERCEL_SCRIPT_USAGE.md`

**Content to Include**:
- [ ] Overview of consolidated script
- [ ] All available actions with descriptions
- [ ] Complete parameter reference
- [ ] Common usage examples:
  ```powershell
  # Complete setup
  .\scripts\vercel.ps1 -Action setup
  
  # Deploy all projects
  .\scripts\vercel.ps1 -Action deploy
  
  # Deploy specific project
  .\scripts\vercel.ps1 -Action deploy -Project ask
  
  # Sync environment variables
  .\scripts\vercel.ps1 -Action sync -Environment all -Force
  
  # Verify configuration
  .\scripts\vercel.ps1 -Action verify
  ```
- [ ] Parameter combinations that work together
- [ ] Troubleshooting common issues
- [ ] Migration from old scripts

#### 2.3 Update Other Documentation References
**Priority**: Low  
**Estimated Time**: 30 minutes

Search and update any other files that reference old scripts:

- [ ] Search codebase for references to old script names
- [ ] Update any README files
- [ ] Update any deployment guides
- [ ] Update any CI/CD documentation
- [ ] Check for references in comments or code

### 3. Script Improvements

#### 3.1 Add Help/Usage Information
**Priority**: Medium  
**Estimated Time**: 30 minutes

- [ ] Add `-Help` or `-?` parameter that displays usage
- [ ] Add inline help comments in script header
- [ ] Display available actions if invalid action provided
- [ ] Show parameter help when `-Help` is used

#### 3.2 Enhance Verification Function
**Priority**: Medium  
**Estimated Time**: 1 hour

**Current Limitation**: Verification function has placeholder comment:
```powershell
# Note: Full env var verification would require CLI or additional API calls
```

**Tasks**:
- [ ] Implement full environment variable verification using Vercel API
- [ ] Compare actual Vercel env vars with `.env.production` files
- [ ] Report missing variables
- [ ] Report mismatched values
- [ ] Show detailed comparison

#### 3.3 Add Project Creation Functionality
**Priority**: Low  
**Estimated Time**: 1-2 hours

**Note**: `create-all-vercel-projects.ps1` was deleted but had project creation logic.

**Tasks**:
- [ ] Add `create` action to `vercel.ps1`
- [ ] Implement project creation via Vercel API
- [ ] Support creating projects from scratch
- [ ] Set root directories during creation
- [ ] Link projects after creation

#### 3.4 Improve Error Messages
**Priority**: Low  
**Estimated Time**: 30 minutes

- [ ] Make error messages more specific
- [ ] Add suggestions for fixing common errors
- [ ] Include relevant Vercel dashboard URLs in error messages
- [ ] Add troubleshooting links

#### 3.5 Add Logging/Output Options
**Priority**: Low  
**Estimated Time**: 45 minutes

- [ ] Add `-Verbose` switch for detailed output
- [ ] Add `-Quiet` switch for minimal output
- [ ] Add `-LogFile` parameter to save output to file
- [ ] Format output for better readability

### 4. Integration & Workflow

#### 4.1 Update CI/CD References
**Priority**: Medium  
**Estimated Time**: 30 minutes

- [ ] Check for GitHub Actions workflows using old scripts
- [ ] Update any CI/CD pipelines to use new script
- [ ] Test CI/CD integration if applicable
- [ ] Document CI/CD usage patterns

#### 4.2 Create Quick Reference Guide
**Priority**: Low  
**Estimated Time**: 20 minutes

Create a simple cheat sheet:

```markdown
# Vercel Script Quick Reference

## Common Commands
- Setup: `.\scripts\vercel.ps1 -Action setup`
- Deploy: `.\scripts\vercel.ps1 -Action deploy`
- Sync Env: `.\scripts\vercel.ps1 -Action sync -Force`
- Verify: `.\scripts\vercel.ps1 -Action verify`
```

### 5. Security Considerations

#### 5.1 Review Hardcoded Token
**Priority**: High  
**Estimated Time**: 15 minutes

**Current State**: Token is hardcoded in script: `qBiwTlx8W3uA7nhcXT890h0s`

**Tasks**:
- [ ] Verify token is not exposed in public repositories
- [ ] Consider if token should be in `.gitignore` patterns
- [ ] Document token rotation procedure
- [ ] Add note about token security in script comments
- [ ] Consider environment variable as primary, hardcoded as fallback

#### 5.2 Add Token Validation
**Priority**: Low  
**Estimated Time**: 30 minutes

- [ ] Validate token format before use
- [ ] Test token validity early in script execution
- [ ] Provide clear error if token is invalid
- [ ] Suggest where to get new token

### 6. Code Quality

#### 6.1 Code Review
**Priority**: Medium  
**Estimated Time**: 1 hour

- [ ] Review consolidated script for:
  - Code duplication
  - Error handling consistency
  - Function organization
  - Variable naming
  - Comments and documentation
- [ ] Refactor if needed
- [ ] Ensure consistent coding style

#### 6.2 Add Unit Tests (Optional)
**Priority**: Low  
**Estimated Time**: 2-3 hours

Consider adding Pester tests for:
- [ ] Helper functions
- [ ] Parameter validation
- [ ] Error handling
- [ ] Mock API calls

### 7. Deployment & Rollout

#### 7.1 Test in Production-Like Environment
**Priority**: High  
**Estimated Time**: 1 hour

- [ ] Test script against actual Vercel projects
- [ ] Verify no breaking changes
- [ ] Test with all project types (ASK, Reframe, Sketch2BIM, Portfolio)
- [ ] Verify deployments actually work

#### 7.2 Create Migration Checklist
**Priority**: Medium  
**Estimated Time**: 30 minutes

For team members or future reference:

- [ ] Document what changed
- [ ] List old script names and their replacements
- [ ] Provide migration examples
- [ ] Note any breaking changes
- [ ] Document new features

### 8. Monitoring & Maintenance

#### 8.1 Add Script Version Tracking
**Priority**: Low  
**Estimated Time**: 15 minutes

- [ ] Add version number to script header
- [ ] Add changelog or version history
- [ ] Document script version in usage output

#### 8.2 Document Maintenance Procedures
**Priority**: Low  
**Estimated Time**: 30 minutes

- [ ] How to update project configurations
- [ ] How to add new projects
- [ ] How to update environment variable lists
- [ ] How to handle Vercel API changes

## Implementation Priority

### Phase 1: Critical (Complete First)
1. Test all action modes (1.1)
2. Update VERCEL_AUTOMATION.md (2.1)
3. Review hardcoded token security (5.1)
4. Test in production-like environment (7.1)

### Phase 2: Important (Complete Soon)
1. Test edge cases (1.2)
2. Test error handling (1.3)
3. Create script usage documentation (2.2)
4. Enhance verification function (3.2)
5. Code review (6.1)

### Phase 3: Nice to Have (Complete When Time Permits)
1. Add help/usage information (3.1)
2. Add project creation functionality (3.3)
3. Improve error messages (3.4)
4. Add logging/output options (3.5)
5. Update other documentation references (2.3)
6. Update CI/CD references (4.1)
7. Create quick reference guide (4.2)
8. Add token validation (5.2)
9. Add unit tests (6.2)
10. Create migration checklist (7.2)
11. Add script version tracking (8.1)
12. Document maintenance procedures (8.2)

## Success Criteria

The consolidation is complete when:

- [x] All old scripts are deleted
- [x] New consolidated script exists
- [ ] All action modes tested and working
- [ ] Documentation updated
- [ ] Script works in production environment
- [ ] Team can use new script without issues
- [ ] No references to old scripts remain

## Estimated Total Time

- **Phase 1 (Critical)**: 4-5 hours
- **Phase 2 (Important)**: 4-5 hours
- **Phase 3 (Nice to Have)**: 8-10 hours
- **Total**: 16-20 hours

## Notes

- The consolidated script maintains all functionality from the 9 deleted scripts
- Token is hardcoded for convenience but can be overridden via parameter or environment variable
- All actions support `-DryRun` for safe testing
- The script follows the same patterns and structure as the original scripts for consistency
- Portfolio site (`kushalsamant-github-io`) is included but has limited configuration (no env file)

## Related Files

- `scripts/vercel.ps1` - Consolidated script
- `.cursor/plans/docs/VERCEL_AUTOMATION.md` - Needs updating
- `ask.env.production` - Contains ASK frontend variables
- `reframe.env.production` - Contains Reframe frontend variables
- `sketch2bim.env.production` - Contains Sketch2BIM frontend variables

## Changelog

### 2024-12-XX - Script Consolidation
- Consolidated 9 Vercel scripts into single `vercel.ps1`
- Hardcoded Vercel token for convenience
- Added deployment trigger functionality
- Deleted redundant scripts:
  - `setup-vercel-all.ps1`
  - `setup-vercel.ps1`
  - `setup-vercel-rootdir.ps1`
  - `sync-vercel-env.ps1`
  - `verify-vercel-setup.ps1`
  - `deploy-vercel-all.ps1`
  - `create-all-vercel-projects.ps1`
  - `delete-and-recreate-vercel-projects.ps1`
  - `reorganize-vercel-projects.ps1`

