from micropython import const
# from modules.settings import settings

class States():
    LENS_CHECK = const(100)
    CAMERA_CHECK = const(200)
    MODE_MENU = const(300)
    MAIN_MENU = const(400)
    SETTINGS_MENU = const(500)
    SETTINGS_MENU_TIMESCALE = const(501)
    SYSTEM_INFO_MENU = const(600)

# states = States()

class Store:
    def __init__(self):
        self.voltage = 0.0
        self.voltage_over_time = []
        self.voltage_data_limit = 64
        self.average_voltage_sample_set = {
            "value": 4,
            "default": 4,
            "min": 0,
            "max": 10,
            "increment": 1.0,
        }
        self.active_trigger_event = False
        self.trigger_event_limit = 24
        self.record = False
        self.trigger_events = []
        # TODO: read from storage on boot
        self.time_scale = {
            "value": 12,
            "default": 12,
            "min": 0,
            "max": 100,
            "increment": 1.0,
        }
        self.display_clear = False
        self.state = States.MODE_MENU
        self.exit = False
        self.long_press = False
        self.menu_index = 0
        self.menus = {
            "exit": States.MAIN_MENU,
            "actions": [
                {"Timescale": States.SETTINGS_MENU_TIMESCALE},
            ] 
        }
        self.settings = [self.time_scale, self.average_voltage_sample_set]

    def get_record(self):
        return self.record
    
    def set_record(self, value):
        self.record = value

    def get_voltage(self):
        return self.voltage
    
    def set_voltage(self, value):
        self.voltage = value

    def get_voltage_over_time(self):
        return self.voltage_over_time
    
    def get_voltage_data_limit(self):
        return self.voltage_data_limit
    
    def set_voltage_over_time(self, value):
        self.voltage_over_time.append(value)
        if len(self.voltage_over_time) > self.voltage_data_limit:
            del self.voltage_over_time[0]

    def get_active_trigger_event(self):
        return self.active_trigger_event
    
    def set_active_trigger_event(self, value):
        self.active_trigger_event = value

    def get_trigger_events(self):
        return self.trigger_events
    
    def set_trigger_events(self, type, time):
        if type == "start":
            self.trigger_events.append({"start": time})
        elif type == "end":
            self.trigger_events[len(self.trigger_events)-1].update({"end": time})
            self.trigger_events[len(self.trigger_events)-1].update({"duration": time - self.trigger_events[len(self.trigger_events)-1]["start"]})
        if len(self.trigger_events) > self.trigger_event_limit:
            self.trigger_events.pop(0)

    def get_time_scale(self):
        return self.time_scale["value"]
    
    def set_time_scale(self, value):
        self.time_scale["value"] = self.time_scale["value"] + value

    def get_display_needs_clear(self):
        return self.display_needs_update
    
    def set_display_needs_clear(self, value):
        self.display_needs_update = value

    def get_long_press(self):
        return self.long_press
    
    def set_long_press(self, value):
        self.long_press = value

    def get_state(self):
        return self.state
    
    def set_state(self, value):
        self.state = value

    def get_exit(self):
        return self.exit
    
    def set_exit(self, value):
        self.exit = value

    def set_menu_index(self, value):
        index = self.menu_index + value
        if index > len(self.menus["actions"]):
            index = 0
        if index < 0:
            index = len(self.menus["actions"])
        self.menu_index = index

    def reset_menu_index(self):
        self.menu_index = 0
        
    def get_menu_index(self):
        return self.menu_index
    
    def set_menus(self, menu):
        self.menus = menu
    
    def get_menus(self):
        return self.menus
    
    def get_average_voltage_sample_set(self):
        return self.average_voltage_sample_set["value"]
    
    def set_average_voltage_sample_set(self, value):
        self.average_voltage_sample_set["value"] = self.average_voltage_sample_set["value"] + value
        # settings.store_settings()
    
store = Store()