@echo off
echo modifying requirements...
%~dp0\.venv\python -m pip uninstall onnxruntime
echo Requirements modified
pause