@echo off
REM Change to repo frontend folder and start Next dev server
cd /d "%~dp0frontend"
echo Installing frontend dependencies...
npm install --no-audit --no-fund
if not exist .env.local (
  echo NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1 > .env.local
)
echo Starting Next dev server...
npm run dev
pause