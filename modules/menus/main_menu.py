import time
from modules.store import store, States
from modules.display import display

menu = {
    "exit": States.MODE_MENU,
    "actions": [
        {"Mode Select": States.MODE_MENU},
        {"Settings": States.SETTINGS_MENU},
        {"System Info": States.SYSTEM_INFO_MENU}
    ]
}

store.set_menus(menu)
while store.get_state() == States.MAIN_MENU:
    display.menu_screen("Main Menu", menu)