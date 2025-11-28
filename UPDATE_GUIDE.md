# 🔄 ML Model Builder - Update System

## How Updates Work

The ML Model Builder includes an automatic update checker that:
1. ✅ Checks for new versions on startup
2. ✅ Notifies you when updates are available
3. ✅ Provides download links to the latest version

## Checking for Updates

### Automatic Check
The app automatically checks for updates when you launch it. If a new version is available, you'll see a notification banner.

### Manual Check
You can manually check for updates by calling:
```
GET /api/updates/check
```

Response:
```json
{
  "current_version": "1.0.0",
  "latest_version": "1.1.0",
  "update_available": true,
  "download_url": "https://github.com/...",
  "release_notes": "What's new..."
}
```

## Updating the Application

### Option 1: Simple Reinstall (Recommended)
1. Download the latest `MLModelBuilder-Installer.tar.gz`
2. Extract it
3. Run `INSTALL.bat` as Administrator
4. Your workspace and settings are preserved automatically!

### Option 2: Manual Update (Advanced)
If you want to update without reinstalling:

**On Windows (WSL):**
```bash
cd ~/MLModelBuilder
git pull origin main  # If installed from git
# OR download new files manually
```

**Important:** After manual update, restart the application.

## What Gets Preserved During Updates

✅ **Always Preserved:**
- Your workspace files (`~/MLModelBuilder/workspace/`)
- Your settings (`.secrets/config.json`)
- Your GitHub token
- Your notebooks and models

❌ **Updated (Overwritten):**
- Backend code
- Frontend code
- System scripts
- Dependencies

## Version History

### 1.0.0 (Initial Release)
- ✅ Setup wizard for first-time users
- ✅ Jupyter notebook environment
- ✅ GitHub integration
- ✅ Model submission workflow
- ✅ Cross-platform support (Windows + Mac)
- ✅ Auto-update checker

## For Developers: Releasing Updates

### 1. Update Version Number
Edit `VERSION` file:
```
1.1.0
```

### 2. Create GitHub Release
```bash
git tag v1.1.0
git push origin v1.1.0
```

On GitHub, create a release with:
- Tag: `v1.1.0`
- Title: `Version 1.1.0`
- Description: Release notes
- Attach: `MLModelBuilder-Installer.tar.gz`

### 3. Users Get Notified
The update checker will automatically detect the new release and notify users.

---

**Users will always have the latest features without losing their work!** 🚀
