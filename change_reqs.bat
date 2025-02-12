@echo off
echo modifying requirements...
%~dp0\.venv\python -m pip install yt-dlp -U 
echo Requirements modified
pause