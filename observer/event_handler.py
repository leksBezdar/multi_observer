import os
import psutil
import inspect

import subprocess
import multiprocessing
from loguru import logger
from watchdog.events import FileSystemEvent, FileSystemEventHandler

from config import ConfigManager


file_processes: dict[str, multiprocessing.Process] = {}


class EventHandler(FileSystemEventHandler):
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            file_path = event.src_path
            logger.debug(f"file {file_path} modified")

            # Пропуск исключенных файлов
            if self._is_exception_file(file_path):
                logger.debug(f"file {file_path} is excluded")
                return

            logger.debug(f'File {file_path} has been modified. Reloading...')

            if file_path in file_processes:
                old_process = file_processes[file_path]

                if old_process.is_alive():
                    logger.debug(f'Terminating previous processes for file {file_path}')
                    self._kill_associated_processes(old_process)

            self._set_new_process(file_path)
    
    @classmethod
    def _set_new_process(cls, file_path: str) -> None:  
        new_process = multiprocessing.Process(target=cls._run_script, args=(file_path,))
        logger.debug(f"Setting new process for file {file_path}")
        new_process.start()
        file_processes[file_path] = new_process
         
    @staticmethod
    def _run_script(file_path: str) -> None:
        abs_path = os.path.abspath(file_path)
        logger.debug(f"Running the script 'python {abs_path}'")
        subprocess.run(['python', abs_path])

    @staticmethod
    def _kill_associated_processes(process: multiprocessing.Process) -> None:
        try:
            parent_process = psutil.Process(process.pid)
            children_processes = parent_process.children(recursive=True)

            for child_process in children_processes:
                child_process.terminate()

            psutil.wait_procs(children_processes, timeout=5)
            process.terminate()
            process.join()

        except Exception as e:
            method_name = inspect.currentframe().f_back.f_code.co_name
            logger.opt(exception=e).critical(f"Error terminating the process in {method_name}")
    
    def _is_exception_file(self, file_path: str) -> bool:
        exception_files = self.config_manager.get_exception_files()
        return file_path in exception_files
