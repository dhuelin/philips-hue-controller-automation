# Hue Light Controller

A project to control Philips Hue lights using a Raspberry Pi. This setup includes Homebridge for iOS integration and a Flask web application for control.

## Prerequisites

- Raspberry Pi with Raspbian OS
- Philips Hue Bridge and Lights
- Domain name for external access (optional)

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
   - `flask_app/config.py`

4. Set your phone's MAC address in the `wifi_monitor.sh` script.

## Usage

- Access the Flask web application at `http://yourdomain.com` (if using an external domain).
- Control the lights via the iOS Home app using Homebridge.
- Add new automations via the web interface under the "Automations" section.

## Running the Server

To start the server, use the provided script:

```bash
cd ~/workspace/philips-hue-controller-automation/scripts
./start.sh
