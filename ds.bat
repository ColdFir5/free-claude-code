@echo off
set "FCC_ORIGINAL_DIR=%CD%"
pushd "%~dp0"
call start.bat %*
popd
