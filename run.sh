#!/bin/bash

# Set the environment name
ENV_DIR="venv"

# Check if virtual environment exists
if [ ! -d "$ENV_DIR" ]; then
    echo "Virtual environment not found, creating one..."
    
    # Create the virtual environment
    python3 -m venv $ENV_DIR
    
    echo "Virtual environment created."
fi

# Activate the virtual environment
source $ENV_DIR/bin/activate

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing requirements from requirements.txt..."
    
    # Install the required packages
    pip install -r requirements.txt
    
    echo "Requirements installed."
else
    echo "requirements.txt not found, skipping package installation."
fi

# Run the Flask app in the background
echo "Starting Flask app (app.py)..."
nohup python3 app.py > flask_app.log 2>&1 &

echo "Flask app started in the background. Logs can be found in flask_app.log."

