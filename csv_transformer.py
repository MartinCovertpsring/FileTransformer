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
# TO-DO
# ==============================
# 1. Fix log transfer file (duplicated logs when created)
# 2. Divide createBakup method into two methods: createCopy and move_file
# 3. Create more log messages
# 4. REWRITE process_file METHOD
# 5. Transfer file methods to FileProcessor, leave EventHandler only for events on directories
# 6. Event methods should have (self, event, action) where action is a FileProcessor method
# 7. create_backupFile is redundant: copy + move methods
# 8. If a file is replaced, it doesn't get processed again. Not a real case use for now but should be addressed latter on. 
# ==============================

# ==============================
# CONFIGURATION PARAMETERS
# ==============================
CURRENT_DATE = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
WATCH_DIRECTORY = r"C:\Test"
POSITION = 5                     # Column index where the new value will be inserted
VALUE = "NOMBRE ARTÍCULO"        # The value to insert into each row
FILENAME_PREFIX = "pedidos"      # Files to match (case-insensitive)
CSV_EXTENSION = ".csv"           # File type to monitor
EXTENSION_LOG = ".log"           # File type to monitor
DIRECTORY_BACKUP = "backup"      # Directory name for file backup
DIRECTORY_LOG = "logs"           # Directory name for file backup
# ==============================


class File:
    def __init__(self, path):
        self._path = os.path.abspath(path)
        self.is_processed = False

    @property
    def path(self):
        return self._path
    
    @property
    def name(self):
        return os.path.splitext(os.path.basename(self._path))[0]
    
    @property
    def type(self):
        return os.path.splitext(self._path)[1].lower()
    
    @property
    def directory(self):
        return os.path.dirname(self._path)
    
    @property
    def is_cvs(self):
        return self.type == CSV_EXTENSION
    
    def __str__(self):
        return f"File(name='{self.name}', type='{self.type}', path='{self.path}')"

class Logger:
    
    _instance = None
    _initialized = False
    
        ###### Creating a Singleton Pattern so that every class can use the same Log file
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    '''
    def __init__(self):

        #Create new log
        #log_file = os.path.join(log_dir, log_filename)
    '''

    def create_log(self):
        log_filename = f"log_{CURRENT_DATE}.log"
        log_dir = os.path.join(WATCH_DIRECTORY, DIRECTORY_LOG)
        # Create and configure logger
        logging.basicConfig(level=logging.INFO,
                            filename=os.path.join(log_dir, log_filename),
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode='w')
        self.logger = logging.getLogger()
    
    def process_old_logs(self):
        #Check if folder old_logs exists
        log_dir = os.path.join(WATCH_DIRECTORY, DIRECTORY_LOG)
        new_log_dir = os.path.join(log_dir, "old logs")
        FileProcessor.mkdir(new_log_dir)

        # Send existing logs to a separate folder
        for file in os.listdir(log_dir):
            file_path = os.path.join(log_dir, file)
            if (
                os.path.isfile(file_path)  # Check the full path, not just filename
                and file.lower().endswith(EXTENSION_LOG)  # Check filename, not full path
            ):
                FileProcessor.move_file(file_path, new_log_dir)

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
    def mkdir(folder_name):
        folder_path = os.path.join(WATCH_DIRECTORY, folder_name)
        try:
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
        except FileExistsError:
            return
        except PermissionError:
            return
        except Exception as e:
            return

    @staticmethod
    def move_file(file, destination):
        logger = Logger() 
        try:
            # Handle both File objects and string paths
            if hasattr(file, 'path'):
                # It's a File object - use its path
                shutil.move(file.path, destination)
            else:
                # It's probably a string path
                shutil.move(file, destination)
        except FileExistsError:
            return
        except Exception as e:
            logger.error(f"Error sending file {file} to {destination}")

    @staticmethod
    def copy_file(file, destination):
        logger = Logger()  # Get the singleton instance
        time.sleep(1)
        try:
            # Handle both File objects and string paths
            if hasattr(file, 'path'):
                # It's a File object - use its path
                shutil.copy2(file.path, destination)
            else:
                # It's probably a string path
                shutil.copy2(file, destination)
        except PermissionError:
            logger.error(f"File {file} is still locked, skipping copy")
        except Exception as e:
            print(f"Error copying {file}: {e}")

    @staticmethod
    def process_existing_files(directory, file_extension):
        logger = Logger()  # Get the singleton instance
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if(os.path.isfile(file_path)):
                file = File(file_path)
                if (
                    file.type == file_extension
                    and file.name.lower().startswith(FILENAME_PREFIX)
                ):
                    logger.info(f"Existing file processed: {file_path}")
                    print(f"Existing file found: {file_path}")
                    FileProcessor.add_column(file, POSITION, VALUE)

    @staticmethod
    def backup_files(directory, file_extension):
        logger = Logger()  
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if(os.path.isfile(file_path)):
                file = File(file_path)
                if (
                    file.type == file_extension
                ):
                    FileProcessor.copy_file(file_path, (os.path.join(directory, "backup")))
                    logger.info(f"Existing file saved in: {file_path}")


    def add_column(file, position, value):
        logger = Logger()  # Get the singleton instance
        time.sleep(1)  # Wait for file to finish writing
        try:
                # Read all data first
            with open(file.path, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile, delimiter=";")
                data = list(reader)

            # Write modified data back
            with open(file.path, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, delimiter=";")

                # Modify header
                header = data[0]
                header.insert(position, value)
                writer.writerow(header)

                # Modify and write each data row
                for row in data[1:]:
                    row.insert(position, value)
                    writer.writerow(row)

            with open(file.path, 'rb') as f:
                data = f.read()
                # Step 3: Detect Encoding using chardet Library
                encoding_result = chardet.detect(data)
                # Step 4: Retrieve Encoding Information
                encoding = encoding_result['encoding']
                # Step 5: Print Detected Encoding Information
            logger.info(f"File processed: {file.path}, encoded in {encoding}")
            print(f"File processed: {file.path}")
            print("Press Ctrl + C to stop")
        except Exception as e:
            print(f"Error processing file: {e}")


class MyEventHandler(FileSystemEventHandler):

    def __init__(self, logger):
        self.logger = logger

    def on_created(self, event):
        if not event.is_directory:
            file = File(event.src_path)
            if file.is_cvs:
                FileProcessor.copy_file(file.path, (os.path.join(WATCH_DIRECTORY, "backup")) )
                self.logger.info(f"New file detected: {file.path}")
                print(f"New file detected: {file.path}")
            if file.is_cvs and file.name.startswith(FILENAME_PREFIX):
                FileProcessor.add_column(file, POSITION, VALUE)


# ==============================
#              MAIN
# ==============================


print(r"""
                      _____                                       
                     | ___ \                                      
      ___ _____   __ | |_/ / __ ___   ___ ___  ___ ___  ___  _ __ 
     / __/ __\ \ / / |  __/ '__/ _ \ / __/ _ \/ __/ __|/ _ \| '__|
    | (__\__ \\ V /  | |  | | | (_) | (_|  __/\__ \__ \ (_) | |   
     \___|___/ \_/   \_|  |_|  \___/ \___\___||___/___/\___/|_|   
                                                                 
""")

log_handler = Logger()
file_handler = FileProcessor()
file_handler.mkdir(DIRECTORY_LOG)
file_handler.mkdir(DIRECTORY_BACKUP)
event_handler = MyEventHandler(log_handler)
log_handler.process_old_logs()
log_handler.create_log()
file_handler.backup_files(WATCH_DIRECTORY, CSV_EXTENSION)
file_handler.process_existing_files(WATCH_DIRECTORY, CSV_EXTENSION)
observer = Observer()
observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)
observer.start()


try:
    while True:
            time.sleep(2)
except KeyboardInterrupt:
        print("\nStopping file watcher...")
        observer.stop()
finally:
        observer.join()
        print("File watcher stopped.")
