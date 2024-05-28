#!/bin/bash

cd ~/workspace/philips-hue-controller-automation

# Activate the virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Please run the install script first."
    exit 1
fi

echo "Choose how to start the server:"
echo "1. Local Network"
echo "2. External Domain"
read -p "Enter your choice [1 or 2]: " choice

if [ "$choice" -eq 1 ]; then
    python3 -m flask_app.app
elif [ "$choice" -eq 2 ]; then
    python3 -m flask_app.app --external
else
    echo "Invalid choice. Please run the script again."
fi
