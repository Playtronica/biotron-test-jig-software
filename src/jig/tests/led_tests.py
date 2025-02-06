import time

import variables
from base_logger import get_logger_for_file
from jig.jig_hardware_control.ads1015_4051 import MultiplexerADCReader

logger = get_logger_for_file(__name__)


adc_read = MultiplexerADCReader()


def led_tests():
    for multiplexer_num in range(2):
        for multiplexer_channel_num in range(8):
            adc_val = adc_read.read_channel(multiplexer_num, multiplexer_channel_num)
            logger.info(f"Value of multiplexer {multiplexer_num} {multiplexer_channel_num}: {adc_val}")

            if multiplexer_num == 0 and multiplexer_channel_num < 3:
                if adc_val > variables.LED_TEST_BLUE_LEDS_MIN_REQ:
                    logger.warn(f"Problems with blue led {multiplexer_num} {multiplexer_channel_num}: {adc_val}")
                    return "BLUE_LED_TEST_FAILED"
            elif multiplexer_num == 1 and multiplexer_channel_num == 2:
                logger.warn("BROKEN. IGNORE")
            else:
                if adc_val > variables.LED_TEST_GREEN_LEDS_MIN_REQ:
                    logger.warn(f"Problems with green led {multiplexer_num} {multiplexer_channel_num}: {adc_val}")
                    return "GREEN_LED_TEST_FAILED"

            time.sleep(0.1)

    return
