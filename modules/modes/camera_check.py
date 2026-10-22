
from modules.display import display
# from modules.utilities import map_range,adc_to_voltage, Performance, Memory, Debug
from modules.store import store, States

menu = {
    "exit": States.MAIN_MENU,
    "actions": []
}

store.set_menus(menu)
store.set_display_needs_clear(True)
store.set_menu_index(0)
while store.get_state() == States.CAMERA_CHECK:
    display.camera_testing()
