""" Wav-file-based rating task. Wav files are presented 
    in random order (obviating the need for naming 
    conventions). Simple GUI with custom rating slider 
    widgets. Data are saved as .csv files.

    Version 1.0.0
    Written by: Travis M. Moore
    Created: Jun 29, 2022
    Last Edited: Jul 4, 2022
"""

# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Custom modules
import view as v
import models as m
from mainmenu import MainMenu

class Application(tk.Tk):
    """ Application root window """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings_model = m.SettingsModel()
        self._load_settings()

        # Initialize objects
        self.model = m.CSVModel()
        self.main_frame = v.MainFrame(self, self.model, self.settings)
        self.main_frame.grid(row=1, column=0)
        self.main_frame.bind('<<SaveRecord>>', self._on_submit)

        # Menu
        menu = MainMenu(self, self.settings)
        self.config(menu=menu)
        # Create callback dictionary
        event_callbacks = {
            '<<FileSelect>>': self._on_submit,
            '<<FileQuit>>': lambda _: self.quit()
        }
        # Bind callbacks to sequences
        for sequence, callback in event_callbacks.items():
            self.bind(sequence, callback)

        # Status label to display trial count
        self.status = tk.StringVar(value="Trials Completed: 0")
        ttk.Label(self, textvariable=self.status).grid(sticky='w', padx=30, pady=(0,10))
        # Track trial number
        self._records_saved = 0

        # Set up root window
        self.title("Rating Tool")
        self.withdraw()
        # Center the window
        self.update_idletasks()
        # Get current window dimensions
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # find the center point
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        # set the position of the window to the center of the screen
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        #self.resizable(False, False)
        self.deiconify()


    def _load_settings(self):
        """ Load settings into settings dictionary above """
        # Dictionary to translate 'type' strings into tkinter 
        # control variable types
        vartypes = {
            'bool': tk.BooleanVar(),
            'str': tk.StringVar(),
            'int': tk.IntVar(),
            'float': tk.DoubleVar()
        }
        # Create empty dictionary to store settings
        self.settings = dict()
        # Iterate through settings_model and create matching 
        # control varaible for each field
        for key, data in self.settings_model.fields.items():
            # If there's a datatype that doesn't match, assign StringVar
            vartype = vartypes.get(data['type'], tk.StringVar)
            #self.settings[key] = vartype(value=data['value'])

            vartype.set(data['value'])
            self.settings[key] = vartype

            #self.settings[key] = vartype.set(data['value'])
        # Add a trace to call '_save_settings' whenever a variable is changed
        for var in self.settings.values():
            var.trace_add('write', self._save_settings)


    def _save_settings(self, *_):
        """ Save the current settings to a preferences file """
        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
            self.settings_model.save()


    def _on_submit(self, *_):
        """ Save trial ratings, update trial counter,
            and reset sliders.
         """
        data = self.main_frame.get()
        self.model.save_record(data)
        self._records_saved += 1
        self.status.set(f"Trials Completed: {self._records_saved}")
        self.main_frame.reset()


    # def _on_import(self):
    #     global audio_obj
    #     audio_obj = Audio()
    #     audio_obj.do_import_audio()

    #     self.main_frame._vars['In Name'].set(f'Name: {audio_obj.name}')
    #     self.main_frame._vars['In Data Type'].set(f'Data Type: {audio_obj.data_type}')
    #     self.main_frame._vars['In Sampling Rate'].set(f'Sampling Rate (Hz): {audio_obj.fs}')


if __name__ == "__main__":
    app = Application()
    app.mainloop()