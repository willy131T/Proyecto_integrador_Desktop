@echo off
title OdontoCloud API Server (FastAPI)
cd /d "%~dp0"
echo ======================================================
echo   Iniciando Servidor API OdontoCloud (FastAPI)
echo   Documentacion interactiva en: http://127.0.0.1:8000/docs
echo ======================================================
if exist "venv\Scripts\python.exe" (
    "venv\Scripts\python.exe" -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
) else (
    python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
)
pause