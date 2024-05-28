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
    export FLASK_APP=flask_app.app
    flask run --host=0.0.0.0 --port=5000
elif [ "$choice" -eq 2 ]; then
    export FLASK_APP=flask_app.app
    flask run --host=$(python3 -c "from flask_app.config import Config; config = Config(); print(config.get_external_domain())") --port=$(python3 -c "from flask_app.config import Config; config = Config(); print(config.get_external_port())")
else
    echo "Invalid choice. Please run the script again."
fi
