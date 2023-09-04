@echo off

:: Update packages via requirements.txt
echo Installing requirements...
%~dp0\venv\python -m pip install -r requirements.txt

:: End text
echo Requirements installed.

:: Pause for user input
pause