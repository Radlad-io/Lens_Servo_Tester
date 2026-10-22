import sdcard
import uos
import random
import modules.utilities as Utilities
from modules.assignments import STORAGE_CS, STORAGE_SPI

debug = Utilities.debug

class Storage:
    def __init__(self):
        self.CS_PIN = STORAGE_CS
        self.SPI_PIN = STORAGE_SPI
        self.sd = sdcard.SDCard(self.SPI_PIN, self.CS_PIN)
        self.vfs = uos.VfsFat(self.sd)
        self.mount_sd_card()
        self.log_file_path = f"logs/{random.randrange(1000000,9999999)}.csv"
        # TODO: should probably do a little checking to make sure the file doesn't exist
        # TODO: should there be a max log file limit?
        self.create_file(self.log_file_path,"")
        self.create_file(self.log_file_path, "tickstamp, type, message, verbose, \n")
    
    def mount_sd_card(self):
        try:
            uos.mount(self.vfs, "/sd")
        except Exception as e:
            debug.error_msg("Unable to mount SD Card Volume")

    def create_file(self, path, contents):
        """
        Function to create a file.
        
        :param path: path to file (omit sd root /sd/)
        :param contents: content should match pathe extension type
        """
        try: 
            # uos.mount(self.vfs, "/sd")
            with open(f"sd/{path}", "w") as file:
                file.write(contents)
                debug.success_msg(f"File created ({path})")
        except Exception as e:
            debug.error_msg(f"Couldn't create file ({path})")
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
            debug.success_msg(f"File exists ({path})")
            return True
        except Exception as e:
            debug.error_msg(f"File does not exist ({path})")
            return False
    
    def append_to_log_file(self, content):
        self.append_to_file(self.log_file_path, content)

    def append_to_file(self, path, content):
        print(path, content)
        # Open a file in append mode ('a')
        # tickstamp, type, message, verbose_output
        is_string = isinstance(content, str)
        if not is_string:
            debug.error_msg("Content needs to be a string")
            return
        try:
            with open(path, "a") as logf:
                # Write data with commas and a newline character
                logf.write(content)
        except OSError as e:
            print(e)
            debug.error_msg("Disk full or other OS error")
            return    

storage = Storage()