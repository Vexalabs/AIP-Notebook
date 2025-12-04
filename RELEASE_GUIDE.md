# Creating a GitHub Release for Updates

## 📦 Quick Guide

To enable archive-based updates, you need to create a GitHub release with the installer package attached.

---

## 🚀 Step-by-Step

### 1. Create the Package

```bash
# Navigate to project directory
cd /opt/docker/4C_Predictions/model_builder_env

# Create distribution package
chmod +x create-package.sh
./create-package.sh

# Package created at:
# dist/AIP-Model-Builder-Installer.tar.gz
```

### 2. Update VERSION File

```bash
# Update version (e.g., from 1.0.0 to 1.0.1)
echo "1.0.1" > VERSION

# Commit the change
git add VERSION
git commit -m "Bump version to 1.0.1"
git push origin main
```

### 3. Create Git Tag

```bash
# Create tag
git tag v1.0.1

# Push tag to GitHub
git push origin v1.0.1
```

### 4. Create GitHub Release

1. **Go to GitHub Releases**
   - Navigate to: https://github.com/Vexalabs/AIP-Notebook/releases
   - Click **"Create a new release"**

2. **Fill in Release Details**
   - **Tag:** Select `v1.0.1` (the tag you just pushed)
   - **Title:** `AIP Notebook v1.0.1`
   - **Description:** Add release notes (what's new, bug fixes, etc.)

3. **Upload Installer Package**
   - Click **"Attach binaries"** or drag and drop
   - Upload: `dist/AIP-Model-Builder-Installer.tar.gz`
   - **IMPORTANT:** The filename MUST be exactly `AIP-Model-Builder-Installer.tar.gz`

4. **Publish Release**
   - Click **"Publish release"**

### 5. Test the Update

```bash
# Open your app
./run.sh

# Open browser to http://localhost:3000
# Should see "Update Available: v1.0.1"
# Click "Update Now"
# Should download and install successfully! ✅
```

---

## 📋 Release Checklist

Before creating a release:

- [ ] Update `VERSION` file
- [ ] Test the application locally
- [ ] Create distribution package (`./create-package.sh`)
- [ ] Commit and push changes
- [ ] Create and push Git tag
- [ ] Create GitHub release
- [ ] Upload installer package (exact name: `AIP-Model-Builder-Installer.tar.gz`)
- [ ] Publish release
- [ ] Test update on production installation

---

## 🎯 Example Release Notes

```markdown
## What's New in v1.0.1

### Features
- ✨ Auto-update system with dual Git/Archive support
- 🔄 Real-time update progress tracking
- 💾 Automatic backup before updates

### Improvements
- ⚡ Faster updates for Git-based installations
- 🛡️ Better error handling and validation
- 📝 Improved documentation

### Bug Fixes
- 🐛 Fixed portability issues with hardcoded paths
- 🔧 Fixed update system for production packages

### Installation
Download `AIP-Model-Builder-Installer.tar.gz` and follow the installation instructions.

### Updating
If you're already running v1.0.0, simply click "Update Now" in the application!
```

---

## 🔍 Troubleshooting

### Error: "Update package not found in latest release"

**Cause:** The installer package is not attached to the release.

**Solution:**
1. Go to the release on GitHub
2. Click "Edit release"
3. Upload `AIP-Model-Builder-Installer.tar.gz`
4. Save changes

### Error: "No releases have been published yet"

**Cause:** No GitHub releases exist.

**Solution:**
1. Follow steps above to create first release
2. Make sure to publish (not save as draft)

### Error: "Already running latest version"

**Cause:** VERSION file matches latest release tag.

**Solution:**
1. Update VERSION file to a newer version
2. Create new release with that version

---

## 📊 Version Numbering

Follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR** - Breaking changes (1.0.0 → 2.0.0)
- **MINOR** - New features (1.0.0 → 1.1.0)
- **PATCH** - Bug fixes (1.0.0 → 1.0.1)

**Examples:**
- `1.0.0` - Initial release
- `1.0.1` - Bug fix
- `1.1.0` - New feature (auto-update)
- `2.0.0` - Major rewrite

---

## 🔄 Update Flow

```
Developer creates release
    ↓
Uploads installer package
    ↓
Publishes release
    ↓
User opens app
    ↓
App checks GitHub API
    ↓
Sees v1.0.1 > v1.0.0
    ↓
Shows "Update Available"
    ↓
User clicks "Update Now"
    ↓
Downloads installer package
    ↓
Extracts and applies update
    ↓
Restarts application
    ↓
Now running v1.0.1! ✅
```

---

## 🎯 Quick Commands

```bash
# Full release workflow
echo "1.0.1" > VERSION
git add VERSION
git commit -m "Bump version to 1.0.1"
git push origin main
git tag v1.0.1
git push origin v1.0.1
./create-package.sh

# Then go to GitHub and create release with the package
```

---

## ✅ First Release Setup

If this is your first release:

```bash
# 1. Ensure VERSION file exists
echo "1.0.0" > VERSION

# 2. Create package
./create-package.sh

# 3. Commit everything
git add .
git commit -m "Initial release v1.0.0"
git push origin main

# 4. Create tag
git tag v1.0.0
git push origin v1.0.0

# 5. Go to GitHub and create release
# Upload: dist/AIP-Model-Builder-Installer.tar.gz
```

---

## 📝 Notes

- **Package name MUST be:** `AIP-Model-Builder-Installer.tar.gz`
- **Tag format:** `v1.0.0` (with 'v' prefix)
- **VERSION file:** `1.0.0` (without 'v' prefix)
- **Release must be published** (not draft)

---

**Ready to create your first release!** 🚀
