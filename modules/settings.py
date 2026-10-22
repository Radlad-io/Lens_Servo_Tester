# test
import uos
import json
import random
from modules.storage import storage
import modules.utilities as Utilities

debug = Utilities.debug

class Settings:
    def __init__(self):
        self.file_name = "settings.json"
        self.settings_directory = "settings"
        self.path = f"{self.settings_directory}/{self.file_name}"
        # self.values = {
        #     "timescale": store.get_time_scale(),
        #     "average_voltage_sample_set": store.get_average_voltage_sample_set(),
        # }
        # json_str = json.dumps(self.values)
        self.settings_file_check = storage.file_check(self.path)
        self.check_for_settings_file()
        # self.create_log_file()

    # def store_settings(self):
    #     storage.create_file(self.path, json.dumps(self.values))
    
    # def load_settings(self):
    #     store.set_time_scale()
    
    def check_for_settings_file(self):
        storage.file_check(self.path)


settings = Settings()