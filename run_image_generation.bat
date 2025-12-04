@echo off
REM Kalshi Image Generation Service - Windows Batch Wrapper
REM This script runs the image generation service from Windows using WSL

setlocal enabledelayedexpansion

echo ==========================================
echo Kalshi Image Generation Service
echo ==========================================
echo.

REM Check if WSL is available
wsl --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] WSL is not installed or not available
    echo Please install WSL: https://docs.microsoft.com/en-us/windows/wsl/install
    exit /b 1
)

REM Get the WSL path
REM Get the WSL path
for /f "delims=" %%i in ('wsl -d Ubuntu wslpath -u "%cd%"') do set REPO_ROOT=%%i
set "WSL_PATH=%REPO_ROOT%/backend/scripts"

REM Parse command line arguments
set "ARGS="
set "DRY_RUN="
set "MAX_ARTICLES="
set "VERBOSE="

:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="--dry-run" (
    set "DRY_RUN=--dry-run"
    set "ARGS=!ARGS! --dry-run"
)
if /i "%~1"=="--max-articles" (
    set "MAX_ARTICLES=%~2"
    set "ARGS=!ARGS! --max-articles %~2"
    shift
)
if /i "%~1"=="--verbose" (
    set "VERBOSE=--verbose"
    set "ARGS=!ARGS! --verbose"
)
if /i "%~1"=="-h" goto show_help
if /i "%~1"=="--help" goto show_help
shift
goto parse_args
:end_parse

REM Check if .env file exists
if exist "backend\.env" (
    echo [OK] Found .env file
) else (
    echo [WARNING] No .env file found
    echo Please create backend\.env with your configuration
    echo You can copy from backend\env.template
    echo.
)

REM Run the Python script via WSL
echo Starting image generation service...
echo.

wsl -d Ubuntu bash -c "cd \"%WSL_PATH%\" && python3 generate_images.py %ARGS%"

set EXIT_CODE=%errorlevel%

echo.
if %EXIT_CODE% equ 0 (
    echo [SUCCESS] Image generation completed successfully!
) else (
    echo [ERROR] Image generation failed with exit code %EXIT_CODE%
)

exit /b %EXIT_CODE%

:show_help
echo.
echo Usage: run_image_generation.bat [OPTIONS]
echo.
echo Options:
echo   --dry-run              Show what would be processed without processing
echo   --max-articles N       Process at most N articles
echo   --verbose              Enable verbose logging
echo   -h, --help             Show this help message
echo.
echo Environment variables (set in backend\.env):
echo   DB_HOST                Database host
echo   DB_USER                Database user
echo   DB_PASSWORD            Database password
echo   DB_NAME                Database name (default: PMP_Backend)
echo   GCP_PROJECT_ID         GCP Project ID
echo   GCS_BUCKET             GCS bucket (default: kalshi-vs-ai)
echo   GOOGLE_APPLICATION_CREDENTIALS  Path to GCP service account key
echo.
echo Examples:
echo   run_image_generation.bat --dry-run
echo   run_image_generation.bat --max-articles 5
echo   run_image_generation.bat --max-articles 10 --verbose
echo.
exit /b 0
