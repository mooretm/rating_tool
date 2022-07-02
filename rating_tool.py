""" Wav-file-based rating task. Wav files are presented 
    in random order (obviating the need for naming 
    conventions). Simple GUI with custom rating slider 
    widgets. Data are saved as .csv files.

    Version 1.0.0
    Written by: Travis M. Moore
    Created: Jun 29, 2022
    Last Edited: Jul 1, 2022
"""

# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Custom modules
import view as v
import models as m


class Application(tk.Tk):
    """ Application root window """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initialize objects
        self.model = m.CSVModel()
        self.main_frame = v.MainFrame(self, self.model)
        self.main_frame.grid(row=1, column=0)
        self.main_frame.bind('<<SaveRecord>>', self._on_submit)

        # Status label to display trial count
        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status).grid(sticky='w', padx=20)
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