@echo off
echo Installing packages with uv...

set UV_PATH=G:\Shared Drives\GLM\06_PIPELINE\python\uv\uv.exe
set VENV_DIR=G:\Shared Drives\GLM\06_PIPELINE\python\source\venv

:: Navigate to project folder if needed
cd /d G:\Shared drives\GLM\06_PIPELINE\python\source

call "%VENV_DIR%\Scripts\activate.bat"

"%UV_PATH%" pip freeze -r requirements.txt