import os

from watchdog.observers import Observer

from event_handler import EventHandler
from config import ConfigManager


def start_watching_files(config_file='config.txt'):
    config_manager = ConfigManager(config_file)
    observer = Observer()

    try:
        folders_to_watch = config_manager.get_folder_paths()

        for folder_path in folders_to_watch:
            observer.schedule(EventHandler(config_manager), os.path.dirname(folder_path), recursive=False)

        observer.start()

        try:
            while True:
                observer.join(1)

        except KeyboardInterrupt:
            print("Observer shutdown initiated by keyboard interrupt")

    except Exception as e:
        print(f"An unexpected error starting the observer: {e}")

    finally:
        observer.stop()
        observer.join()
        print("Observer shutdown completed")
