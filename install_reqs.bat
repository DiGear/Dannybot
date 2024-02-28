@echo off
echo Installing requirements...
%~dp0\.venv\python -m pip install -r requirements.txt
echo Requirements installed.
pause