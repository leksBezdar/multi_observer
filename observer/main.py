from loguru import logger
from observer import start_watching_files


debug_mode = True

def check_if_debug_enabled():
    if debug_mode:
        logger.add(
            "logs/debug.log",
            level="DEBUG",
            rotation="100 MB",
            retention="1 week", 
        )
        logger.info("DEBUG MODE IS ENABLED")
    else:
        logger.disable("INFO")
        logger.info("DEBUG MODE IS DISABLED")

if __name__ == "__main__":
    check_if_debug_enabled()
    start_watching_files()
