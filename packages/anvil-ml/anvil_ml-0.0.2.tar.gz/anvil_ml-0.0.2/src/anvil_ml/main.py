# Import logger
import sys

sys.path.insert(0, "..")
from utils.logger import LOGGER as logger

from fire import Fire

test_registery = []


def register(func):
    logger.info(f"Registering {func.__name__} as a test")
    test_registery.append(func)
    return func


def main():
    logger.error("Hello, World!")
    for test in test_registery:
        test()


if __name__ == "__main__":
    Fire(main)
