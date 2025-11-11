import datetime
import csv
import os
import time
import chardet
import shutil
import logging
import pandas
import tkinter as tk
from tkinter import filedialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler



# ==============================
# TO-DO
# ==============================
# 1. Fix log transfer file (duplicated logs when created)
# 2.
# 3. Create more log messages
# 4.
# 5.
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
DELIMITER = ";"
ENCODING = "utf-8"
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
    def is_csv(self):
        return self.type == CSV_EXTENSION
    
    def __str__(self):
        return f"File(name='{self.name}', type='{self.type}', path='{self.path}')"
    
    def read_file(self): 
        content = ""
        try:
            with open(self.path, 'r', newline='') as infile:
                return infile.read()
        except Exception as e:
            print(f"Error reading file: {e}")
        return content

class CSV(File):
    
    def __init__(self, path):
        super().__init__(path)  

    def get_encoding(self):
        try:
            with open(self.path, 'rb') as f:
                result = chardet.detect(f.read())
            return result['encoding']
        except Exception as e:
            print(f"Error encoding {self.name}: {e}")

    def read_csv(self):
        content = self.read_file()
        rows = csv.reader(content.splitlines(), delimiter= self.get_delimiter())
        return list(rows)

    def get_delimiter(self):
        try:
            sample = self.read_file()[:1024] 
            sniffer = csv.Sniffer()  
            delimiter = sniffer.sniff(sample).delimiter
            return delimiter
        except Exception as e:
            print(f"Error detecting delimiter: {e}")
            return ';'  

    def column(self, position: int):
        try:
            column = []
            rows = self.read_csv()
            for row in rows:
                column.append(row[position])
            return column
        except IndexError:
            print(f"Error: Column position {position} is out of bounds")
            return 
        except Exception as e:
            print(f"Error processing file: {e}")
            return 

    def header(self):
        position = 0
        try:
            data = self.read_csv()[position]
            return data
        except IndexError:
            print(f"Error: Column position {position} is out of bounds")
            return 
        except Exception as e:
            print(f"Error processing file: {e}")
            return 

    def row(self, position):
        try:
            data = self.read_csv()[position]
            return data
        except IndexError:
            print(f"Error: Row position {position} is out of bounds")
            pass 
        except Exception as e:
            print(f"Error processing file: {e}")
            pass 
    
    def get_value(self, row_index: int, position: int):
        try:
            row_data = self.row(row_index)
            if row_data is None:
                return 
            return row_data[position]
        except IndexError:
            print(f"Error: Position {position} is out of bounds in row {row_index}")
            pass
        except Exception as e:
            print(f"Error getting value: {e}")
            pass 
    
    def set_value(self, value, row, position):
        return

    def add_column(self, position):
        value = VALUE
        try:
            rows = self.read_csv()
            delimiter = self.get_delimiter()
            # Insert the new column at the given position
            for row in rows:
                if position < 0 or position > len(row):
                    row.append(value)
                else:
                    row.insert(position, value)
            # Write back to the same file safely
            with open(self.path, 'w', newline='', encoding=ENCODING) as outfile:
                writer = csv.writer(outfile, delimiter=delimiter)
                writer.writerows(rows)
            return 
        except Exception as e:
            print(f"Error adding column: {e}")
            return 

    def del_column(self, position):
        return
    
    def add_row(self, position):
        return
    
    def del_row(self, position):
        return

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
        except FileExistsError: #DirExistsError??
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
            if(os.path.isfile(file_path)) and file_path.endswith(CSV_EXTENSION):
                file = CSV(file_path)
                if (
                    file.name.lower().startswith(FILENAME_PREFIX)
                ):
                    logger.info(f"Existing file processed: {file_path}")
                    print(f"Existing file found: {file_path}")
                    file.add_column(POSITION)

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

class MyEventHandler(FileSystemEventHandler):

    def __init__(self, logger):
        self.logger = logger

    def on_created(self, event):
        if event.is_directory:
            return
        file = File(event.src_path)
        if not file.is_csv:
            return
        csv_file = CSV(event.src_path)
        FileProcessor.copy_file(csv_file.path, (os.path.join(WATCH_DIRECTORY, "backup")) ) #This needs cleaning
        self.logger.info(f"New file detected: {file.path}")
        print(f"New file detected: {file.path}")
        if file.name.startswith(FILENAME_PREFIX):
            csv_file.add_column(POSITION)



# ==============================
#              MAIN
# ==============================


print(r"""
'    ______ _ _        _____      _                       _             
'    |  ___(_) |      |_   _|    | |                     | |            
'    | |_   _| | ___    | | _ __ | |_ ___  __ _ _ __ __ _| |_ ___  _ __ 
'    |  _| | | |/ _ \   | || '_ \| __/ _ \/ _` | '__/ _` | __/ _ \| '__|
'    | |   | | |  __/  _| || | | | ||  __/ (_| | | | (_| | || (_) | |   
'    \_|   |_|_|\___|  \___/_| |_|\__\___|\__, |_|  \__,_|\__\___/|_|   
'                                          __/ |                        
'                                         |___/                         
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
