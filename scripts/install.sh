#!/bin/bash

# Create project directory
mkdir -p ~/workspace/philips-hue-controller-automation
cd ~/workspace/philips-hue-controller-automation

# Detect OS and install dependencies
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux (Ubuntu/Debian)
    sudo apt-get update
    sudo apt-get install -y python3-venv nodejs npm
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Please install Homebrew first."
        exit 1
    fi
    brew install python3 node
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi

# Set up Python virtual environment
if [ -d "venv" ]; then
    echo "Using existing virtual environment."
else
    echo "Creating new virtual environment."
    python3 -m venv venv
fi
source venv/bin/activate

# Install and configure Homebridge
sudo npm install -g --unsafe-perm homebridge homebridge-hue
mkdir -p homebridge
if [ ! -f homebridge/config.json ]; then
    echo "Please create the homebridge/config.json file with your configuration."
    exit 1
fi

# Install Python packages
pip install -r flask_app/requirements.txt

# Set up cron job for checking phone connection
# crontab entry commented out as it may not be relevant for macOS and Linux setup may vary
# (crontab -l 2>/dev/null; echo "* * * * * /home/pi/workspace/philips-hue-controller-automation/scripts/wifi_monitor.sh") | crontab -

echo "Installation complete. Please configure your Hue bridge IP and username in the respective files."