from flask import Flask, render_template, request, redirect, url_for
from phue import Bridge, PhueRegistrationException
from .config import Config
from .utils import load_automations, save_automations
import os
import json

app = Flask(__name__)

# Load configuration
config = Config()

# Ensure ~/.python_hue configuration file exists
config_path = os.path.expanduser("~/.python_hue")
if not os.path.exists(config_path):
    bridge_ip = config.get_hue_bridge_ip()
    bridge_username = config.get_hue_username()
    bridge = Bridge(bridge_ip)
    try:
        bridge.connect()
        with open(config_path, 'w') as file:
            json.dump({bridge_ip: {"username": bridge_username}}, file)
        print("Hue bridge connected and configuration saved.")
    except PhueRegistrationException:
        print("Please press the button on the Hue bridge and run the script again.")
        exit(1)

# Initialize the Bridge
bridge = Bridge(config.get_hue_bridge_ip(), config.get_hue_username())

@app.route('/')
def index():
    lights = bridge.get_light_objects('id')
    return render_template('index.html', lights=lights)

@app.route('/lights')
def lights():
    lights = bridge.get_light_objects('id')
    return render_template('lights.html', lights=lights)

@app.route('/toggle/<light_id>')
def toggle(light_id):
    light = bridge.get_light(int(light_id))
    light.on = not light.on
    return ('', 204)

@app.route('/automations')
def automations():
    automations = load_automations()
    return render_template('automations.html', automations=automations)

@app.route('/add_automation', methods=['POST'])
def add_automation():
    data = request.form
    automation = {
        'name': data['name'],
        'trigger': data['trigger'],
        'action': data['action']
    }
    automations = load_automations()
    automations.append(automation)
    save_automations(automations)
    return redirect(url_for('automations'))

@app.route('/delete_automation/<name>')
def delete_automation(name):
    automations = load_automations()
    automations = [a for a in automations if a['name'] != name]
    save_automations(automations)
    return redirect(url_for('automations'))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Start the Flask server.')
    parser.add_argument('--external', action='store_true', help='Run server with external configuration')
    args = parser.parse_args()

    if args.external:
        app.run(host=config.get_external_domain(), port=config.get_external_port())
    else:
        app.run(host=config.get_local_host(), port=config.get_local_port())
