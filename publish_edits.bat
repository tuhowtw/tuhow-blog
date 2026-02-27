@echo off
cd /d "%~dp0"

echo Adding changes...
git add .

set /p commitMsg="Enter commit message (or press Enter for 'Auto-publish edits'): "
if "%commitMsg%"=="" set commitMsg=Auto-publish edits

echo.
echo Committing...
git commit -m "%commitMsg%"

echo.
echo Pushing to GitHub...
git push

echo.
echo Done! Your site will be updated in ~1 minute.
pause
