@echo off
:: Helper script - syncs deps then starts the proxy server.
cd /d "%~dp0"

echo Syncing dependencies...
uv sync
if errorlevel 1 (
    echo ERROR: uv sync failed. Check your uv installation.
    pause
    exit /b 1
)

echo Starting free-claude-code proxy server...
uv run python server.py
pause
