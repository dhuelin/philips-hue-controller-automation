from flask import Flask, jsonify, render_template, request, redirect, url_for
from phue import Bridge, PhueRegistrationException
from .config import Config
from .utils import load_automations, save_automations, execute_automation
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import json

app = Flask(__name__, template_folder='templates', static_folder='static')

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

scheduler = BackgroundScheduler()

def schedule_automations():
    scheduler.remove_all_jobs()
    automations = load_automations()
    for automation in automations:
        if automation['active'] == True and automation['trigger'] == 'time':
            trigger_time = datetime.strptime(automation['time'], '%H:%M').time()
            for day in automation['days']:
                scheduler.add_job(
                    execute_automation,
                    'cron',
                    day_of_week=day,
                    hour=trigger_time.hour,
                    minute=trigger_time.minute,
                    args=[automation['action'], automation['settings'], automation['lights']]
                )

scheduler.start()
schedule_automations()

@app.route('/')
def index():
    print("Index route reached")
    lights = bridge.get_light_objects('id')
    print(f"Lights: {lights}")
    return render_template('index.html', lights=lights)

@app.route('/lights')
def lights():
    lights = bridge.get_light_objects('id')
    return render_template('lights.html', lights=lights)

@app.route('/light/<int:light_id>')
def lightDetail(light_id):
    light = bridge.get_light_objects('id')[light_id]
    light_attrs = {attr: getattr(light, attr) for attr in dir(light) if not attr.startswith('_') and not callable(getattr(light, attr))}
    return render_template('lightdetail.html', light=light_attrs)

@app.route('/toggle/<int:light_id>')
def toggle(light_id):
    light = bridge.get_light_objects('id')[light_id]
    light.on = not light.on
    return ('', 204)

@app.route('/automations')
def automations():
    automations = load_automations()
    return render_template('automations.html', automations=automations)

""" @app.route('/add_automation', methods=['POST'])
def add_automation():
    data = request.get_json()
    automation = {
        'name': data['name'],
        'trigger': data['trigger'],
        'days': data.get('days', []),
        'time': data.get('time', ''),
        'lights': data['lights'],
        'action': data['action'],
        'settings': data['settings']
    }
    automations = load_automations()
    automations.append(automation)
    save_automations(automations)
    return redirect(url_for('automations')) """

@app.route('/update_automation', methods=['POST'])
def add_automation(automation):
    data = request.get_json()
    automation = {
        'name': data['name'],
        'active': data['active'],
        'trigger': data['trigger'],
        'days': data.get('days', []),
        'time': data.get('time', ''),
        'lights': data['lights'],
        'action': data['action'],
        'settings': data['settings']
    }
    automations = load_automations()
    automations.append(automation)
    save_automations(automations)
    return redirect(url_for('automations'))


@app.route('/toggle_automation/<int:automation_id>', methods=['POST'])
def toggle_automation(automation_id):
    automations = load_automations()
    for automation in automations:
        if automation['id'] == automation_id:
            print("automation found with id" + automation_id)
            print("automation['active'] before: " + str(automation['active']))
            automation['active'] = not automation['active']
            print("automation['active'] after: " + str(automation['active']))
            break
    
    save_automations(automations)
    reload_all_automations()
    return jsonify({'success': True})

@app.route('/delete_automation/<name>')
def delete_automation(name):
    automations = load_automations()
    automations = [a for a in automations if a['name'] != name]
    save_automations(automations)
    reload_all_automations()
    return redirect(url_for('automations'))

def reload_all_automations():
    scheduler.remove_all_jobs()
    schedule_automations()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Start the Flask server.')
    parser.add_argument('--external', action='store_true', help='Run server with external configuration')
    args = parser.parse_args()

    if args.external:
        app.run(host=config.get_external_domain(), port=config.get_external_port())
    else:
        app.run(host=config.get_local_host(), port=config.get_local_port())
