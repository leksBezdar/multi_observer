import os
import configparser
from loguru import logger

class ConfigManager:
    def __init__(self, config_file: str):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self._load_config()

    def _load_config(self) -> None:
        logger.debug("Loading config")
        self.config.read(self.config_file)

    def get_folder_paths(self) -> list:
        if 'Folders' in self.config:
            project_root = os.path.abspath('.')
            logger.debug(f"Project root: {project_root}")
        folders_to_watch = [os.path.join(project_root, file.strip()) for file in self.config['Folders']['Paths'].split(',')]
        logger.debug(f"Folders to watch: {folders_to_watch}")
        return folders_to_watch

    def get_exception_files(self) -> list:
        if 'Folders' in self.config and 'Exception_files' in self.config['Folders']:
            exception_files = [os.path.join(os.path.abspath('.'), file.strip()) for file in self.config['Folders']['Exception_files'].split(',')]
            logger.debug(f"exception_files: {exception_files}")
            return exception_files