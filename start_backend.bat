@echo off
title ResumePilot - FastAPI Backend
color 0a
cd /d %~dp0backend

echo ============================================================
echo   ResumePilot Backend - FastAPI Server
echo ============================================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo [Backend] Virtual environment activated.
echo [Backend] Starting FastAPI server on http://127.0.0.1:8000
echo [Backend] Press CTRL+C to stop the server.
echo.

REM Start uvicorn directly - all errors will be fully visible
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

echo.
echo [Backend] Server stopped.
pause
