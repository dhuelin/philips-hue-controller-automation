import json

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        with open('homebridge/config.json', 'r') as file:
            config = json.load(file)
            self.hue_bridge_ip = config.get('bridge_ip')
            self.hue_username = config.get('bridge_username')

    def get_hue_bridge_ip(self):
        return self.hue_bridge_ip

    def get_hue_username(self):
        return self.hue_username
