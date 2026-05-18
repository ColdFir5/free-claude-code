@echo off
:: ============================================================
::  free-claude-code -- Skip Permissions Start
:: ============================================================
cd /d "%~dp0"

curl -s -o NUL http://127.0.0.1:8082/health
if not errorlevel 1 (
    echo Proxy server already running.
    goto launch
)

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

:launch

echo Proxy is ready! Launching Claude Code (skip permissions)...
uv run python -c "import sys; from cli.entrypoints import launch_claude; launch_claude(['--dangerously-skip-permissions'] + sys.argv[1:])" %*
