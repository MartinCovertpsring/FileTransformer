import time
from watchdog.observers import Observer
from config import Config
from event_handler import MyEventHandler
from file_processor import FileProcessor, Logger

def display_banner():
    print(r"""
    ______ _ _        _____      _                       _             
    |  ___(_) |      |_   _|    | |                     | |            
    | |_   _| | ___    | | _ __ | |_ ___  __ _ _ __ __ _| |_ ___  _ __ 
    |  _| | | |/ _ \   | || '_ \| __/ _ \/ ` | '__/ _` | __/ _ \| '__|
    | |   | | |  __/  _| || | | | ||  __/ (_| | | | (_| | || (_) | |   
    \_|   |_|_|\___|  \___/_| |_|\__\___|\__, |_|  \__,_|\__\___/|_|   
                                          __/ |                        
                                         |___/                         
""")


def initialize_directories():
    file_handler = FileProcessor()
    file_handler.mkdir(Config.DIRECTORY_LOG)
    file_handler.mkdir(Config.DIRECTORY_BACKUP)

def setup_logging(log_handler):
    log_handler.process_old_logs()
    log_handler.create_log()

def process_initial_files(file_handler):
    file_handler.backup_files(Config.WATCH_DIRECTORY, Config.CSV_EXTENSION)
    file_handler.process_existing_files(Config.WATCH_DIRECTORY, Config.CSV_EXTENSION)

def start_file_watcher(event_handler):
    observer = Observer()
    observer.schedule(event_handler, Config.WATCH_DIRECTORY, recursive=False)
    observer.start()
    return observer

def run_monitoring_loop(observer):
    try:
        print(f"\nMonitoring directory: {Config.WATCH_DIRECTORY}")
        print("Press Ctrl+C to stop...\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping file watcher...")
        observer.stop()
    finally:
        observer.join()
        print("File watcher stopped.")

def main():
    display_banner()

    # Initialize components
    log_handler = Logger()
    file_handler = FileProcessor()
    event_handler = MyEventHandler(log_handler)

    # Setup application
    initialize_directories()
    setup_logging(log_handler)
    process_initial_files(file_handler)
    
    # Start monitoring
    observer = start_file_watcher(event_handler)
    run_monitoring_loop(observer)


if __name__ == "__main__":
    main()