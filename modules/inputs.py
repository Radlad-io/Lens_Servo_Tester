from machine import Pin
import time
from micropython import const
from modules.store import store, States
from modules.assignments import ENCODER_DT, ENCODER_CLK, ENCODER_SW

class Press_Types():
    NO_PRESS = const(1),
    SHORT_PRESS = const(2),
    LONG_PRESS = const(3),

class Inputs:
    def __init__(self):
        self.DT_Pin = ENCODER_DT
        self.CLK_Pin = ENCODER_CLK
        self.SW = ENCODER_SW
        self.value = 0
        self.button_state = Press_Types.LONG_PRESS
        self.previousValue = 1
        self.short_press_threshold = 10 
        self.long_press_threshold = 650 
        self.press_start_time = 0
        self.long_press_in_progress = False

    def rotary_changed(self):
        if self.previousValue != self.CLK_Pin.value():
            if self.CLK_Pin.value() == 0:
                if self.DT_Pin.value() == 0:
                    store.set_menu_index(-1)
                else:
                    store.set_menu_index(1)
            self.previousValue = self.CLK_Pin.value()
         
    def button_changed(self):
        #  Button is pressed
        if not self.SW.value():
            if self.press_start_time == 0:
                self.press_start_time = time.ticks_ms() # Record the start time
            press_duration = time.ticks_diff(time.ticks_ms(), self.press_start_time)
            if press_duration >= self.long_press_threshold and not store.get_long_press():
                store.set_long_press(True)

        else:
        # Button is released
            store.set_display_needs_clear(True)
            if self.press_start_time != 0:
                press_duration = time.ticks_diff(time.ticks_ms(), self.press_start_time)
                if press_duration >= self.long_press_threshold:
                    self.button_state = Press_Types.LONG_PRESS
                else:
                    self.button_state = Press_Types.SHORT_PRESS
                self.press_start_time = 0 # Reset the start time
                store.set_long_press(False) #Reset long press 
                return self.button_state
            else:
                self.button_state = Press_Types.NO_PRESS
                return self.button_state
            

inputs = Inputs()