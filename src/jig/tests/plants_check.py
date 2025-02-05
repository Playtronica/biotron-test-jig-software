import time

import variables
from jig.jig_hardware_control.pin_controller import PinController
from .serial_tests import SerialTests
from base_logger import get_logger_for_file

serial = SerialTests()
pin_controller = PinController()
logger = get_logger_for_file(__name__)


def get_plants_state():
    res = 0
    for _ in range(variables.PHOTORESISTOR_SAMPLES):
        data = serial.last_data.copy()
        if "generator_freq" not in data:
            logger.warning("Photo resistors data missing")
            return -1
        res += data["generator_freq"]
        time.sleep(1)

    return res / variables.PHOTORESISTOR_SAMPLES


def plants_test():
    no_connection_plant_state = get_plants_state()
    if no_connection_plant_state == -1:
        logger.warn("Some problems with getting status")
        return ""

    logger.info(f"Plant state without connection: {no_connection_plant_state}")

    pin_controller.relay_set(1, 1)
    connection_plant_state = get_plants_state()
    pin_controller.relay_set(1, 0)

    if connection_plant_state == -1:
        logger.warn("Some problems with getting status")
        return ""

    logger.info(f"Plant state with connection: {connection_plant_state}")