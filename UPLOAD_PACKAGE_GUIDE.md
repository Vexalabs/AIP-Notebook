# 🚀 Quick Fix: Upload Installer to Release

## ✅ Your Situation

You have:
- ✅ Release v1.2.1 created on GitHub
- ✅ Installer package created locally (`dist/AIP-Model-Builder-Installer.tar.gz`)
- ❌ Package not uploaded to release yet

**Error message:**
```
Release v1.2.1 exists but has no assets attached. 
Please upload 'AIP-Model-Builder-Installer.tar.gz' to the release.
```

---

## 📦 How to Upload the Package

### Step 1: Locate Your Package

Your installer is here:
```
/opt/docker/4C_Predictions/model_builder_env/dist/AIP-Model-Builder-Installer.tar.gz
```

In Windows, that's:
```
\\wsl.localhost\Ubuntu\opt\docker\4C_Predictions\model_builder_env\dist\AIP-Model-Builder-Installer.tar.gz
```

### Step 2: Go to GitHub Release

1. Open your browser
2. Go to: https://github.com/Vexalabs/AIP-Notebook/releases
3. Find release **v1.2.1**
4. Click **"Edit"** (pencil icon)

### Step 3: Upload the Package

1. Scroll down to **"Attach binaries by dropping them here or selecting them"**
2. Click to browse, or drag and drop
3. Select: `AIP-Model-Builder-Installer.tar.gz`
4. Wait for upload to complete
5. Click **"Update release"**

### Step 4: Test the Update

```bash
# Open your app
./run.sh

# Open browser to http://localhost:3000
# Click "Update Now"
# Should work now! ✅
```

---

## 🖼️ Visual Guide

```
GitHub Release Page
├── Release v1.2.1
│   ├── [Edit] ← Click here
│   │
│   └── Edit Release Page
│       ├── Tag: v1.2.1
│       ├── Title: ...
│       ├── Description: ...
│       │
│       └── Assets
│           ├── [Attach binaries...] ← Click or drag here
│           │
│           └── Upload: AIP-Model-Builder-Installer.tar.gz
│               │
│               └── [Update release] ← Click to save
```

---

## ⚡ Quick Commands

### Copy Package to Desktop (easier to upload)

**Windows:**
```powershell
# Copy to Desktop for easy access
copy "\\wsl.localhost\Ubuntu\opt\docker\4C_Predictions\model_builder_env\dist\AIP-Model-Builder-Installer.tar.gz" "%USERPROFILE%\Desktop\"
```

**Mac/Linux:**
```bash
# Copy to Desktop
cp /opt/docker/4C_Predictions/model_builder_env/dist/AIP-Model-Builder-Installer.tar.gz ~/Desktop/
```

Then upload from Desktop!

---

## ✅ Verification

After uploading, verify:

1. **On GitHub:**
   - Go to release page
   - Should see `AIP-Model-Builder-Installer.tar.gz` under Assets
   - File size should be ~132K

2. **In App:**
   - Refresh browser
   - Click "Update Now"
   - Should start downloading and updating! ✅

---

## 🔍 Troubleshooting

### Wrong filename?
**Must be exactly:** `AIP-Model-Builder-Installer.tar.gz`
- ❌ `AIP-Model-Builder-Installer (1).tar.gz`
- ❌ `installer.tar.gz`
- ✅ `AIP-Model-Builder-Installer.tar.gz`

### Can't find the file?
```bash
# Verify it exists
ls -lh /opt/docker/4C_Predictions/model_builder_env/dist/

# Should show:
# AIP-Model-Builder-Installer.tar.gz (132K)
```

### Upload failed?
- Check internet connection
- Try smaller file (compress more)
- Try different browser

---

## 📝 Future Releases

For next time, remember:

```bash
# 1. Create package
./create-package.sh

# 2. Create tag
git tag v1.2.2
git push origin v1.2.2

# 3. Create release on GitHub
# 4. UPLOAD PACKAGE ← Don't forget!
# 5. Publish release
```

---

## 🎯 Summary

**Current Status:**
- ✅ Release v1.2.1 exists
- ❌ Package not uploaded yet

**Action Needed:**
1. Go to: https://github.com/Vexalabs/AIP-Notebook/releases/tag/v1.2.1
2. Click "Edit"
3. Upload: `dist/AIP-Model-Builder-Installer.tar.gz`
4. Click "Update release"

**Then:**
- Updates will work! ✅

---

**Quick Link:** https://github.com/Vexalabs/AIP-Notebook/releases/tag/v1.2.1

**File Location:** `\\wsl.localhost\Ubuntu\opt\docker\4C_Predictions\model_builder_env\dist\AIP-Model-Builder-Installer.tar.gz`

**Upload it and you're done!** 🚀
