from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import datetime

import csv
import os
import time
import chardet
import shutil
import logging

# ==============================
# CONFIGURATION PARAMETERS
# ==============================
CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
WATCH_DIRECTORY = r"C:\Test"
POSITION = 5                     # Column index where the new value will be inserted
VALUE = "NOMBRE ARTÍCULO"        # The value to insert into each row
FILENAME_PREFIX = "pedidos"      # Files to match (case-insensitive)
CSV_EXTENSION = ".csv"          # File type to monitor
DIRECTORY_BACKUP = "backup"      # Directory name for file backup
DIRECTORY_LOG = "logs"           # Directory name for file backup
# ==============================

class Logger:
    
    ###### Creating a Singleton Pattern so that every class can use the same Log file
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance


    def __init__(self):
        log_filename = f"log_{CURRENT_DATE}.log"
        log_dir = os.path.join(WATCH_DIRECTORY, DIRECTORY_LOG)
        #log_file = os.path.join(log_dir, log_filename)
        # Create and configure logger
        logging.basicConfig(level=logging.INFO,
                            filename=os.path.join(log_dir, log_filename),
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode='w')
        self.logger = logging.getLogger()


    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

class FileProcessor:


    @staticmethod
    def create_backupFile(file_path, backupFolder):
            logger = Logger()  # Get the singleton instance
            time.sleep(1)
            try:
                shutil.copy2(file_path, backupFolder)
                logger.info(f"Backed up  file {file_path}")
                print(f"Backed up  file {file_path}")
            except PermissionError:
                print(f"File {file_path} is still locked, skipping backup")
            except Exception as e:
                print(f"Error creating backup: {e}")
    
    @staticmethod
    def mkdir(backup, logs):
        path_backup = os.path.join(WATCH_DIRECTORY, backup)
        path_logs = os.path.join(WATCH_DIRECTORY, logs)
        try:
            if not os.path.exists(path_backup):
                os.mkdir(path_backup)
            if not os.path.exists(path_logs):
                os.mkdir(path_logs)
        except FileExistsError:
            return
        except PermissionError:
            return
        except Exception as e:
            return
        
    #def process_file(file_type)

class MyEventHandler(FileSystemEventHandler):

    def __init__(self, logger):
        self.logger = logger

    def process_existing_files(self, file_extension):
        for filename in os.listdir(WATCH_DIRECTORY):
            file_path = os.path.join(WATCH_DIRECTORY, filename)
            if (
                os.path.isfile(file_path)
                and filename.lower().endswith(file_extension)
                and filename.lower().startswith(FILENAME_PREFIX)
            ):
                self.logger.info(f"Existing file processed: {file_path}")
                print(f"Existing file found: {file_path}")
                self.process_file(file_path)
    
    def backup_existing_files(self, file_extension):
        for filename in os.listdir(WATCH_DIRECTORY):
            file_path = os.path.join(WATCH_DIRECTORY, filename)
            if (
                os.path.isfile(file_path)
                and filename.lower().endswith(file_extension)
            ):
                FileProcessor.create_backupFile(file_path, (os.path.join(WATCH_DIRECTORY, "backup")))
                self.logger.info(f"Existing file saved in: {file_path}")

    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            filename = os.path.basename(file_path).lower()
            if filename.endswith(CSV_EXTENSION):
                FileProcessor.create_backupFile(file_path, (os.path.join(WATCH_DIRECTORY, "backup")) )
                self.logger.info(f"New file detected: {file_path}")
                print(f"New file detected: {file_path}")
            if filename.endswith(CSV_EXTENSION) and filename.startswith(FILENAME_PREFIX):
                self.process_file(file_path)

    def process_file(self, file_path):
        time.sleep(1)  # Wait for file to finish writing
        try:
             # Read all data first
            with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile, delimiter=";")
                data = list(reader)

            # Write modified data back
            with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, delimiter=";")

                # Modify header
                header = data[0]
                header.insert(POSITION, VALUE)
                writer.writerow(header)

                # Modify and write each data row
                for row in data[1:]:
                    row.insert(POSITION, VALUE)
                    writer.writerow(row)
            
            with open(file_path, 'rb') as f:
                data = f.read()
                # Step 3: Detect Encoding using chardet Library
                encoding_result = chardet.detect(data)
                # Step 4: Retrieve Encoding Information
                encoding = encoding_result['encoding']
                # Step 5: Print Detected Encoding Information
            self.logger.info(f"File processed: {file_path}, encoded in {encoding}")
            print(f"File processed: {file_path}")
            print("Press Ctrl + C to stop")
        except Exception as e:
            print(f"Error processing file: {e}")


# ==============================
#              MAIN
# ==============================


log_handler = Logger()
event_handler = MyEventHandler(log_handler)
file_handler = FileProcessor()
file_handler.mkdir(DIRECTORY_LOG, DIRECTORY_BACKUP)
#event_handler.mkdir(DIRECTORY_LOG, DIRECTORY_BACKUP)
event_handler.backup_existing_files(CSV_EXTENSION)
event_handler.process_existing_files(CSV_EXTENSION)
observer = Observer()
observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)
observer.start()

try:
    while True:
            time.sleep(2)  # This should work now
except KeyboardInterrupt:
        print("\nStopping file watcher...")
        observer.stop()
finally:
        observer.join()
        print("File watcher stopped.")
