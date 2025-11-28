@echo off
echo ========================================
echo   ML Model Builder - Installer Wrapper
echo ========================================
echo.
echo Requesting Administrator privileges...
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Success: Administrative permissions confirmed.
) else (
    echo Failure: Current permissions inadequate.
    echo Please right-click and select "Run as Administrator".
    pause
    exit
)

echo Running PowerShell Installer...
powershell -ExecutionPolicy Bypass -File "%~dp0install.ps1"

if %errorLevel% neq 0 (
    echo.
    echo Installation failed with error code %errorLevel%
    pause
    exit /b %errorLevel%
)

echo.
echo Installation wrapper finished.
pause
