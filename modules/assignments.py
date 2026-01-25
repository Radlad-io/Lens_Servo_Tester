from machine import Pin, ADC, SPI, ADC

# SD CARD
STORAGE_CS = Pin(9, Pin.OUT)
STORAGE_SPI = SPI(1,
              baudrate=1000000,
              polarity=0,
              phase=0,
              bits=8,
              firstbit=SPI.MSB,
              sck=Pin(10),
              mosi=Pin(11),
              miso=Pin(8))

# ROTARY ENCODER
ENCODER_CLK = Pin(0, Pin.IN, Pin.PULL_UP)
ENCODER_DT = Pin(1, Pin.IN, Pin.PULL_UP)
ENCODER_SW = Pin(2, Pin.IN, Pin.PULL_UP)

# LENS INPUT
LENS_POT = ADC(Pin(26))

# GENERAL
TEMP_SENSOR_PIN = ADC(4)

# TRIGGER
TRIGGER_PIN = Pin(12, Pin.IN, Pin.PULL_UP)