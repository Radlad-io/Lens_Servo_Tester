import time
from modules.store import store, States
from modules.display import display


menu = {
    "exit": States.LENS_CHECK,
    "actions": [
        {"Lens Check": States.LENS_CHECK},
        {"Camera Check": States.CAMERA_CHECK}
    ]
}

store.set_menus(menu)

while store.get_state() == States.SETTINGS_MENU:
    display.menu_screen("Settings", menu)
    time.sleep_ms(100)