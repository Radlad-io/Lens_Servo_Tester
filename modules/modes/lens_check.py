
from modules.display import display
from modules.utilities import map_range,adc_to_voltage, Performance, Memory, Debug
from modules.store import store, States
from modules.storage import storage
import modules.assignments as assignments

menu = {
    "exit": States.MAIN_MENU,
    "actions": [
        {"Lens Check": States.LENS_CHECK},
        {"Camera Check": States.CAMERA_CHECK}
    ]
}

store.set_menus(menu)
store.set_display_needs_clear(True)
store.reset_menu_index()

# DEFINITIONS
pot = assignments.LENS_POT
trigger = assignments.TRIGGER_PIN
voltage = 0

perforance = Performance()

while store.get_state() == States.LENS_CHECK:
    # perforance.start()
    display.lens_check_screen(voltage, map_range(pot.read_u16(), 0, 65535, 0.000, 1.0))
    # perforance.measure()

