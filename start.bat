@echo off
color 0A
cls

REM Animated intro - pulse effect
for /L %%i in (1,1,3) do (
    cls
    echo.
    echo   ################################################################
    echo   ##                                                            ##
    echo   ##   N   N   OOO   TTTTT  EEEEE  BBBB    OOO    OOO   K   K  ##
    echo   ##   NN  N  O   O    T    E      B   B  O   O  O   O  K  K   ##
    echo   ##   N N N  O   O    T    EEEE   BBBB   O   O  O   O  KKK    ##
    echo   ##   N  NN  O   O    T    E      B   B  O   O  O   O  K  K   ##
    echo   ##   N   N   OOO     T    EEEEE  BBBB    OOO    OOO   K   K  ##
    echo   ##                                                            ##
    echo   ##              AIP Notebook - Launching...                   ##
    echo   ##              Your AI Development Environment               ##
    echo   ##                                                            ##
    echo   ################################################################
    echo.
    timeout /t 1 /nobreak > nul
)

cls
echo.
echo   ################################################################
echo   ##                                                            ##
echo   ##   N   N   OOO   TTTTT  EEEEE  BBBB    OOO    OOO   K   K  ##
echo   ##   NN  N  O   O    T    E      B   B  O   O  O   O  K  K   ##
echo   ##   N N N  O   O    T    EEEE   BBBB   O   O  O   O  KKK    ##
echo   ##   N  NN  O   O    T    E      B   B  O   O  O   O  K  K   ##
echo   ##   N   N   OOO     T    EEEEE  BBBB    OOO    OOO   K   K  ##
echo   ##                                                            ##
echo   ##              AIP Notebook - Launching...                   ##
echo   ##              Your AI Development Environment               ##
echo   ##                                                            ##
echo   ################################################################
echo.

echo   [*] Starting backend and frontend in WSL...
echo.

REM Start the services in WSL
REM Get current directory in WSL format
for /f "delims=" %%i in ('wsl -d Ubuntu wslpath -u "%cd%"') do set WSL_DIR=%%i

REM Start the services in WSL
start /B wsl -d Ubuntu bash -c "cd \"%WSL_DIR%\" && ./run.sh"

echo   [*] Initializing services...
timeout /t 5 /nobreak > nul

echo.
echo   ################################################################
echo   ##          [OK] Services Started Successfully!               ##
echo   ################################################################
echo.
echo     Frontend: http://localhost:3000
echo     Backend:  http://localhost:8000
echo.
echo   [*] Opening browser...
timeout /t 2 /nobreak > nul

REM Open the browser
start http://localhost:3000

echo.
echo   ################################################################
echo   ##          *** Application is Running! ***                   ##
echo   ################################################################
echo.
echo   Press any key to stop the services...
pause > nul

echo.
echo   [*] Stopping services...
wsl -d Ubuntu bash -c "pkill -f uvicorn; pkill -f vite"

echo   [OK] Services stopped.
color
timeout /t 2 /nobreak > nul
