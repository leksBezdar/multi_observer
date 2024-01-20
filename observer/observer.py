import inspect
import os

from watchdog.observers import Observer
from loguru import logger
from event_handler import EventHandler
from config import ConfigManager


def start_watching_files(config_file='config.txt'):
    config_manager = ConfigManager(config_file)
    observer = Observer()

    try:
        logger.debug(f"Start watching files from {config_file}")
        folders_to_watch = config_manager.get_folder_paths()
        logger.debug(f"Got folders to watch: {folders_to_watch}")
        
        for folder_path in folders_to_watch:
            logger.debug(f"Watvhing folder path: {folder_path}")
            observer.schedule(EventHandler(config_manager), os.path.dirname(folder_path), recursive=False)

        observer.start()

        try:
            while True:
                # Проверяет каждую секунду, не появились ли новые события
                observer.join(1)

        except KeyboardInterrupt:
            logger.debug(f"Observer shutdown initiated by keyboard interrupt")

    except Exception as e:
        method_name = inspect.currentframe().f_back.f_code.co_name 
        logger.opt(exception=e).critical(f"An unexpected error starting the observer in {method_name}")

    finally:
        observer.stop()
        observer.join()
        logger.debug("Observer shutdown completed")
