@echo off
setlocal

REM Letakkan folder backend ini berdampingan dengan folder frontend.
REM Contoh:
REM project\
REM   frontend\
REM   na_willa_fastapi_backend_ready\

set "BACKEND_DIR=%~dp0"
set "PROJECT_DIR=%~dp0.."
set "FRONTEND_DIR=%PROJECT_DIR%\frontend"

if not exist "%FRONTEND_DIR%\package.json" (
    echo [ERROR] Frontend tidak ditemukan di:
    echo %FRONTEND_DIR%
    echo.
    echo Gunakan run_backend.bat jika hanya ingin menjalankan backend.
    pause
    exit /b 1
)

start "Na Willa - Backend" cmd /k "cd /d ""%BACKEND_DIR%"" && call run_backend.bat"

if not exist "%FRONTEND_DIR%\node_modules" (
    cd /d "%FRONTEND_DIR%"
    call npm install
)

start "Na Willa - Frontend" cmd /k "cd /d ""%FRONTEND_DIR%"" && npm run dev"

endlocal
