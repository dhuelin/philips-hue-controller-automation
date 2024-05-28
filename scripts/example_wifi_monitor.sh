#!/bin/bash

# Check if the phone is connected to the WiFi
PHONE_MAC="your_phone_mac_address"
if /usr/sbin/arp-scan --localnet | grep -q "$PHONE_MAC"; then
    # If the phone is connected, execute the automation to turn on lights
    /usr/bin/python3 /home/pi/utils.py --action "turn_on_lights"
fi
