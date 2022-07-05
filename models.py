""" Model class """
# GUI modules
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# Import system modules
import csv
from pathlib import Path
from datetime import datetime
import os

# Import data modules
import json

# Import science modules
import numpy as np
from scipy.io import wavfile

# Import audio modules
import sounddevice as sd

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


class Audio:
    """ An object for use with .wav files. Audio objects 
        can import .wav files, handle audio data type 
        conversion, and store information about a .wav 
        file.
    """
    def __init__(self):
        # Initialize attributes
        self.name = None
        self.file_path = None
        self.data_type = None
        self.fs = None
        self.dur = None
        self.t = None
        self.original_audio = None
        self.modified_audio = None

        # Dictionary of data types and ranges
        self.wav_dict = {
            'float32': (-1.0, 1.0),
            'int32': (-2147483648, 2147483647),
            'int16': (-32768, 32767),
            'uint8': (0, 255)
        }


    def do_import_audio(self):
        """ Select file using system file dialog 
            and read it into a dictionary.
        """
        file_name = filedialog.askopenfilename()
        self.file_path = file_name.split(os.sep)
        just_name = file_name.split('/')[-1]
        self.name = str(just_name)

        fs, audio_file = wavfile.read(file_name)
        self.fs = fs
        self.original_audio = audio_file

        audio_dtype = np.dtype(audio_file[0])
        self.data_type = audio_dtype
        print(f"Incoming data type: {audio_dtype}")

        # Immediately convert to float64 for manipulating
        if audio_dtype == 'float64':
            pass
        else:
            # 1. Convert to float64
            audio_file = audio_file.astype(np.float64)
            print(f"Forced audio data type: {type(audio_file[0])}")
            # 2. Divide by original dtype max val
            audio_file = audio_file / self.wav_dict[str(audio_dtype)][1]
            self.modified_audio = audio_file

        self.dur = len(audio_file) / self.fs
        self.t = np.arange(0,self.dur, 1/self.fs)


    def do_convert_to_original_dtype(self):
        # Convert back to original audio data type
        print(self.modified_audio)
        sig = self.modified_audio * self.wav_dict[str(self.data_type)][1]
        if self.data_type != 'float32':
            # Round to return to integer values
            sig = np.round(sig)
        # Convert back to original data type
        sig = sig.astype(self.data_type)
        #print(f"Converted data type: {str(type(sig[0]))}")
        self.modified_audio = sig
