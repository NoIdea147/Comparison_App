import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graphenerstellung:
    def __init__(self, bauteil, schichtmodell, groesse, nutzen_dauer, bewertung, hauptprogramm):
        self.hauptprogramm=hauptprogramm
        # ...
        

        def zeige_ergebnisse(self, gesamtkosten_elektrik, gesamtkosten_pneumatik):
        # Hier können Sie die Ergebnisse auf dem Bildschirm anzeigen
        # ...

            def zeige_graphen(self):
                # Hier können Sie die Graphen anzeigen

                # Elektrik Graph
                fig_elektrik, ax_elektrik = plt.subplots()
                x_werte = list(range(self.nutzen_dauer + 1))
                y_werte_elektrik = self.berechne_kosten_entwicklung("elektrik", x_werte)
                ax_elektrik.plot(x_werte, y_werte_elektrik, label="Elektrik")
                ax_elektrik.set_xlabel("Nutzungsdauer (Jahre)")
                ax_elektrik.set_ylabel("Kosten (Euro)")
                ax_elektrik.legend()
                ax_elektrik.set_title("Entwicklung der Gesamtkosten - Elektrik")

                # Pneumatik Graph
                fig_pneumatik, ax_pneumatik = plt.subplots()
                y_werte_pneumatik = self.berechne_kosten_entwicklung("pneumatik", x_werte)
                ax_pneumatik.plot(x_werte, y_werte_pneumatik, label="Pneumatik")
                ax_pneumatik.set_xlabel("Nutzungsdauer (Jahre)")
                ax_pneumatik.set_ylabel("Kosten (Euro)")
                ax_pneumatik.legend()
                ax_pneumatik.set_title("Entwicklung der Gesamtkosten - Pneumatik")

                # Integration der Graphen in das Tkinter-Fenster
                canvas_elektrik = FigureCanvasTkAgg(fig_elektrik, master=self.root)
                canvas_elektrik.draw()
                canvas_elektrik.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

                canvas_pneumatik = FigureCanvasTkAgg(fig_pneumatik, master=self.root)
                canvas_pneumatik.draw()
                canvas_pneumatik.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)



    def berechne_kosten_entwicklung(self, antriebsart, x_werte):
        # Hier können Sie die Logik für die Entwicklung der Kosten implementieren
        startwert = self.berechne_anschaffungskosten(antriebsart)
        wartungskosten = self.berechne_wartungskosten(antriebsart)
        betriebskosten = self.berechne_betriebskosten(antriebsart)

        kosten_entwicklung = [startwert + wartungskosten + betriebskosten * i for i in x_werte]
        return kosten_entwicklung
    

if __name__ == "__main__":
    # Beispielaufruf für das Modul
    bauteil = "Gurtumsetzer"  # Hier sollte der Wert des ausgewählten Bauteils aus Teil 1 übergeben werden
    schichtmodell = "Zweischichtmodell"  # Beispielwert, ersetzen Sie durch den ausgewählten Wert
    groesse = "klein (10)"  # Beispielwert, ersetzen Sie durch den ausgewählten Wert
    nutzen_dauer = 10  # Beispielwert, ersetzen Sie durch den ausgewählten Wert
    bewertung = "Sehr wichtig"  # Beispielwert, ersetzen Sie durch den ausgewählten Wert

    