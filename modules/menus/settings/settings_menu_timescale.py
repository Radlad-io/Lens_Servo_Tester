import time
from modules.store import store, States
from modules.display import display

menu = {
    "exit": States.SETTINGS_MENU,
    "actions": []
}

store.set_menus(menu)
while store.get_state() == States.SETTINGS_MENU_TIMESCALE:
    display.settings_menu("Set Timescale", store.get_time_scale())