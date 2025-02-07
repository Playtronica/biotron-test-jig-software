import time

import variables
from base_logger import get_logger_for_file
from jig.jig_hardware_control.ads1015_4051 import MultiplexerADCReader
from jig.tests.midi_processes import send_test_green_sysex_messages_to_midi_device, \
    send_test_blue_sysex_messages_to_midi_device

logger = get_logger_for_file(__name__)


adc_read = MultiplexerADCReader()




def led_tests(data):
    for multiplexer_num in range(2):
        for multiplexer_channel_num in range(8):
            adc_val = adc_read.read_channel(multiplexer_num, multiplexer_channel_num)
            logger.info(f"Value of multiplexer {multiplexer_num} {multiplexer_channel_num}: {adc_val}")
            adc_val -= 0.05

            if multiplexer_num == 1 and multiplexer_channel_num == 2:
                logger.warn("BROKEN. IGNORE")
                continue

            # if adc_val >= data[(multiplexer_num, multiplexer_channel_num)]:
            #     logger.warn(f"Problems with blue led {multiplexer_num} {multiplexer_channel_num}: {adc_val}")
            #     return "BLUE_LED_TEST_FAILED"

            time.sleep(0.1)

    return


def check_blue_led():
    send_test_blue_sysex_messages_to_midi_device()
    data = {
        (0, 0): 3.196, (0, 1): 3.196, (0, 2): 3.1725,
        (0, 3): 2.7808333333333333, (0, 4): 3.196, (0, 5): 2.726,
        (0, 6): 2.7965, (0, 7): 2.9296666666666664, (1, 0): 2.7886666666666664,
        (1, 1): 2.8905, (1, 2): 0.015666666666666666, (1, 3): 2.9061666666666666,
        (1, 4): 2.8434999999999997, (1, 5): 2.827833333333333, (1, 6): 2.7808333333333333, (1, 7): 2.726
    }
    return led_tests(data)


def check_green_led():
    send_test_green_sysex_messages_to_midi_device()
    data = {
        (0, 0): 3.196, (0, 1): 3.196, (0, 2): 3.1725,
        (0, 3): 2.7808333333333333, (0, 4): 3.196, (0, 5): 2.726,
        (0, 6): 2.7965, (0, 7): 2.9296666666666664, (1, 0): 2.7886666666666664,
        (1, 1): 2.8905, (1, 2): 0.015666666666666666, (1, 3): 2.9061666666666666,
        (1, 4): 2.8434999999999997, (1, 5): 2.827833333333333, (1, 6): 2.7808333333333333, (1, 7): 2.726
    }
    return led_tests(data)