import tkinter as tk
from tkinter import ttk


class Slider(tk.Frame):
    """ A widget for subjective ratings with 
        visual anchors.
    """
    def __init__(self, parent, question, anchors, slider_args=None, 
    label_args=None, **kwargs):
        super().__init__(parent, **kwargs)
        slider_args = slider_args or {}
        label_args = label_args or {}

        # Create question label frame
        lfrm_main = ttk.LabelFrame(self, text=question)
        lfrm_main.grid(padx=20, pady=(20,0))

        # Create slider
        scl_slider = ttk.Scale(lfrm_main, **slider_args)
        scl_slider.grid(row=1, column=0, columnspan=len(anchors),pady=5)

        # Create verbal anchors
        for idx, anchor in enumerate(anchors):
            #x = ((values[idx] - slider_args['from_']) / slider_args['to']) * 
            # (scl_slider.winfo_width() - slider_args['length']) + slider_args['length'] / 2
            ttk.Label(lfrm_main, text=anchor, anchor='c', width=15, 
                **label_args).grid(row=0, column=idx, pady=5)

        # Display slider value
        frm_rating = ttk.Label(lfrm_main)
        frm_rating.grid(row=2, column=0, columnspan=len(anchors))
        ttk.Label(frm_rating, text="Rating: ").grid(row=1, column=0, 
            sticky='e', pady=(0,10))
        ttk.Label(frm_rating, textvariable=slider_args['variable']
            ).grid(row=1, column=1, sticky='w', pady=(0,10))
