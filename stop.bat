@echo off
echo ========================================
echo   ML Model Builder - Stopping Services
echo ========================================
echo.

echo Stopping backend and frontend...
wsl -d Ubuntu bash -c "pkill -f uvicorn; pkill -f vite; pkill -f jupyter"

echo.
echo Services stopped successfully!
echo.
timeout /t 2 /nobreak > nul
