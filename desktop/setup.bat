@echo off
echo ================================
echo  PRAGYA Setup
echo ================================

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ================================
echo  SETUP CHECKLIST
echo ================================
echo.
echo [1] GROQ (free, fast - primary LLM)
echo     - Go to https://console.groq.com
echo     - Sign up free, copy API key
echo     - Paste into ../.env as GROQ_API_KEY
echo.
echo [2] OLLAMA (free, offline - fallback LLM)
echo     - Go to https://ollama.com and install
echo     - Then run: ollama pull llama3
echo     - Runs automatically on localhost:11434
echo.
echo [3] Copy ../.env.example to ../.env and fill in keys
echo.
echo [4] Adding Pragya to Windows startup...
python install_startup.py

echo.
echo [5] Run Pragya now:
echo     python main.py
echo     (or restart your PC — it will start automatically)
echo.
pause
