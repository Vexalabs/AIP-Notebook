# 📦 ML Model Builder - Distribution Guide

## Overview

This guide explains how to package and distribute ML Model Builder to end users.

## 🎯 What Users Get

A one-click installable package that:
1. ✅ Automatically installs all prerequisites (WSL, Python, Node.js)
2. ✅ Sets up the application in their user directory
3. ✅ Creates a desktop shortcut
4. ✅ Launches with a friendly setup wizard
5. ✅ Provides complete Jupyter + GitHub integration

## 📦 Creating the Distribution Package

### Step 1: Run the Package Creator

```powershell
# From the project root
.\create-package.ps1
```

This creates `dist/MLModelBuilder-Installer.zip` containing everything users need.

### Step 2: Upload to Your Website

Upload the ZIP file to your download server. Users will:
1. Download `MLModelBuilder-Installer.zip`
2. Extract to a temporary folder
3. Run `INSTALL.bat`
4. Follow the installer

## 🔧 Installation Process (User Perspective)

### For Users WITH WSL Already Installed:
1. Extract ZIP
2. Run `INSTALL.bat` (as Administrator)
3. Installer completes in ~2-5 minutes
4. Desktop shortcut created
5. Application ready to use

### For Users WITHOUT WSL:
1. Extract ZIP
2. Run `INSTALL.bat` (as Administrator)
3. WSL installs (requires restart)
4. After restart, run `INSTALL.bat` again
5. Installer completes setup
6. Desktop shortcut created
7. Application ready to use

## 🎨 User Experience Flow

```
Download ZIP
    ↓
Extract
    ↓
Run INSTALL.bat
    ↓
[Installer checks WSL]
    ↓
├─ WSL exists? → Continue
└─ No WSL? → Install WSL → Prompt restart → Run installer again
    ↓
Install Python/Node in WSL
    ↓
Copy files to %APPDATA%\MLModelBuilder
    ↓
Run setup.sh
    ↓
Create desktop shortcut
    ↓
[Installation Complete]
    ↓
User double-clicks "ML Model Builder" on desktop
    ↓
Browser opens to http://localhost:3000
    ↓
[Setup Wizard appears if first time]
    ↓
├─ Token exists? → Go to main app
└─ No token? → Setup wizard
    ↓
    Step 1: Welcome
    Step 2: Create GitHub token guide
    Step 3: Enter & validate token
    Step 4: Success!
    ↓
[Main Application]
    ↓
User starts environment → Jupyter launches
    ↓
User builds model in notebook
    ↓
User submits → PR created on GitHub
```

## 📋 System Requirements

Inform users they need:
- **OS:** Windows 10 (2004+) or Windows 11
- **Processor:** 64-bit
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 10GB free space
- **Privileges:** Administrator access for installation

## 🌐 Download Page Template

Here's sample HTML for your website's download page:

```html
<div class="download-section">
  <h2>Download ML Model Builder</h2>
  <p>Build and submit machine learning models with ease!</p>
  
  <a href="/downloads/MLModelBuilder-Installer.zip" class="download-btn">
    Download for Windows (v1.0.0)
  </a>
  
  <h3>System Requirements</h3>
  <ul>
    <li>Windows 10 (Build 19041+) or Windows 11</li>
    <li>4GB RAM (8GB recommended)</li>
    <li>10GB free disk space</li>
  </ul>
  
  <h3>Installation Steps</h3>
  <ol>
    <li>Download the ZIP file above</li>
    <li>Extract to a temporary folder</li>
    <li>Right-click <code>INSTALL.bat</code> and "Run as Administrator"</li>
    <li>Follow the installer prompts</li>
    <li>Launch from desktop shortcut when ready!</li>
  </ol>
  
  <p><strong>First-time users:</strong> The app includes a setup wizard
  to help you create a GitHub token for model submissions.</p>
</div>
```

## 🔐 Security Considerations

### For Distribution:
- ✅ Don't include `.secrets/` directory
- ✅ Don't include any tokens or credentials
- ✅ Use `.gitignore` to prevent accidental inclusion
- ✅ Users create their own tokens via setup wizard

### For Users:
- Tokens are stored locally in `%APPDATA%\MLModelBuilder\.secrets\`
- Never shared or transmitted except to GitHub API
- Users can regenerate tokens anytime via GitHub

## 📊 Distribution Checklist

Before releasing:
- [ ] Run `create-package.ps1`
- [ ] Test installer on clean Windows machine
- [ ] Verify all dependencies install correctly
- [ ] Test first-time setup wizard
- [ ] Test model submission flow
- [ ] Upload ZIP to download server
- [ ] Update website with download link
- [ ] Prepare support documentation
- [ ] Create video tutorial (optional but recommended)

## 🚀 Future Enhancements

### Phase 3 Ideas:
- **Auto-updater:** Check for new versions on startup
- **Offline installer:** Bundle dependencies to work without internet
- **Electron wrapper:** Native desktop app (no browser required)
- **macOS/Linux support:** Cross-platform distribution
- **Cloud deployment:** Web-based version (no installation)

## 📞 Support

Prepare support resources:
1. **FAQ document** - Common issues and solutions
2. **Video walkthrough** - Setup and usage demo
3. **GitHub issues** - Community support
4. **Email support** - Direct help channel

---

## 🎉 You're Ready to Distribute!

Your package includes:
- ✅ Automated installer
- ✅ Setup wizard for first-time users
- ✅ Complete development environment
- ✅ GitHub integration
- ✅ Sample notebooks and models

**Run `create-package.ps1` and start sharing!**
