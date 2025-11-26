from csv_file import CSV
from config import Config
import chardet
import pandas as pd
import csv

def desplit_rows(self):
    rows = self.read_csv()
    result_rows = []

    for row in rows:
        if len(row) > Config.ROW_SPLIT:
            # split into two parts
            first_part = row[:Config.ROW_SPLIT]           # elements 0–45
            second_part = row[Config.ROW_SPLIT:]          # elements 46+
            result_rows.append(first_part)
            result_rows.append(second_part)
        else:
            result_rows.append(row)

    # write updated rows to new CSV
    with open(self.path, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(result_rows)

if __name__ == "__main__":
    #path = r"C:\Users\marti\OneDrive\Documentos\programació\Python\CSV transformer\app\files\test_splitrows.csv"
    path = r"C:\Test\Pedidos_20251110_1156.csv"
    path = r"C:\Test\Pedidos1.csv"
    file = CSV(path)
    #print(file.read_csv())
    print(file.get_encoding())