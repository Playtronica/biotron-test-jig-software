# TODO Was renamed from TestSystem, cut from whole code, and was made like singleton
import time

import variables
from base_logger import get_logger_for_file

from .jig_hardware_control.pin_controller import PinController

logger = get_logger_for_file(__name__)


class JigEnvironment:
    _instance = None

    def __init__(self,):
        self.pins = PinController()
        # self.screen = Screen()  # Инициализируем Screen через класс Screen
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
        print("USB port 1: OFF")
        self.pins.usb_power_set(1, False)  # Выключаем USB 1

        # self.screen.waiting_screen()
        print("Screen updated to waiting state.")

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def run_single_test(self, test_data, test_number):
        """
        Обрабатывает один тест с обновлением текущей операции, запуском теста и проверкой состояния.

        :param test_system: Система тестов.
        :param test_data: Словарь с данными для выполнения теста (функция, описание, аргументы).
        :param test_number: Номер теста, который будет автоматически передан для ошибки и описания.
        :return: Результат выполнения теста (0 - успех, номер теста - ошибка).
        """
        operation_description = f"{test_number:02d} {test_data['operation']}"  # Формируем описание с номером теста

        self.current_test_function = operation_description  # Обновляем текущее описание операции

        print(f"Running {operation_description}")

        if test_data['function'](*test_data['args']):
            result = 0  # Если тест успешен, результат = 0
        else:
            result = test_number  # Если ошибка, возвращаем номер теста

        return result

    def __main_cycle(self):
        if not self.__is_pin_status_changed():
            return

        # Проверяем текущее состояние пина
        if self.current_pin_state == 0:
            self.__device_connected()
        elif self.current_pin_state == 1:
            self.__device_disconnected()

    def __is_pin_status_changed(self):
        print(f"Current pin state: {self.current_pin_state}")

        for checks in range(self.debounce_check_count):
            self.current_pin_state = self.pins.gpio_read_pin(0)
            if self.current_pin_state == self.last_pin_state:
                if checks != 0:
                    logger.warn("Debounce check failed")
                logger.debug("Device status has not changed")
                return False
            if checks == 0:
                logger.debug(
                    f"Pin state changed from {self.last_pin_state} to {self.current_pin_state}."
                    f" Waiting for debounce time..."
                )
            time.sleep(self.debounce_time)

        logger.debug("Debounce check finished successfully")
        logger.debug(f"Pin state after debounce: {self.current_pin_state}")

        self.last_pin_state = self.current_pin_state
        logger.debug(f"Last pin state updated to: {self.last_pin_state}")
        return True

    def __device_connected(self):
        logger.info("Pin state is 0, starting test sequence...")
        result = self.run_test_sequence()
        if result != 0:
            self.error_code = result
            logger.warn(f"Test sequence finished with error code: {self.error_code}")
        else:
            logger.info("Test sequence completed successfully.")

    def run_test_sequence(self):
        """
        Запускает последовательность тестов, используя список тестов с параметрами.
        """
        status = 0  # Инициализируем статус как 0 (успех)

        """
        Start the test sequence in a separate thread.
        """
        logger.info("Starting test sequence")
        self.error_code = None
        self.current_test_function = ""  # Новый атрибут для текущей функции

        # Сбрасываем и начинаем отсчет времени выполнения тестов
        self.test_start_time = int(time.time())
        self.execution_time = 0  # Сбрасываем переменную времени
        last_update_time = 0
        update_threshold = 2

        # Список тестов с параметрами
        test_sequence = [
            # {'function': rp2040.rp2040_mode, 'args': ['boot', 1, 2], 'operation': '*Switch to BOOT'},
            # # mode, usb_port, relay_num
            # {'function': rp2040.rp2040_flash, 'args': ['test.uf2'], 'operation': '*Flash TEST.uf2'},
            # {'function': rp2040.rp2040_mode, 'args': ['normal', 1, 2], 'operation': '*Switch to NORMAL'},
            #
            # {'function': pins.relay_set, 'args': [1, 0, 2], 'operation': 'Open relay 1'},
            # {'function': test_uart_value_in_range, 'args': ['/dev/ttyACM0', 115200, 3500, 4500, 10],
            #  'operation': 'Test serial'},
            # {'function': pins.relay_set, 'args': [1, 1, 2], 'operation': 'Close relay 1'},
            # {'function': test_uart_value_in_range, 'args': ['/dev/ttyACM0', 115200, 300, 1000, 10],
            #  'operation': 'Test serial'},
            #
            # {'function': pins.usb_power_set, 'args': [1, 0], 'operation': 'Turn USB1 OFF'},
            # # turn OFF USB1 to speed up next test
            # {'function': pins.relay_set, 'args': [2, 1, 1], 'operation': 'Close relay 2'},
            # # Close the BOOT relay to speed up next test
            #
            # {'function': rp2040.rp2040_mode, 'args': ['boot', 1, 2], 'operation': 'Switch to BOOT'},
            # {'function': rp2040.rp2040_flash, 'args': ['touch_me 0512242.uf2'], 'operation': 'Flash NORMAL.uf2'},
            # {'function': rp2040.rp2040_mode, 'args': ['normal', 1, 2], 'operation': 'Switch to NORMAL'},
            #
            # {'function': pins.relay_set, 'args': [2, 1], 'operation': 'Close relay 2'},
            # # Close the BOOT relay to speed up next test
        ]

        try:
            # Выполнение тестов через цикл с автоматическим присвоением номера теста
            for i, test_data in enumerate(test_sequence, start=1):
                self.execution_time = int(time.time() - self.test_start_time)

                # Проверяем, не превысило ли время выполнения максимальное значение
                if self.execution_time > self.max_test_time:
                    print(f"Test sequence timed out after {self.execution_time} seconds.")
                    self.error_code = -1  # Устанавливаем ошибку 0 при истечении времени
                    break  # Если тест завершился с ошибкой, возвращаем её

                self.current_test_function = f"{i:02d} {test_data['operation']}"  # Update test description with the test number
                # Check if enough time has passed since the last screen update or if execution_time is 0
                if (self.execution_time == 0) or (
                        self.execution_time - last_update_time) >= update_threshold:
                    # If the time since the last update exceeds the threshold or execution_time is 0, update the screen
                    # self.screen.test_screen(self.current_test_function, self.execution_time,
                    #                         self.test_count)
                    last_update_time = self.execution_time  # Update the last update time

                status = self.run_single_test(test_data, i)
                print(f"Operation: {self.current_test_function} | Result: {status} ")

                if status != 0:
                    # Обновляем ошибку в тестовой системе и завершаем тесты
                    self.error_code = status
                    break  # Если тест завершился с ошибкой, возвращаем её

            self.error_code = status
            # Останавливаем отсчет времени при завершении тестов
            self.execution_time = int(time.time() - self.test_start_time)
            print(f"Final execution time: {self.execution_time} seconds")
            print(f"Result: {self.error_code}")

            self.test_count += 1
            if self.test_count > 9999:
                self.test_count = 0  # Сбрасываем в 0, если счетчик больше 9999

            # self.screen.result_screen(self.execution_time, self.test_count, self.error_code)

            # Выключаем USB 1 после завершения тестов
            print("USB port 1: OFF")
            self.pins.usb_power_set(1, False)  # Пример вызова функции для выключения USB 1

        except Exception as e:
            print(f"Error during test sequence: {e}")
            self.error_code = -1
            return -1  # Если произошла неожиданная ошибка

        return status  # Возвращаем результат выполнения всех тестов

    def __device_disconnected(self):
        logger.info("Board removed, ready for next test")
        # self.screen.waiting_screen()
        logger.info("Screen updated to waiting state.")

    def init_jig_main_cycle(self):
        print("Entering main loop...")
        time.sleep(1)

        try:
            while True:
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
            self.pins.usb_power_set(1, True)  # Включаем USB 1
            # self.screen.turn_off_screen()


