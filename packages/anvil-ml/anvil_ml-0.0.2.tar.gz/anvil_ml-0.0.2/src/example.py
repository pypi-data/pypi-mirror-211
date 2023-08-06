from anvil_ml.main import register
from utils.logger import LOGGER as logger


@register
def test1():
    logger.info("Test1 is running")
