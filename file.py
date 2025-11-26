import os
from config import Config

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
    
    def set_name(self, name):
        try:
            directory = self.directory
            new_path = os.path.join(directory, name)
            os.rename(self.path, new_path)
            # Update the internal path
            self._path = new_path
            print(f"File renamed to: {name}")
        except FileNotFoundError:
            print(f"Error: File '{self.path}' not found")
        except FileExistsError:
            print(f"Error: File '{new_path}' already exists")
        except Exception as e:
            print(f"Error renaming file: {e}")


    @property
    def type(self):
        return os.path.splitext(self._path)[1].lower()
    
    @property
    def directory(self):
        return os.path.dirname(self._path)
    
    @property
    def is_csv(self):
        return self.type == Config.CSV_EXTENSION
    
    def __str__(self):
        return f"File(name='{self.name}', type='{self.type}', path='{self.path}')"
    
    def read_file(self): 
        content = ""
        try:
            with open(self.path, 'r', encoding='utf-8', newline='') as infile:
                return infile.read()
        except Exception as e:
            print(f"Error reading file: {e}")
        return content
