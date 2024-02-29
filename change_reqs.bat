@echo off
echo modifying requirements...
%~dp0\.venv\python -m pip install onnxruntime-gpu
echo Requirements modified
pause