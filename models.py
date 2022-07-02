""" Model class """
# Import system modules
import csv
from pathlib import Path
from datetime import datetime
import os

# Import custom modules
from constants import FieldTypes as FT


class CSVModel:
    """ CSV file storage """
    def __init__(self):
        datestring = datetime.today().strftime("%Y_%m_%d")
        filename = "ratings_{}.csv".format(datestring)
        self.file = Path(filename)

        # Check for write access to store csv
        file_exists = os.access(self.file, os.F_OK)
        parent_writable = os.access(self.file.parent, os.W_OK)
        file_writable = os.access(self.file, os.W_OK)
        if (
            (not file_exists and not parent_writable) or
            (file_exists and not file_writable)
        ):
            msg = f"Permission denied accessing file: {filename}"
            raise PermissionError(msg)

    # Data dictionary
    fields = {
        "Awareness Rating": {'req': True, 'type': FT.decimal},
        "Acceptability Rating": {'req': True, 'type': FT.decimal}
        }

    
    def save_record(self, data):
        """ Save a dictionary of data to .csv file """
        newfile = not self.file.exists()
        with open(self.file, 'a', newline='') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)