@echo off
setlocal
cd /d "%~dp0"

if "%~1"=="" (
    echo Please drag and drop a Markdown file onto this script.
    pause
    exit /b
)

python publisher.py "%~1"
pause
