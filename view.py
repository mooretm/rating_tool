""" Wav-file-based rating task. Wav files are presented 
    in random order (obviating the need for naming 
    conventions). Simple GUI with custom rating slider 
    widgets. Data are saved as .csv.

    Version 1.0.0
    Written by: Travis M. Moore
    Created: Jun 29, 2022
    Last Edited: Jul 1, 2022
"""

# Import system packages
import os
import sys
from pathlib import Path

# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Custom widgets
import widgets as w

# Import data science packages
import numpy as np
from scipy.io import wavfile
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


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


class MainFrame(ttk.Frame):
    def __init__(self, parents, model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = model
        fields = self.model.fields

        # Slider functions
        def get_current_value():
            """ Retrieves current slider values """
            return int(self._vars['Awareness Rating'].get()), int(self._vars['Acceptability Rating'].get())


        def slider_changed(event):
            """ Updates slider values when moved """
            self._vars['Awareness Rating'].set(get_current_value()[0])
            self._vars['Acceptability Rating'].set(get_current_value()[1])


        # Data dictionary
        self._vars = {
            'Awareness Rating': tk.DoubleVar(value=50),
            'Acceptability Rating': tk.DoubleVar(value=50),
        }

        # Verbal anchors
        aware_anchors = ['Not\nAware', 'Slightly\nAware', 
            'Somewhat\nAware', 'Moderately\nAware', 'Extremely\nAware']
        accept_anchors = ['Not\nAcceptable', 'Slightly\nAcceptable', 
            'Somewhat\nAcceptable', 'Moderately\nAcceptable', 
            'Extremely\nAcceptable']

        # Styles
        style = ttk.Style(self)
        style.configure('TLabel', font=("Helvetica", 11))
        style.configure('TLabelframe.Label', font=("Helvetica", 12))
        style.configure('TButton', font=("Helvetica", 11))

        # Awareness Slider
        w.Slider(self, 
            question="Please rate how aware you were of the transition:",
            anchors=aware_anchors, 
            slider_args={'from_':0, 'to':100, 'length':500, 
                'orient':'horizontal', 'command':slider_changed, 
                'variable':self._vars['Awareness Rating']}
            ).grid(row=5,column=0)

        # Acceptability Slider
        w.Slider(self, 
            question="Please rate how acceptable the transition was:",
            anchors=accept_anchors, 
            slider_args={'from_':0, 'to':100, 'length':500, 
                'orient':'horizontal', 'command':slider_changed, 
                'variable':self._vars['Acceptability Rating']}
            ).grid(row=10,column=0)

        # Button frame
        frm_button = ttk.Frame(self)
        frm_button.grid(row=15, column=0, columnspan=5, padx=20, pady=20)

        # Play button
        self.btn_play = ttk.Button(frm_button, text="Play", command=self.play)
        self.btn_play.grid(row=0, column=0, sticky='w', padx=15)

        # Submit button
        self.btn_submit = ttk.Button(frm_button, text="Submit", 
            state="disabled", command=self._on_submit)
        self.btn_submit.grid(row=0, column=1, sticky='e', padx=15)


    def play(self):
        """ Present audio. Can be repeated as many times as 
            the listener wants.
        """
        # Enable submit button after listening at least once
        self.btn_submit.config(state="enabled")

        # Play audio

    
    def _on_submit(self):
        self.event_generate('<<SaveRecord>>')


    def get(self):
        """ Retrieve data as dictionary """
        data = dict()
        for key, variable in self._vars.items():
            try:
                data[key] = variable.get()
            except tk.TclError:
                message=f'Error with: {key}.'
                raise ValueError(message)
        return data


    def reset(self):
        """ Clear all values """
        #messagebox.showinfo(title="Data", message=[self._vars['Awareness Rating'].get(), self._vars['Acceptability Rating'].get()])     
        for var in self._vars.values():
            var.set(50)

        # Disable submit button on press
        # Set focus to play button
        self.btn_submit.config(state="disabled")
        self.btn_play.focus()



