@echo off
chcp 65001 >nul 2>&1

set "BACKEND_DIR=%~dp0backend"
set "FRONTEND_DIR=%~dp0huiben-qianduan-main"

echo ============================================
echo   HuiZhi BenCao - Start Script
echo ============================================
echo.

echo [1/2] Starting Backend (port 8000)...
cd /d "%BACKEND_DIR%"

if exist "venv\Scripts\python.exe" (
    echo      Using venv...
    start "Backend" cmd /k "venv\Scripts\pip install -r requirements.txt 2>&1 & venv\Scripts\python main.py"
) else (
    echo      Using system Python...
    start "Backend" cmd /k "pip install -r requirements.txt --break-system-packages 2>&1 & python main.py"
)

echo      Waiting 6s for backend...
timeout /t 6 /nobreak >nul

echo [2/2] Starting Frontend (port 5173)...
cd /d "%FRONTEND_DIR%"
start "Frontend" cmd /k "npm run dev"

echo.
echo ============================================
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo   API Docs: http://localhost:8000/docs
echo ============================================
echo.
pause
