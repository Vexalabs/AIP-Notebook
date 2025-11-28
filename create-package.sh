#!/bin/bash
# ML Model Builder - Distribution Package Creator (WSL)

echo "========================================"
echo "  Creating Distribution Package"
echo "========================================"
echo ""

# Create dist directory
DIST_DIR="./dist"
PACKAGE_NAME="AIP-Model-Builder-Installer"
PACKAGE_DIR="$DIST_DIR/$PACKAGE_NAME"
APP_DIR="$PACKAGE_DIR/AIP-Model-Builder"

echo "Creating package directory..."
rm -rf "$DIST_DIR"
mkdir -p "$APP_DIR"

# Files and directories to copy
echo "Copying project files..."

# Copy directories to app subdirectory
for dir in backend frontend workspace docs sample_models; do
    if [ -d "$dir" ]; then
        echo "  Copying $dir/..."
        # Use cp instead of rsync since rsync might be missing
        cp -r "$dir" "$APP_DIR/"
        # Remove excluded directories from destination
        rm -rf "$APP_DIR/$dir/node_modules"
        rm -rf "$APP_DIR/$dir/venv"
        rm -rf "$APP_DIR/$dir/__pycache__"
        rm -rf "$APP_DIR/$dir/.git"
        rm -rf "$APP_DIR/$dir/.ipynb_checkpoints"
    fi
done

# Copy individual files to app subdirectory
for file in .gitignore config.template.json readme.md \
            QUICK_START_GUIDE.md WORKSPACE_STATUS.md SETUP_WIZARD_README.md \
            USER_MANUAL.md DISTRIBUTION_GUIDE.md PROJECT_COMPLETE.md UPDATE_GUIDE.md \
            VERSION setup.sh run.sh start.bat stop.bat install.ps1 install_mac.sh; do
    if [ -f "$file" ]; then
        echo "  Copying $file..."
        cp "$file" "$APP_DIR/"
        # Make scripts executable
        if [[ "$file" == *.sh ]]; then
            chmod +x "$APP_DIR/$file"
        fi
    fi
done

# Create installation instructions at ROOT level
echo "Creating installation instructions..."
cat > "$PACKAGE_DIR/INSTALL_INSTRUCTIONS.txt" << 'EOF'
# ML Model Builder - Installation Package

## Windows Users 🪟

1. Right-click `INSTALL.bat` and select "Run as Administrator"
2. Follow the prompts
3. Launch "ML Model Builder" from your desktop

## Mac Users 🍎

1. Open Terminal
2. Navigate to the AIP-Model-Builder folder
3. Run: `bash install_mac.sh`
4. Launch "AIP Model Builder.command" from your desktop

## First Launch

When you first launch the application:
1. Your browser will open automatically
2. Follow the setup wizard to create a GitHub token
3. Start building models!

## System Requirements

- **Windows:** Windows 10/11 (WSL support)
- **Mac:** macOS 10.15+ (Python 3 & Node.js required)

## Need Help?

Windows Installation:
1. Extract this archive
2. Navigate to the AIP-Model-Builder folder
3. Right-click install.ps1 and select "Run with PowerShell"
   OR run Install_Windows.bat as Administrator

Mac/Linux Installation:
1. Extract this archive
2. Open Terminal in the extracted folder
3. Run: bash Install_Mac.sh

What Gets Installed:
- FastAPI Backend (Python)
- React Frontend (Node.js)
- Jupyter Notebook Environment
- Sample ML Models (Crypto, Soccer)

See AIP-Model-Builder/USER_MANUAL.md for complete documentation.
EOF

# Create Windows installer wrapper at ROOT level
echo "Creating Install_Windows.bat..."
cat > "$PACKAGE_DIR/Install_Windows.bat" <<'EOF'
@echo off
color 0A
cls
echo.
echo   ################################################################
echo   ##                                                            ##
echo   ##              AIP Notebook - Installation                  ##
echo   ##              Empowering AI Innovation                      ##
echo   ##                                                            ##
echo   ################################################################
echo.
echo   Starting installation...
echo.

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Run the PowerShell installer from the AIP-Model-Builder subdirectory
PowerShell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%AIP-Model-Builder\install.ps1"

pause
EOF

# Create Mac installer wrapper at ROOT level
echo "Creating Install_Mac.sh..."
cat > "$PACKAGE_DIR/Install_Mac.sh" <<'EOF'
#!/bin/bash

echo "========================================="
echo "  AIP Notebook - Installation"
echo "  Empowering AI Innovation"
echo "========================================="
echo ""
echo "Starting installation..."
echo ""

# Navigate to app directory and run installer
cd "$(dirname "$0")/AIP-Model-Builder"
bash install_mac.sh

echo ""
echo "Installation complete!"
echo ""
read -p "Press Enter to exit..."
EOF

chmod +x "$PACKAGE_DIR/Install_Mac.sh"

# Create the archive
echo ""
echo "Creating archive..."
cd "$DIST_DIR"
ARCHIVE_FILE="${PACKAGE_NAME}.tar.gz"

if [ -f "$ARCHIVE_FILE" ]; then
    rm "$ARCHIVE_FILE"
fi

tar -czf "$ARCHIVE_FILE" "$PACKAGE_NAME"

cd ..

# Get file size
SIZE=$(du -h "$DIST_DIR/$ARCHIVE_FILE" | cut -f1)

echo ""
echo "========================================"
echo "  Package Created Successfully!"
echo "========================================"
echo ""
echo "Package location:"
echo "  $(pwd)/$DIST_DIR/$ARCHIVE_FILE"
echo ""
echo "Package size: $SIZE"
echo ""
echo "Package structure:"
echo "  ${PACKAGE_NAME}/"
echo "    ├── Install_Windows.bat         (Windows: Run this!)"
echo "    ├── Install_Mac.sh              (Mac: Run this!)"
echo "    ├── INSTALL_INSTRUCTIONS.txt"
echo "    └── AIP-Model-Builder/             (Application files)"
echo ""
echo "To test the installer:"
echo "  Windows:"
echo "    1. Extract the archive (right-click > Extract All)"
echo "    2. Navigate to the extracted folder"
echo "    3. Right-click Install_Windows.bat and Run as Administrator"
echo "  Mac:"
echo "    1. Extract the archive"
echo "    2. Open Terminal and run: bash Install_Mac.sh"
echo ""
echo "The archive is ready for distribution!"
echo ""
