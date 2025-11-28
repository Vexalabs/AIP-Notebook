# Files to Remove Before Publishing to Public Git Repository

## 🔴 CRITICAL - Remove Immediately (Security/Sensitive)

### Secrets and Configuration
- `.secrets/` - Contains sensitive API keys and tokens
- `config.json` - May contain user-specific configuration
- `backend/.env` - Environment variables (if exists)
- Any files with API keys, tokens, or credentials

### Test Files with Potential Secrets
- `backend/test_token.py` - May contain test credentials
- `backend/test_repro.py` - Test file, not needed in production

## 🟡 Build Artifacts & Dependencies (Should be in .gitignore)

### Python
- `backend/__pycache__/` - Python bytecode cache
- `backend/routes/__pycache__/` - Python bytecode cache
- `backend/services/__pycache__/` - Python bytecode cache
- `backend/venv/` - Virtual environment (users will create their own)
- `**/*.pyc` - All Python compiled files
- `**/__pycache__/` - All Python cache directories

### Node.js
- `frontend/node_modules/` - NPM dependencies (users will install)
- `frontend/dist/` - Build output
- `frontend/package-lock.json` - Lock file (optional to keep)

### Distribution
- `dist/` - Distribution packages (generated, not source)
- `dist/AIP-Model-Builder-Installer/` - Extracted package
- `dist/AIP-Model-Builder-Installer.tar.gz` - Built package

## 🟢 Documentation Cleanup (Optional - Review First)

### Internal/Development Docs (Keep or Remove Based on Audience)
- `FIX_NO_SAMPLES_FOUND.md` - Internal troubleshooting doc
- `FIX_SUMMARY.md` - Internal fix notes
- `INSTALLATION_FIX_SUMMARY.md` - Internal notes
- `FINAL_PACKAGE_SUMMARY.md` - Internal summary
- `SAMPLE_MODELS_RESTRUCTURE.md` - Internal restructure notes
- `WORKSPACE_STATUS.md` - Internal status doc

### Keep These Docs (User-Facing)
- ✅ `README.md` - Main project documentation
- ✅ `QUICK_START_GUIDE.md` - User guide
- ✅ `SETUP_WIZARD_README.md` - Setup instructions
- ✅ `USER_MANUAL.md` - User manual
- ✅ `DISTRIBUTION_GUIDE.md` - Distribution instructions
- ✅ `UPDATE_GUIDE.md` - Update instructions
- ✅ `PROJECT_COMPLETE.md` - Project overview
- ✅ `docs/` - All documentation in docs folder

## 🔵 Workspace & User Data

### User-Generated Content
- `workspace/` - User workspace (should be empty or have .gitkeep)
- `workspace/sample_models/` - If this contains user data, clean it

## 📋 Recommended .gitignore Additions

Create or update `.gitignore` with:

```gitignore
# Secrets
.secrets/
config.json
*.env
.env.*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Node
node_modules/
dist/
npm-debug.log*
package-lock.json

# Distribution
dist/
build/
*.tar.gz
*.zip

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# User workspace
workspace/*
!workspace/.gitkeep

# Logs
*.log
logs/
```

## 🚀 Cleanup Script

Here's a script to remove all the files:

```bash
#!/bin/bash
# cleanup-for-public.sh

echo "Cleaning up repository for public release..."

# Remove secrets and sensitive files
rm -rf .secrets/
rm -f config.json
rm -f backend/.env
rm -f backend/test_token.py
rm -f backend/test_repro.py

# Remove build artifacts
rm -rf backend/__pycache__/
rm -rf backend/routes/__pycache__/
rm -rf backend/services/__pycache__/
rm -rf backend/venv/
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete

# Remove Node artifacts
rm -rf frontend/node_modules/
rm -rf frontend/dist/

# Remove distribution files
rm -rf dist/

# Remove internal docs (optional - review first)
rm -f FIX_NO_SAMPLES_FOUND.md
rm -f FIX_SUMMARY.md
rm -f INSTALLATION_FIX_SUMMARY.md
rm -f FINAL_PACKAGE_SUMMARY.md
rm -f SAMPLE_MODELS_RESTRUCTURE.md
rm -f WORKSPACE_STATUS.md

# Clean workspace (keep structure, remove user data)
rm -rf workspace/*
touch workspace/.gitkeep

echo "Cleanup complete! Review changes before committing."
```

## ✅ Final Checklist Before Publishing

1. [ ] Run cleanup script
2. [ ] Review and update `.gitignore`
3. [ ] Check for any remaining sensitive data: `git grep -i "api.key\|token\|password\|secret"`
4. [ ] Update `README.md` with public-facing information
5. [ ] Remove any internal comments or TODOs
6. [ ] Test that the repository can be cloned and installed fresh
7. [ ] Add LICENSE file
8. [ ] Add CONTRIBUTING.md (if accepting contributions)
9. [ ] Review all remaining files one more time
10. [ ] Create initial commit with clean state

## 📝 Notes

- **Keep**: All installer scripts (`install.ps1`, `install_mac.sh`, `create-package.sh`)
- **Keep**: All sample models in `sample_models/` (these are templates)
- **Keep**: All documentation in `docs/`
- **Remove**: Anything user-specific or generated during development
- **Remove**: All secrets, credentials, and API keys
