@echo off
title Chatbot Setup
echo ==========================================
echo       Starting Chatbot Setup...
echo ==========================================
echo.
echo [1/2] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies. Please check your internet connection or Python installation.
    pause
    exit /b %errorlevel%
)
echo [SUCCESS] Dependencies installed.
echo.
echo [2/2] Launching Streamlit...
echo.
streamlit run chatbot.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Streamlit failed to start.
    pause
    exit /b %errorlevel%
)
pause
