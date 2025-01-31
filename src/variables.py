import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = Path(__file__).parent.parent
FIRMWARE_PATH = ROOT_PATH / "firmware"
os.makedirs(FIRMWARE_PATH, exist_ok=True)

LOGGER_PATH = ROOT_PATH / "logs"
os.makedirs(LOGGER_PATH, exist_ok=True)

MAX_TEST_TIME = 70

