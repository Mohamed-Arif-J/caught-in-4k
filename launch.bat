@echo off
cd /d "%~dp0"
set "HF_HOME=%~dp0hf_cache"
call .\venv\Scripts\activate.bat
python server.py
pause