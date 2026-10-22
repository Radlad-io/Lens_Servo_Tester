import time
from modules.store import store, States
from modules.display import display


menu = {
    "exit": States.MAIN_MENU,
    "actions": [
        {"Timescale": States.SETTINGS_MENU_TIMESCALE},
    ]
}

store.set_menus(menu)

while store.get_state() == States.SETTINGS_MENU:
    display.menu_screen("Settings", menu)
    time.sleep_ms(100)