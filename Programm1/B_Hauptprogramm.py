import tkinter as tk
from tkinter import ttk
from B_Hauptmenü import Hauptmenü
from B_ManuelleDateneingabe import ManuelleDateneingabe
from B_Datenbankzugriff import Datenbankzugriff
from B_Berechnungen import Berechnungen
from B_Grafenerstellung import Graphenerstellung
from B_Ausgabe import Ausgabe
from B_PDFExport import PDFExport
from B_ManuelleÄnderung import ManuelleDatenAenderung

class Hauptprogramm:
    def __init__(self):
        self.hauptmenue = Hauptmenü(self)
        self.manuelle_dateneingabe = ManuelleDateneingabe(self)
        self.datenbankzugriff = Datenbankzugriff(self)
        self.berechnungen = Berechnungen(self)
        self.graphenerstellung = Graphenerstellung(self)
        self.ausgabe = Ausgabe(self)
        self.pdf_export = PDFExport(self)
        self.manuelle_daten_aenderung = ManuelleDatenAenderung(self)

    def start(self):
        self.hauptmenue.anzeigen()

    def zeige_manuelle_dateneingabe(self):
        self.manuelle_dateneingabe.anzeigen()

    def zeige_datenbankzugriff(self):
        self.datenbankzugriff.anzeigen()

    def zeige_berechnungen(self):
        self.berechnungen.anzeigen()

    def zeige_graphenerstellung(self):
        self.graphenerstellung.anzeigen()

    def zeige_ausgabe(self, gesamtkosten_elektrik, gesamtkosten_pneumatik, graphen_elektrik, graphen_pneumatik):
        self.ausgabe.anzeigen(gesamtkosten_elektrik, gesamtkosten_pneumatik, graphen_elektrik, graphen_pneumatik)

    def zeige_pdf_export(self, elektrik_ergebnisse, pneumatik_ergebnisse):
        self.pdf_export.erstelle_pdf(elektrik_ergebnisse, pneumatik_ergebnisse)

    def zeige_manuelle_daten_aenderung(self):
        self.manuelle_daten_aenderung.anzeigen()

if __name__ == "__main__":
    hauptprogramm = Hauptprogramm()
    hauptprogramm.start()
    hauptprogramm.hauptmenue.root.mainloop()
