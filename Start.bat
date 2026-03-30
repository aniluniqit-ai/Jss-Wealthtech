@echo off
title Jss Wealthtech
color 0B
echo.
echo  ========================================
echo   ॥ जय श्री सांवरीया सेठ ि॥
echo   Jss Wealthtech V8.0
echo  ========================================
echo.
echo Starting...
cd /d "%~dp0"
python omai_main.py
if errorlevel 1 (
    echo.
    echo Error! Run Install.bat first.
    pause
)
