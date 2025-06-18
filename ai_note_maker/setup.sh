#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies using pyproject.toml..."
pip install --upgrade pip
pip install reportlab python-dotenv requests transformers accelerate google-generativeai

echo 
echo "Setup complete."

# to execute, run the following
# $chmod +x setup.sh
# ./ai_note_maker/setup.sh