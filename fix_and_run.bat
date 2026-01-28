@echo off
echo Upgrading Google GenAI libraries...
pip install --upgrade langchain-google-genai google-generativeai langchain
echo.
echo Starting Chatbot...
python chatbot.py
pause
