""" Model class """
# Import system modules
import csv
from pathlib import Path
from datetime import datetime
import os

# Import data modules
import json

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


class SettingsModel:
    """ A model for saving settings """
    # fields = {
    #     'Subject': {'type': 'str', 'value': '999'},
    #     'Condition': {'type': 'str', 'value': 'Quiet'},
    #     'Presentation Level': {'type': 'float', 'value': 65},
    #     'Speaker Number': {'type': 'int', 'value': 1},
    #     'Audio Files Path': {'type': 'str', 'value': 'Please select a path'}
    # }
    fields = {
        'autofill date': {'type': 'bool', 'value': True}
    }


    def __init__(self):
        filename = 'rating_tool.json'
        # Store settings file in user's home directory
        self.filepath = Path.home() / filename
        # Load settings file
        self.load()


    def load(self):
        """ Load the settings from the file """
        # If the file doesn't exist, return
        if not self.filepath.exists():
            return

        # Open the file and read in the raw values
        with open(self.filepath, 'r') as fh:
            raw_values = json.load(fh)

        # Don't implicitly trust the raw values; only get known keys
        for key in self.fields:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.fields[key]['value'] = raw_value


    def save(self):
        """ Save the current settings to the file """
        with open(self.filepath, 'w') as fh:
            json.dump(self.fields, fh)

    
    def set(self, key, value):
        """ Set a variable value """
        if (
            key in self.fields and 
            type(value).__name__ == self.fields[key]['type']
        ):
            self.fields[key]['value'] = value
        else:
            raise ValueError("Bad key or wrong variable type")

