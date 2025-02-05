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
        self.lines = self.chip.get_lines([variables.RGB_LED_RED_PIN, variables.RGB_LED_GREEN_PIN, variables.RGB_LED_BLUE_PIN])
        self.lines.request(consumer="rgb_control", type=gpiod.LINE_REQ_DIR_OUT)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def set_color(self, color):
        if type(color) is RgbColorsEnum:
            color = color.value

        self.lines.set_values([1 - color[0], 1 - color[1], 1 - color[2]])

