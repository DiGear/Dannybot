@echo off
echo freezing requirements...
%~dp0\.venv\python -m pip freeze
echo Requirements freezed.
pause