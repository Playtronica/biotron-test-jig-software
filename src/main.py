import variables

from base_logger import get_logger_for_file
import subprocess

from firmware_updater import update_firmware_files
from jig.JigEnvironment import JigEnvironment
from jig.tests.load_firmware_to_device import load_firmware_to_device

logger = get_logger_for_file(__name__)


def check_internet_connection():
    try:
        subprocess.check_output(["ping", "-c", "1", "www.baidu.com"])
        logger.info("Internet connection established")
        return True
    except subprocess.CalledProcessError:
        logger.error("Internet connection error")
        return False


def initial_part():
    res = check_internet_connection()
    if res:
        update_firmware_files('Playtronica', 'biotron-firmware')
    else:
        logger.error("Internet connection error")



if __name__ == '__main__':
    initial_part()

    jig = JigEnvironment()
    jig.init_jig_main_cycle()



