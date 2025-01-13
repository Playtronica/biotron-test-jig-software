import os
from pathlib import Path

ROOT_PATH = Path(__file__).parent
FIRMWARE_PATH = ROOT_PATH / "firmware"
LOGGER_PATH = ROOT_PATH / "logs"

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')