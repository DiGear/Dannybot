@echo off
echo modifying requirements...
%~dp0\.venv\python -m pip install -U discord.py[voice]
echo Requirements modified
pause