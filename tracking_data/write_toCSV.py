import csv

class CSVWriter:
    def __init__(self, file_path, fieldnames):
        self.file_path = file_path
        self.fieldnames = fieldnames
        self.csv_file = open(file_path, mode='a', newline='')
        #self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=fieldnames)

        # Write the header row if the file is empty
        if self.csv_file.tell() == 0:
            self.csv_writer.writeheader()

    def write_row(self, row_data):
        self.csv_writer.writerow(row_data)

    def close_file(self):
        self.csv_file.close()
