import gpiod
import enum
import variables

class RgbColorsEnum(enum.Enum):
    NONE=(1, 1, 1)
    RED=(0, 1, 1)
    GREEN=(1, 0, 1)
    BLUE=(1, 1, 0)
    YELLOW=(0, 0, 1)
    PURPLE=(0, 1, 0)
    LIGHT_BLUE=(1, 0, 0)
    WHITE=(0, 0, 0)

class RgbLed:
    _instance = None

    def __init__(self):
        self.chip = gpiod.Chip(variables.RGB_LED_CHIP_NAME)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_color(self, color):
        if type(color) is RgbColorsEnum:
            color = color.value

