from micropython import const
import time
import modules.utilities as Utilities
from modules.storage import storage

class LogTypes():
    INIT = const(100)
    EXIT = const(200)
    SUCCESS = const(300)
    WARNING = const(400)
    ERROR = const(500)
    EVENT = const(600)

class Logger:
    def __init__(self) -> None:
        self.logging = True

    def log(self, log_type, message, verbose_output=""):
        timestamp = time.ticks_ms()
        file_content = f"{timestamp},{log_type},{message},{verbose_output}"
        if log_type == LogTypes.INIT:
            Utilities.debug.success_msg(message)
            pass
        if log_type == LogTypes.SUCCESS:
            Utilities.debug.success_msg(message)
            pass
        if log_type == LogTypes.WARNING:
            Utilities.debug.warning_msg(message)
            pass
        if log_type == LogTypes.ERROR:
            Utilities.debug.error_msg(message)
            pass
        if log_type == LogTypes.EVENT:
            Utilities.debug.success_msg(message)
            pass

        if self.logging:
            storage.append_to_log_file(file_content)
        

logger = Logger()
