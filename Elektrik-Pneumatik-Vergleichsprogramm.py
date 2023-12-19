# Bibiliotheken importieren
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from matplotlib.backends.backend_pdf import PdfPages
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import math


# Programm als Klasse erstellen
class FullScreenApp:


# Datentyp, verfügbare Bauteile auswählen
    def __init__(self, root):
        self.root = root
        self.root.title("Main menu")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        self.results_window = None
        self.canvas1 = None
        self.canvas2 = None

        self.component_data = ["Gurtumsetzer", "Staurollenförderer"]

        # Standardwerte für Optionen
        self.standardwert_wirkungsgrad_elektrisch = 0.95
        self.standardwert_wirkungsgrad_pneumatisch = 0.27
        self.standardwert_strompreis = 0.21
        self.standardwert_ueberschneidungsfaktor = 0.6

        # Globale Variablen für Optionen
        self.strompreis_entry = tk.DoubleVar(value=self.standardwert_strompreis)
        self.wirkungsgrad_elektrisch_entry = tk.DoubleVar(value=self.standardwert_wirkungsgrad_elektrisch)
        self.wirkungsgrad_pneumatisch_entry = tk.DoubleVar(value=self.standardwert_wirkungsgrad_pneumatisch)
        self.ueberschneidungsfaktor_entry = tk.DoubleVar(value=self.standardwert_ueberschneidungsfaktor)

        # Datentyp für manuelle Daten
        self.selected_component = None
        self.manual_data = {
            "Schichtmodell": tk.StringVar(value=""),
            "AnlagenGroesse": tk.StringVar(value=""),
            "Durchsatz": tk.DoubleVar(value=""),
            "Masse": tk.StringVar(value=""),
            "Nutzungsdauer": tk.IntVar(value=""),
            "Wartungskosten": tk.StringVar(value=""), 
            "Energiekosten": tk.StringVar(value=""),  
            "Anschaffungskosten": tk.StringVar(value=""),          
            "BerechnungStarten": tk.StringVar(value="Ja")
        }

        self.create_menu()


# Hauptmenü erstellen
    def create_menu(self):
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(side="top", fill="x")

        ttk.Label(self.root, text = "Elektrik - Pneumatik - Vergleichsprogramm", font=("Helvetica", 24)).pack(pady=4)

        ttk.Label(self.root, text="Bauteil auswählen:", font = ("Helvetica", 14)).pack(pady=20)
        self.component_dropdown = ttk.Combobox(self.root, values=self.component_data)
        self.component_dropdown.pack(pady=10)

        ttk.Button(self.root, text="Begin Selection", command=self.modify_data).pack(pady=10)

        ttk.Button(menu_frame, text="Options", command=self.open_options_window).pack(side="left", padx=10)   


# Optionsfesnter erstellen
    def open_options_window(self):
        options_window = tk.Toplevel(self.root)
        options_window.geometry("250x400")
        options_window.title("Options")

        ttk.Label(options_window, text="Wirkungsgrad elektrisch:").pack(pady=10)
        wirkungsgrad_elektrisch_entry = ttk.Entry(options_window, textvariable=self.wirkungsgrad_elektrisch_entry)
        wirkungsgrad_elektrisch_entry.pack(pady=5)

        ttk.Label(options_window, text="Wirkungsgrad pneumatisch:").pack(pady=10)
        wirkungsgrad_pneumatisch_entry = ttk.Entry(options_window, textvariable=self.wirkungsgrad_pneumatisch_entry)
        wirkungsgrad_pneumatisch_entry.pack(pady=5)

        ttk.Label(options_window, text="Strompreis:").pack(pady=10)
        strompreis_entry = ttk.Entry(options_window, textvariable=self.strompreis_entry)
        strompreis_entry.pack(pady=5)

        ttk.Label(options_window, text="Überschneidungsfaktor:").pack(pady=10)
        ueberschneidungsfaktor_entry = ttk.Entry(options_window, textvariable=self.ueberschneidungsfaktor_entry)
        ueberschneidungsfaktor_entry.pack(pady=5)

        # Bestätigen-Button hinzufügen
        ttk.Button(options_window, text="Bestätigen", command=self.save_options).pack(pady=10)


# Speichern der Aenderung von Optionen
    def save_options(self):
        # Werte speichern
        self.standardwert_wirkungsgrad_elektrisch = self.wirkungsgrad_elektrisch_entry.get()
        self.standardwert_wirkungsgrad_pneumatisch = self.wirkungsgrad_pneumatisch_entry.get()
        self.standardwert_strompreis = self.strompreis_entry.get()
        self.standardwert_ueberschneidungsfaktor = self.ueberschneidungsfaktor_entry.get()



        # Modify Data input


# Manuelle Dateneingabe    
    def modify_data(self):
        self.selected_component = self.component_dropdown.get()
        
        # Fenster erstellen
        modify_window = tk.Toplevel(self.root)
        modify_window.geometry("1920x1080")
        modify_window.title("Modify Data")

        ttk.Label(modify_window, text="Manual data input", font=("Helvetica", 24)).pack(pady=20)

        # Felder für die Eingabe und Dropdown Menüs
        ttk.Label(modify_window, text="Schichtmodell:").pack(pady=10)
        schichtmodell_dropdown = ttk.Combobox(modify_window, values=["Zweischichtbetrieb", "Dreischichtbetrieb", "Dauerbetrieb"], textvariable=self.manual_data["Schichtmodell"])
        schichtmodell_dropdown.pack(pady=5)

        ttk.Label(modify_window, text="Anlagen Größe:").pack(pady=10)
        anlagen_groesse_dropdown = ttk.Combobox(modify_window, values=["Klein (10 Stück)", "Mittel (50 Stück)", "Groß (100 Stück)"], textvariable=self.manual_data["AnlagenGroesse"])
        anlagen_groesse_dropdown.pack(pady=5)

        ttk.Label(modify_window, text="Masse:").pack(pady=10)
        masse_dropdown = ttk.Combobox(modify_window, values=["Wenig Gewicht (bis 10kg)", "Mittleres Gewicht (bis 30kg)", "Hohes Gewicht (bis 50kg)"], textvariable=self.manual_data["Masse"])
        masse_dropdown.pack(pady=5)

        ttk.Label(modify_window, text="Durchsatz:").pack(pady=10)
        durchsatz_entry = ttk.Entry(modify_window, textvariable=self.manual_data["Durchsatz"])
        durchsatz_entry.pack(pady=5)

        ttk.Label(modify_window, text="Nutzungsdauer (Jahre):").pack(pady=10)
        nutzungsdauer_entry = ttk.Entry(modify_window, textvariable=self.manual_data["Nutzungsdauer"])
        nutzungsdauer_entry.pack(pady=5)

        ttk.Label(modify_window, text="Bewertungssystem:", font=("Helvetica", 18)).pack(pady=20)

        ttk.Label(modify_window, text="Wartungskosten:").pack(pady=10)
        wartungskosten_dropdown = ttk.Combobox(modify_window, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Wartungskosten"])
        wartungskosten_dropdown.pack(pady=5)

        ttk.Label(modify_window, text="Energiekosten:").pack(pady=10)
        energiekosten_dropdown = ttk.Combobox(modify_window, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Energiekosten"])
        energiekosten_dropdown.pack(pady=5)

        ttk.Label(modify_window, text="Anschaffungskosten:").pack(pady=10)
        anschaffungskosten_dropdown = ttk.Combobox(modify_window, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Anschaffungskosten"])
        anschaffungskosten_dropdown.pack(pady=5)

        # Create buttons for calculations and data modification
        ttk.Button(modify_window, text="Calculate and Display", command=self.calculate_and_display).pack(pady=10)


# Bestätigen der Daten
    def change_data(self):

        messagebox.showinfo("Daten bestätigen", "Daten wurden erfolgreich bestätigt.")

        self.calculate_and_display()




        # Berechnungen


# Berechnungen und Graphen Ausgabe
    def calculate_and_display(self):
        if self.selected_component:

            # Zugriff auf globale Variablen
            strompreis = float(self.strompreis_entry.get())
            wirkungsgrad_elektrisch = float(self.wirkungsgrad_elektrisch_entry.get())
            wirkungsgrad_pneumatik = float(self.wirkungsgrad_pneumatisch_entry.get())
            ueberschneidungsfaktor = float(self.ueberschneidungsfaktor_entry.get())


            # Die Manuellen Daten aufrufen
            schichtmodell = self.manual_data["Schichtmodell"].get()
            anlagen_groesse = self.manual_data["AnlagenGroesse"].get()
            nutzungsdauer = self.manual_data["Nutzungsdauer"].get()
            masse = self.manual_data["Masse"].get()
            durchsatz = self.manual_data["Durchsatz"].get()
            wartungskosten_value = self.manual_data["Wartungskosten"].get()
            energiekosten = self.manual_data["Energiekosten"].get()
            anschaffungskosten = self.manual_data["Anschaffungskosten"].get()
            weg = 0.1


            # Auswärtung der Größe der Anlage
            if anlagen_groesse=="Klein (10 Stück)":
                anzahl_anlage = 10
            elif anlagen_groesse=="Mittel (50 Stück)":
                anzahl_anlage = 50
            elif anlagen_groesse=="Groß (100 Stück)":
                anzahl_anlage = 100

            # Auswärtung des Schichtmodells
            if schichtmodell=="Zweischichtbetrieb":
                stunden_pro_woche=16*5
            elif schichtmodell=="Dreischichtbetrieb":
                stunden_pro_woche=24*5
            elif schichtmodell=="Dauerbetrieb":
                stunden_pro_woche=24*7

            # Auswärtung maximal Gewicht Angabe
            if masse=="Wenig Gewicht (bis 10kg)":
                max_masse=10
            elif masse=="Mittleres Gewicht (bis 30kg)":
                max_masse=30
            elif masse=="Hohes Gewicht (bis 50kg)":
                max_masse=50

            # Auswärtung Bewertung Wartungskosten
            if wartungskosten_value=="vernachlässigbar":
                beww = 0
            elif wartungskosten_value=="unwichtig":
                beww = 0.5
            elif wartungskosten_value=="neutral":
                beww = 1
            elif wartungskosten_value=="wichtig":
                beww = 1.5
            elif wartungskosten_value=="sehr wichtig":
                beww = 2
            
            print(beww)
            # Auswärtung Bewertung Energiekosten
            if energiekosten=="vernachlässigbar":
                bewe = 0
            elif energiekosten=="unwichtig":
                bewe = 0.5
            elif energiekosten=="neutral":
                bewe = 1
            elif energiekosten=="wichtig":
                bewe = 1.5
            elif energiekosten=="sehr wichtig":
                bewe = 2

            # Auswärtung Bewertung Anschaffungskosten
            if anschaffungskosten=="vernachlässigbar":
                bewa = 0
            elif anschaffungskosten=="unwichtig":
                bewa = 0.5
            elif anschaffungskosten=="neutral":
                bewa = 1
            elif anschaffungskosten=="wichtig":
                bewa = 1.5
            elif anschaffungskosten=="sehr wichtig":
                bewa = 2

            # Betrieb hinsichtlich Wartungskosten
            if schichtmodell == "Zweischichtbetrieb":
                wartungsfaktor = 0.65
            elif schichtmodell =="Dreischichtbetrieb":
                wartungsfaktor = 0.85
            elif schichtmodell == "Dauerbetrieb":
                wartungsfaktor = 1
            

            # Angaben Elektrik          
            anschaffungskosten_elektrik_preis = 3000
            routine_wartung_motor_kosten = 250
            max_leistung_eletrik = 0.35
            v_elektrisch = weg/0.2

            # Berechnung Motor
            leistung_elektrik_st = max_masse * 9.81 * v_elektrisch / 1000
            leistung_elektrik_b = max_leistung_eletrik - leistung_elektrik_st
            wurzel = leistung_elektrik_b * 1000 * 2 / max_masse
            square_root = np.sqrt(wurzel)
            zeit_b = 0.1 / square_root

            # Definition der Durchschnittlichen Leistung in einer Minute
            leistung_elektrik = (0.2 * durchsatz * leistung_elektrik_st + zeit_b * durchsatz * leistung_elektrik_b)/60


            # Angaben Pneumatik
            anschaffungskosten_pneumatik_preis  =1000
            routine_wartung_kompressor_kosten = 500
            routine_wartung_zylinder_kosten = 250
            vstrom_zylinder = 0.196
            ges_vstrom_zylinder = vstrom_zylinder * anzahl_anlage * ueberschneidungsfaktor / wirkungsgrad_pneumatik

            # Berechnung der Leistung anhand der Kompressoren
            leistung_kompressor_klein = 10
            druck_kompressor_klein = 600000
            vstrom_kompressor_klein = leistung_kompressor_klein *1000 * 1000/druck_kompressor_klein

            leistung_kompressor_mittel = 20
            druck_kompressor_mittel = 600000
            vstrom_kompressor_mittel = leistung_kompressor_mittel *1000 * 1000/druck_kompressor_mittel

            leistung_kompressor_groß = 30
            druck_kompressor_groß = 600000
            vstrom_kompressor_groß = leistung_kompressor_groß *1000 * 1000/druck_kompressor_groß

            if ges_vstrom_zylinder < vstrom_kompressor_klein:            
                leistung_pneumatik = leistung_kompressor_klein
                anschaffungskosten_kompressor_preis = 10000

            elif ges_vstrom_zylinder < vstrom_kompressor_mittel and ges_vstrom_zylinder >= vstrom_kompressor_klein:  
                leistung_pneumatik = leistung_kompressor_mittel
                anschaffungskosten_kompressor_preis = 30000

            elif ges_vstrom_zylinder < vstrom_kompressor_groß and ges_vstrom_zylinder >= vstrom_kompressor_mittel:
                leistung_pneumatik = leistung_kompressor_groß
                anschaffungskosten_kompressor_preis = 60000


            # Anschaffungskosten Berechnung
            anschaffungskosten_elektrik = anschaffungskosten_elektrik_preis * anzahl_anlage * bewa
            anschaffungskosten_pneumatik = (anschaffungskosten_pneumatik_preis * anzahl_anlage + anschaffungskosten_kompressor_preis) * bewa

            # Energiekosten Berechnung
            energiekosten_elektrik = leistung_elektrik * stunden_pro_woche * 52 * nutzungsdauer * anzahl_anlage * strompreis * bewe / wirkungsgrad_elektrisch 
            energiekosten_pneumatik = leistung_pneumatik * stunden_pro_woche * 52 *  nutzungsdauer * strompreis * bewe
          
            # Wartungskosten Elektrik:                  
            # Definieren Sie Symbole
            x = sp.symbols('x')

            # Definieren Sie die exponentiellen Funktionen
            def exponential_function1(x):
                return 0.02 * sp.exp(-0.55 * x) + 0.01  # Abnahme

            def exponential_function2(x):
                return 0.01 * sp.exp(0.2 * (x - 20)) + 0.01 # Zunahme

            # Zusammenführung Graphen
            def ausfalls_wartung_motor(x):
                condition = sp.LessThan(x, 6.2)
                return sp.Piecewise((exponential_function1(x), condition), (exponential_function2(x), True))

            # Berechnen Sie das bestimmte Integral von 0 bis 30
            integral_result = sp.integrate(ausfalls_wartung_motor(x), (x, 0, nutzungsdauer)).evalf()

            # Ergebnisse
            wartungskosten_elektrik = (routine_wartung_motor_kosten * nutzungsdauer * anzahl_anlage + integral_result * 2000 * anzahl_anlage) * beww * wartungsfaktor
            routine_wartungskosten_elektrik = anzahl_anlage * routine_wartung_motor_kosten * nutzungsdauer * wartungsfaktor * beww
            

            # Wartungskosten Pneumatik:
            # Definieren Sie Symbole
            x = sp.symbols('x')

            # Definieren Sie die exponentiellen Funktionen
            def exponential_function1_p(x):
                return 0.04 * sp.exp(-0.55 * x) + 0.03  # Abnahme

            def exponential_function2_p(x):
                return 0.02 * sp.exp(0.2 * (x - 20)) + 0.03 # Zunahme

            # Zusammenführung Graphen
            def ausfalls_wartung_pneumatik(x):
                condition = sp.LessThan(x, 6.2)
                return sp.Piecewise((exponential_function1_p(x), condition), (exponential_function2_p(x), True))

            # Berechnen Sie das bestimmte Integral von 0 bis 30
            integral_result = sp.integrate(ausfalls_wartung_pneumatik(x), (x, 0, nutzungsdauer)).evalf()

            # Ergebnisse
            wartungskosten_pneumatik = ((routine_wartung_kompressor_kosten  + routine_wartung_zylinder_kosten * anzahl_anlage) * nutzungsdauer + integral_result * anschaffungskosten_pneumatik_preis * anzahl_anlage + integral_result * anschaffungskosten_kompressor_preis) * beww * wartungsfaktor
            routine_wartungskosten_pneumatik = (anzahl_anlage * routine_wartung_zylinder_kosten + routine_wartung_kompressor_kosten) * nutzungsdauer * wartungsfaktor * beww

            # Berechnung Anschaffungskosten
            gesamtkosten_elektrik = anschaffungskosten_elektrik + wartungskosten_elektrik + energiekosten_elektrik
            gesamtkosten_pneumatik = anschaffungskosten_pneumatik + wartungskosten_pneumatik + energiekosten_pneumatik
          

        # Datenausgabe:
            # Bestätigung das die Ausgabe starten sollte
            berechnung_starten = self.manual_data["BerechnungStarten"].get()
            if berechnung_starten == "Ja":

                # Neues Fenster für Berechnungen und Graphen
                self.results_window = tk.Toplevel(self.root)
                self.results_window.geometry("1920x1080")
                self.results_window.title("Cost Analysis Results")
     
                # Frame für Berechnungen Ausgabe
                frame_elektrik = ttk.Frame(self.results_window)
                frame_elektrik.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

                frame_pneumatik = ttk.Frame(self.results_window)
                frame_pneumatik.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)



                # Elektrik Ausgabe
                ttk.Label(frame_elektrik, text="Elektrisch", font=("Helvetica", 20, "bold")).pack(side=tk.TOP, pady=10)

                ttk.Label(frame_elektrik, text=f"Wartungskosten Elektrik: {round(wartungskosten_elektrik, 2)}", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_elektrik, text=f"Routinewartungskosten: {round(routine_wartungskosten_elektrik, 2)}", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_elektrik, text=f"Energiekosten Elektrik: {round(energiekosten_elektrik, 2)}", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_elektrik, text=f"Installationskosten Elektrik: {round(anschaffungskosten_elektrik, 2)}", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_elektrik, text=f"Gesamtkosten Elektrik: {round(gesamtkosten_elektrik, 2)}", font=("Helvetica", 14)).pack(pady=4)

                # Frame für Graphen Elektrik
                frame_graph_elektrik = ttk.Frame(frame_elektrik)
                frame_graph_elektrik.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)


                # Graphen für Elektro
                figure_elektrik = Figure(figsize=(7.2, 5.5), tight_layout=True)

                # Parameter für Berechnungen
                x = sp.symbols('x')
                nutzungsdauer = int(self.manual_data["Nutzungsdauer"].get())

                # 1. routine_wartungskosten_elektrik
                routine_wartungskosten_elektrik = routine_wartung_motor_kosten * anzahl_anlage * x * beww * wartungsfaktor

                # 2. energiekosten_elektrik
                energiekosten_elektrik = leistung_elektrik * stunden_pro_woche * 52 * x * anzahl_anlage * strompreis * bewe / wirkungsgrad_elektrisch 

                # 3. ausfalls_wartung_motor
                x = sp.symbols('x')

                # Definieren Sie die exponentiellen Funktionen
                def exponential_function1(x):
                    return 0.02 * sp.exp(-0.55 * x) + 0.01  # Abnahme

                def exponential_function2(x):
                    return 0.01 * sp.exp(0.2 * (x - 20)) + 0.01 # Zunahme

                # Zusammenführung Graphen
                def ausfalls_wartung_motor(x):
                    condition = sp.LessThan(x, 6.2)
                    return sp.Piecewise((exponential_function1(x), condition), (exponential_function2(x), True))

                # Berechnen Sie das bestimmte Integral von 0 bis 30
                integral_values = [sp.integrate(beww * wartungsfaktor * anzahl_anlage * anschaffungskosten_elektrik_preis * ausfalls_wartung_motor(x), (x, 0, i)).evalf() for i in range(nutzungsdauer + 1)]
               

                # 4. gesamtkosten_elektrik
                # Berechnung der Werte
                x_values = range(nutzungsdauer + 1)
                elektrik_routine_wartungskosten_values = [routine_wartungskosten_elektrik.subs(x, i).evalf() for i in x_values]
                elektrik_energiekosten_values = [energiekosten_elektrik.subs(x, i).evalf() for i in x_values]
                

                # Erstellen des Gesamtgraphen
                gesamt_graph_elektrik = [anschaffungskosten_elektrik + routine + energie + ausfall for routine, energie, ausfall in zip(elektrik_routine_wartungskosten_values, elektrik_energiekosten_values, integral_values)]
                
                # Berechnung und Hinzufügen der Graphen
                # Berechnung und Hinzufügen der Graphen
                subplot1_elektrik = figure_elektrik.add_subplot(2, 2, 1)
                routine_wartungskosten_values = [routine_wartungskosten_elektrik.subs(x, i).evalf() for i in x_values]
                max_routine_wartungskosten = max(routine_wartungskosten_values)
                subplot1_elektrik.plot(x_values, routine_wartungskosten_values, linestyle='-', color='orange')
                subplot1_elektrik.set_title("Routine Wartungskosten")
                subplot1_elektrik.set_xlabel("Nutzungsdauer [Jahre]")
                subplot1_elektrik.set_ylabel("Kosten [€]")  
                
                subplot2_elektrik = figure_elektrik.add_subplot(2, 2, 2)
                subplot2_elektrik.plot([i for i in range(nutzungsdauer + 1)], [energiekosten_elektrik.subs(x, i) for i in range(nutzungsdauer + 1)], linestyle='-', color='orange')
                subplot2_elektrik.set_title("Energiekosten Elektrik")
                subplot2_elektrik.set_xlabel("Nutzungsdauer [Jahre]")
                subplot2_elektrik.set_ylabel("Kosten [€]")
                
                subplot3_elektrik = figure_elektrik.add_subplot(2, 2, 3)
                subplot3_elektrik.plot([i for i in range(nutzungsdauer + 1)], [beww * wartungsfaktor * anzahl_anlage * 2000 * ausfalls_wartung_motor(i) for i in range(nutzungsdauer + 1)], linestyle='-', color='orange')
                subplot3_elektrik.set_title("Ausfalls-/Wartungskosten Motor")
                subplot3_elektrik.set_xlabel("Nutzungsdauer [Jahre]")
                subplot3_elektrik.set_ylabel("Kosten [€]")
                

                subplot4_elektrik = figure_elektrik.add_subplot(2, 2, 4)
                subplot4_elektrik.plot([i for i in range(nutzungsdauer + 1)], gesamt_graph_elektrik, linestyle='-', color='orange')
                subplot4_elektrik.set_title("Gesamtkosten Elektrik")
                subplot4_elektrik.set_xlabel("Nutzungsdauer [Jahre]")
                subplot4_elektrik.set_ylabel("Kosten [€]")

                for subplot in figure_elektrik.get_axes():
                    subplot.grid(True, linestyle='--', alpha=0.7)
             
                canvas_elektrik = FigureCanvasTkAgg(figure_elektrik, master=frame_graph_elektrik)
                canvas_elektrik.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



                # Pneumatik Ausgabe
                ttk.Label(frame_pneumatik, text="Pneumatisch", font=("Helvetica", 20, "bold")).pack(side=tk.TOP, pady=10)

                ttk.Label(frame_pneumatik, text=f"Wartungskosten Pneumatik: {round(wartungskosten_pneumatik, 2)}", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_pneumatik, text=f"Routinewartungskosten: {round(routine_wartungskosten_pneumatik, 2)}", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_pneumatik, text=f"Energiekosten Pneumatik: {round(energiekosten_pneumatik, 2)}", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_pneumatik, text=f"Installationskosten Pneumatik: {round(anschaffungskosten_pneumatik, 2)}", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_pneumatik, text=f"Gesamtkosten Pneumatik: {round(gesamtkosten_pneumatik, 2)}", font=("Helvetica", 14)).pack(pady=4)

                # Frame für Graphen Pneumatik
                frame_graph_pneumatik = ttk.Frame(frame_pneumatik)
                frame_graph_pneumatik.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)
                
                # Graphen für Pneumatik
                figure_pneumatik = Figure(figsize=(7.2, 5.5), tight_layout=True)

                # Parameter für Berechnungen
                x = sp.symbols('x')
                nutzungsdauer = int(self.manual_data["Nutzungsdauer"].get())

                # 1. routine_wartungskosten_pneumatik
                routine_wartungskosten_pneumatik = (routine_wartung_zylinder_kosten * anzahl_anlage + routine_wartung_kompressor_kosten) * x * wartungsfaktor * beww

                # 2. energiekosten_pneumatik
                energiekosten_pneumatik = leistung_pneumatik * stunden_pro_woche * 52 *  x * strompreis * bewe

                # 3. ausfalls_wartung_pneumatik
                def exponential_function1(x):
                    return 0.04 * sp.exp(-0.55 * x) + 0.03

                def exponential_function2(x):
                    return 0.02 * sp.exp(0.2 * (x - 20)) + 0.03

                def ausfalls_wartung_pneumatik(x):
                    condition = sp.LessThan(x, 6.2)
                    return sp.Piecewise((exponential_function1(x), condition), (exponential_function2(x), True))

                integral_values_zylinder = [sp.integrate(beww * anzahl_anlage * wartungsfaktor * anschaffungskosten_pneumatik_preis * ausfalls_wartung_pneumatik(x), (x, 0, i)).evalf() for i in range(nutzungsdauer + 1)]


                def exponential_function1(x):
                    return 0.04 * sp.exp(-0.55 * x) + 0.03

                def exponential_function2(x):
                    return 0.02 * sp.exp(0.2 * (x - 20)) + 0.03

                def ausfalls_wartung_pneumatik(x):
                    condition = sp.LessThan(x, 6.2)
                    return sp.Piecewise((exponential_function1(x), condition), (exponential_function2(x), True))

                integral_values_kompressor = [sp.integrate(beww * wartungsfaktor * anschaffungskosten_kompressor_preis * ausfalls_wartung_pneumatik(x), (x, 0, i)).evalf() for i in range(nutzungsdauer + 1)]


                # 4. gesamtkosten pneumatik
                # Berechnung der Werte
                x_values = range(nutzungsdauer + 1)
                pneumatik_routine_wartungskosten_values = [routine_wartungskosten_pneumatik.subs(x, i).evalf() for i in x_values]
                pneumatik_energiekosten_values = [energiekosten_pneumatik.subs(x, i).evalf() for i in x_values]
                

           

                # Erstellen des Gesamtgraphen
                gesamt_graph_pneumatik = [anschaffungskosten_pneumatik + routine + energie + ausfallzylinder + ausfallkompressor for routine, energie, ausfallzylinder, ausfallkompressor in zip(pneumatik_routine_wartungskosten_values, pneumatik_energiekosten_values, integral_values_zylinder, integral_values_kompressor)]
                
                # Berechnung und Hinzufügen der Graphen
                subplot1_pneumatik = figure_pneumatik.add_subplot(2, 2, 1)
                subplot1_pneumatik.plot([i for i in range(nutzungsdauer + 1)], [routine_wartungskosten_pneumatik.subs(x, i) for i in range(nutzungsdauer + 1)], linestyle='-', color='blue')
                subplot1_pneumatik.set_title("Routine Wartungskosten")
                subplot1_pneumatik.set_xlabel("Nutzungsdauer [Jahre]")
                subplot1_pneumatik.set_ylabel("Kosten [€]")

                subplot2_pneumatik = figure_pneumatik.add_subplot(2, 2, 2)
                subplot2_pneumatik.plot([i for i in range(nutzungsdauer + 1)], [energiekosten_pneumatik.subs(x, i) for i in range(nutzungsdauer + 1)], linestyle='-', color='blue')
                subplot2_pneumatik.set_title("Energiekosten Pneumatik")
                subplot2_pneumatik.set_xlabel("Nutzungsdauer [Jahre]")
                subplot2_pneumatik.set_ylabel("Kosten [€]")

                subplot3_pneumatik = figure_pneumatik.add_subplot(2, 2, 3)
                subplot3_pneumatik.plot([i for i in range(nutzungsdauer + 1)], [beww * wartungsfaktor * anzahl_anlage * anschaffungskosten_pneumatik_preis * ausfalls_wartung_pneumatik(i) for i in range(nutzungsdauer + 1)], linestyle='-', color='blue')
                subplot3_pneumatik.set_title("Ausfalls-/Wartungskosten Pneumatik")
                subplot3_pneumatik.set_xlabel("Nutzungsdauer [Jahre]")
                subplot3_pneumatik.set_ylabel("Kosten [€]")

                subplot4_pneumatik = figure_pneumatik.add_subplot(2, 2, 4)
                subplot4_pneumatik.plot([i for i in range(nutzungsdauer + 1)], gesamt_graph_pneumatik, linestyle='-', color='blue')
                subplot4_pneumatik.set_title("Gesamtkosten Pneumatik")
                subplot4_pneumatik.set_xlabel("Nutzungsdauer [Jahre]")
                subplot4_pneumatik.set_ylabel("Kosten [€]")
                
                canvas_pneumatik = FigureCanvasTkAgg(figure_pneumatik, master=frame_graph_pneumatik)
                canvas_pneumatik.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

                for subplot in figure_pneumatik.get_axes():
                    subplot.grid(True, linestyle='--', alpha=0.7)



                # Frame für Datenausgabe im Ergebnisfenster
                frame_datenausgabe = ttk.Frame(self.results_window)
                frame_datenausgabe.place(x=665, y=0)

                ttk.Label(frame_datenausgabe, text="Datenausgabe", font=("Helvetica", 20, "bold")).pack(side=tk.TOP, pady=3)
                ttk.Label(frame_datenausgabe, text=f"Bauteil: {self.selected_component}", font=("Helvetica", 12)).pack(side=tk.TOP, pady=3)
                ttk.Label(frame_datenausgabe, text=f"Schichtmodell: {schichtmodell}", font=("Helvetica", 12)).pack(side=tk.TOP, pady=4)
                ttk.Label(frame_datenausgabe, text=f"Nutzungsdauer: {nutzungsdauer} Jahre", font=("Helvetica", 12)).pack(side=tk.TOP, pady=4)
                ttk.Label(frame_datenausgabe, text=f"Größe der Anlage: {anzahl_anlage} Stück", font=("Helvetica", 12)).pack(side=tk.TOP, pady=4)
                ttk.Button(frame_datenausgabe, text="Hauptmenü", command=self.back_to_main_menu).pack(side=tk.TOP, pady=4)
                ttk.Button(frame_datenausgabe, text="Modify manual data", command=self.modify_data).pack(side=tk.TOP, pady=4)
             



        # Zurück zum Hauptmenü   


# Zurück zum Hauptmenü und Fenster zerstören   
    def back_to_main_menu(self):
        # Placeholder confirmation message
        user_response = messagebox.askyesno("Back to Hauptmenü", "Do you want to go back to Hauptmenü?")
        if user_response:
            self.root.destroy()
            root = tk.Tk()
            app = FullScreenApp(root)
            root.mainloop()


# Ergebnisse als PDF speichern (noch nicht funktionsfähig)   
    def save_results_as_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            # Create a PdfPages object to save the content
            with PdfPages(file_path) as pdf:
                # Render the Matplotlib figures to PNG images
                png_data1 = self.render_figure_to_png(self.canvas1.figure)
                png_data2 = self.render_figure_to_png(self.canvas2.figure)

                # Save the PNG images to the PDF
                pdf.savefig(png_data1, format="png")
                pdf.savefig(png_data2, format="png")

                # Additional pages can be added here if needed

                # Close the PdfPages object
                pdf.close()


# Graphen als PNG speichern (Versuch für PDF speichern)
    def render_figure_to_png(self, figure):
        # Render the Matplotlib figure to a PNG image
        figure_canvas = FigureCanvasTkAgg(figure, master=self.root)
        figure_canvas.draw()
        figure_image = ImageTk.PhotoImage(figure_canvas.get_tk_widget().master, master=figure_canvas.get_tk_widget())
        figure_canvas.get_tk_widget().destroy()
        
        return figure_image


# Programm ausführen
if __name__ == "__main__":
    root = tk.Tk()
    app = FullScreenApp(root)
root.mainloop()