from config import Config
from file import File
from io import StringIO
import chardet
import csv


class CSV(File):

    def __init__(self, path):
        super().__init__(path)  

    def get_encoding(self):
        try:
            with open(self.path, 'rb') as f:
                result = chardet.detect(f.read(4096))
            return result['encoding']
        except Exception as e:
            print(f"Error encoding {self.name}: {e}")

    def set_encoding(self, new_encoding):
        try:
            with open(self.path, 'r', encoding='utf-8', newline='') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
        except Exception as e:
            print(f"Error reading file: {e}")
            return False
        
        try:
            with open(self.path, 'w', encoding=new_encoding, errors='replace', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
        except Exception as e:
            print(f"Error reading file: {e}")
        return 

    def read_csv(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return list(csv.reader(f, delimiter=";"))

    def get_delimiter(self):
        try:
            with open(self.path, 'r', newline='') as infile:
                sample = infile.read(4096)
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

    def add_column(self, position):
        value = Config.VALUE
        try:
            rows = self.read_csv()
            delimiter = ";"
            if not (0 <= position <= len(rows[0])):
                raise IndexError(f"Column position {position} is out of bounds")
            for row in rows:
                row.insert(position, value)
            # Write back to the same file safely
            with open(self.path, 'w', newline='', encoding=Config.ENCODING) as outfile:
                writer = csv.writer(outfile, delimiter=delimiter)
                writer.writerows(rows)
        except IndexError:
            print(f"Error adding column: Column position {position} is out of bounds")
        except Exception as e:
            print(f"Error adding column: {e}")
            return 

    def del_column(self, position):
        try:
            rows = self.read_csv()
            delimiter = self.get_delimiter()
            for row in rows:
                del row[position]
            # Write back to the same file safely
            with open(self.path, 'w', newline='', encoding=Config.ENCODING) as outfile:
                writer = csv.writer(outfile, delimiter=delimiter)
                writer.writerows(rows)
        except IndexError:
            print(f"Error deleting column: Column position {position} is out of bounds")
        except Exception as e:
            print(f"Error deleting column: {e}")
            return 

    def add_row(self, position):
        value = Config.VALUE_EMPTY
        try:
            rows = self.read_csv()
            delimiter = ";"
            if not (0 <= position <= len(rows[0])):
                raise IndexError(f"Column position {position} is out of bounds")
            for row in rows:
                row.insert(position, value)
            # Write back to the same file safely
            with open(self.path, 'w', newline='', encoding=Config.ENCODING) as outfile:
                writer = csv.writer(outfile, delimiter=delimiter)
                writer.writerows(rows)
        except IndexError:
            print(f"Error: row position {position} is out of bounds")
        except Exception as e:
            print(f"Error adding row: {e}")
            return 

    def del_row(self, position):
        value = Config.VALUE_EMPTY
        try:
            rows = self.read_csv()
            delimiter = self.get_delimiter()
            if not (0 <= position <= len(rows[0])):
                raise IndexError(f"Column position {position} is out of bounds")
            for row in rows:
                row.pop(position)
            # Write back to the same file safely
            with open(self.path, 'w', newline='', encoding=Config.ENCODING) as outfile:
                writer = csv.writer(outfile, delimiter=";")
                writer.writerows(rows)
        except IndexError:
            print(f"Error: row position {position} is out of bounds")
        except Exception as e:
            print(f"Error adding row: {e}")
            return 

    def set_value(self, value, row, column):
        try:
            rows = self.read_csv()
            #delimiter = self.get_delimiter()
            if row < 0 or row >= len(rows):
                raise IndexError(f"Row {row} is out of bounds")
            if column < 0 or column >= len(rows[row]):
                raise IndexError(f"Column {column} is out of bounds")
            rows[row][column] = value
            # Write back to the same file safely
            with open(self.path, 'w', newline='', encoding=Config.ENCODING) as outfile:
                writer = csv.writer(outfile, delimiter=";")
                writer.writerows(rows)
        except Exception as e:
            print(f"Error adding row: {e}")
            return 

    def del_value(self, row, column):
        try:
            rows = self.read_csv()
            #delimiter = self.get_delimiter()
            if row < 0 or row >= len(rows):
                raise IndexError(f"Row {row} is out of bounds")
            if column < 0 or column >= len(rows[row]):
                raise IndexError(f"Column {column} is out of bounds")
            rows[row][column] = ""
            # Write back to the same file safely
            with open(self.path, 'w', newline='', encoding=Config.ENCODING) as outfile:
                writer = csv.writer(outfile, delimiter=";")
                writer.writerows(rows)
        except Exception as e:
            print(f"Error adding row: {e}")
            return 

    def replace_value_all(self, current_value, new_value):
        try:
            data = self.read_csv()
            delimiter = ";"
            if not current_value:
                raise ValueError(f"Empty value")
            for row in data:
                for i, value in enumerate(row):
                    if row[i].startswith(current_value):
                        row[i] = new_value
            # Write back to the same file safely
            with open(self.path, 'w', newline='', encoding=Config.ENCODING) as outfile:
                writer = csv.writer(outfile, delimiter=delimiter)
                writer.writerows(data)
        except ValueError:
            print(f"Empty value")
        except Exception as e:
            print(f"Error adding column: {e}")
            return 

    def convert_to_ansi(self, output_path=None):
        # Read the file in binary mode
        with open(self.path, 'rb') as file:
            raw_data = file.read()
        # Try UTF-8 first 
        for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']:
            try:
                text_content = raw_data.decode(encoding)
                print(f"Successfully decoded with: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError("Could not decode the file with any common encoding")
        # Convert to ANSI (Windows-1252)
        ansi_content = self.clean_text_for_ansi(text_content)
        if output_path is None:
            output_path = self.path

        with open(output_path, 'wb') as output_file:
            output_file.write(ansi_content)

        print(f"File converted and saved to: {output_path}")

    def clean_text_for_ansi(self, text):
        """Replace ALL characters that can't be represented in ANSI (CP-1252)"""
        # Apply replacements from config
        for unicode_char, replacement in Config.UNICODE_TO_ANSI_REPLACEMENTS.items():
            text = text.replace(unicode_char, replacement)

        return text.encode('cp1252', errors='replace')
    
    def split_rows(self):
        rows = self.read_csv()
        if not rows:
            return  # empty file

        header = rows[0]       # keep header as-is
        data_rows = rows[1:]   # all rows except header
        result_rows = [header] # start result with header

        for row in data_rows:

            if "SERIE" in row:
                index = row.index("SERIE")
                first_part = row[:index]
                second_part = row[index:]
                # Only add first_part if it has any content
                if first_part:
                    result_rows.append(first_part)
                result_rows.append(second_part)
            else:
                result_rows.append(row)

        # Write the modified rows back to the original file
        with open(self.path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerows(result_rows)

    def merge_serie_rows(self):
        rows = self.read_csv()
        if not rows:
            return  # empty file

        header = rows[0]       # keep header as-is
        data_rows = rows[1:]   # all rows except header
        result_rows = [header] # start result with header

        for row in data_rows:
            if "SERIE" in row:
                # Append this row to the previous row
                if result_rows:
                    result_rows[-1].extend(row)
                else:
                    # Edge case: first row is SERIE, just add it
                    result_rows.append(row)
            else:
                result_rows.append(row)

        # Write the modified rows back to the original file
        with open(self.path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerows(result_rows)

        
