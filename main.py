import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox

from tensorflow.python.keras.engine.training_utils import collect_per_output_metric_info


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()

        self.title("Title goes here")
        self.minsize(700, 400)
        # self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='hXUrRNqC_400x400.png'))

        self.label_email = tk.Label(self, text="Load Email")
        self.label_email.grid(column=0, row=0, padx=10, pady=10)

        self.str_email = tk.StringVar()
        self.str_email.set("Use 'Browse' button to select email file")
        self.entry_email = tk.Entry(self, width=80, textvariable=self.str_email)
        self.entry_email.grid(column=0, row=1, padx=10, pady=10)

        self.button_email = tk.Button(self, text="Browse", command=self.browse_email)
        self.button_email.grid(column=1, row=1)

        # root path
        self.label_root = tk.Label(self, text="Search directory")
        self.label_root.grid(column=0, row=2, padx=10, pady=10)

        self.str_root = tk.StringVar()
        self.str_root.set('default search dir is not selected')
        self.entry_root = tk.Entry(self, width=80, textvariable=self.str_root)
        self.entry_root.grid(column=0, row=3, padx=10, pady=10)

        self.button_root = tk.Button(self, text="Browse", command=self.browse_root)
        self.button_root.grid(column=1, row=3)

    def browse_root(self):
        directory = filedialog.askdirectory()
        self.str_root.set(directory)

    def browse_email(self):
        file = filedialog.askopenfilename(filetypes=[("E-mail file", ".eml")])
        if file:
            self.str_email.set(file)



window = Window()
window.mainloop()
