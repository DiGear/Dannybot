@echo off
echo modiying requirements...
%~dp0\.venv\python -m pip freeze
echo Requirements installed.
pause