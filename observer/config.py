import os
import configparser

from loguru import logger


class ConfigManager:
    def __init__(self, config_file: str):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self._load_config()
        self.folders_to_watch = self._get_folder_paths()
        self.exception_files = self._get_exception_files()
    
    def _load_config(self) -> None:
        logger.debug("Loading config")
        self.config.read(self.config_file)

    def _get_folder_paths(self) -> list:
        
        if 'Folders' in self.config:
            project_root = os.path.abspath('.')
            logger.debug(f"Project root: {project_root}")
            
            config_folders = self.config['Folders']['Paths'].split(',')
            abs_paths_folders_to_watch = [os.path.join(project_root, folder.strip()) for folder in config_folders]
            logger.debug(f"Folders to watch: {abs_paths_folders_to_watch}")
            
            return abs_paths_folders_to_watch
        return []

    def _get_exception_files(self) -> list:
        if 'Folders' in self.config and 'Exception_files' in self.config['Folders']:
            
            config_exception_files = self.config['Folders']['Exception_files'].split(',')
            abs_paths_exception_files = [os.path.join(os.path.abspath('.'), file.strip()) for file in config_exception_files]
            logger.debug(f"exception_files: {abs_paths_exception_files}")
            
            return abs_paths_exception_files
        return []
    
    @classmethod
    def get_target_files(cls) -> list:
        
        target_files = []

        for folder_path in cls.folders_to_watch:
            logger.debug(f"Start getting target files from folder {folder_path}") 
            valid_files = cls._get_valid_folder_files(folder_path)

            target_files.extend(valid_files)
            
        logger.debug(f"Got target files: {target_files}")
        return target_files
    
    @classmethod
    def _get_valid_folder_files(cls, folder_path: str) -> list:
        
        files_in_folder = os.listdir(folder_path)
        logger.debug(f"Got every file from folder: {files_in_folder}")
        
        valid_files = []

        for file in files_in_folder:
            file_path = os.path.join(folder_path, file)
            
            if os.path.isfile(file_path) and file not in cls.exception_files:
                valid_files.append(file_path)
        
        return valid_files
        