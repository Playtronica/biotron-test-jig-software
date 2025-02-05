import serial
from threading import Thread
from base_logger import get_logger_for_file


logger = get_logger_for_file(__name__)

class SerialTests:
    _instance = None

    def __init__(self):
        self.is_enabled = False
        self.serial = None
        self.thread = None

        last_data = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def start_serial(self):
        if self.is_enabled:
            logger.warn("Serial thread has already been enabled")
            return
        self.serial = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
        self.thread = Thread(target=self.__proceess)
        self.thread.start()
        self.is_enabled = True

    def stop_serial(self):
        if not self.is_enabled:
            logger.warn("Serial thread has not already been enabled")
            return
        self.thread.stop()
        self.thread.join()
        self.is_enabled = False
        self.serial.close()
        self.serial = None

    def __proceess(self):
        try:
            while True:
                line = self.serial.readline().decode("ascii")
                if not line or line[0] != "{":
                    continue
                self.last_data = eval(line)
        except Exception as e:
            logger.error("Exception while reading serial data: {}".format(e))
            self.is_enabled = False
            self.serial.close()
            self.serial = None