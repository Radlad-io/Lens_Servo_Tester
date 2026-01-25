# test
import time
import json
from modules.assignments import TEMP_SENSOR_PIN
from modules.storage import storage

class Settings:
    def __init__(self):
        self.file_name = "settings.json"
        self.settings_directory = "settings"
        self.temperature_voltage = TEMP_SENSOR_PIN.read_u16() * (3.3 / 65535.0)
        self.values = {
            "version": "v0.1.0", 
            "freq" : 240000000,
            "temp" : 27 - (self.temperature_voltage - 0.706) / 0.001721 # in celsius
        }
        storage.create_file(f"{self.settings_directory}/{self.file_name}", json.dumps(self.values))

    def get_setting(self, setting_key):
        return self.values[setting_key]
    
    def set_setting(self, setting_key, value):
        self.values[setting_key] = value

    def store_settings(self):
        storage.create_file(f"{self.settings_directory}/{self.file_name}", json.dumps(self.values))
        

settings = Settings()