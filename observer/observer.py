import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent
import os
import multiprocessing
import psutil


file_processes: dict[str, multiprocessing.Process] = {}  # Словарь для отслеживания процессов по файлам


def run_script(file_path):
    abs_path = os.path.abspath(file_path)
    subprocess.run(['python', abs_path])

class EventHandler(FileSystemEventHandler):
    def on_modified(self, event: FileSystemEvent):
        if not event.is_directory and event.src_path.endswith('.py'): # Добавить возможность отслеживать все файлы папок (добавить функционал exclude)
            
            if event.src_path.endswith('.py'): 
                print(f'Файл {event.src_path} был изменен. Перезагружаю...')
                
                if event.src_path in file_processes:
                    old_process = file_processes[event.src_path]
                    
                    if old_process.is_alive():
                        print(f'Завершение предыдущих процессов файла {event.src_path}')
                        terminate_process_and_children(old_process)
                        
                new_process = multiprocessing.Process(target=run_script, args=(event.src_path,))
                new_process.start()
                file_processes[event.src_path] = new_process


def terminate_process_and_children(process: multiprocessing.Process):
    try:
        parent = psutil.Process(process.pid)
        children = parent.children(recursive=True)
        
        for child in children:
            child.terminate()
            
        psutil.wait_procs(children, timeout=5)
        process.terminate()
        process.join()
        
    except Exception as e:
        print(f"Ошибка в завершении процесса: {e}")


if __name__ == "__main__":
    root_path = '.'  # Отслеживаемая директория (вынести в настраиваемый конфиг)
    event_handler = EventHandler()
    observer = Observer()

    handler_added = False
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py") and not handler_added:
                observer.schedule(event_handler, root, recursive=False)
                handler_added = True


    observer.start()

    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        
    except Exception as e:
        print(f"Непредвиденная ошибка запуска обсервера {e}")

