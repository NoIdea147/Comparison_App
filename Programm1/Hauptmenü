import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Hauptmenü:
    def __init__(self, hauptprogramm):
        self.hauptporogramm=hauptprogramm
        self.root = tk.Tk()
        self.root.title("Hauptmenü")
        self.root.geometry("800x600")  # Passen Sie die Größe nach Bedarf an

        # Menüleiste
        menubar = tk.Menu(self.root)
        menubar.add_command(label="Optionen", command=self.zeige_optionsfenster)
        self.root.config(menu=menubar)

        # Dropdown-Menü für Bauteilauswahl
        bauteil_var = tk.StringVar()
        bauteil_dropdown = ttk.Combobox(self.root, textvariable=bauteil_var, values=["Staurollenförderer", "Gurtumsetzer"])
        bauteil_dropdown.set("Bauteil auswählen")
        bauteil_dropdown.pack(pady=20)

        # Button für Bauteilauswahl
        auswahl_button = tk.Button(self.root, text="Bauteil auswählen", command=self.zeige_manuelle_dateneingabe)
        auswahl_button.pack(pady=20)

    def anzeigen(self):
        self.root.deiconify()

    def start(self):
        self.root.mainloop()

    def zeige_optionsfenster(self):
        # Hier können Sie die Logik für das Optionsfenster implementieren
        pass

    def zeige_manuelle_dateneingabe(self):
        # Hier können Sie die Logik für den Übergang zur manuellen Dateneingabe implementieren
        pass

if __name__ == "__main__":
    hauptmenü = Hauptmenü()
    hauptmenü.start()