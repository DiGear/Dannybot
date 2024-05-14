@echo off
echo modifying requirements...
%~dp0\.venv\python -m pip install -U openai-whisper
echo Requirements modified
pause