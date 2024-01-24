import os
import configparser

from loguru import logger


class ConfigLoader:
    def __init__(self, config_file: str):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self._load_config()

    def _load_config(self) -> None:
        logger.debug("Loading config")

        try:
            self.config.read(self.config_file)
        except Exception as e:
            logger.opt(exception=e).critical("Failed to load config")


class FileManager:
    def __init__(self, config: configparser.ConfigParser):
        self.config = config
        self.project_root = os.path.abspath('.')
        self.folders_to_watch = self._get_folder_paths()
        self.exception_files = self._get_exception_files()
        self.files_to_reload = self._get_files_to_reload()

    def _get_folder_paths(self) -> list:
        logger.debug("Getting folder paths")

        try:
            if 'Folders' in self.config:
                logger.debug(f"Project root: {self.project_root}")

                config_folders = self.config['Folders']['Paths'].split(',')
                abs_paths_folders_to_watch = [os.path.join(self.project_root, folder.strip()) for folder in config_folders]
                logger.debug(f"Folders to watch: {abs_paths_folders_to_watch}")

                return abs_paths_folders_to_watch
            return []

        except Exception as e:
            logger.opt(exception=e).critical("Failed to get folder paths")

    def _get_exception_files(self) -> list:
        logger.debug("Getting exception files")

        try:
            if 'Folders' in self.config and 'Exception_files' in self.config['Folders']:

                config_exception_files = self.config['Folders']['Exception_files'].split(',')
                abs_paths_exception_files = [os.path.join(os.path.abspath('.'), file.strip()) for file in config_exception_files]
                logger.debug(f"exception_files: {abs_paths_exception_files}")

                return abs_paths_exception_files
            return []

        except Exception as e:
            logger.opt(exception=e).critical("Failed to get exception files")

    @classmethod
    def get_target_files(cls) -> list:
        logger.debug("Getting target files")

        try:
            target_files = []

            for folder_path in cls.folders_to_watch:
                logger.debug(f"Start getting target files from folder {folder_path}")
                valid_files = cls._get_valid_folder_files(folder_path)

                target_files.extend(valid_files)

            logger.debug(f"Got target files: {target_files}")
            return target_files

        except Exception as e:
            logger.opt(exception=e).critical("Failed to get target files")

    @classmethod
    def _get_valid_folder_files(cls, folder_path: str) -> list:
        logger.debug("Getting valid folder files")

        try:
            files_in_folder = os.listdir(folder_path)
            logger.debug(f"Got every file from folder: {files_in_folder}")

            valid_files = []

            for file in files_in_folder:
                file_path = os.path.join(folder_path, file)

                if os.path.isfile(file_path) and file not in cls.exception_files:
                    valid_files.append(file_path)

            return valid_files

        except Exception as e:
            logger.opt(exception=e).critical(
                "Failed to get valid folder files")

    def _get_files_to_reload(self) -> list:
        logger.debug("Getting files to reload")

        try:
            if 'Folders' in self.config:
                logger.debug(f"Project root: {self.project_root}")

                config_files_to_reload = self.config['Folders']['Files_to_reload'].split(',')
                files_to_reload = [os.path.join(self.project_root, file.strip()) for file in config_files_to_reload]
                logger.debug(f"Files_to_update: {files_to_reload}")

                return files_to_reload
            return []
        
        except Exception as e:
            logger.opt(exception=e).critical("Failed to get files to update")

class ConfigManager:
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config_loader = ConfigLoader(config_file)
        self.file_manager = FileManager(self.config_loader.config)
        
    def get_target_files(self):
        return self.file_manager.get_target_files()
    
    def get_folders_to_watch(self):
        return self.file_manager.folders_to_watch
    
    def get_exception_files(self):
        return self.file_manager.exception_files
    
    def get_files_to_reload(self):
        return self.file_manager.files_to_reload