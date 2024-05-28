#!/bin/bash

export PYTHONPATH=$(pwd)/../flask_app

echo "Choose how to start the server:"
echo "1. Local Network"
echo "2. External Domain"
read -p "Enter your choice [1 or 2]: " choice

if [ "$choice" -eq 1 ]; then
    source ../venv/bin/activate
    python3 ~/app.py
elif [ "$choice" -eq 2 ]; then
    python3 ~/app.py --external
else
    echo "Invalid choice. Please run the script again."
fi
