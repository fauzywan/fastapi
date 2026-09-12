@echo off
setlocal

cd /d "%~dp0"

echo ==========================================
echo  NA WILLA - FASTAPI BACKEND
echo  Python 3.14
echo ==========================================
echo.

set "PYTHON=C:\Users\Iwan Fauzy\AppData\Local\Programs\Python\Python314\python.exe"
set "VENV=venv"

REM ==========================================
REM 1. CEK PYTHON 3.14
REM ==========================================

echo [1/4] Mengecek Python 3.14...

if not exist "%PYTHON%" (
    echo.
    echo [ERROR] Python 3.14 tidak ditemukan:
    echo %PYTHON%
    echo.
    pause
    exit /b 1
)

"%PYTHON%" --version

if errorlevel 1 (
    echo.
    echo [ERROR] Python 3.14 tidak dapat dijalankan.
    pause
    exit /b 1
)


REM ==========================================
REM 2. BUAT VIRTUAL ENVIRONMENT
REM ==========================================

echo.
echo [2/4] Memeriksa virtual environment...

if not exist "%VENV%\Scripts\python.exe" (
    echo Venv belum ada.
    echo Membuat venv menggunakan Python 3.14...
    echo.

    "%PYTHON%" -m venv "%VENV%"

    if errorlevel 1 (
        echo.
        echo [ERROR] Gagal membuat virtual environment.
        pause
        exit /b 1
    )
)

"%VENV%\Scripts\python.exe" --version


REM ==========================================
REM 3. INSTALL DEPENDENCY
REM ==========================================

echo.
echo [3/4] Memastikan dependency terpasang...
echo.

"%VENV%\Scripts\python.exe" -m pip install --upgrade pip

if errorlevel 1 (
    echo.
    echo [ERROR] Upgrade pip gagal.
    pause
    exit /b 1
)

"%VENV%\Scripts\python.exe" -m pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Instalasi dependency gagal.
    pause
    exit /b 1
)


REM ==========================================
REM 4. JALANKAN FASTAPI
REM ==========================================

echo.
echo [4/4] Menjalankan FastAPI...
echo.
echo Backend : http://127.0.0.1:8000
echo Docs    : http://127.0.0.1:8000/docs
echo.

"%VENV%\Scripts\python.exe" -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload


pause
endlocal