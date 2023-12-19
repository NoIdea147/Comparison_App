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
from DB_Test import druck_kompressor_klein
from database_init import Beschleunigug
from database_init import Hub
from database_init import Kolbendurchmesser
from database_init import Luftverbrauch
from database_init import Druck
from database_init import Volumenstrom
from database_init import Leistung



class FullScreenApp:
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

        self.selected_component = None
        self.manual_data = {
            "Schichtmodell": tk.StringVar(value=""),
            "AnlagenGroesse": tk.StringVar(value=""),
            "Durchsatz": tk.DoubleVar(value=""),
            "Masse": tk.StringVar(value=""),
            "Nutzungsdauer": tk.IntVar(value=""),
            "Wartungskosten": tk.DoubleVar(value=""), 
            "Energiekosten": tk.DoubleVar(value=""),  
            "Anschaffungskosten": tk.DoubleVar(value=""),          
            "BerechnungStarten": tk.StringVar(value="Ja")
        }

        self.create_menu()

    def create_menu(self):
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(side="top", fill="x")

        ttk.Label(self.root, text="Select Component:").pack(pady=50)
        self.component_dropdown = ttk.Combobox(self.root, values=self.component_data)
        self.component_dropdown.pack(pady=10)

        ttk.Button(self.root, text="Begin Selection", command=self.modify_data).pack(pady=10)

        ttk.Button(menu_frame, text="Options", command=self.open_options_window).pack(side="left", padx=10)


        # Modify Data input
    def modify_data(self):
        self.selected_component = self.component_dropdown.get()
        
        # Create a new window to modify manual data
        modify_window = tk.Toplevel(self.root)
        modify_window.geometry("1920x1080")
        modify_window.title("Modify Data")

        ttk.Label(modify_window, text="Manual data input", font=("Helvetica", 24)).pack(pady=20)

        # Create entry fields for manual data
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

            #ttk.Label(modify_window, text="Wartungskosten:").pack(pady=10)
            #wartungskosten_dropdown = ttk.Combobox(modify_window, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Wartungskosten"])
            #wartungskosten_dropdown.pack(pady=5)

            #ttk.Label(modify_window, text="Energiekosten:").pack(pady=10)
            #energiekosten_dropdown = ttk.Combobox(modify_window, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Energiekosten"])
            #energiekosten_dropdown.pack(pady=5)

            #ttk.Label(modify_window, text="Anschaffungskosten:").pack(pady=10)
            #anschaffungskosten_dropdown = ttk.Combobox(modify_window, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Anschaffungskosten"])
            #anschaffungskosten_dropdown.pack(pady=5)

        # Create buttons for calculations and data modification
        ttk.Button(modify_window, text="Calculate and Display", command=self.calculate_and_display).pack(pady=10)


    def change_data(self):
        # Implement functionality to change manual data
        # Place holder message for demonstration purposes
        messagebox.showinfo("Confirm Data", "Data confirmed successfully.")

        self.calculate_and_display()




        # Berechnungen
    def calculate_and_display(self):
        if self.selected_component:


            # Nur Vorübergehend:
            strompreis_entry = 0.41
            wirkungsgrad_elektrisch_entry = 0.95
            wirkungsgrad_pneumatik_entry = 0.27
            überschneidungsfaktor = 0.6

            # Perform calculations using manual data
            schichtmodell = self.manual_data["Schichtmodell"].get()
            anlagen_groesse = self.manual_data["AnlagenGroesse"].get()
            nutzungsdauer = self.manual_data["Nutzungsdauer"].get()
            masse = self.manual_data["Masse"].get()
            durchsatz = self.manual_data["Durchsatz"].get()
            #wartungskosten = self.manual_data["Wartungskosten"].get()
            #energiekosten = self.manual_data["Energiekosten"].get()
            #-anschaffungskosten = self.manual_data["Anschaffungskosten"].get()

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
            #if wartungskosten=="vernachlässigbar":
            #    beww = 0
            #elif wartungskosten=="unwichtig":
            #    beww = 1
            #elif wartungskosten=="neutral":
            #    beww = 2
            #elif wartungskosten=="wichtig":
            #    beww = 3
            #elif wartungskosten=="sehr wichtig":
            #    beww = 4

            # Auswärtung Bewertung Energiekosten
            #if energiekosten=="vernachlässigbar":
            #    bewe = 1
            #elif energiekosten=="unwichtig":
            #    bewe = 1
            #elif energiekosten=="neutral":
            #    bewe = 1
            #elif energiekosten=="wichtig":
            #    bewe = 1
            #elif energiekosten=="sehr wichtig":
            #    bewe = 2

            # Auswärtung Bewertung Anschaffungskosten
            #if anschaffungskosten=="vernachlässigbar":
            #    bewa = 1
            #elif anschaffungskosten=="unwichtig":
            #    bewa = 1
            #elif anschaffungskosten=="neutral":
            #    bewa = 1
            #elif anschaffungskosten=="wichtig":
            #    bewa = 1
            #elif anschaffungskosten=="sehr wichtig":
            #    bewa = 2
            
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
            anschaffungskosten_kompressor_preis = 10000
            anschaffungskosten_pneumatik_preis=1000
            routine_wartung_kompressor_kosten = 500
            routine_wartung_zylinder_kosten = 250
            vstrom_zylinder = 0.205
            ges_vstrom_zylinder = vstrom_zylinder * anzahl_anlage * überschneidungsfaktor / wirkungsgrad_pneumatik_entry


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

            elif ges_vstrom_zylinder < vstrom_kompressor_mittel and ges_vstrom_zylinder >= vstrom_kompressor_klein:  
                leistung_pneumatik = leistung_kompressor_mittel

            elif ges_vstrom_zylinder < vstrom_kompressor_groß and ges_vstrom_zylinder >= vstrom_kompressor_mittel:
                leistung_pneumatik = leistung_kompressor_groß


            # Anschaffungskosten Berechnung
            anschaffungskosten_elektrik = anschaffungskosten_elektrik_preis * anzahl_anlage #* bewa
            anschaffungskosten_pneumatik = (anschaffungskosten_pneumatik_preis * anzahl_anlage + anschaffungskosten_kompressor_preis) #* bewa

            # Energiekosten Berechnung
            energiekosten_elektrik = leistung_elektrik * stunden_pro_woche * 52 * nutzungsdauer * anzahl_anlage * strompreis_entry * wirkungsgrad_elektrisch_entry #* bewe
            energiekosten_pneumatik = leistung_pneumatik * stunden_pro_woche * 52 *  nutzungsdauer * strompreis_entry #* bewe
          
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

            # Multiplizieren Sie das Integralergebnis mit den Routine-Wartungskosten
            wartungskosten_elektrik = (routine_wartung_motor_kosten * nutzungsdauer * anzahl_anlage + integral_result * 2000 * anzahl_anlage) #* beww
            routine_wartungskosten_elektrik = anzahl_anlage * routine_wartung_motor_kosten * nutzungsdauer
            

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

            # Multiplizieren Sie das Integralergebnis mit den Routine-Wartungskosten
            wartungskosten_pneumatik = ((routine_wartung_kompressor_kosten  + routine_wartung_zylinder_kosten * anzahl_anlage) * nutzungsdauer + integral_result * 2000 * anzahl_anlage + integral_result * 10000) #* beww
            routine_wartungskosten_pneumatik = (anzahl_anlage * routine_wartung_zylinder_kosten + routine_wartung_kompressor_kosten) * nutzungsdauer

            gesamtkosten_elektrik = anschaffungskosten_elektrik + wartungskosten_elektrik + energiekosten_elektrik
            gesamtkosten_pneumatik = anschaffungskosten_pneumatik + wartungskosten_pneumatik + energiekosten_pneumatik
          

        # Datenausgabe:
            # Optionally check if the calculation should start
            berechnung_starten = self.manual_data["BerechnungStarten"].get()
            if berechnung_starten == "Ja":
                # Perform calculations based on manual data
                # Replace with your actual calculations

                # Display results in a new window
                self.results_window = tk.Toplevel(self.root)
                self.results_window.geometry("1920x1080")
                self.results_window.title("Cost Analysis Results")

        
                # Display cost values
                frame_elektrik = ttk.Frame(self.results_window)
                frame_elektrik.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

                frame_pneumatik = ttk.Frame(self.results_window)
                frame_pneumatik.pack(side=tk.RIGHT, anchor=tk.NE, padx=10, pady=10)



                # Elektrik Ausgabe
                ttk.Label(frame_elektrik, text="Elektrisch", font=("Helvetica", 20, "bold")).pack(side=tk.TOP, pady=10)

                ttk.Label(frame_elektrik, text=f"Wartungskosten Elektrik: {round(wartungskosten_elektrik, 2)}", font=("Helvetica", 16)).pack(pady=5)
                ttk.Label(frame_elektrik, text=f"Energiekosten Elektrik: {round(energiekosten_elektrik, 2)}", font=("Helvetica", 16)).pack(pady=5)
                ttk.Label(frame_elektrik, text=f"Installationskosten Elektrik: {round(anschaffungskosten_elektrik, 2)}", font=("Helvetica", 16)).pack(pady=5)
                ttk.Label(frame_elektrik, text=f"Gesamtkosten Elektrik: {round(gesamtkosten_elektrik, 2)}", font=("Helvetica", 16)).pack(pady=5)

                # Frame für Graphen Elektrik
                frame_graph_elektrik = ttk.Frame(frame_elektrik)
                frame_graph_elektrik.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)


                # Graphen für Elektro
                figure_elektrik = Figure(figsize=(7.2, 5.5), tight_layout=True)

                # Parameter für Berechnungen
                x = sp.symbols('x')
                nutzungsdauer = int(self.manual_data["Nutzungsdauer"].get())

                # 1. routine_wartungskosten_elektrik
                routine_wartungskosten_elektrik = routine_wartung_motor_kosten * anzahl_anlage * x #* beww

                # 2. energiekosten_elektrik
                energiekosten_elektrik = leistung_elektrik * stunden_pro_woche * 52 * x * anzahl_anlage * strompreis_entry * wirkungsgrad_elektrisch_entry #* bewe

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
                integral_result = sp.integrate(ausfalls_wartung_motor(x), (x, 0, nutzungsdauer)).evalf()

                # 4. gesamtkosten_elektrik
                # Berechnung der Werte
                x_values = range(nutzungsdauer + 1)
                elektrik_routine_wartungskosten_values = [routine_wartungskosten_elektrik.subs(x, i).evalf() for i in x_values]
                elektrik_energiekosten_values = [energiekosten_elektrik.subs(x, i).evalf() for i in x_values]
                ausfall_wartung_motor_values = [2000 * anzahl_anlage * ausfalls_wartung_motor(i).evalf() for i in x_values]

                print(ausfall_wartung_motor_values)

                # Erstellen des Gesamtgraphen
                gesamt_graph_elektrik = [anschaffungskosten_elektrik + routine + energie + ausfall for routine, energie, ausfall in zip(elektrik_routine_wartungskosten_values, elektrik_energiekosten_values, ausfall_wartung_motor_values)]

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
                subplot3_elektrik.plot([i for i in range(nutzungsdauer + 1)], [anzahl_anlage * 2000 * ausfalls_wartung_motor(i) for i in range(nutzungsdauer + 1)], linestyle='-', color='orange')
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

                ttk.Label(frame_pneumatik, text=f"Wartungskosten Pneumatik: {round(wartungskosten_pneumatik, 2)}", font=("Helvetica", 16)).pack(pady=5)
                ttk.Label(frame_pneumatik, text=f"Energiekosten Pneumatik: {round(energiekosten_pneumatik, 2)}", font=("Helvetica", 16)).pack(pady=5)
                ttk.Label(frame_pneumatik, text=f"Installationskosten Pneumatik: {round(anschaffungskosten_pneumatik, 2)}", font=("Helvetica", 16)).pack(pady=5)
                ttk.Label(frame_pneumatik, text=f"Gesamtkosten Pneumatik: {round(gesamtkosten_pneumatik, 2)}", font=("Helvetica", 16)).pack(pady=5)

                # Frame für Graphen Pneumatik
                frame_graph_pneumatik = ttk.Frame(frame_pneumatik)
                frame_graph_pneumatik.pack(side=tk.BOTTOM, anchor=tk.S, pady=10)
                
                # Graphen für Pneumatik
                figure_pneumatik = Figure(figsize=(7.2, 5.5), tight_layout=True)

                # Parameter für Berechnungen
                x = sp.symbols('x')
                nutzungsdauer = int(self.manual_data["Nutzungsdauer"].get())

                # 1. routine_wartungskosten_pneumatik
                routine_wartungskosten_pneumatik = (routine_wartung_zylinder_kosten * anzahl_anlage + routine_wartung_kompressor_kosten) * x 

                # 2. energiekosten_pneumatik
                energiekosten_pneumatik = leistung_pneumatik * stunden_pro_woche * 52 *  x * strompreis_entry 

                # 3. ausfalls_wartung_pneumatik
                def exponential_function1(x):
                    return 0.04 * sp.exp(-0.55 * x) + 0.03

                def exponential_function2(x):
                    return 0.02 * sp.exp(0.2 * (x - 20)) + 0.03

                def ausfalls_wartung_pneumatik(x):
                    condition = sp.LessThan(x, 6.2)
                    return sp.Piecewise((exponential_function1(x), condition), (exponential_function2(x), True))

                integral_result = sp.integrate(2*ausfalls_wartung_pneumatik(x), (x, 0, nutzungsdauer)).evalf()

                # 4. gesamtkosten pneumatik
                # Berechnung der Werte
                x_values = range(nutzungsdauer + 1)
                pneumatik_routine_wartungskosten_values = [routine_wartungskosten_pneumatik.subs(x, i).evalf() for i in x_values]
                pneumatik_energiekosten_values = [energiekosten_pneumatik.subs(x, i).evalf() for i in x_values]
                ausfall_wartung_pneuamtik_values = [2000 * anzahl_anlage * ausfalls_wartung_pneumatik(i).evalf() for i in x_values]

                print(ausfall_wartung_pneuamtik_values)

                # Erstellen des Gesamtgraphen
                gesamt_graph_pneumatik = [anschaffungskosten_pneumatik + routine + energie + ausfall for routine, energie, ausfall in zip(pneumatik_routine_wartungskosten_values, pneumatik_energiekosten_values, ausfall_wartung_pneuamtik_values)]

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
                subplot3_pneumatik.plot([i for i in range(nutzungsdauer + 1)], [anzahl_anlage * 2000 * ausfalls_wartung_pneumatik(i) for i in range(nutzungsdauer + 1)], linestyle='-', color='blue')
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
    def back_to_main_menu(self):
        # Placeholder confirmation message
        user_response = messagebox.askyesno("Back to Hauptmenü", "Do you want to go back to Hauptmenü?")
        if user_response:
            self.root.destroy()
            root = tk.Tk()
            app = FullScreenApp(root)
            root.mainloop()




        # Als PDF speichern
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

    def render_figure_to_png(self, figure):
        # Render the Matplotlib figure to a PNG image
        figure_canvas = FigureCanvasTkAgg(figure, master=self.root)
        figure_canvas.draw()
        figure_image = ImageTk.PhotoImage(figure_canvas.get_tk_widget().master, master=figure_canvas.get_tk_widget())
        figure_canvas.get_tk_widget().destroy()
        
        return figure_image
    



        # Options Fenster
    def open_options_window(self):
        options_window = tk.Toplevel(self.root)
        options_window.geometry("250x300")
        options_window.title("Options")

        ttk.Label(options_window, text="Wirkungsgrad elektrisch:").pack(pady=10)
        wirkungsgrad_elektrisch_entry = ttk.Entry(options_window)
        wirkungsgrad_elektrisch_entry.pack(pady=5)

        ttk.Label(options_window, text="Wirkungsgrad pneumatisch:").pack(pady=10)
        wirkungsgrad_pneumatisch_entry = ttk.Entry(options_window)
        wirkungsgrad_pneumatisch_entry.pack(pady=5)

        ttk.Label(options_window, text="Strompreis:").pack(pady=10)
        strompreis_entry = ttk.Entry(options_window)
        strompreis_entry.pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = FullScreenApp(root)

root.mainloop()