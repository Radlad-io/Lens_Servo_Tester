import time
from modules.store import store, States
from modules.display import display

menu = {
    "exit": States.MODE_MENU,
    "actions": [
        {"Lens Check": States.LENS_CHECK},
        {"Camera Check": States.CAMERA_CHECK},
        {"System Settings": States.SYSTEM_INFO_MENU}
    ]
}

store.set_menus(menu)
while store.get_state() == States.MAIN_MENU:
    display.menu_screen("Main Menu", menu)