import time
from modules.store import store, States
from modules.display import display

menu = {
    "exit": States.MAIN_MENU,
    "actions": []
}

store.set_menus(menu)
while store.get_state() == States.SYSTEM_INFO_MENU:
    display.system_info_menu()