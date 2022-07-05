# Import system packages
import os

# Import GUI packages
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

# Custom widgets
import widgets as w

# Import data science packages
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)


class MainFrame(ttk.Frame):
    def __init__(self, parent, model, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = model
        self.fields = self.model.fields
        self.settings = settings

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
        sldr_aware = w.RatingSlider(self, 
            question="Please rate how aware you were of the transition:",
            anchors=aware_anchors, 
            slider_args={'from_':0, 'to':100, 'length':500, 
                'orient':'horizontal', 'command':slider_changed, 
                'variable':self._vars['Awareness Rating']}
            ).grid(row=5,column=0)

        # Acceptability Slider
        sldr_accept = w.RatingSlider(self, 
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
        for var in self._vars.values():
            var.set(50)

        # Disable submit button on press
        # Set focus to play button
        self.btn_submit.config(state="disabled")
        self.btn_play.focus()



