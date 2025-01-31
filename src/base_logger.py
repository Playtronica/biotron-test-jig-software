import logging
import time
from variables import LOGGER_PATH

base_logger = logging.getLogger("biotron_test_jig")

base_logger.setLevel(logging.INFO)

name_of_file = time.strftime("%Y.%m.%d-%H:%M:%S")
handler = logging.FileHandler(LOGGER_PATH / f'{name_of_file}.log', mode="w+")
formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler.setFormatter(formatter)
base_logger.addHandler(handler)

def get_logger_for_file(name):
    return base_logger.getChild(name)