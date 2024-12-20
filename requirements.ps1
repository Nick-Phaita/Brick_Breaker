# requirements.ps1

Write-Host "Setting up the environment and launching the game..."

# Step 1: Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install it and try again."
    exit
}

# Step 1.1: Check Python version
$pythonVersion = [version]((python --version).Split()[1])
if ($pythonVersion -lt [version]"3.7.0") {
    Write-Host "Python 3.7 or higher is required. Please update Python and try again."
    exit
}

# Step 2: Create a virtual environment
if (-not (Test-Path -Path "./.venv")) {
    Write-Host "Creating a virtual environment..."
    python -m venv .venv
}

# Step 3: Activate the virtual environment
Write-Host "Activating the virtual environment..."
.\.venv\Scripts\Activate.ps1

# Step 4: Install dependencies
if (-not (Test-Path -Path "./requirements.txt")) {
    Write-Host "requirements.txt not found. Please provide a requirements file."
    exit
}

Write-Host "Installing dependencies..."
try {
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
} catch {
    Write-Host "Error installing dependencies. Please check requirements.txt and try again."
    exit
}

# Step 5: Launch the game
Write-Host "Launching the game..."
try {
    python main.py
} catch {
    Write-Host "An error occurred while launching the game. Please check your code and try again."
    exit
}

# Optional: Keep the virtual environment active for debugging
Write-Host "The game has exited. Type 'deactivate' to exit the virtual environment."
