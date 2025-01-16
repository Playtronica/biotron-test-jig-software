import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_PATH = Path(__file__).parent.parent
ENV_PATH = ROOT_PATH / ".env"
load_dotenv(ENV_PATH)

ROOT_PATH = Path(__file__).parent.parent
FIRMWARE_PATH = ROOT_PATH / "firmware"
LOGGER_PATH = ROOT_PATH / "logs"

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')