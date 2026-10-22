# Modules.Display
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_RGB332, PEN_P8
import time
import math
from modules.utilities import map_range
from modules.store import store, States

# store = Store()
lcd = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P8, rotate=180)

class Display:
    def __init__(self):
        lcd.set_font("bitmap8")
        self.previous_voltage = 0

        # DIMENSIONS
        self.WIDTH, self.HEIGHT = lcd.get_bounds()

        # PALLET
        self.WHITE = lcd.create_pen(217, 217, 217)
        self.OFFWHITE = lcd.create_pen(195, 195, 195)
        self.BLACK = lcd.create_pen(0, 0, 0)
        self.DARKGRAY = lcd.create_pen(30, 30, 30)
        self.LIGHTGRAY = lcd.create_pen(88, 88, 88)
        self.RED = lcd.create_pen(255, 0, 0)
        self.GREEN = lcd.create_pen(42, 174, 27)
        self.YELLOW = lcd.create_pen(193, 164, 21)
        self.LINE_PALLET = self.create_red_hue_pallet()

        # MEMU STYES
        self.menu_font_size = 2
        self.menu_item_height = 40
        self.menu_item_bg = lcd.create_pen(25, 25, 25)
        self.menu_item_bg_active = lcd.create_pen(200, 200, 200)
        self.menu_item_margin = 2
        self.menu_item_text = self.WHITE
        self.menu_item_text_active = self.BLACK
        self.menu_title_height = 55
        
        # TEST SCREEN STYLES
        # self.active_index = 0
        self.clear()

        # SET BACKGROUND
        lcd.set_pen(self.BLACK)
        lcd.rectangle(0, 0, self.WIDTH, self.HEIGHT)

        # TRIGGER GRAPH 

        # TEST
        self.pos_x = 0

    def create_red_hue_pallet(self):
        base = 25
        pallet = []
        count = store.get_voltage_data_limit()
        for i in range(count):
            hue = map_range(i,0,count, base, 255)
            pallet.append(lcd.create_pen(int(hue), base, base))
        return pallet
        
    def splash_screen(self):
        self.clear()
        lcd.set_font("sans")
        lcd.set_pen(self.WHITE)
        lcd.text("LENS SERVO ", 20, 100, self.WIDTH, 1)
        lcd.text("SYSTEM TESTER", 20, 135, self.WIDTH, 1)
        lcd.text("LOADING...", 20, 165, self.WIDTH, 0.5)
        self.update()

    def mode_select(self):
        if store.get_display_needs_clear():
            self.clear()
        lcd.set_font("sans")
        lcd.set_pen(self.WHITE)
        lcd.text("Mode Select", 20, 100, self.WIDTH, 1)
        self.long_press_gui()
        self.update()
    
        
    def camera_testing(self):
        self.clear()
        lcd.set_font("sans")
        lcd.set_pen(self.WHITE)
        lcd.text("CAMERA TESTING", 20, 100, self.WIDTH, 1)
        self.long_press_gui()
        self.update()
    
    def settings_menu(self):
        self.clear()
        lcd.set_font("sans")
        lcd.set_pen(self.WHITE)
        lcd.text("Settings Menu", 20, 100, self.WIDTH, 1)
        self.long_press_gui()
        self.update()
    
# TODO: Cache the layout calculations instead of running them every frame, they don't change.
# TODO: Break these into reusable components.
# TODO: Add a cliping mask to the graph so the occasional glitched line doesn't draw outside of the graph.

    def lens_check_screen(self, voltage=3.3, distance=1.0):
        if store.get_display_needs_clear():
            self.clear()
            
        lcd.set_font("bitmap8")
        # HEADER STYLES
        header_height = 30
        header_divide = 80
        header_margin = 7

        # HEADER
        lcd.set_pen(self.DARKGRAY)
        lcd.rectangle(0, 0, self.WIDTH - header_divide, header_height )
        lcd.set_pen(self.WHITE)
        lcd.text("Lens Testing", header_margin * 2, header_margin, self.WIDTH - header_divide + header_margin*2, 2)

        # HEADER - REC INDICATOR
        if store.get_record():
            lcd.set_pen(self.RED)
        else:
            lcd.set_pen(self.BLACK)
        lcd.rectangle(self.WIDTH - header_divide, 0, header_divide, header_height)

        if store.get_record():
            lcd.set_pen(self.WHITE)
        else:
            lcd.set_pen(self.GREEN)

        lcd.circle(self.WIDTH - header_divide + 22, header_margin * 2, 6)

        if store.get_record():
            lcd.set_pen(self.RED)
        else:
            lcd.set_pen(self.BLACK)
        lcd.circle(self.WIDTH - header_divide + 22, header_margin * 2, 3)
        
        lcd.set_pen(self.WHITE)
        if store.get_record() == True:
            lcd.text("REC", self.WIDTH - header_divide + 36, header_margin, self.WIDTH - header_divide, 2)
        else:
            lcd.text("STB", self.WIDTH - header_divide + 36, header_margin, self.WIDTH - header_divide, 2)


        # FOCUS GRAPH STYLES
        graph_width = 300
        graph_height = 120
        graph_start = 50
        graph_border_size = 3
        graph_origin_x = int(int(self.WIDTH) / 2 - graph_width / 2 - graph_border_size)
        # FIXME: (I wrote fixme here but didn't say what and now I have forgoten what I need to fix)
        graph_origin_y = graph_width + graph_border_size * 2
        graph_end_y = graph_start + graph_height + graph_border_size
        graph_segments_x = 10
        graph_segments_y = 4


        # FOCUS GRAPH 
        # background
        lcd.set_pen(self.DARKGRAY)
        lcd.rectangle(graph_origin_x, graph_start, graph_origin_y, graph_height + graph_border_size * 2)
        lcd.set_pen(self.BLACK)
        lcd.rectangle(graph_origin_x + graph_border_size, graph_start + graph_border_size, graph_width, graph_height)
        
        # display.line(x1, y1, x2, y2)
        lcd.set_pen(self.DARKGRAY)
        for i in range(graph_segments_x):
            lcd.line(int(graph_origin_x + graph_border_size + i*graph_width/graph_segments_x), graph_start, int(graph_origin_x + graph_border_size + i*graph_width/graph_segments_x), int(graph_end_y), 1)
        for i in range(graph_segments_y):
            lcd.line( int(graph_origin_x + graph_border_size),
                         int(graph_start + i * 30 + graph_border_size),
                         graph_origin_x + graph_width +graph_border_size,
                         int(graph_start + i * 30 + graph_border_size),
                         1)
        
        lcd.set_pen(self.BLACK)
        lcd.rectangle(graph_origin_x + 8, graph_start + graph_height - 26, 50,29)
        lcd.rectangle(graph_origin_x + graph_width - 38, graph_start + 4, 40,29)
        lcd.set_pen(self.DARKGRAY)
        lcd.text("NEAR",graph_origin_x + 14, graph_start + graph_height - 19,self.WIDTH,2)
        lcd.text("FAR",graph_origin_x + graph_width - 42, graph_start + 11,self.WIDTH,2)

        graph_data = store.get_voltage_over_time()
        lcd.set_pen(self.WHITE)
        
        for i in range(len(graph_data)-2):
            lcd.set_pen(self.LINE_PALLET[i])
            pos_x_offset = (self.WIDTH - graph_width) / 2 + graph_border_size
            pos_x_start = (graph_width / (len(graph_data)-1) * i) + pos_x_offset
            pos_y_start = map_range(graph_data[i], 0, 3.3, graph_start, graph_start + graph_height)
            pos_x_end = (graph_width / (len(graph_data)-1) * (i+1)) + pos_x_offset
            pos_y_end = map_range(graph_data[i+1], 0, 3.3, graph_start, graph_start + graph_height)
            lcd.line(int(pos_x_start), int(pos_y_start), int(pos_x_end), int(pos_y_end))
            
            # if i % 4 == 0:
            #     if graph_data[i] > 1.5:
            #         lcd.text(f"{graph_data[i]:.2f}", int(8 * i)+5, int(self.HEIGHT - map_range(graph_data[i], 0,3.3, 70, 250) +10), 100, 1)
            #     else:
            #         lcd.text(f"{graph_data[i]:.2f}", int(8 * i)+5, int(self.HEIGHT - map_range(graph_data[i], 0,3.3, 70, 250) -10), 100, 1)
            #     lcd.set_pen(self.RED)
            #     lcd.line(int(8 * i)+20, int(self.HEIGHT - map_range(graph_data[i], 0,3.3, 70, 250))-4,int(8 * i)+20, int(self.HEIGHT - map_range(graph_data[i], 0,3.3, 70, 250))+4,2)

        # BANNERS
        banner_width = 96
        banner_height = 26
        banner_border = 12
        banner_text_y_offset = 0
        banner_text_x_offset = 2
        
        # TRIGGER GRAPH
        spacing = 14
        trigger_graph_height = 36
        trigger_graph_origin_x = graph_start + graph_height
        trigger_graph_origin_y = graph_start + graph_height + graph_border_size * 2 + spacing

        # Trigger Graph
        lcd.set_pen(self.DARKGRAY)
        events = store.get_trigger_events()
        lcd.rectangle(graph_origin_x,trigger_graph_origin_y,graph_width + graph_border_size * 2, trigger_graph_height)
        lcd.set_pen(self.BLACK)
        lcd.rectangle(int(graph_origin_x + graph_border_size), int(trigger_graph_origin_y + graph_border_size),graph_width,trigger_graph_height-graph_border_size*2)
         
        lcd.set_clip(int(graph_origin_x + graph_border_size), int(trigger_graph_origin_y + graph_border_size+graph_border_size),graph_width,trigger_graph_height-graph_border_size*2-graph_border_size*2)
        for i in range(len(events)):
            current_tick = time.ticks_ms()
            time_scale = 24
            block_x = math.floor(self.WIDTH - (current_tick - events[i]["start"] ) / time_scale)
            block_y = trigger_graph_origin_y + graph_border_size
            ball_rad = 13
            min_text_duration = 0.5
            if "duration" in events[i]:
                lcd.set_pen(self.LIGHTGRAY)
                duration = events[i]["duration"] / 1000
                block_w = math.floor(events[i]["duration"] / time_scale)
                lcd.circle(block_x + 6, int(block_y + ball_rad+2), ball_rad)
                lcd.rectangle(block_x, block_y, block_w , trigger_graph_height)
                lcd.circle(block_x+block_w - 6 , int(block_y + ball_rad+2), ball_rad)

                if duration >= min_text_duration:
                    lcd.set_pen(self.WHITE)
                    text_w = lcd.measure_text(f'{duration:.2}s', 1)
                    lcd.text(f"{duration:.2}s", int(block_x + block_w /2 - text_w/2 ), block_y + 11,block_w,1)
            else:
                lcd.set_pen(self.RED)
                lcd.circle(block_x + 6, int(block_y + ball_rad+2), ball_rad)
                lcd.rectangle(block_x, block_y, self.WIDTH, trigger_graph_height)
       
        lcd.remove_clip()

           
        # uppder banner
        lcd.set_pen(self.DARKGRAY)
        lcd.rectangle(int(int(self.WIDTH) / 2 - banner_width / 2 + graph_border_size), graph_start - int(banner_height/2), banner_width, banner_height)
        lcd.set_pen(self.BLACK)
        lcd.rectangle(int(int(self.WIDTH) / 2 - banner_width / 2 + graph_border_size + banner_border/4), graph_start - int(banner_height/2- banner_border/4), int(banner_width - banner_border / 2), int(banner_height - banner_border / 2))
        lcd.set_pen(self.LIGHTGRAY)
        upper_banner_text_w = lcd.measure_text(f'0.000', 2)
        lcd.text(f'v{store.get_voltage():.3f}', int(int(self.WIDTH) / 2 - banner_width / 2) + int(upper_banner_text_w/2), graph_start - int(banner_height/ 2 - banner_border / 2)+ banner_text_y_offset, self.WIDTH - header_divide + header_margin*2, 2)

        # middle banner
        lcd.set_pen(self.DARKGRAY)
        lcd.rectangle(int(int(self.WIDTH) / 2 - banner_width / 2 + graph_border_size), graph_start + graph_height - int(banner_height/2), banner_width, banner_height)
        lcd.set_pen(self.BLACK)
        lcd.rectangle(int(int(self.WIDTH) / 2 - banner_width / 2 + graph_border_size + banner_border/4), graph_start +  graph_height- int(banner_height/2 - banner_border/4), int(banner_width - banner_border / 2), int(banner_height - banner_border / 2))
        lcd.set_pen(self.LIGHTGRAY)
        middle_banner_text_w = lcd.measure_text("FOCUS", 2)
        lcd.text("FOCUS", int(self.WIDTH / 2 - middle_banner_text_w/2)+banner_text_x_offset, graph_start + graph_height - int(banner_height/ 2 - banner_border / 2) + banner_text_y_offset, self.WIDTH - header_divide + header_margin*2, 2)

        # lower banner
        lcd.set_pen(self.DARKGRAY)
        lcd.rectangle(int(int(self.WIDTH) / 2 - banner_width / 2 + graph_border_size), int(trigger_graph_origin_y + trigger_graph_height / 2), banner_width, banner_height)
        lcd.set_pen(self.BLACK)
        lcd.rectangle(int(int(self.WIDTH) / 2 - banner_width / 2 + graph_border_size + banner_border/4), int(trigger_graph_origin_y + trigger_graph_height / 2 + graph_border_size), int(banner_width - banner_border / 2), int(banner_height - banner_border / 2))
        lcd.set_pen(self.LIGHTGRAY)
        bottom_banner_text_w = lcd.measure_text("TRIGGER", 2)
        lcd.text("TRIGGER", int(self.WIDTH / 2 - bottom_banner_text_w/2)+banner_text_x_offset, int(trigger_graph_origin_y + trigger_graph_height / 2 + banner_border / 2)+banner_text_y_offset, self.WIDTH - header_divide + header_margin*2, 2)
        
        self.long_press_gui()
        self.update()


    def long_press_gui(self):
        if store.get_long_press():
            lcd.set_font("bitmap6")
            text = "RELEASE"
            border_w = 8
            box_h = 30
            lcd.set_pen(self.RED)
            text_w = lcd.measure_text(text,2)
            lcd.line(0,0,self.WIDTH,0,border_w ) #top
            lcd.line(self.WIDTH,0,self.WIDTH,self.HEIGHT,border_w ) #right
            lcd.line(0,self.HEIGHT,self.WIDTH,self.HEIGHT,border_w ) #bottom
            lcd.line(0,0,0,self.HEIGHT,border_w ) #left
            lcd.rectangle(int(self.WIDTH/2 - text_w/ 2 - border_w),int(self.HEIGHT/2-box_h/2+border_w),int(text_w+border_w*2), box_h)
            lcd.set_pen(self.WHITE)
            lcd.text(text,int(self.WIDTH/2 - text_w/ 2),int(self.HEIGHT/2),2)

    def _trigger_events_graph(self):
        # BACKGROUND
        lcd.set_pen(self.WHITE)
        events = store.get_trigger_events()

        lcd.set_pen(self.RED)
        lcd.rectangle(10,100,self.WIDTH - 20, 40)
        lcd.set_pen(self.BLACK)
        lcd.rectangle(15,105,self.WIDTH - 30, 30)
        lcd.set_clip(15, 105, self.WIDTH-30, 30)

        lcd.set_pen(self.RED)
        for i in range(len(events)):
            if "duration" in events[i]:
                # display.rectangle(int(map_range(events[i]["start"],0,time.ticks_ms(),0,self.WIDTH)),105, int(events[i]["duration"] / 2), 30)
                lcd.rectangle(math.floor(self.WIDTH - (time.ticks_ms() - events[i]["start"] ) / 16), 105, math.floor(events[i]["duration"] / 16), 30)
            else:
                lcd.rectangle(math.floor(self.WIDTH - (time.ticks_ms() - events[i]["start"] ) / 16), 105, self.WIDTH, 30)

        lcd.remove_clip()
        self.update()
        
    def menu_screen(self, title, menu):
        if store.get_display_needs_clear():
            self.clear()
        title_height = 65
        self._menu_title(title)

        item_m = 2
        lcd.set_font("bitmap8")
        menu_items = menu["actions"]
        menu_length = len(menu_items)
        shift = 0
        # short_list =
        for i in range(0,menu_length+1):
            item_text = ""
            selected = True if store.get_menu_index() == i  else False
            if i == menu_length:
                item_text = "Return"
            else:
                item_text = next(iter(menu_items[i].keys()))

            if selected:
                lcd.set_pen(self.OFFWHITE)
            elif i == menu_length:
                lcd.set_pen(self.BLACK)
            else:
                lcd.set_pen(self.DARKGRAY)
            lcd.rectangle(0, self.menu_item_height * i + i*self.menu_item_margin + title_height + int(item_m *i), self.WIDTH, self.menu_item_height)
            
            if selected:
                lcd.set_pen(self.BLACK)
            else:
                lcd.set_pen(self.WHITE)

            size = 2
            text_margin = 14
            item_y = self.menu_item_height * i + title_height+i*2
            lcd.text(item_text , 20, int(item_y+text_margin + (item_m*i)), self.WIDTH, size)
        self.update()    
    
    def _menu_title(self, title):
        lcd.set_pen(self.BLACK)
        lcd.rectangle(0, 0, self.WIDTH, self.HEIGHT)
        lcd.set_pen(self.WHITE)
        lcd.set_font("bitmap6")
        size = 3
        title_margin = 50
        title_x = self.WIDTH / 2 - lcd.measure_text(title, size) / 2
        title_y = title_margin / size
        lcd.text(title, int(title_x), int(title_y), self.WIDTH, size)

    def _stats_list(self, items):
        margin = 20
        value_x_offset = 135
        item_height = 22
        lcd.set_font("bitmap8")
        lcd.set_pen(self.WHITE) 
        for i in range(len(items)):
            key = list(items[i].keys())[0]
            value = list(items[i].values())[0]
            lcd.text(f"{key}:", int(margin), int(self.menu_title_height + item_height * i), self.WIDTH, 2)
            lcd.text(f"{value}", int(value_x_offset+margin), int(self.menu_title_height + item_height * i), self.WIDTH, 2)
        self.update()
        return

    def system_info_menu(self):
        if store.get_display_needs_clear():
            self.clear()
        lcd.set_font("bitmap8")
        self._menu_title("System Info")
        self._stats_list([{"VERSION":"v0.1.0"},{"FREQUENCY":"240MHz"},{"TEMPRATURE":"36 °c"},{"FS STATUS":"Good"},{"LENS CONFIGS":"002"},{"AUTHOR":"Kevin Merinsky"}])
        self.long_press_gui()

    def settings_menu(self, title="set", value=12):
        if store.get_display_needs_clear():
            self.clear()
        self._menu_title(title)
        lcd.set_font("bitmap8")
        # ARROW UP

        # lcd.text("↑", 50, 50, self.WIDTH, 2)
        # VALUE
        header_h = 75
        font_size = 8
        text_w = lcd.measure_text(f"{value}",font_size)
        center = self.WIDTH /2 - text_w/2 
        lcd.text(f"{value}", int(center), header_h, self.WIDTH, font_size)
        # ARROW DOWN
        # lcd.text("↓", int(self.WIDTH-50), 50, self.WIDTH, 3)
        # DESCRIPTION
        self.update()

    def clear(self):
        lcd.set_pen(self.BLACK)
        lcd.clear()
        store.set_display_needs_clear(False)
        
    def update(self):
        lcd.update()

display = Display()

# menu = {
#     "exit": States.MODE_MENU,
#     "actions": [
#         {"Lens Check": States.LENS_CHECK},
#         {"Camera Check": States.CAMERA_CHECK},
#     ]
# }
# display.menu_screen("test", menu)