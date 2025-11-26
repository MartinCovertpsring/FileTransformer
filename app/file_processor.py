import os
import csv
import shutil
import time
import logging
from file import File
from csv_file import CSV
from config import Config

class FileProcessor:

    @staticmethod
    def mkdir(folder_name):
        folder_path = os.path.join(Config.WATCH_DIRECTORY, folder_name)
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
            if(os.path.isfile(file_path)) and file_path.endswith(Config.CSV_EXTENSION):
                csv_file = CSV(file_path)
                if (
                    csv_file.name.lower().startswith(Config.FILENAME_PREFIX.lower())
                ):
                    logger.info(f"Existing file processed: {file_path}")
                    print(f"Existing file found: {file_path}")
                    csv_file.split_rows()
                    csv_file.add_column(Config.POSITION)
                    csv_file.merge_serie_rows()
                    csv_file.convert_to_ansi()
                    #CLEAN THIS LATTER
                    with open(csv_file.path, "r", encoding=csv_file.get_encoding()) as f:
                        rows = list(csv.reader(f, delimiter=";"))
                    for row in rows:
                        if row[8] in ["?", "�"]:
                            row[8] = 0
                    with open(csv_file.path, "w", newline="", encoding=csv_file.get_encoding()) as f:
                        writer = csv.writer(f, delimiter=";")
                        writer.writerows(rows)             

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
        log_filename = f"log_{Config.CURRENT_DATE}.log"
        log_dir = os.path.join(Config.WATCH_DIRECTORY, Config.DIRECTORY_LOG)
        # Create and configure logger
        logging.basicConfig(level=logging.INFO,
                            filename=os.path.join(log_dir, log_filename),
                            format='%(asctime)s - %(levelname)s - %(message)s',
                            filemode='w')
        self.logger = logging.getLogger()
    
    def process_old_logs(self):
        #Check if folder old_logs exists
        log_dir = os.path.join(Config.WATCH_DIRECTORY, Config.DIRECTORY_LOG)
        new_log_dir = os.path.join(log_dir, "old logs")
        FileProcessor.mkdir(new_log_dir)

        # Send existing logs to a separate folder
        for file in os.listdir(log_dir):
            file_path = os.path.join(log_dir, file)
            if (
                os.path.isfile(file_path)  # Check the full path, not just filename
                and file.lower().endswith(Config.EXTENSION_LOG)  # Check filename, not full path
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
