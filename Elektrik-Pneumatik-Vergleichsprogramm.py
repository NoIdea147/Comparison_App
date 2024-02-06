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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader


# Programm als Klasse erstellen
class FullScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Elektrik - Pneumatik - Vergleichsprogramm")

        # Größe des Hauptfensters (Vollbild)
        window_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}")


        # Initialisierung anderer Komponenten oder Funktionen hier


# Kompletten Bildschirm ausfüllen
    def toggle_fullscreen(self):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))


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

        # Globale Variablen für Einstellungen
        self.rabatte_entry = tk.DoubleVar(value=0)

        # Datentyp für manuelle Daten
        self.selected_component = None
        self.manual_data = {
            "Schichtmodell": tk.StringVar(value=""),
            "AnlagenGroesse": tk.IntVar(value=""),
            "Durchsatz": tk.IntVar(value=""),
            "Masse": tk.StringVar(value=""),
            "Nutzungsdauer": tk.IntVar(value=""),
            "Wartungskosten": tk.StringVar(value=""), 
            "Energiekosten": tk.StringVar(value=""),  
            "Anschaffungskosten": tk.StringVar(value=""),          
            "BerechnungStarten": tk.StringVar(value="Ja"),
            "Druck": tk.IntVar(value="")
        }

        self.create_menu()


# Programm schließen
    def close_program(self):
        self.root.destroy()


# Hauptmenü erstellen
    def create_menu(self):
        self.menu_frame = tk.Frame(self.root, borderwidth=1, relief="solid", bg="white")
        self.menu_frame.pack(side="top", fill="x")
   
        # Auswahlleiste
       
        self.bauteilauswahl = tk.Button(self.root, text="Bauteilauswahl", font = ("Helvetica", 16), bg="turquoise", command=self.auswahl_bauteil, width=18, height=5)
        self.bauteilauswahl.pack(anchor="w")

        parameter = tk.Button(self.root, text="Parameter", font = ("Helvetica", 16), bg="turquoise", command=self.open_options_window, width=18, height=5)
        parameter.pack(anchor="w")

        einstellungen = tk.Button(self.root, text="Einstellungen", font = ("Helvetica", 16), bg="turquoise", command=self.open_einstellungen_window, width=18, height=5)
        einstellungen.pack(anchor="w")

        motoren = tk.Button(self.root, text="Motoren", font = ("Helvetica", 16), bg="turquoise", command=self.motoren_window, width=18, height=5)
        motoren.pack(anchor="w")

        zylinder = tk.Button(self.root, text="Pneumatikzylinder", font = ("Helvetica", 16), bg="turquoise", command=self.zylinder_window, width=18, height=5)
        zylinder.pack(anchor="w")

        kompressoren = tk.Button(self.root, text="Kompressoren", font = ("Helvetica", 16), bg="turquoise", command=self.kompressor_window, width=18, height=5)
        kompressoren.pack(anchor="w")

        ttk.Label(self.menu_frame, text = "Elektrik - Pneumatik - Vergleichsprogramm", font=("Helvetica", 16)).grid(row=1, column=1, padx=532)

         # Button zum Beenden hinzufügen
        close_button = tk.Button(self.menu_frame, text="Beenden", command=self.ask_exit, bg="red", fg="white", font=("Helvetica", 12))
        close_button.grid(row=1, column=2)


# Bauteil Auswahl 
    def auswahl_bauteil(self):
        button_x = self.bauteilauswahl.winfo_x()
        button_width = self.bauteilauswahl.winfo_width()

        auswahl_frame = tk.Frame(self.root, width = 500, height = 100)
        auswahl_frame.place(x=button_x + button_width, y=35)

        ttk.Label(auswahl_frame, text="Bauteil auswählen:", font=("Helvetica", 14)).grid(row=1, column=1, padx=(10, 10), pady=(30, 5))
        self.component_dropdown = ttk.Combobox(auswahl_frame, values=self.component_data, width=30)
        self.component_dropdown.grid(row=1, column=2, padx=(10, 10), pady=(30, 5))

        tk.Button(auswahl_frame, text="Dateneingabe beginnen", command=self.modify_data, font=("Helvetica", 14), width=30, bg ="turquoise").grid(row=2, column=2, padx=(10, 10), pady=(10, 5))


# Programm beenden
    def ask_exit(self):
        # Zeige eine Bestätigungsbox an
        result = messagebox.askyesno("Beenden", "Wirklich beenden?")
        if result:
            # Benutzer hat "OK" ausgewählt, beende das Programm
            self.close_program()
    def close_program(self):
        self.root.destroy()
  

# Optionsfesnter erstellen
    def open_options_window(self):
        self.options_window = tk.Toplevel(self.root)
        self.options_window.geometry("550x660+220+170")
        self.options_window.title("Options")

        self.frame_options_btn = tk.Frame(self.options_window, borderwidth=1, relief="solid", bg="white")
        self.frame_options_btn.pack(side="top", fill="x")

        self.frame_wirkungsgrad = tk.Frame(self.options_window, width=500, height=600, bg="white")
        self.frame_strompreis = tk.Frame(self.options_window, width=500, height=600, bg="white")
        self.frame_anschaffungskosten = tk.Frame(self.options_window, width=500, height=600, bg="white")
        self.frame_wartungskosten = tk.Frame(self.options_window, width=500, height=600, bg="white")

        self.frame_wirkungsgrad.pack_propagate(False)
        self.frame_strompreis.pack_propagate(False)
        self.frame_anschaffungskosten.pack_propagate(False)
        self.frame_wartungskosten.pack_propagate(False)

        self.create_options()

        self.hide_frames()

    def create_options(self):
        btn_wirkungsgrad = tk.Button(self.frame_options_btn, text="Wirkungsgrad", font=("Helvetica", 10), command=lambda: self.show_frame(self.frame_wirkungsgrad), bg="white").pack(side="left")
        btn_strompreis = tk.Button(self.frame_options_btn, text="Strompreis", font=("Helvetica", 10), command=lambda: self.show_frame(self.frame_strompreis), bg="white").pack(side="left")
        btn_anschaffungskosten = tk.Button(self.frame_options_btn, text="Anschaffungskosten", font=("Helvetica", 10), command=lambda: self.show_frame(self.frame_anschaffungskosten), bg="white").pack(side="left")
        btn_wartungskosten = tk.Button(self.frame_options_btn, text="Wartungskosten", font=("Helvetica", 10), command=lambda: self.show_frame(self.frame_wartungskosten), bg="white").pack(side="left")

        btn_save = tk.Button(self.frame_options_btn, text="Werte speichern", font=("Helvetica", 10), command=self.save_options, bg="lightgray").pack(side="right")

        btn_wirkungsgrad.pack(side="left", padx=5)
        btn_strompreis.pack(side="left", padx=5)
        btn_anschaffungskosten.pack(side="left", padx=5)
        btn_wartungskosten.pack(side="left", padx=5)
        btn_save.pack(side="left", padx=5)

        ttk.Label(self.frame_wirkungsgrad, text="Wirkungsgrad elektrisch:").pack(pady=10)
        wirkungsgrad_elektrisch_entry = ttk.Entry(self.frame_wirkungsgrad, textvariable=self.wirkungsgrad_elektrisch_entry)
        wirkungsgrad_elektrisch_entry.pack(pady=5)

        ttk.Label(self.frame_wirkungsgrad, text="Wirkungsgrad pneumatisch:").pack(pady=10)
        wirkungsgrad_pneumatisch_entry = ttk.Entry(self.frame_wirkungsgrad, textvariable=self.wirkungsgrad_pneumatisch_entry)
        wirkungsgrad_pneumatisch_entry.pack(pady=5)

        ttk.Label(self.frame_strompreis, text="Strompreis:").pack(pady=10)
        strompreis_entry = ttk.Entry(self.frame_strompreis, textvariable=self.strompreis_entry)
        strompreis_entry.pack(pady=5)

        ttk.Label(self.frame_strompreis, text="Überschneidungsfaktor:").pack(pady=10)
        ueberschneidungsfaktor_entry = ttk.Entry(self.frame_strompreis, textvariable=self.ueberschneidungsfaktor_entry)
        ueberschneidungsfaktor_entry.pack(pady=5)

    def hide_frames(self):
        self.frame_wirkungsgrad.pack_forget()
        self.frame_strompreis.pack_forget()
        self.frame_anschaffungskosten.pack_forget()
        self.frame_wartungskosten.pack_forget()

    def show_frame(self, frame):
        self.hide_frames()
        frame.pack(side="top", fill="both", expand=True)

    def save_options(self):
        self.standardwert_wirkungsgrad_elektrisch = self.wirkungsgrad_elektrisch_entry.get()
        self.standardwert_wirkungsgrad_pneumatisch = self.wirkungsgrad_pneumatisch_entry.get()
        self.standardwert_strompreis = self.strompreis_entry.get()
        self.standardwert_ueberschneidungsfaktor = self.ueberschneidungsfaktor_entry.get()



        # Modify Data input


# Einstellungsfenster erstellen
    def open_einstellungen_window(self):
        options_window = tk.Toplevel(self.root)
        options_window.geometry("250x400")
        options_window.title("Options")



# Motoren Vorschau
    def motoren_window(self):
        motoren_window = tk.Toplevel(self.root)
        motoren_window.geometry("250x400")
        motoren_window.title("Motoren")


# Zylinder Vorschau
    def zylinder_window(self):
        zylinder_window = tk.Toplevel(self.root)
        zylinder_window.geometry("250x400")
        zylinder_window.title("Zylinder")

# Kompressor Vorschau
    def kompressor_window(self):
        kompressor_window = tk.Toplevel(self.root)
        kompressor_window.geometry("250x400")
        kompressor_window.title("Kompressoren")


# Manuelle Dateneingabe    
    def modify_data(self):
        self.selected_component = self.component_dropdown.get()
        
        # Fenster erstellen
        modify_window = tk.Toplevel(self.root)
        modify_window.geometry("550x660+220+170")
        modify_window.title("Modify Data")

        input_frame = tk.Frame(modify_window, width=200, height=300)
        input_frame.place(x=10, y=10)

        ttk.Label(modify_window, text="Manual data input:", font=("Helvetica", 22)).grid(row=2, column=0, padx=(10, 10), pady=(10, 10))

        # Felder für die Eingabe und Dropdown Menüs
        ttk.Label(input_frame, text="Schichtmodell:", font=("Helvetica", 14)).grid(row=4, column=0, padx=(10, 10), pady=(60, 5))
        schichtmodell_dropdown = ttk.Combobox(input_frame, values=["Zweischichtbetrieb", "Dreischichtbetrieb", "Dauerbetrieb"], textvariable=self.manual_data["Schichtmodell"])
        schichtmodell_dropdown.grid(row=4, column=1, padx=(10, 10), pady=(60, 5))

        ttk.Label(input_frame, text="Anlagen Größe:", font=("Helvetica", 14)).grid(row=6, column=0, padx=(10, 10), pady=(10, 5))
        anzahl_anlage = tk.Entry(input_frame, width=23, textvariable=self.manual_data["AnlagenGroesse"])
        anzahl_anlage.grid(row=6, column=1, padx=(10, 10), pady=(10, 5))

        ttk.Label(input_frame, text="Masse in [kg]:", font=("Helvetica", 14)).grid(row=8, column=0, padx=(10, 10), pady=(10, 5))
        masse_dropdown = ttk.Combobox(input_frame, values=["Wenig Gewicht (bis 10kg)", "Mittleres Gewicht (bis 30kg)", "Hohes Gewicht (bis 50kg)"], textvariable=self.manual_data["Masse"])
        masse_dropdown.grid(row=8, column=1, padx=(10, 10), pady=(10, 5))

        ttk.Label(input_frame, text="Durchsatz pro Stunde:", font=("Helvetica", 14)).grid(row=10, column=0, padx=(10, 10), pady=(10, 5))
        durchsatz_entry = tk.Entry(input_frame, width=23, textvariable=self.manual_data["Durchsatz"])
        durchsatz_entry.grid(row=10, column=1, padx=(10, 10), pady=(10, 5))

        ttk.Label(input_frame, text="Nutzungsdauer (Jahre):", font=("Helvetica", 14)).grid(row=12, column=0, padx=(10, 10), pady=(10, 5))
        nutzungsdauer_entry = tk.Entry(input_frame, width=23, textvariable=self.manual_data["Nutzungsdauer"])
        nutzungsdauer_entry.grid(row=12, column=1, padx=(10, 10), pady=(10, 5))

        ttk.Label(input_frame, text="Druck des Kompressors in [bar]:", font=("Helvetica", 14)).grid(row=14, column=0, padx=(10, 10), pady=(10, 10))
        druck_entry = tk.Entry(input_frame, width=23, textvariable=self.manual_data["Druck"])
        druck_entry.grid(row=14, column=1, padx=(10, 10), pady=(10, 10))

        ttk.Label(input_frame, text="Bewertungssystem:", font=("Helvetica", 18)).grid(row=16, column=0, padx=(10, 10), pady=(10, 5))

        ttk.Label(input_frame, text="Wartungskosten:", font=("Helvetica", 14)).grid(row=18, column=0, padx=(10, 10), pady=(10, 5))
        wartungskosten_dropdown = ttk.Combobox(input_frame, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Wartungskosten"])
        wartungskosten_dropdown.grid(row=18, column=1, padx=(10, 10), pady=(10, 5))

        ttk.Label(input_frame, text="Energiekosten:", font=("Helvetica", 14)).grid(row=20, column=0, padx=(10, 10), pady=(10, 5))
        energiekosten_dropdown = ttk.Combobox(input_frame, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Energiekosten"])
        energiekosten_dropdown.grid(row=20, column=1, padx=(10, 10), pady=(10, 5))

        ttk.Label(input_frame, text="Anschaffungskosten:", font=("Helvetica", 14)).grid(row=22, column=0, padx=(10, 10), pady=(10, 10))
        anschaffungskosten_dropdown = ttk.Combobox(input_frame, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Anschaffungskosten"])
        anschaffungskosten_dropdown.grid(row=22, column=1, padx=(10, 10), pady=(10, 10))

        # Create buttons for calculations and data modification
        tk.Button(input_frame, text="Berechnung starten", font=("Helvetica", 14), width=20, bg = "turquoise", command=self.calculate_and_display).grid(row=40, column=0, padx=(10, 10), pady=(10, 10))


# Bestätigen der Daten
    def change_data(self):

        messagebox.showinfo("Daten bestätigen", "Daten wurden erfolgreich bestätigt.")

        self.calculate_and_display()


# Berechnungen und Graphen Ausgabe
    def calculate_and_display(self):
        if self.selected_component:

            # Zugriff auf globale Variablen
            strompreis = float(self.strompreis_entry.get())
            wirkungsgrad_elektrisch = float(self.wirkungsgrad_elektrisch_entry.get())
            wirkungsgrad_pneumatik = float(self.wirkungsgrad_pneumatisch_entry.get())
            ueberschneidungsfaktor = float(self.ueberschneidungsfaktor_entry.get())


            # Die Manuellen Daten aufrufen
            self.schichtmodell = self.manual_data["Schichtmodell"].get()
            self.anzahl_anlage = self.manual_data["AnlagenGroesse"].get()
            self.nutzungsdauer = self.manual_data["Nutzungsdauer"].get()
            self.masse = self.manual_data["Masse"].get()
            self.durchsatz = self.manual_data["Durchsatz"].get()
            self.druck = self.manual_data["Druck"].get()
            wartungskosten_value = self.manual_data["Wartungskosten"].get()
            energiekosten = self.manual_data["Energiekosten"].get()
            anschaffungskosten = self.manual_data["Anschaffungskosten"].get()
            hub = 35    # in mm


            # Auswärtung des Schichtmodells [Stunden/Woche]
            if self.schichtmodell=="Zweischichtbetrieb":
                stunden_pro_woche=16*5
            elif self.schichtmodell=="Dreischichtbetrieb":
                stunden_pro_woche=24*5
            elif self.schichtmodell=="Dauerbetrieb":
                stunden_pro_woche=24*7

            # Auswärtung maximal Gewicht Angabe [kg]
            if self.masse=="Wenig Gewicht (bis 10kg)":
                max_masse=10
            elif self.masse=="Mittleres Gewicht (bis 30kg)":
                max_masse=30
            elif self.masse=="Hohes Gewicht (bis 50kg)":
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
            if self.schichtmodell == "Zweischichtbetrieb":
                wartungsfaktor = 0.65
            elif self.schichtmodell =="Dreischichtbetrieb":
                wartungsfaktor = 0.85
            elif self.schichtmodell == "Dauerbetrieb":
                wartungsfaktor = 1
            

            # Angaben Elektrik          
            anschaffungskosten_elektrik_preis = 3000        # Euro
            routine_wartung_motor_kosten = 250      # Euro
            max_leistung_eletrik = 0.35     # kW
            v_elektrisch = (hub/1000)/0.2       # m/s

            # Berechnung Motor
            leistung_elektrik_st = max_masse * 9.81 * v_elektrisch / 1000       # kW
            leistung_elektrik_b = max_leistung_eletrik - leistung_elektrik_st       #kW
            wurzel = leistung_elektrik_b * 1000 * 2 / max_masse
            square_root = np.sqrt(wurzel)
            zeit_b = 0.1 / square_root      # sec

            # Definition der Durchschnittlichen Leistung in einer Minute
            leistung_elektrik = (0.2 * self.durchsatz/60 * leistung_elektrik_st + zeit_b * self.durchsatz/60 * leistung_elektrik_b)/60        # Watt

            # Angaben Pneumatik
            anschaffungskosten_pneumatik_preis  = 1000      # Euro
            anschaffungskosten_kompressor_preis = 10000     # Euro
            routine_wartung_kompressor_kosten = 500         # Euro
            routine_wartung_zylinder_kosten = 250           # Euro
            pi = math.pi
            kolbendurchmesser = 20      # mm
            zylindertyp = 2         # einfach wirkend = 1; doppelt wirkend = 2
            vstrom_zylinder = (((kolbendurchmesser/100)**2)*pi)/4 * hub/100 * self.druck * self.durchsatz/60 * zylindertyp        # l/min
            
            ges_vstrom_zylinder =(vstrom_zylinder * self.anzahl_anlage * ueberschneidungsfaktor/wirkungsgrad_pneumatik)/60       # l/s
          
            leistung_pneumatik = ges_vstrom_zylinder/1000 * self.druck * 100000      # Watt
            
            # Anschaffungskosten Berechnung
            self.anschaffungskosten_elektrik = anschaffungskosten_elektrik_preis * self.anzahl_anlage * bewa
            self.anschaffungskosten_pneumatik = (anschaffungskosten_pneumatik_preis * self.anzahl_anlage + anschaffungskosten_kompressor_preis) * bewa

            # Energiekosten Berechnung
            self.energiekosten_elektrik = leistung_elektrik * stunden_pro_woche * 52 * self.nutzungsdauer * self.anzahl_anlage * strompreis * bewe / wirkungsgrad_elektrisch       # Euro
            self.energiekosten_pneumatik = leistung_pneumatik/1000 * stunden_pro_woche * 52 *  self.nutzungsdauer * strompreis * bewe         # Euro
          
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
            integral_result = sp.integrate(ausfalls_wartung_motor(x), (x, 0, self.nutzungsdauer)).evalf()

            # Ergebnisse
            self.wartungskosten_elektrik = (routine_wartung_motor_kosten * self.nutzungsdauer * self.anzahl_anlage + integral_result * 2000 * self.anzahl_anlage) * beww * wartungsfaktor
            self.routine_wartungskosten_elektrik = self.anzahl_anlage * routine_wartung_motor_kosten * self.nutzungsdauer * wartungsfaktor * beww
            

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
            integral_result = sp.integrate(ausfalls_wartung_pneumatik(x), (x, 0, self.nutzungsdauer)).evalf()
          
            # Ergebnisse
            self.wartungskosten_pneumatik = ((routine_wartung_kompressor_kosten  + routine_wartung_zylinder_kosten * self.anzahl_anlage) * self.nutzungsdauer + integral_result * anschaffungskosten_pneumatik_preis * self.anzahl_anlage + integral_result * anschaffungskosten_kompressor_preis) * beww * wartungsfaktor
            self.routine_wartungskosten_pneumatik = (self.anzahl_anlage * routine_wartung_zylinder_kosten + routine_wartung_kompressor_kosten) * self.nutzungsdauer * wartungsfaktor * beww

            # Berechnung Anschaffungskosten
            self.gesamtkosten_elektrik = self.anschaffungskosten_elektrik + self.wartungskosten_elektrik + self.energiekosten_elektrik
            self.gesamtkosten_pneumatik = self.anschaffungskosten_pneumatik + self.wartungskosten_pneumatik + self.energiekosten_pneumatik
          

        # Datenausgabe:
            # Bestätigung das die Ausgabe starten sollte
            berechnung_starten = self.manual_data["BerechnungStarten"].get()
            if berechnung_starten == "Ja":

                # Neues Fenster für Berechnungen und Graphen
                self.results_window = tk.Toplevel(self.root)
                self.results_window.geometry("1920x1080")
                self.results_window.title("Cost Analysis Results")
     
                # Frame für Berechnungen Ausgabe
               
                frame_elektrik = tk.Frame(self.results_window, width=300, height=300)
                frame_elektrik.pack(anchor="s", side="left", pady=150, padx=50)

                frame_pneumatik = tk.Frame(self.results_window, width=300, height=300)
                frame_pneumatik.pack(anchor="s", side="right", pady=150, padx=50)
               

                def formatiere_zahl(zahl):
                    return '{:,.0f}'.format(zahl).replace(',', ' ')



                # Elektrik Ausgabe
                ttk.Label(frame_elektrik, text="Elektrisch:", font=("Helvetica", 20, "bold")).pack(pady=10)

                ttk.Label(frame_elektrik, text=f"Wartungskosten: {formatiere_zahl(self.wartungskosten_elektrik)} €", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_elektrik, text=f"Routinewartungskosten: {formatiere_zahl(self.routine_wartungskosten_elektrik)} €", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_elektrik, text=f"Energiekosten: {formatiere_zahl(self.energiekosten_elektrik)} €", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_elektrik, text=f"Anschaffungskosten: {formatiere_zahl(self.anschaffungskosten_elektrik)} €", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_elektrik, text=f"Gesamtkosten: {formatiere_zahl(self.gesamtkosten_elektrik)} €", font=("Helvetica", 14)).pack(pady=4)

                # Zentrieren der Labels und Buttons im Frame
                for child in frame_elektrik.winfo_children():
                    child.pack_configure(pady=4)
             
                # Parameter für Berechnungen
                x = sp.symbols('x')
                nutzungsdauer = int(self.manual_data["Nutzungsdauer"].get())

                # 1. routine_wartungskosten_elektrik
                routine_wartungskosten_elektrik = routine_wartung_motor_kosten * self.anzahl_anlage * x * beww * wartungsfaktor

                # 2. energiekosten_elektrik
                energiekosten_elektrik = leistung_elektrik * stunden_pro_woche * 52 * x * self.anzahl_anlage * strompreis * bewe / wirkungsgrad_elektrisch 

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
                integral_values = [sp.integrate(beww * wartungsfaktor * self.anzahl_anlage * anschaffungskosten_elektrik_preis * ausfalls_wartung_motor(x), (x, 0, i)).evalf() for i in range(self.nutzungsdauer + 1)]
               

                # 4. gesamtkosten_elektrik
                # Berechnung der Werte
                x_values = range(self.nutzungsdauer + 1)
                self.elektrik_routine_wartungskosten_values = [routine_wartungskosten_elektrik.subs(x, i).evalf() for i in x_values]
                self.elektrik_energiekosten_values = [energiekosten_elektrik.subs(x, i).evalf() for i in x_values]
                
                # Erstellen des Gesamtgraphen
                self.gesamt_graph_elektrik = [self.anschaffungskosten_elektrik + routine + energie + ausfall for routine, energie, ausfall in zip(self.elektrik_routine_wartungskosten_values, self.elektrik_energiekosten_values, integral_values)]
                


                # Pneumatik Ausgabe
                ttk.Label(frame_pneumatik, text="Pneumatisch:", font=("Helvetica", 20, "bold")).pack(pady=10)

                ttk.Label(frame_pneumatik, text=f"Wartungskosten: {formatiere_zahl(self.wartungskosten_pneumatik)} €", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_pneumatik, text=f"Routinewartungskosten: {formatiere_zahl(self.routine_wartungskosten_pneumatik)} €", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_pneumatik, text=f"Energiekosten: {formatiere_zahl(self.energiekosten_pneumatik)} €", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_pneumatik, text=f"Anschaffungskosten: {formatiere_zahl(self.anschaffungskosten_pneumatik)} €", font=("Helvetica", 14)).pack(pady=4)
                ttk.Label(frame_pneumatik, text=f"Gesamtkosten: {formatiere_zahl(self.gesamtkosten_pneumatik)} €", font=("Helvetica", 14)).pack(pady=4)

                # Zentrieren der Labels und Buttons im Frame
                for child in frame_pneumatik.winfo_children():
                    child.pack_configure(pady=4)

                # Parameter für Berechnungen
                x = sp.symbols('x')
                self.nutzungsdauer = int(self.manual_data["Nutzungsdauer"].get())

                # 1. routine_wartungskosten_pneumatik
                routine_wartungskosten_pneumatik = (routine_wartung_zylinder_kosten * self.anzahl_anlage + routine_wartung_kompressor_kosten) * x * wartungsfaktor * beww

                # 2. energiekosten_pneumatik
                energiekosten_pneumatik = leistung_pneumatik/1000 * stunden_pro_woche * 52 *  x * strompreis * bewe

                # 3. ausfalls_wartung_pneumatik
                def exponential_function1(x):
                    return 0.04 * sp.exp(-0.55 * x) + 0.03

                def exponential_function2(x):
                    return 0.02 * sp.exp(0.2 * (x - 20)) + 0.03

                def ausfalls_wartung_pneumatik(x):
                    condition = sp.LessThan(x, 6.2)
                    return sp.Piecewise((exponential_function1(x), condition), (exponential_function2(x), True))

                self.integral_values_zylinder = [sp.integrate(beww * self.anzahl_anlage * wartungsfaktor * anschaffungskosten_pneumatik_preis * ausfalls_wartung_pneumatik(x), (x, 0, i)).evalf() for i in range(self.nutzungsdauer + 1)]


                def exponential_function1(x):
                    return 0.04 * sp.exp(-0.55 * x) + 0.03

                def exponential_function2(x):
                    return 0.02 * sp.exp(0.2 * (x - 20)) + 0.03

                def ausfalls_wartung_pneumatik(x):
                    condition = sp.LessThan(x, 6.2)
                    return sp.Piecewise((exponential_function1(x), condition), (exponential_function2(x), True))

                self.integral_values_kompressor = [sp.integrate(beww * wartungsfaktor * anschaffungskosten_kompressor_preis * ausfalls_wartung_pneumatik(x), (x, 0, i)).evalf() for i in range(self.nutzungsdauer + 1)]


                # 4. gesamtkosten pneumatik
                # Berechnung der Werte
                x_values = range(self.nutzungsdauer + 1)
                self.pneumatik_routine_wartungskosten_values = [routine_wartungskosten_pneumatik.subs(x, i).evalf() for i in x_values]
                self.pneumatik_energiekosten_values = [energiekosten_pneumatik.subs(x, i).evalf() for i in x_values]
                
                # Erstellen des Gesamtgraphen
                gesamt_graph_pneumatik = [self.anschaffungskosten_pneumatik + routine + energie + ausfallzylinder + ausfallkompressor for routine, energie, ausfallzylinder, ausfallkompressor in zip(self.pneumatik_routine_wartungskosten_values, self.pneumatik_energiekosten_values, self.integral_values_zylinder, self.integral_values_kompressor)]
                


                # Graph für Elektrik und Pneumatik Gesamtkosten vereint
                # Frame für kombinierten Graphen
                frame_graph_combined = ttk.Frame(self.results_window)
                frame_graph_combined.pack(side=tk.BOTTOM, anchor=tk.CENTER, pady=10)
                
                # Graphen für Pneumatik
                figure_combined = Figure(figsize=(7.2, 4.5), tight_layout=True)

                # Parameter für Berechnungen
                x = sp.symbols('x')
                self.nutzungsdauer = int(self.manual_data["Nutzungsdauer"].get())

               # Plot Elektrik
                subplot_combined = figure_combined.add_subplot(1, 1, 1)
                subplot_combined.plot([i for i in range(self.nutzungsdauer + 1)], self.gesamt_graph_elektrik, linestyle='-', color='orange', label='Elektrik')

                # Plot Pneumatik
                gesamt_graph_pneumatik = [self.anschaffungskosten_pneumatik + routine + energie + ausfallzylinder + ausfallkompressor for routine, energie, ausfallzylinder, ausfallkompressor in zip(self.pneumatik_routine_wartungskosten_values, self.pneumatik_energiekosten_values, self.integral_values_zylinder, self.integral_values_kompressor)]
                subplot_combined.plot([i for i in range(self.nutzungsdauer + 1)], gesamt_graph_pneumatik, linestyle='-', color='blue', label='Pneumatik')

                subplot_combined.set_title("Gesamtkosten Elektrik und Pneumatik")
                subplot_combined.set_xlabel("Nutzungsdauer [Jahre]")
                subplot_combined.set_ylabel("Kosten [€]")
                subplot_combined.legend()

                # Create a Tkinter canvas for the combined plot
                canvas_combined = FigureCanvasTkAgg(figure_combined, master=frame_graph_combined)
                canvas_combined.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

               

                # Frame für Datenausgabe im Ergebnisfenster
                frame_datenausgabe = tk.Frame(self.results_window, width=500, height=300)
                frame_datenausgabe.place(x=660, y=20)

                ttk.Label(frame_datenausgabe, text="Datenausgabe", font=("Helvetica", 20, "bold")).pack(pady=3)
                ttk.Label(frame_datenausgabe, text=f"Bauteil: {self.selected_component}", font=("Helvetica", 12)).pack(pady=4)
                ttk.Label(frame_datenausgabe, text=f"Schichtmodell: {self.schichtmodell}", font=("Helvetica", 12)).pack(pady=4)
                ttk.Label(frame_datenausgabe, text=f"Nutzungsdauer: {self.nutzungsdauer} Jahre", font=("Helvetica", 12)).pack(pady=4)
                ttk.Label(frame_datenausgabe, text=f"Größe der Anlage: {self.anzahl_anlage} Stück", font=("Helvetica", 12)).pack(pady=4)
                ttk.Label(frame_datenausgabe, text=f"Masse: {self.masse}", font=("Helvetica", 12)).pack(pady=4)
                ttk.Label(frame_datenausgabe, text=f"Durchsatz: {self.durchsatz} pro Stunde", font=("Helvetica", 12)).pack(pady=4)
                ttk.Label(frame_datenausgabe, text=f"Druck: {self.druck} bar", font=("Helvetica", 12)).pack(pady=4)

                # Frame für Buttons und Einstellungen im Results Window
                frame_buttons = tk.Frame(self.results_window, width=300, height=200)
                frame_buttons.place(x=10, y=10)

                # Button hinzufügen
                tk.Button(frame_buttons, width=30, height=2, font=("Helvetica", 12), text="Hauptmenü", bg = "turquise", command=self.back_to_main_menu).pack(pady=4)
                tk.Button(frame_buttons, width=30, height=2, font=("Helvetica", 12), text="Modify manual data", bg = "light grey", command=self.modify_data).pack(pady=4)
                tk.Button(frame_buttons, width=30, height=2, font=("Helvetica", 12), text="PDF speichern", bg = "light grey", command=self.create_pdf).pack(pady=4)
                

# Zurück zum Hauptmenü und Fenster zerstören   
    def back_to_main_menu(self):
        # Placeholder confirmation message
        user_response = messagebox.askyesno("Zurück zum Hauptmenü Hauptmenü", "Möchten Sie wirklich zurück zum Hauptmenü?")
        if user_response:
            self.root.destroy()
            root = tk.Tk()
            app = FullScreenApp(root)
            app.toggle_fullscreen()
            root.mainloop()


# Ergebnisse als PDF speichern 
    def create_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        
        def formatiere_zahl(zahl):
            return '{:,.0f}'.format(zahl).replace(',', ' ')    

        if file_path:
            # Erstelle ein Canvas-Objekt von reportlab
            c = canvas.Canvas(file_path, pagesize=(600, 800))

        # Rahmen definieren
            # Zeichne den äußersten Rahmen
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(1)
            c.rect(20, 20, 560, 760)

            # Rahmen für Überschrift und Logos
            c.setStrokeColorRGB(0, 0, 0)  
            c.setLineWidth(1)  
            c.rect(25, 690, 550, 85)  

            # Rahmen für Angegebene Daten
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(1)
            c.rect(25, 485, 550, 200)

            # Rahmen für Elektrik
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(1)
            c.rect(25, 280, 273, 200)

            # Rahmen für Pneumatik
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(1)
            c.rect(302, 280, 273, 200)

            # Rahmen für Graphen
            c.setStrokeColorRGB(0, 0, 0)
            c.setLineWidth(1)
            c.rect(25, 25, 550, 250)

        # Berechnungen Ausgabe
            # Festgelegte Bedingungen
            c.setFont("Helvetica", 20)
            c.drawString(30, 660, "Festgelegte Bedingungen:")

            c.setFont("Helvetica", 14)
            c.drawString(30, 635, f"Bauteil: {self.selected_component}")
            c.drawString(30, 610, f"Schichtmodell: {self.schichtmodell}")
            c.drawString(30, 585, f"Nutzungsdauer: {formatiere_zahl(self.nutzungsdauer)} Jahre")
            c.drawString(30, 560, f"Stückzahl der Anlage: {formatiere_zahl(self.anzahl_anlage)} Stück")
            c.drawString(30, 535, f"Druck Kompressor: {formatiere_zahl(self.druck)} bar")

            # Elektrik Ausgabe
            c.setFont("Helvetica", 20)
            c.drawString(30, 440, "Elektrisch:")

            c.setFont("Helvetica", 14)
            c.drawString(30, 410, f"Wartungskosten: {formatiere_zahl(self.wartungskosten_elektrik)} €")
            c.drawString(30, 385, f"Routinewartungskosten: {formatiere_zahl(self.routine_wartungskosten_elektrik)} €")
            c.drawString(30, 360, f"Energiekosten: {formatiere_zahl(self.energiekosten_elektrik)} €")
            c.drawString(30, 335, f"Anschaffungskosten: {formatiere_zahl(self.anschaffungskosten_elektrik)} €")
            c.drawString(30, 310, f"Gesamtkosten: {formatiere_zahl(self.gesamtkosten_elektrik)} €")

            # Pneumatik Ausgabe
            c.setFont("Helvetica", 20)
            c.drawString(307, 440, "Pneumatisch:")

            c.setFont("Helvetica", 14)
            c.drawString(307, 410, f"Wartungskosten: {formatiere_zahl(self.wartungskosten_pneumatik)} €")
            c.drawString(307, 385, f"Routinewartungskosten: {formatiere_zahl(self.routine_wartungskosten_pneumatik)} €")
            c.drawString(307, 360, f"Energiekosten: {formatiere_zahl(self.energiekosten_pneumatik)} €")
            c.drawString(307, 335, f"Anschaffungskosten: {formatiere_zahl(self.anschaffungskosten_pneumatik)} €")
            c.drawString(307, 310, f"Gesamtkosten: {formatiere_zahl(self.gesamtkosten_pneumatik)} €")

        # Graph für Elektrik und Pneumatik Gesamtkosten vereint
            # Frame für kombinierten Graphen
            frame_graph_combined = ttk.Frame(self.results_window)
            frame_graph_combined.pack(side=tk.BOTTOM, anchor=tk.CENTER, pady=10)
            
            # Graphen für Pneumatik
            figure_combined = Figure(figsize=(7.5, 3), tight_layout=True)

            # Parameter für Berechnungen
            x = sp.symbols('x')
            nutzungsdauer = int(self.manual_data["Nutzungsdauer"].get())

            # Plot Elektrik
            subplot_combined = figure_combined.add_subplot(1, 1, 1)
            subplot_combined.plot([i for i in range(nutzungsdauer + 1)], self.gesamt_graph_elektrik, linestyle='-', color='orange', label='Elektrik')

            # Plot Pneumatik
            gesamt_graph_pneumatik = [self.anschaffungskosten_pneumatik + routine + energie + ausfallzylinder + ausfallkompressor for routine, energie, ausfallzylinder, ausfallkompressor in zip(self.pneumatik_routine_wartungskosten_values, self.pneumatik_energiekosten_values, self.integral_values_zylinder, self.integral_values_kompressor)]
            subplot_combined.plot([i for i in range(nutzungsdauer + 1)], gesamt_graph_pneumatik, linestyle='-', color='blue', label='Pneumatik')

            subplot_combined.set_title("Gesamtkosten Elektrik und Pneumatik")
            subplot_combined.set_xlabel("Nutzungsdauer [Jahre]")
            subplot_combined.set_ylabel("Kosten [€]")
            subplot_combined.legend()


            # Speichere die Figur als Bild
            plot_img = "plot.png"
            figure_combined.savefig(plot_img, format="png", bbox_inches="tight", pad_inches=0.1)
            plt.close(figure_combined)

            # Füge das Bild in das PDF ein
            c.drawInlineImage(plot_img, 30, 30, width=530, height=230)

            # Logo HTL
            logo_path = r"C:\Users\micha\OneDrive\Dokumente\5AHME\Diplomarbeit\HTL_Logo.png"
            logo = ImageReader(logo_path)

            # Position und Größe des Logos anpassen
            logo_width = 100  # Breite des Logos in Punkten
            logo_height = 20  # Höhe des Logos in Punkten
            logo_x = 40  # X-Position des Logos in Punkten
            logo_y = 695  # Y-Position des Logos in Punkten

            # Füge das Logo zum PDF hinzu
            c.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height)

            # Logo Knapp
            logo_path = r"C:\Users\micha\OneDrive\Dokumente\5AHME\Diplomarbeit\Knapp_Logo.png"
            logo = ImageReader(logo_path)

            # Position und Größe des Logos anpassen
            logo_width = 100  # Breite des Logos in Punkten
            logo_height = 40  # Höhe des Logos in Punkten
            logo_x = 40  # X-Position des Logos in Punkten
            logo_y = 725  # Y-Position des Logos in Punkten

            # Füge das Logo zum PDF hinzu
            c.drawImage(logo, logo_x, logo_y, width=logo_width, height=logo_height)

            # Überschrift
            c.setFont("Helvetica", 20)
            c.drawString(170, 725, "Elektrik - Pneuamtik - Vergleich")


            # Speichere das Canvas-Objekt als PDF
            c.save()

            print(f"PDF erstellt: {file_path}")

   
# Programm ausführen
if __name__ == "__main__":
    root = tk.Tk()
    app = FullScreenApp(root)
    app.toggle_fullscreen()
root.mainloop()