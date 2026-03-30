@echo off
title Jss Wealthtech - Build EXE
color 0E
echo Building EXE...
cd /d "%~dp0"
echo %CD% | find /i "system32" >nul
if %errorlevel%==0 (
    echo ERROR: Do NOT run from System32!
    pause
    exit /b 1
)
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
echo Building (3-5 min)...
pyinstaller --noconfirm --onefile --windowed --name "Jss_Wealthtech" --add-data "config;config" --add-data "images;images" --hidden-import=neo_api_client --hidden-import=PIL --hidden-import=pandas --hidden-import=numpy --hidden-import=requests --hidden-import=pyotp --hidden-import=openpyxl --hidden-import=flask --hidden-import=telethon omai_main.py
echo.
if exist "dist\Jss_Wealthtech.exe" (
    echo SUCCESS! EXE created: dist\Jss_Wealthtech.exe
) else (
    echo BUILD FAILED!
)
echo.
pause
