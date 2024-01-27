import sys
from loguru import logger

from observer import start_watching_files

debug_mode = True

def check_if_debug_enabled():
    if debug_mode:
        logger.add(
            sink="logs/debug.log",
            level="DEBUG",
            rotation="1 day",
            retention="1 day"
        )
        logger.info("DEBUG MODE IS ENABLED")
    else:
        logger.remove()
        logger.add(sys.stderr, level="INFO")
        logger.info("DEBUG MODE IS DISABLED")

if __name__ == "__main__":
    check_if_debug_enabled()
    start_watching_files()
