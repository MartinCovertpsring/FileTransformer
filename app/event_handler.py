import os
import csv
from csv_file import CSV
from config import Config
from file import File
from file_processor import FileProcessor
from watchdog.events import FileSystemEventHandler


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
        FileProcessor.copy_file(csv_file.path, (os.path.join(Config.WATCH_DIRECTORY, "backup")) ) #This needs cleaning
        self.logger.info(f"New file detected: {file.path}")
        print(f"New file detected: {file.path}")
        if file.name.lower().startswith(Config.FILENAME_PREFIX.lower()):           
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