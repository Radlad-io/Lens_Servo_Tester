import sdcard
import uos
from modules.assignments import STORAGE_CS, STORAGE_SPI

class Storage:
    def __init__(self):
        self.CS_PIN = STORAGE_CS
        self.SPI_PIN = STORAGE_SPI
        self.sd = sdcard.SDCard(self.SPI_PIN, self.CS_PIN)
        self.vfs = uos.VfsFat(self.sd)

    def create_file(self, path, contents):
        """
        Function to create a file.
        
        :param path: path to file (omit sd root /sd/)
        :param contents: content should match pathe extension type
        """
        try: 
            uos.mount(self.vfs, "/sd")
            with open(f"sd/{path}", "w") as file:
                file.write(contents)
        except Exception as e:
            print(e)
            return
    
    def read_file(self, path):
        """
        Function to read a file from the SD card
        
        :param path: path to file (omit sd root /sd/)
        """
        try:
            with open(f"sd/{path}", "r") as file:
                data = file.read()
                return data
        except Exception as e:
            print(e)
            return
    
    def file_check(self, path):
        """
        Function to check if a file exists. Returns Bool.
        
        :param path: path to file (omit sd root /sd/)
        """
        try:
            data = uos.stat(f"sd/{path}")
            return True
        except Exception as e:
            return False
        

storage = Storage()