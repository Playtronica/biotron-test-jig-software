from base_logger import initialize_logger, get_logger_child
import subprocess
import os

import variables
from firmware_updater import update_firmware_files


def create_initial_structure():
    os.makedirs(variables.FIRMWARE_PATH, exist_ok=True)
    os.makedirs(variables.LOGGER_PATH, exist_ok=True)


def check_internet_connection():
    try:
        subprocess.check_output(["ping", "-c", "1", "www.baidu.com"])
        main_logger.info("Internet connection established")
        return True
    except subprocess.CalledProcessError:
        main_logger.error("Internet connection error")
        return False


create_initial_structure()
initialize_logger()
main_logger = get_logger_child("main")


if __name__ == '__main__':
    check_internet_connection()
    update_firmware_files('Playtronica', 'biotron-firmware')