@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_CMD=python"
py -3.13 --version >nul 2>&1
if not errorlevel 1 set "PYTHON_CMD=py -3.13"

if not exist "venv\Scripts\python.exe" (
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo Gagal membuat venv. Disarankan Python 3.13.
        pause
        exit /b 1
    )
)

"venv\Scripts\python.exe" -m pip install --upgrade pip
"venv\Scripts\python.exe" -m pip install -r requirements.txt

echo.
echo Setup selesai.
pause
endlocal
