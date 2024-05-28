# Hue Light Controller

A project to control Philips Hue lights using a Raspberry Pi. This setup includes Homebridge for iOS integration, a Flask web application for control, and Nginx for secure external access.

## Prerequisites

- Raspberry Pi with Raspbian OS
- Philips Hue Bridge and Lights
- Domain name for external access

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/hue-light-controller.git
    cd hue-light-controller/scripts
    ```

2. Run the installation script:

    ```bash
    ./install.sh
    ```

3. Configure your Hue bridge IP and username in the respective files:
   - `homebridge/config.json`
   - `flask_app/app.py`

4. Set your domain name in `nginx/flask_app` and re-run Certbot if necessary:

    ```bash
    sudo certbot --nginx -d yourdomain.com
    ```

5. Set your phone's MAC address in the `wifi_monitor.sh` script.

## Usage

- Access the Flask web application at `http://yourdomain.com`.
- Control the lights via the iOS Home app using Homebridge.
- Add new automations via the web interface under the "Automations" section.

## Notes

- Ensure your Raspberry Pi's firewall allows traffic on the necessary ports.
- Keep your system and packages updated for security.

## .gitignore

```plaintext
# Ignore personal configuration files
*.pyc
__pycache__/
.DS_Store
.env
*.log

# Ignore Homebridge config
homebridge/config.json

# Ignore Nginx site configuration
nginx/flask_app

# Ignore automation files that may contain personal info
flask_app/automations.json
scripts/wifi_monitor.sh
