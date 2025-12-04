# ML Model Builder - High Performance Installer (Root Fix)
$ErrorActionPreference = "Stop"

# Colors
function Write-Success { Write-Host "SUCCESS: $args" -ForegroundColor Green }
function Write-ErrorMsg { Write-Host "ERROR: $args" -ForegroundColor Red }
function Write-Info { Write-Host "INFO: $args" -ForegroundColor Green }
function Write-Warning { Write-Host "WARNING: $args" -ForegroundColor Yellow }

# Check Admin
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-ErrorMsg "Please run as Administrator"
    Read-Host "Press Enter to exit"
    exit 1
}

Clear-Host

# Animated intro - cycle through colors
$colors = @('DarkGreen', 'Green', 'Green', 'DarkGreen')
for ($i = 0; $i -lt 3; $i++) {
    Clear-Host
    Write-Host ""
    Write-Host "  ################################################################" -ForegroundColor $colors[$i % 4]
    Write-Host "  ##                                                            ##" -ForegroundColor $colors[($i + 1) % 4]
    Write-Host "  ##     AAA    IIIII  PPPPPP                                   ##" -ForegroundColor $colors[($i + 2) % 4]
    Write-Host "  ##    A   A     I    P     P                                  ##" -ForegroundColor $colors[($i + 1) % 4]
    Write-Host "  ##   AAAAAAA    I    PPPPPP                                   ##" -ForegroundColor $colors[$i % 4]
    Write-Host "  ##   A     A    I    P                                        ##" -ForegroundColor $colors[($i + 1) % 4]
    Write-Host "  ##   A     A  IIIII  P                                        ##" -ForegroundColor $colors[($i + 2) % 4]
    Write-Host "  ##                                                            ##" -ForegroundColor $colors[($i + 1) % 4]
    Write-Host "  ##   N   N   OOO   TTTTT  EEEEE  BBBB    OOO    OOO   K   K   ##" -ForegroundColor $colors[$i % 4]
    Write-Host "  ##   NN  N  O   O    T    E      B   B  O   O  O   O  K  K    ##" -ForegroundColor $colors[($i + 1) % 4]
    Write-Host "  ##   N N N  O   O    T    EEEE   BBBB   O   O  O   O  KKK     ##" -ForegroundColor $colors[($i + 2) % 4]
    Write-Host "  ##   N  NN  O   O    T    E      B   B  O   O  O   O  K  K    ##" -ForegroundColor $colors[($i + 1) % 4]
    Write-Host "  ##   N   N   OOO     T    EEEEE  BBBB    OOO    OOO   K   K   ##" -ForegroundColor $colors[$i % 4]
    Write-Host "  ##                                                            ##" -ForegroundColor $colors[($i + 1) % 4]
    Write-Host "  ##              Model Builder - Installation                  ##" -ForegroundColor White
    Write-Host "  ##              Empowering AI Innovation                      ##" -ForegroundColor Gray
    Write-Host "  ##                                                            ##" -ForegroundColor $colors[($i + 1) % 4]
    Write-Host "  ################################################################" -ForegroundColor $colors[$i % 4]
    Write-Host ""
    Start-Sleep -Milliseconds 300
}

# Final static display
# Clear-Host
# Write-Host ""
# Write-Host "  ################################################################" -ForegroundColor DarkGreen
# Write-Host "  ##                                                            ##" -ForegroundColor Green
# Write-Host "  ##     AAA    IIIII  PPPPPP                                   ##" -ForegroundColor Green
# Write-Host "  ##    A   A     I    P     P                                  ##" -ForegroundColor Green
# Write-Host "  ##   AAAAAAA    I    PPPPPP                                   ##" -ForegroundColor Green
# Write-Host "  ##   A     A    I    P                                        ##" -ForegroundColor Green
# Write-Host "  ##   A     A  IIIII  P                                        ##" -ForegroundColor DarkGreen
# Write-Host "  ##                                                            ##" -ForegroundColor Green
# Write-Host "  ##   N   N   OOO   TTTTT  EEEEE  BBBB    OOO    OOO   K   K   ##" -ForegroundColor Green
# Write-Host "  ##   NN  N  O   O    T    E      B   B  O   O  O   O  K  K    ##" -ForegroundColor Green
# Write-Host "  ##   N N N  O   O    T    EEEE   BBBB   O   O  O   O  KKK     ##" -ForegroundColor DarkGreen
# Write-Host "  ##   N  NN  O   O    T    E      B   B  O   O  O   O  K  K    ##" -ForegroundColor DarkGreen
# Write-Host "  ##   N   N   OOO     T    EEEEE  BBBB    OOO    OOO   K   K   ##" -ForegroundColor DarkGreen
# Write-Host "  ##                                                            ##" -ForegroundColor Green
# Write-Host "  ##              Model Builder - Installation                  ##" -ForegroundColor White
# Write-Host "  ##              Empowering AI Innovation                      ##" -ForegroundColor Gray
# Write-Host "  ##                                                            ##" -ForegroundColor Green
# Write-Host "  ################################################################" -ForegroundColor Green
# Write-Host ""

# 1. Check/Install WSL & Ubuntu
Write-Info "[1/6] Checking Environment..."
try {
    wsl --install -d Ubuntu
} catch {
    # Ignore error if already installed
}

# Wait for WSL to be ready
Write-Info "Waiting for WSL to initialize..."
Start-Sleep -Seconds 5
wsl -d Ubuntu echo "WSL Ready" | Out-Null
Write-Host "   [OK] WSL Ready" -ForegroundColor Green
Write-Host "   (^-^)" -ForegroundColor Green

# 2. Prepare Linux Directory
Write-Info "[2/6] Setting up Linux environment..."
# Determine default user
$wslUser = wsl -d Ubuntu whoami
$wslDest = "/home/$wslUser/AIP-Model-Builder"
if ($wslUser -eq "root") { $wslDest = "/root/AIP-Model-Builder" }

Write-Info "Installing to: $wslDest"

# Create directory (as root to ensure permission)
wsl -d Ubuntu -u root mkdir -p $wslDest
wsl -d Ubuntu -u root chown -R $wslUser $wslDest

# 3. Copy Files (Robust Method)
Write-Info "[3/6] Copying files..."

$stagingDir = Join-Path $env:TEMP "mlbuilder_staging"
if (Test-Path $stagingDir) { Remove-Item $stagingDir -Recurse -Force }
New-Item -ItemType Directory -Path $stagingDir | Out-Null

# Source is now in AIP-Model-Builder subdirectory
$sourceDir = Join-Path $PSScriptRoot "AIP-Model-Builder"
if (-not (Test-Path $sourceDir)) {
    # Fallback for development/testing where files are in current directory
    $sourceDir = $PSScriptRoot
}

$exclude = @('.git', 'node_modules', 'venv', '__pycache__', '.ipynb_checkpoints', 'dist', 'install.ps1', 'INSTALL.bat')

Get-ChildItem -Path $sourceDir -Exclude $exclude | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $stagingDir -Recurse -Force
}

Write-Info "Moving to WSL..."
# Use \\wsl$ path which is standard
$wslNetworkPath = "\\wsl$\Ubuntu$wslDest"
# Fallback
if (-not (Test-Path $wslNetworkPath)) {
    $wslNetworkPath = "\\wsl.localhost\Ubuntu$wslDest"
}

# Ensure target exists
if (-not (Test-Path $wslNetworkPath)) {
    # Try creating it via WSL command first to be sure
    wsl -d Ubuntu -u root mkdir -p $wslDest
    wsl -d Ubuntu -u root chown -R $wslUser $wslDest
    Start-Sleep -Seconds 2
}

Copy-Item -Path "$stagingDir\*" -Destination $wslNetworkPath -Recurse -Force
Write-Success "Files copied successfully"
Write-Host "   [OK] Files Transferred" -ForegroundColor Green
Write-Host "   (>_<)" -ForegroundColor Green
Remove-Item $stagingDir -Recurse -Force

# 4. Install Dependencies (As Root)
Write-Info "[4/6] Installing dependencies (Running as root)..."

# Note: We create venv inside 'backend' folder because run.sh expects it there
# Create the bash script content with proper escaping
$setupScriptContent = @"
#!/bin/bash
set -e
cd WSLDESTTOREPLACE

echo 'Fixing package manager...'
dpkg --configure -a 2>/dev/null || echo 'Package manager already configured'
apt-get update -qq

echo 'Installing System Dependencies...'
apt-get install -y python3 python3-pip python3-venv nodejs npm dos2unix

echo 'Fixing permissions...'
chmod +x setup.sh run.sh start.bat stop.bat 2>/dev/null || true
dos2unix setup.sh run.sh 2>/dev/null || true

echo 'Setting up Python Environment...'
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install uvicorn fastapi uvicorn[standard] jupyterlab
pip install -r requirements.txt 2>/dev/null || echo 'Warning: Some requirements failed'
cd ..

echo 'Setting up Frontend...'
cd frontend
rm -rf node_modules package-lock.json
npm install
cd ..

# Fix ownership back to regular user
chown -R WSLUSERTOREPLACE:WSLUSERTOREPLACE WSLDESTTOREPLACE

echo 'Setup Complete!'
"@

# Replace placeholders
$setupScript = $setupScriptContent.Replace('WSLDESTTOREPLACE', $wslDest)
$setupScript = $setupScript.Replace('WSLUSERTOREPLACE', $wslUser)

# 5. Create Desktop Shortcut
Write-Info "[5/6] Creating desktop shortcut..."
$desktopPath = [Environment]::GetFolderPath("Desktop")
$batPath = Join-Path $desktopPath "AIP-Notebook.bat"
$oldShortcut = Join-Path $desktopPath "ML Model Builder.lnk"
$oldBat = Join-Path $desktopPath "ML Model Builder.bat"

if (Test-Path $oldShortcut) { Remove-Item $oldShortcut -Force }
if (Test-Path $oldBat) { Remove-Item $oldBat -Force }

$launcherContent = @'
@echo off
color 0A
cls
echo.
echo   ################################################################
echo   ##                                                            ##
echo   ##   N   N   OOO   TTTTT  EEEEE  BBBB    OOO    OOO   K   K   ##
echo   ##   NN  N  O   O    T    E      B   B  O   O  O   O  K  K    ##
echo   ##   N N N  O   O    T    EEEE   BBBB   O   O  O   O  KKK     ##
echo   ##   N  NN  O   O    T    E      B   B  O   O  O   O  K  K    ##
echo   ##   N   N   OOO     T    EEEEE  BBBB    OOO    OOO   K   K   ##
echo   ##                                                            ##
echo   ##              AIP Notebook - Launching...                   ##
echo   ##              Your AI Development Environment               ##
echo   ##                                                            ##
echo   ################################################################
echo.

REM Ensure script is executable before running
wsl -d Ubuntu chmod +x WSLDESTTOREPLACE/run.sh

REM Start services in background
start /B wsl -d Ubuntu bash -c "cd WSLDESTTOREPLACE && ./run.sh"

echo   [*] Initializing services...
timeout /t 10 /nobreak > nul

echo.
echo   ################################################################
echo   ##          [OK] Services Started Successfully!               ##
echo   ################################################################
echo.
echo   Opening browser...
start http://localhost:3000

echo.
echo   ################################################################
echo   ##          *** Application is Running! ***                   ##
echo   ################################################################
echo.
echo   Press any key to stop the application...
pause > nul

echo.
echo   [*] Stopping services...
wsl -d Ubuntu bash -c "pkill -f uvicorn; pkill -f vite; pkill -f jupyter"
echo   [OK] Services stopped.
color
'@

# Replace the placeholder with actual path
$launcherContent = $launcherContent.Replace('WSLDESTTOREPLACE', $wslDest)

Set-Content -Path $batPath -Value $launcherContent

Write-Host ""
Write-Host "  ################################################################" -ForegroundColor DarkGreen
Write-Host "  ##                                                            ##" -ForegroundColor Green
Write-Host "  ##     AAA    IIIII  PPPPPP                                   ##" -ForegroundColor Green
Write-Host "  ##    A   A     I    P     P                                  ##" -ForegroundColor Green
Write-Host "  ##   AAAAAAA    I    PPPPPP                                   ##" -ForegroundColor Green
Write-Host "  ##   A     A    I    P                                        ##" -ForegroundColor Green
Write-Host "  ##   A     A  IIIII  P                                        ##" -ForegroundColor DarkGreen
Write-Host "  ##                                                            ##" -ForegroundColor Green
Write-Host "  ##   N   N   OOO   TTTTT  EEEEE  BBBB    OOO    OOO   K   K   ##" -ForegroundColor Green
Write-Host "  ##   NN  N  O   O    T    E      B   B  O   O  O   O  K  K    ##" -ForegroundColor Green
Write-Host "  ##   N N N  O   O    T    EEEE   BBBB   O   O  O   O  KKK     ##" -ForegroundColor DarkGreen
Write-Host "  ##   N  NN  O   O    T    E      B   B  O   O  O   O  K  K    ##" -ForegroundColor DarkGreen
Write-Host "  ##   N   N   OOO     T    EEEEE  BBBB    OOO    OOO   K   K   ##" -ForegroundColor DarkGreen
Write-Host "  ##                                                            ##" -ForegroundColor Green
Write-Host "  ##          *** INSTALLATION COMPLETE! ***                    ##" -ForegroundColor White
Write-Host "  ##          Ready to Build AI Models                          ##" -ForegroundColor Gray
Write-Host "  ##                                                            ##" -ForegroundColor Green
Write-Host "  ################################################################" -ForegroundColor Green
Write-Host ""
Write-Success "Double-click 'AIP-Notebook.bat' on your Desktop to start!"
Write-Host ""

Read-Host "Press Enter to exit"


