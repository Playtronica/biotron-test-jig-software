from .I2CLCD import I2CLCD
from .rgb_led import RgbLed

import variables
from base_logger import get_logger_for_file

logger = get_logger_for_file(__name__)


class Display:
    _instance = None

    def __init__(self):
        self.screen = I2CLCD(address=variables.SCREEN_ADDRESS,
                             cols=variables.SCREEN_COLUMNS,
                             rows=variables.SCREEN_ROWS)
        self.rgb_led = RgbLed()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_text(self, lst_of_text):
        if not self.__validate_text_for_screen(lst_of_text):
            logger.warning("Some problems with text")
            return False

        self.screen.clear()
        for i in range(len(lst_of_text)):
            self.screen.set_cursor(0, i)
            self.screen.write(lst_of_text[i])

    def set_color(self, color):
        self.rgb_led.set_color(color)

    def __validate_text_for_screen(self, lst_of_text):
        if len(lst_of_text) > variables.SCREEN_ROWS:
            logger.warn("To many rows")
            return False

        if max(map(len, lst_of_text)) > variables.SCREEN_COLUMNS:
            logger.warn("Text is too long")
            return False

        return True

