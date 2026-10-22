import time
from modules.store import store, States
from modules.display import display

menu = {
    "exit": States.MAIN_MENU,
    "actions": [
        {"Lens Check": States.LENS_CHECK},
        {"Camera Check": States.CAMERA_CHECK}
    ]
}

store.set_menus(menu)
while store.get_state() == States.MODE_MENU:
    display.menu_screen("Mode Select", menu)