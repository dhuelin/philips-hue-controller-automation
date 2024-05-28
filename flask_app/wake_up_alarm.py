from phue import Bridge
import time
from .config import Config

# Load configuration
config = Config()
bridge = Bridge(config.get_hue_bridge_ip(), config.get_hue_username())

def wake_up_alarm():
    light = bridge.get_light_objects('id')[14]
    
    for _ in range(100):  # Flash 10 times
        light.on = True
        light.brightness = 254
        time.sleep(0.5)
        light.on = False
        time.sleep(0.5)

if __name__ == "__main__":
    wake_up_alarm()
