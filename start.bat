@echo off
:: ============================================================
::  free-claude-code -- Normal Start
:: ============================================================
cd /d "%~dp0"

echo Starting free-claude-code proxy server...
start "fcc-server" cmd /k "%~dp0_server.bat"

echo Waiting for proxy to be ready...
:wait_loop
timeout /t 1 /nobreak >nul
curl -s -o NUL http://127.0.0.1:8082/health
if errorlevel 1 (
    echo   still waiting...
    goto wait_loop
)

echo Proxy is ready! Launching Claude Code...
uv run python -c "from cli.entrypoints import launch_claude; launch_claude()"
