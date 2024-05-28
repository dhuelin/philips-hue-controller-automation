#!/bin/bash

# Update and upgrade system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3-pip nodejs npm nginx certbot python3-certbot-nginx

# Install and configure Homebridge
sudo npm install -g --unsafe-perm homebridge homebridge-hue
mkdir -p ~/.homebridge
cp ../homebridge/config.json ~/.homebridge/config.json

# Install Python packages
pip3 install -r ../flask_app/requirements.txt

# Set up Flask app
cp ../flask_app/app.py ~/app.py
cp -r ../flask_app/templates ~/templates
cp -r ../flask_app/static ~/static
cp ../flask_app/utils.py ~/utils.py

# Set up Nginx
sudo cp ../nginx/flask_app /etc/nginx/sites-available/flask_app
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Obtain SSL certificate
# sudo certbot --nginx -d yourdomain.com

# Set up cron job for checking phone connection
# (crontab -l 2>/dev/null; echo "* * * * * /home/pi/scripts/wifi_monitor.sh") | crontab -

echo "Installation complete. Please configure your Hue bridge IP and username in the respective files."