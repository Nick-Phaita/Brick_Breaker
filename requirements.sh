#!/bin/bash

echo "Setting up the environment and launching the game..."

# Step 1: Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Please install it and try again."
    exit 1
fi

# Ensure Python version is compatible
python3 -c 'import sys; assert sys.version_info >= (3, 7), "Python 3.7 or higher is required."' || exit 1

# Step 2: Create a virtual environment
if [ ! -d ".venv" ]; then
    echo "Creating a virtual environment..."
    python3 -m venv .venv
fi

# Step 3: Activate the virtual environment
echo "Activating the virtual environment..."
source .venv/bin/activate || source .venv/Scripts/activate

# Step 4: Install dependencies
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found. Please create one or specify dependencies."
    exit 1
fi

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt || { echo "Dependency installation failed. Exiting."; exit 1; }

# Step 5: Launch the game
echo "Launching the game..."
python main.py

# Keep the virtual environment active for debugging
echo "The game has exited. You are still in the virtual environment."
echo "Type 'deactivate' to exit."
exec $SHELL
