@echo off
echo modifying requirements...
%~dp0\.venv\python -m pip install -U yt-dlp
echo Requirements modified
pause