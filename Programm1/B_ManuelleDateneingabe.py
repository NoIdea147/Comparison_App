import tkinter as tk
from tkinter import ttk

class ManuelleDateneingabe:
    def __init__(self, bauteil, hauptprogramm):
        self.hauptprogramm = hauptprogramm
        self.root = tk.Toplevel()
        self.root.title("Manuelle Dateneingabe")

        # Assuming bauteil is a placeholder value
        bauteil = "Gurtumsetzer"
        self.manuelle_dateneingabe = ManuelleDateneingabe(bauteil, self)


        # Schichtmodell Dropdown-Menü
        schichtmodell_var = tk.StringVar()
        schichtmodell_dropdown = ttk.Combobox(self.root, textvariable=schichtmodell_var, values=["Zweischichtmodell", "Dreischichtmodell", "Dauerbetrieb"])
        schichtmodell_dropdown.set("Schichtmodell wählen")
        schichtmodell_dropdown.pack(pady=10)

        # Größe der Anlage Dropdown-Menü
        groesse_var = tk.StringVar()
        groesse_dropdown = ttk.Combobox(self.root, textvariable=groesse_var, values=["klein (10)", "mittel (50)", "groß (100)"])
        groesse_dropdown.set("Größe der Anlage wählen")
        groesse_dropdown.pack(pady=10)

        # Nutzungsdauer Eingabefeld
        nutzen_dauer_label = tk.Label(self.root, text="Nutzungsdauer:")
        nutzen_dauer_label.pack()
        nutzen_dauer_entry = tk.Entry(self.root)
        nutzen_dauer_entry.pack(pady=10)

        # Bewertungssystem Dropdown-Menü
        bewertung_var = tk.StringVar()
        bewertung_dropdown = ttk.Combobox(self.root, textvariable=bewertung_var, values=["Sehr wichtig", "Wichtig", "Ausgeglichen", "Unwichtig", "Sehr unwichtig"])
        bewertung_dropdown.set("Bewertungssystem wählen")
        bewertung_dropdown.pack(pady=10)

        # Button für Berechnungen und nächsten Schritt
        berechnen_button = tk.Button(self.root, text="Berechnen", command=self.zeige_berechnungsfenster)
        berechnen_button.pack(pady=20)

    def anzeigen(self):
        self.root.deiconify()  # Zeigt die manuelle Dateneingabe an

    def zeige_berechnungsfenster(self):
        # Hier können Sie die Logik für das Berechnungsfenster implementieren
        pass

    

if __name__ == "__main__":
    # Beispielaufruf für das Modul
    bauteil = "Gurtumsetzer"  # Hier sollte der Wert des ausgewählten Bauteils aus Teil 1 übergeben werden
    manuelle_dateneingabe = ManuelleDateneingabe(bauteil)
    manuelle_dateneingabe.root.mainloop()
