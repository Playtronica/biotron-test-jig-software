import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_PATH = Path(__file__).parent.parent
FIRMWARE_PATH = ROOT_PATH / "firmware"
LOGGER_PATH = ROOT_PATH / "logs"

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')