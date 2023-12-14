# Test_haupt.py
import tkinter as tk
from Test_pdf import PDFGenerator
from Test_plot import Graph
from Test_gui import GUI

class Hauptprogramm:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hauptprogramm")

        # Modul 1: Plot generieren
        self.graph = Graph(self.root, self)

        # Button zum Öffnen der GUI
        self.open_gui_button = tk.Button(self.root, text="Zur GUI", command=self.open_gui)
        self.open_gui_button.pack(side=tk.BOTTOM)

        # Modul 3: PDF-Datei generieren
        self.pdf_generator = PDFGenerator('output.pdf')

    def open_gui(self):
        # Modul 2: GUI mit Button erstellen
        self.gui = GUI()
        self.gui.run()

    def destroy_root(self):
        self.root.destroy()

    def run(self):
        # Hier könnten weitere Anpassungen je nach Anforderungen erfolgen

        # Starte die Hauptfenster-Schleife
        self.root.mainloop()

if __name__ == "__main__":
    hauptprogramm = Hauptprogramm()
    hauptprogramm.run()
