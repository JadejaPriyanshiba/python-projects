@echo off
:: Setup script for Windows

:: Create virtual environment
python -m venv .venv

:: Activate virtual environment
call .venv\Scripts\activate.bat

:: Upgrade pip and install dependencies from pyproject.toml
pip install --upgrade pip

echo Setup complete.
pause

:: this can be executed by double clicking or with command prompt