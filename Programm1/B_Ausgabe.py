import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Ausgabe:
    def __init__(self, gesamtkosten_elektrik, gesamtkosten_pneumatik, graphen_elektrik, graphen_pneumatik, hauptprogramm):
        self.hauptprogramm=hauptprogramm
        self.root = tk.Toplevel()
        self.root.title("Ausgabe")

        # Elektrik Ergebnisse und Graphen
        self.zeige_ergebnisse("Elektrik", gesamtkosten_elektrik)
        self.zeige_graphen("Elektrik", graphen_elektrik)

        # Pneumatik Ergebnisse und Graphen
        self.zeige_ergebnisse("Pneumatik", gesamtkosten_pneumatik)
        self.zeige_graphen("Pneumatik", graphen_pneumatik)

    def zeige_ergebnisse(self, antriebsart, gesamtkosten):
        label = ttk.Label(self.root, text=f"{antriebsart} Ergebnisse:")
        label.pack()

        # Hier können Sie die Ergebnisse auf dem Bildschirm anzeigen
        # Beispiel:
        ergebnisse_text = f"Gesamtkosten: {gesamtkosten} Euro"
        ergebnisse_label = ttk.Label(self.root, text=ergebnisse_text)
        ergebnisse_label.pack()

    def zeige_graphen(self, antriebsart, graphen):
        label = ttk.Label(self.root, text=f"{antriebsart} Graphen:")
        label.pack()

        # Hier können Sie die Graphen anzeigen
        # Beispiel:
        fig, ax = plt.subplots()
        ax.plot(graphen["x"], graphen["y"])
        ax.set_xlabel("Nutzungsdauer (Jahre)")
        ax.set_ylabel("Kosten (Euro)")
        ax.set_title("Entwicklung der Gesamtkosten")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def anzeigen(self):
        self.root.deiconify()

if __name__ == "__main__":
    # Beispielaufruf für das Modul
    gesamtkosten_elektrik = 10000  # Beispielwert, ersetzen Sie durch den tatsächlichen Wert
    gesamtkosten_pneumatik = 8000  # Beispielwert, ersetzen Sie durch den tatsächlichen Wert

    graphen_elektrik = {"x": [0, 1, 2], "y": [10000, 12000, 15000]}  # Beispielwerte, ersetzen Sie durch die tatsächlichen Werte
    graphen_pneumatik = {"x": [0, 1, 2], "y": [8000, 9000, 10000]}  # Beispielwerte, ersetzen Sie durch die tatsächlichen Werte

    ausgabe = Ausgabe(gesamtkosten_elektrik, gesamtkosten_pneumatik, graphen_elektrik, graphen_pneumatik)
    ausgabe.root.mainloop()
