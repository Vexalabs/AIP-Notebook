# Dual Update System - Git + Archive Support

## ✅ Problem Solved

**Issue:** Production packages don't include `.git` directory, causing "not a git repository" error.

**Solution:** Auto-detect installation type and use appropriate update method.

---

## 🔄 How It Works

### Automatic Detection

```python
# Backend automatically detects installation type
is_git_repo = (app_dir / ".git").exists()

if is_git_repo:
    # Development installation → Git-based update
    perform_git_update()
else:
    # Production installation → Archive-based update
    perform_archive_update()
```

### Two Update Paths

```
┌─────────────────────────────────────┐
│   User Clicks "Update Now"          │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────────────┐
        │ Check for    │
        │ .git folder  │
        └──────┬───────┘
               │
       ┌───────┴───────┐
       │               │
       ▼               ▼
┌─────────────┐  ┌──────────────┐
│ .git EXISTS │  │ NO .git      │
│ (Dev Mode)  │  │ (Prod Mode)  │
└──────┬──────┘  └──────┬───────┘
       │                │
       ▼                ▼
┌─────────────┐  ┌──────────────┐
│ Git Pull    │  │ Download     │
│ Update      │  │ Archive      │
└─────────────┘  └──────────────┘
```

---

## 📋 Installation Types

### Development Installation (Git-Based)

**How Installed:**
```bash
git clone https://github.com/Vexalabs/AIP-Notebook.git
cd AIP-Notebook
./run.sh
```

**Structure:**
```
AIP-Notebook/
├── .git/          ← Git repository
├── backend/
├── frontend/
└── VERSION
```

**Update Method:** Git pull
- Fast (1-5 MB delta)
- Preserves local changes
- Can switch branches

---

### Production Installation (Archive-Based)

**How Installed:**
```bash
# Extract AIP-Model-Builder-Installer.tar.gz
cd AIP-Model-Builder
./run.sh
```

**Structure:**
```
AIP-Model-Builder/
├── backend/       ← No .git folder
├── frontend/
└── VERSION
```

**Update Method:** Download archive
- Downloads full package
- Replaces files (preserves workspace)
- Clean installation

---

## 🎯 Update Behavior

### Git-Based Update (Development)

**Process:**
1. ✅ Validate Git is installed
2. ✅ Create backup
3. ✅ `git stash` (save local changes)
4. ✅ `git pull origin main`
5. ✅ Update dependencies
6. ✅ Restart services

**Advantages:**
- ⚡ Fast (only downloads changes)
- 💾 Preserves uncommitted work
- 🔄 Can rollback with Git
- 🌿 Can switch branches

**Requirements:**
- Git must be installed
- Must have internet connection
- Must be Git repository

---

### Archive-Based Update (Production)

**Process:**
1. ✅ Fetch latest release from GitHub
2. ✅ Create backup
3. ✅ Download installer archive
4. ✅ Extract to temp directory
5. ✅ Copy files (preserve workspace & .secrets)
6. ✅ Update dependencies
7. ✅ Restart services

**Advantages:**
- ✅ Works without Git
- ✅ Clean installation
- ✅ Same as manual install
- ✅ Preserves user data

**Requirements:**
- Internet connection
- Enough disk space
- GitHub release with installer asset

---

## 📊 Comparison

| Feature | Git-Based | Archive-Based |
|---------|-----------|---------------|
| **Speed** | ⚡ Fast (1-5 MB) | 🐢 Slower (50-100 MB) |
| **Requires Git** | ✅ Yes | ❌ No |
| **Preserves Changes** | ✅ Yes (stash) | ⚠️ Only workspace |
| **Clean Install** | ❌ No | ✅ Yes |
| **Rollback** | ✅ Git checkout | ⚠️ From backup |
| **Best For** | Development | Production |

---

## 🧪 Testing

### Test Git-Based Update

```bash
# Clone repository
git clone https://github.com/Vexalabs/AIP-Notebook.git
cd AIP-Notebook

# Run app
./run.sh

# Open browser, click "Update Now"
# Should use Git pull ✓
```

### Test Archive-Based Update

```bash
# Extract production package
tar -xzf AIP-Model-Builder-Installer.tar.gz
cd AIP-Model-Builder-Installer
./Install_Mac.sh  # or Install_Windows.bat

# Run app
./run.sh

# Open browser, click "Update Now"
# Should download archive ✓
```

---

## 🔍 How to Tell Which Method Is Used

### Check Update Response

```bash
# Call update endpoint
curl -X POST http://localhost:8000/api/updates/perform

# Response includes update_type:
{
  "status": "success",
  "message": "...",
  "update_type": "git"      ← Git-based
  # OR
  "update_type": "archive"  ← Archive-based
}
```

### Check Logs

```bash
# Git-based update log
cat update.log
# Shows: "Pulling latest code..."

# Archive-based update log
cat update.log
# Shows: "Starting archive-based update..."
```

---

## 🛠️ Configuration

### Force Archive Update (Even with Git)

If you want to force archive-based updates even in a Git repository:

```python
# In backend/routes/updates.py
# Change line ~287:
is_git_repo = False  # Always use archive-based
```

### Disable Git Updates

If you only want archive-based updates:

```python
# In backend/routes/updates.py
# Change line ~289:
if False:  # Never use Git-based
    return await perform_git_update(app_dir)
else:
    return await perform_archive_update(app_dir)
```

---

## 📝 Update Scripts

### Git-Based Script

```bash
#!/bin/bash
cd "$APP_DIR"
git stash
git fetch origin main
git pull origin main
pip install -r backend/requirements.txt
npm install && npm run build
pkill -f uvicorn && pkill -f vite
./run.sh
```

### Archive-Based Script

```bash
#!/bin/bash
curl -L -o update.tar.gz "$URL"
tar -xzf update.tar.gz
rsync -av --exclude workspace --exclude .secrets SOURCE/ APP/
pip install -r backend/requirements.txt
npm install && npm run build
pkill -f uvicorn && pkill -f vite
./run.sh
```

---

## ✅ Benefits

### For Developers
- ✅ Fast Git-based updates
- ✅ Preserves local changes
- ✅ Can test branches

### For End Users
- ✅ Works without Git
- ✅ Clean installations
- ✅ Same as manual install

### For Both
- ✅ Automatic detection
- ✅ No configuration needed
- ✅ Preserves user data
- ✅ Automatic backup

---

## 🚀 Summary

**The update system now supports both:**

1. **Git-based updates** (development)
   - Fast, efficient
   - Requires Git
   - Preserves changes

2. **Archive-based updates** (production)
   - Works without Git
   - Clean installation
   - Preserves workspace

**Detection is automatic** - no user configuration needed!

---

**Status:** ✅ Dual update system implemented  
**Date:** 2025-12-03
