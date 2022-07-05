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

        self.withdraw()
        self.title("Rating Tool")

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
            '<<FileSession>>': self._on_submit,
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

        # # Set up root window
        self.deiconify()

        self.center_window()


    def center_window(toplevel):
        toplevel.update_idletasks()
        screen_width = toplevel.winfo_screenwidth()
        screen_height = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        toplevel.geometry("+%d+%d" % (x, y)) 


    def _load_settings(self):
        """Load settings into our self.settings dict."""

        vartypes = {
        'bool': tk.BooleanVar,
        'str': tk.StringVar,
        'int': tk.IntVar,
        'float': tk.DoubleVar
        }

        # Create dict of settings variables from the model's settings.
        self.settings = dict()
        for key, data in self.settings_model.fields.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])

        # Put a trace on the variables so they get stored when changed.
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