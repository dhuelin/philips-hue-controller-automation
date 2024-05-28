#!/bin/bash

# Create project directory
mkdir -p ~/workspace/philips-hue-controller-automation
cd ~/workspace/philips-hue-controller-automation

# Install dependencies
sudo apt-get install -y python3-venv nodejs npm

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
pip install --break-system-packages -r flask_app/requirements.txt

# Set up cron job for checking phone connection
#(crontab -l 2>/dev/null; echo "* * * * * /home/pi/workspace/philips-hue-controller-automation/scripts/wifi_monitor.sh") | crontab -

echo "Installation complete. Please configure your Hue bridge IP and username in the respective files."
