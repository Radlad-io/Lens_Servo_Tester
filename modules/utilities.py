import time
import gc

def map_range(value, inMin, inMax, outMin, outMax):
    return outMin + (((value - inMin) / (inMax - inMin)) * (outMax - outMin))

def adc_to_voltage(value):
    return value / 65535 * 3.3

class Performance:
  def __init__(self):
    self.start_time = 0
    self.value = 0
    self.debug_output = True

  def start(self):
    self.start_time = time.ticks_ms()

  def measure(self):
    self.value = time.ticks_ms() - self.start_time
    if self.debug_output:
      print(f"{self.value}ms")

  def reset(self):
    self.value = 0;
    self.start_time = time.ticks_ms();

class Memory:
  def __init__(self) -> None:
    self.gc = gc
    self.debug = Debug()
    self.total_mem = self.gc.mem_alloc() + self.gc.mem_free() / 1024
    self.mem_allocation = self.gc.mem_alloc() / 1024 # in kb

  def measure_memory_usage(self):
    self.mem_allocation = self.gc.mem_alloc() / 1024 # in kb
     
  def check(self):
    self.debug.verbose_msg(f"RAM Used: {self.mem_allocation:.0f}kb / Free RAM: {self.total_mem:.0f}kb")

  def clear(self):
    self.debug.verbose_msg("Clearing Memory")
    self.measure_memory_usage()
    self.debug.verbose_msg(f"RAM in Use: {self.mem_allocation:.3f}kb")
    self.gc.collect()
    self.gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
    self.measure_memory_usage()
    self.debug.verbose_msg(f"RAM in Use: {self.gc.mem_alloc() / 1024:.3f}kb")

class Debug:
    def __init__(self):
      self.RED = '\033[91m'
      self.GREEN = '\033[92m'
      self.YELLOW = '\033[93m'
      self.BLUE = '\033[94m'
      self.ENDC = '\033[0m'
      self.verbose = True

    def init_msg(self, msg):
      print(f"{self.GREEN}Initalizing: {self.ENDC}{msg}")

    def exit_msg(self, msg):
      print(f"{self.YELLOW}Exiting: {self.ENDC}{msg}")

    def success_msg(self, msg):
      print(f"{self.GREEN}Warning: {self.ENDC}{msg}")

    def warning_msg(self, msg):
      print(f"{self.YELLOW}Warning: {self.ENDC}{msg}")
    
    def error_msg(self, msg):
      print(f"{self.RED}Error: {self.ENDC}{msg}")
    
    def verbose_msg(self, msg):
       if self.verbose:
        print(f"{self.BLUE}Verbose Output: {self.ENDC}{msg}")
    
    def overwrite_msg(self, msg):
       if self.verbose:
        print(f"{self.BLUE}Verbose Output: {self.ENDC}{msg}")

debug = Debug()