import logging
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
LOGGER_PATH = ROOT_PATH / "logs"

base_logger = logging.getLogger(__name__)


def initialize_logger():
    base_logger.setLevel(logging.INFO)

    handler = logging.FileHandler(LOGGER_PATH / f'{__name__}.log', mode="w+")
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

    handler.setFormatter(formatter)
    base_logger.addHandler(handler)


def get_logger_child(name):
    return base_logger.getChild(name)