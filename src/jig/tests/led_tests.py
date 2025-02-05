import time
from base_logger import get_logger_for_file
from jig.jig_hardware_control.ads1015_4051 import MultiplexerADCReader

logger = get_logger_for_file(__name__)


adc_read = MultiplexerADCReader()

def led_tests():
    for multiplexer_num in range(2):
        for multiplexer_channel_num in range(8):
            adc_val = adc_read.read_channel(multiplexer_num, multiplexer_channel_num)
            logger.info(f"Value of multiplexer {multiplexer_num} {multiplexer_channel_num}: {adc_val}")
            time.sleep(0.1)