# ML Model Builder - Distribution Package Creator
# This script creates a distributable package ready for end users

Write-Host "Creating distribution package..." -ForegroundColor Cyan

# Create distribution directory
$distDir = ".\dist"
$packageName = "AIP-Model-Builder-Installer"
$packageDir = Join-Path $distDir $packageName

if (Test-Path $distDir) {
    Remove-Item -Path $distDir -Recurse -Force
}
New-Item -ItemType Directory -Path $packageDir -Force | Out-Null

# Copy necessary files
Write-Host "Copying files..." -ForegroundColor Cyan

$filesToCopy = @(
    "backend",
    "frontend",
    "workspace",
    "docs",
    "sample_models",
    ".gitignore",
    "config.template.json",
    "readme.md",
    "QUICK_START_GUIDE.md",
    "WORKSPACE_STATUS.md",
    "SETUP_WIZARD_README.md",
    "setup.sh",
    "run.sh",
    "start.bat",
    "stop.bat",
    "install.ps1"
)

foreach ($item in $filesToCopy) {
    if (Test-Path $item) {
        Copy-Item -Path $item -Destination $packageDir -Recurse -Force
    }
}

# Create README for the package
$readmeContent = @"
# ML Model Builder - Installation Package

## Quick Start

1. **Extract this folder** to a temporary location
2. **Right-click `Install_Windows.bat`** and select **"Run as Administrator"**
3. **Follow the installer** - it will:
   - Install WSL and Ubuntu (if needed)
   - Install Python and Node.js
   - Set up the application
   - Create a desktop shortcut
4. **Double-click "AIP Notebook"** on your desktop to start!

## System Requirements

- Windows 10 version 2004 or higher (Build 19041 and above)
- 64-bit processor
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space

## First-Time Setup

When you launch the application for the first time:
1. Your browser will open automatically
2. Follow the setup wizard to create a GitHub token
3. Start building and submitting ML models!

## Need Help?

- See `QUICK_START_GUIDE.md` for detailed instructions
- Check `SETUP_WIZARD_README.md` for token setup help
- Read `readme.md` for project overview

## What's Included

- Full ML model development environment
- Jupyter notebook integration
- Automatic GitHub submission
- Sample models and templates

---

**Ready to build ML models? Run `install.ps1` to get started!**
"@

Set-Content -Path (Join-Path $packageDir "INSTALL_INSTRUCTIONS.txt") -Value $readmeContent

# Create a simple batch file to run the installer
# Create a simple batch file to run the installer
$installerBatch = @"
@echo off
color 0A
echo ========================================
echo   AIP Model Builder - Installer
echo ========================================
echo.
echo This will install AIP Model Builder on your system.
echo.
echo Required: Administrator privileges
echo.
pause

PowerShell -ExecutionPolicy Bypass -File "%~dp0MLModelBuilder\install.ps1"
color
"@

Set-Content -Path (Join-Path $packageDir "Install_Windows.bat") -Value $installerBatch

# Create ZIP file
Write-Host "Creating ZIP package..." -ForegroundColor Cyan
$zipPath = Join-Path $distDir "$packageName.zip"

if (Test-Path $zipPath) {
    Remove-Item $zipPath -Force
}

Compress-Archive -Path $packageDir -DestinationPath $zipPath -CompressionLevel Optimal

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  Distribution Package Created!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Package location:" -ForegroundColor Cyan
Write-Host "  $zipPath" -ForegroundColor White
Write-Host ""
Write-Host "Package size:" -ForegroundColor Cyan
$sizeInMB = [math]::Round((Get-Item $zipPath).Length / 1MB, 2)
Write-Host "  $sizeInMB MB" -ForegroundColor White
Write-Host ""
Write-Host "To distribute:" -ForegroundColor Cyan
Write-Host "  1. Upload $packageName.zip to your website" -ForegroundColor White
Write-Host "  2. Users download and extract" -ForegroundColor White
Write-Host "  3. Users run Install_Windows.bat" -ForegroundColor White
Write-Host ""
Write-Host "Press Enter to finish..."
Read-Host
