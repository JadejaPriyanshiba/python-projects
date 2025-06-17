Write-Host "Creating virtual environment..."
python -m venv .venv

Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

Write-Host "Installing dependencies using pyproject.toml..."
pip install --upgrade pip
pip install reportlab, python-dotenv, requests

Write-Host "Setup complete."

# You may need to change the PowerShell execution policy:
# $ Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser