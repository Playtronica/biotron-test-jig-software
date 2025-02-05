import mido
import mido.backends.rtmidi

from base_logger import get_logger_for_file
logger = get_logger_for_file(__name__)

biotron_midi_output = None

sysex_test_mode = mido.Message.from_bytes([240, 11, 20, 13, 0, 247])
sysex_enable_logs = mido.Message.from_bytes([240, 11, 20, 13, 2, 247])


def find_midi_device():
    try:
        global biotron_midi_output
        print(mido.get_output_names())
        for output_device in mido.get_output_names():
            if "Biotron" in output_device:
                logger.info("Biotron was found")
                biotron_midi_output = mido.open_output(output_device)
                return True
        return False
    except Exception as e:
        logger.error(f"Some error while connecting to biotron: {e}")
        return False


def close_midi_connection_from_device():
    try:
        global biotron_midi_output
        if not biotron_midi_output:
            logger.info("Device is not connected")
            return False

        biotron_midi_output.close()
        biotron_midi_output = None
        return True
    except Exception as e:
        logger.error(f"Some error while closing midi device: {e}")
        return False


def send_debug_sysex_messages_to_midi_device():
    try:
        if not biotron_midi_output:
            logger.warn("MIDI Device is not found")
            return False

        biotron_midi_output.send(sysex_test_mode)
        biotron_midi_output.send(sysex_enable_logs)
        return True
    except Exception as e:
        logger.error(f"Some error while sending debug sys ex: {e}")
        return False


def midi_processes():
    if not find_midi_device():
        logger.warn("MIDI Device is not found")
        return "MIDI_NOT_FOUND"

    if not send_debug_sysex_messages_to_midi_device():
        logger.warn("Failed to send sysex messages")
        return "SYSEX_ERROR"

    if not close_midi_connection_from_device():
        logger.warn("Failed to close midi connection")
        return "MIDI_CLOSE_ERROR"

    return
