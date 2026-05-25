@echo off
title ResumeAI - Dev Launch Control
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
echo    🚀 AI-POWERED RESUME TAILORING & ATS OPTIMIZATION CONTROLLER
echo =========================================================================
echo.
echo    Preparing development environments...
echo.

REM 1. Check Frontend configuration and set up .env.local if missing
if not exist "%~dp0frontend\.env.local" (
    echo [Setup] Creating frontend .env.local connection string...
    echo NEXT_PUBLIC_API_URL=http://127.0.0.1:8000/api/v1 > "%~dp0frontend\.env.local"
)

REM 2. Launch Backend FastAPI server
echo [Backend] Launching FastAPI Service on Port 8000...
start "ResumeAI - FastAPI Backend" cmd /k "cd /d %~dp0backend && echo [Backend] Activating virtual environment... && venv\Scripts\activate && echo [Backend] Starting FastAPI Server on Port 8000... && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

REM 3. Launch Frontend Next.js server
echo [Frontend] Launching Next.js Dev Server on Port 3000...
start "ResumeAI - NextJS Frontend" cmd /k "cd /d %~dp0frontend && echo [Frontend] Starting Next.js Dev Server on Port 3000... && npm run dev"

echo.
echo =========================================================================
echo    🎉 CONGRATULATIONS! BOTH DEV SERVERS LAUNCHED SUCCESSFUL!
echo =========================================================================
echo.
echo    - FastAPI Swagger Docs:  http://localhost:8000/docs
echo    - Next.js Developer UI:  http://localhost:3000
echo.
echo    Keep this console open. Press any key to safely exit launch controller.
echo =========================================================================
pause > nul
