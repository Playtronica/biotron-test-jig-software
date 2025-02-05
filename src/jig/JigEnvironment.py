# TODO Was renamed from TestSystem, cut from whole code, and was made like singleton
import time

import variables
from base_logger import get_logger_for_file

from jig.jig_hardware_control.pin_controller import PinController
from jig.jig_hardware_control.Display import Display

from jig.tests.load_firmware_to_device import load_firmware_to_device
from jig.tests.midi_processes import midi_processes
from jig.tests.photoresistors_test import photoresistors_test
from jig.tests.plants_check import plants_test
from jig.tests.serial_tests import SerialTests

logger = get_logger_for_file(__name__)

class JigEnvironment:
    _instance = None

    def __init__(self,):
        self.pins = PinController()
        self.screen = Display()  # Инициализируем Screen через класс Screen
        self.serial = SerialTests()
        self.error_code = None  # To display errors
        self.pins.gpio_set_pin_direction(0, 1)  # pin 0 port 0 as input (1)
        self.current_test_function = ""  # Новый атрибут для текущей функции
        self.test_start_time = 0  # Инициализируем время старта теста
        self.execution_time = 0  # Переменная для отсчета времени выполнения теста
        self.max_test_time = variables.MAX_TEST_TIME  # Максимальное время выполнения тестов
        self.test_count = 0  # Счетчик протестированных устройств
        self.debounce_time = 0.05  # 50 миллисекунд для защиты от дребезга
        self.debounce_check_count = 2
        self.current_pin_state = 0

        self.last_pin_state = self.pins.gpio_read_pin(0)  # Начальное состояние пина

        # При старте программы выключаем USB 1
        # self.pins.usb_power_set(1, False)  # Выключаем USB 1
        self.pins.relay_set(2, 0)  # TODO check gpio boots

        logger.info("Screen updated to waiting state.")



    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def init_jig_main_cycle(self):
        logger.info("Entering main loop...")
        time.sleep(1)

        self.screen.set_text([
            "hello world",
            "shadowik"
        ])

        try:
            # while True:
            self.__main_cycle()
        except OSError as e:
            # Логируем ошибку и продолжаем выполнение программы
            logger.error(f"Error reading pin state: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize the TestSystem: {e}")
        except KeyboardInterrupt:
            logger.error("Program interrupted by user")
        finally:
            # При завершении программы включаем USB 1
            logger.info("USB port 1: ON")
            self.pins.usb_power_set(0, True)  # Включаем USB 1

            # self.screen.turn_off_screen()


    def __main_cycle(self):
        # if not self.__is_pin_status_changed():
        #     return
        #
        # if self.current_pin_state == 0:
        #     self.__device_connected()
        # elif self.current_pin_state == 1:
        #     self.__device_disconnected()
        self.__device_connected()

    def __is_pin_status_changed(self):
        logger.debug(f"Current pin state: {self.current_pin_state}")

        for checks in range(self.debounce_check_count):
            self.current_pin_state = self.pins.gpio_read_pin(0)
            if self.current_pin_state == self.last_pin_state:
                if checks != 0:
                    logger.warn("Debounce check failed")
                logger.debug("Device status has not changed")
                return False
            if checks == 0:
                logger.info(
                    f"Pin state changed from {self.last_pin_state} to {self.current_pin_state}."
                    f" Waiting for debounce time..."
                )
            time.sleep(self.debounce_time)

        logger.info("Debounce check finished successfully")
        logger.info(f"Pin state after debounce: {self.current_pin_state}")

        self.last_pin_state = self.current_pin_state
        logger.info(f"Last pin state updated to: {self.last_pin_state}")
        return True

    def __device_connected(self):
        logger.info("Pin state is 0, starting test sequence...")
        result = self.__test_process()
        result = 0
        if result != 0:
            self.error_code = result
            logger.warn(f"Test sequence finished with error code: {self.error_code}")
        else:
            logger.info("Test sequence completed successfully.")

    def __test_process(self):
        logger.info("Test sequence started.")

        logger.info(f"Boot device")
        self.pins.usb_power_set(1, False)
        time.sleep(1)
        self.pins.relay_set(2, 1)
        time.sleep(1)
        self.pins.usb_power_set(1, True)
        time.sleep(1)
        self.pins.relay_set(2, 0)
        time.sleep(1)
        res = load_firmware_to_device()

        if res is not None:
            logger.warn(f"Test sequence failed: {res}")
            return -1

        # TODO rm long delay
        logger.warn("TEST LONG DELAY")
        time.sleep(10)
        res = midi_processes()
        if res is not None:
            logger.warn(f"Test sequence failed: {res}")
            return -1

        self.serial.start_serial()
        time.sleep(0.1)

        photoresistors_test()
        plants_test()

        self.serial.stop_serial()


        logger.info("Test sequence completed successfully.")
        return 0

    def __device_disconnected(self):
        logger.info("Board removed, ready for next test")
        # self.screen.waiting_screen()
        logger.info("Screen updated to waiting state.")


