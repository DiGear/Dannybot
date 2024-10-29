@echo off
echo modifying requirements...
%~dp0\.venv\python -m pip install pydub
echo Requirements modified
pause