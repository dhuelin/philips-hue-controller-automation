import json
import os

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), '..', 'homebridge', 'config.json')
        with open(config_path, 'r') as file:
            config = json.load(file)
            self.hue_bridge_ip = config.get('bridge_ip')
            self.hue_username = config.get('bridge_username')
            self.local_host = config.get('local_host', '0.0.0.0')
            self.local_port = config.get('local_port', 5000)
            self.external_domain = config.get('external_domain', 'yourdomain.com')
            self.external_port = config.get('external_port', 80)

    def get_hue_bridge_ip(self):
        return self.hue_bridge_ip

    def get_hue_username(self):
        return self.hue_username

    def get_local_host(self):
        return self.local_host

    def get_local_port(self):
        return self.local_port

    def get_external_domain(self):
        return self.external_domain

    def get_external_port(self):
        return self.external_port
