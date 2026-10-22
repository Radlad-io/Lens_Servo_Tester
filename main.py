import _thread
import time
import modules.utilities as Utilities
import modules.assignments as assignments
from modules.inputs import inputs, Press_Types
from modules.store import States, store
from modules.storage import storage
from modules.logger import logger, LogTypes

# MODULES
states = States()
memory = Utilities.Memory()
debug = Utilities.debug

from modules.settings import Settings

def secondary_thread():
    # Moving this function to a module crashes.
    def router(path):
        # debug.init_msg(path)
        logger.log(LogTypes.INIT, path)
        exec(open(path).read())
        memory.clear()

    while True:
        if store.get_state() == states.LENS_CHECK:
            router("modules/modes/lens_check.py")

        if store.get_state() == states.CAMERA_CHECK:
            router("modules/modes/camera_check.py")

        if store.get_state() == states.MAIN_MENU:
            router("modules/menus/main_menu.py")

        if store.get_state() == states.MODE_MENU:
            router("modules/menus/mode_menu.py")

        if store.get_state() == states.SYSTEM_INFO_MENU:
            router("modules/menus/system_info_menu.py")

        if store.get_state() == states.SETTINGS_MENU:
            router("modules/menus/settings_menu.py")

        if store.get_state() == states.SETTINGS_MENU_TIMESCALE:
            router("modules/menus/settings/settings_menu_timescale.py")
        else:
            debug.warning_msg(f"No route found ({store.get_state()}). Trying again.")

def main_thread():
        # DEFINITIONS
        pot = assignments.LENS_POT
        trigger = assignments.TRIGGER_PIN
        # voltage = 0
        needs_update = False
        time.sleep(0.25)
        while True:
            time_scale = store.get_time_scale()
            # Tigger & Record Logic
            if store.get_exit():
                debug.exit_msg("Lens Check: Main Thread")
                return
            time.sleep(0.001)
            if trigger.value() == 0 and store.get_active_trigger_event() == False:
                store.set_active_trigger_event(True)
                store.set_trigger_events("start", time.ticks_ms())
                if needs_update == True and store.get_record() == False:
                    store.set_record(True)
                else:
                    store.set_record(False)
                time.sleep(0.001)

            if trigger.value() == 1 and store.get_active_trigger_event() == True:
                store.set_active_trigger_event(False)
                store.set_trigger_events("end", time.ticks_ms())
                needs_update = True
                time.sleep(0.001)

            now = time.ticks_ms()

            rot_direction = inputs.rotary_changed()
            if store.get_state() == states.SETTINGS_MENU_TIMESCALE:
                if rot_direction == -1:
                    store.set_time_scale(-1)
                elif rot_direction == 1:
                    store.set_time_scale(1)
            else:
                if rot_direction == -1:
                    store.set_menu_index(-1)
                elif rot_direction == 1:
                    store.set_menu_index(1)

            press = inputs.button_changed()

            if press == Press_Types.SHORT_PRESS:
                actions = store.get_menus()["actions"]
                index = store.get_menu_index()
                if index == len(list(actions)):
                    store.set_state(store.get_menus()["exit"])
                else:
                    transition_state = list(actions[index].values())[0]
                    store.set_state(transition_state)

            if press == Press_Types.LONG_PRESS:
                store.set_state(store.get_menus()["exit"])

            store.set_voltage(Utilities.adc_to_voltage(Utilities.map_range(pot.read_u16(), 128, 65535, 0.000, 65535)))
            if now % time_scale == 0:
                store.set_voltage_over_time(Utilities.adc_to_voltage(Utilities.map_range(pot.read_u16(), 128, 65535, 0.000, 65535)))
            
# display.splash_screen()
# time.sleep(1)
gui_thread = _thread.start_new_thread(secondary_thread, ())
main_thread()