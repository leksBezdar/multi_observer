import os
import configparser


class ConfigManager:
    def __init__(self, config_file: str):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self._load_config()

    def _load_config(self) -> None:
        self.config.read(self.config_file)

    def get_folder_paths(self):
        if 'Folders' in self.config:
            project_root = os.path.abspath('.')
        return [os.path.join(project_root, file.strip()) for file in self.config['Folders']['Paths'].split(',')]

    def get_exception_files(self):
        if 'Folders' in self.config and 'Exception_files' in self.config['Folders']:
            return [os.path.join(os.path.abspath('.'), file.strip()) for file in self.config['Folders']['Exception_files'].split(',')]