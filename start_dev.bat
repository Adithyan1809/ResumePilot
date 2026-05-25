@echo off
title ResumePilot - Dev Launcher
color 0b
cls

echo =========================================================================
echo.
echo    ██████╗ ███████╗███████╗██╗   ██╗███╗   ███╗███████╗ █████╗ ██╗
echo    ██╔══██╗██╔════╝██╔════╝██║   ██║████╗ ████║██╔════╝██╔══██╗██║
echo    ██████╔╝█████╗  ███████╗██║   ██║██╔████╔██║█████╗  ███████║██║
echo    ██╔══██╗██╔════╝╚════██║██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██║██║
echo    ██║  ██║███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗██║  ██║██║
echo    ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝
echo.
echo    ResumePilot - Truth-Preserving Resume Intelligence Platform
echo =========================================================================
echo.

REM Clean stray lockfile
if exist "%~dp0package-lock.json" (
    if not exist "%~dp0package.json" (
        del /f /q "%~dp0package-lock.json"
    )
)

echo [1/2] Launching Backend (FastAPI on Port 8000)...
start "ResumePilot - Backend" cmd /k "%~dp0start_backend.bat"

echo [2/2] Launching Frontend (Next.js on Port 3000)...
start "ResumePilot - Frontend" cmd /k "%~dp0start_frontend.bat"

echo.
echo    Both servers are starting up...
echo    Waiting 6 seconds before opening browser...
timeout /t 6 /nobreak > nul

echo    Opening browser at http://localhost:3000
start http://localhost:3000

echo.
echo =========================================================================
echo    FastAPI Docs:   http://localhost:8000/docs
echo    Frontend:       http://localhost:3000
echo    Press any key to close this launcher window.
echo =========================================================================
pause > nul
