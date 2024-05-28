from phue import Bridge
import time
from .config import Config

# Load configuration
config = Config()
bridge = Bridge(config.get_hue_bridge_ip(), config.get_hue_username())

def wake_up_alarm():
    lights = bridge.get_light_objects('id')
    
    for _ in range(100):  # Flash 10 times
        for light in lights.values():
            light.on = True
            light.brightness = 254
        time.sleep(0.5)
        for light in lights.values():
            light.on = False
        time.sleep(0.5)

if __name__ == "__main__":
    wake_up_alarm()
