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
APP_DIR="$PACKAGE_DIR/MLModelBuilder"

echo "Creating package directory..."
rm -rf "$DIST_DIR"
mkdir -p "$APP_DIR"

# Files and directories to copy
echo "Copying project files..."

# Copy directories to app subdirectory
for dir in backend frontend workspace docs sample_models; do
    if [ -d "$dir" ]; then
        echo "  Copying $dir/..."
        # Exclude node_modules, venv, __pycache__, .git
        rsync -a --exclude='node_modules' --exclude='venv' --exclude='__pycache__' \
              --exclude='.git' --exclude='.ipynb_checkpoints' \
              "$dir" "$APP_DIR/"
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
2. Navigate to the MLModelBuilder folder
3. Run: `bash install_mac.sh`
4. Launch "ML Model Builder.command" from your desktop

## First Launch

When you first launch the application:
1. Your browser will open automatically
2. Follow the setup wizard to create a GitHub token
3. Start building models!

## System Requirements

- **Windows:** Windows 10/11 (WSL support)
- **Mac:** macOS 10.15+ (Python 3 & Node.js required)

## Need Help?

See MLModelBuilder/USER_MANUAL.md for complete documentation.
EOF

# Create Windows installer at ROOT level
echo "Creating Install_Windows.bat..."
cat > "$PACKAGE_DIR/Install_Windows.bat" << 'EOF'
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

REM Handle UNC paths by creating a temporary drive mapping
pushd "%~dp0"

PowerShell -ExecutionPolicy Bypass -File "MLModelBuilder\\install.ps1"

REM Clean up drive mapping
popd

color
pause
EOF

# Copy Mac installer to ROOT level
echo "Creating Install_Mac.sh..."
if [ -f "install_mac.sh" ]; then
    cp install_mac.sh "$PACKAGE_DIR/Install_Mac.sh"
    chmod +x "$PACKAGE_DIR/Install_Mac.sh"
fi

# Create archive (tar.gz which Windows can extract)
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
echo "  AIP-Model-Builder-Installer/"
echo "    ├── Install_Windows.bat         (Windows: Run this!)"
echo "    ├── Install_Mac.sh              (Mac: Run this!)"
echo "    ├── INSTALL_INSTRUCTIONS.txt"
echo "    └── MLModelBuilder/             (Application files)"
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
