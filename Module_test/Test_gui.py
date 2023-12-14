# gui_module.py
import tkinter as tk
from Test_haupt import Hauptprogramm

class GUI:
    def open_gui(self):
        self.root = tk.Tk()
        self.root.title('GUI with Button')

        self.button = tk.Button(self.root, text='Open New Window', command=self.open_new_window)
        self.button.pack()

    def open_new_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title('New Window')
        label = tk.Label(new_window, text='This is a new window!')
        label.pack()

    def run(self):
        self.root.mainloop()