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

        # Variablen der Komponenten abrufen
        self.component_data = {
             "Gurtumsetzer": {"strompreis_entry": 0.31, "wirkungsgrad_elektrisch_entry":0.95, "wirkungsgrad_pneumatisch_entry":0.27},
             "Staurollenförderer": {"strompreis_entry": 0.31, "wirkungsgrad_elektrisch_entry":0.95, "wirkungsgrad_pneumatisch_entry":0.27}
        }




        # Create main menu
        self.create_menu()

    def create_menu(self):
        # Main menu frame
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(side="top", fill="x")

        # Component selection
        ttk.Label(self.root, text="Select Component:").pack(pady=50)
        self.component_dropdown = ttk.Combobox(self.root, values=list(self.component_data.keys()))
        self.component_dropdown.pack(pady=10)

        ttk.Button(self.root, text="Begin Selection", command=self.modify_data).pack(pady=10)
        
        ttk.Button(menu_frame, text="Options", command=self.open_options_window).pack(side="left", padx=10)

        # Manuellen Daten der Komponenten
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




        # Create show component Fenster
    def show_component_data(self):
        self.selected_component = self.component_dropdown.get()
        data = self.component_data.get(self.selected_component, {})

        # Create a new window to display component data and allow manual data input.
        data_window = tk.Toplevel(self.root)
        data_window.geometry("1920x1080")
        data_window.title(f"{self.selected_component} Component Data")

        # Display component data
        ttk.Label(data_window, text=f"{self.selected_component} Component Data", font=("Helvetica", 24)).pack(pady=20)
        for key, value in data.items():
            ttk.Label(data_window, text=f"{key}: {value}", font=("Helvetica", 16)).pack(pady=10)

        # Create buttons for calculations and data modification
        ttk.Button(data_window, text="Calculate", command=self.calculate_and_display).pack(pady=10)
        ttk.Button(data_window, text="Modify Data", command=self.modify_data).pack(pady=10)




        # Modify Data input
    def modify_data(self):
        
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

        ttk.Label(modify_window, text="Wartungskosten:").pack(pady=10)
        wartungskosten_dropdown = ttk.Combobox(modify_window, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Wartungskosten"])
        wartungskosten_dropdown.pack(pady=5)

        ttk.Label(modify_window, text="Energiekosten:").pack(pady=10)
        energiekosten_dropdown = ttk.Combobox(modify_window, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Wartungskosten"])
        energiekosten_dropdown.pack(pady=5)

        ttk.Label(modify_window, text="Anschaffungskosten:").pack(pady=10)
        anschaffungskosten_dropdown = ttk.Combobox(modify_window, values=["vernachlässigbar", "unwichtig", "neutral", "wichtig", "sehr wichtig"], textvariable=self.manual_data["Wartungskosten"])
        anschaffungskosten_dropdown.pack(pady=5)

        ttk.Button(modify_window, text="Confirm Data", command=self.change_data).pack(pady=10)

    def change_data(self):
        # Implement functionality to change manual data
        # Placeholder message for demonstration purposes
        messagebox.showinfo("Confirm Data", "Data confirmed successfully.")

        self.show_component_data()




        # Berechnungen
    def calculate_and_display(self):
        if self.selected_component:
            data = self.component_data[self.selected_component]

            # Perform calculations using manual data
            schichtmodell = self.manual_data["Schichtmodell"].get()
            anlagen_groesse = self.manual_data["AnlagenGroesse"].get()
            anschaffungskosten_kompressor = 10000
            leistung_eletrik=0.07
            leistung_pneumatik=0.28
            routine_wartung_kompressor_kosten = 500
            routine_wartung_motor_kosten = 250
            routine_wartung_zylinder_kosten = 250
            nutzungsdauer = self.manual_data["Nutzungsdauer"].get()

            # Nur Vorübergehend:
            strompreis_entry=0.41
            wirkungsgrad_elektrisch_entry=0.95

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

            # Anschaffungskosten Berechnung
            anschaffungskosten_elektrik = 3000 * anzahl_anlage
            anschaffungskosten_pneumatik = 1000 * anzahl_anlage + anschaffungskosten_kompressor

            # Energiekosten Berechnung
            energiekosten_elektrik = leistung_eletrik * stunden_pro_woche * nutzungsdauer * anzahl_anlage * strompreis_entry * wirkungsgrad_elektrisch_entry
            energiekosten_pneumatik = leistung_pneumatik * stunden_pro_woche * nutzungsdauer * anzahl_anlage * strompreis_entry 
          
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
            wartungskosten_elektrik = routine_wartung_motor_kosten * nutzungsdauer + integral_result * 2000 * anzahl_anlage

            

            # Wartungskosten Pneumatik:
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
            wartungskosten_pneumatik = routine_wartung_kompressor_kosten * routine_wartung_zylinder_kosten * nutzungsdauer + integral_result * 2000*100


            nutzungsdauer = self.manual_data["Nutzungsdauer"].get()

            gesamtkosten_elektrik = anschaffungskosten_elektrik + energiekosten_elektrik + wartungskosten_elektrik
            gesamtkosten_pneumatik = anschaffungskosten_pneumatik + energiekosten_pneumatik + wartungskosten_pneumatik



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
                frame_elektrik.pack(side=tk.LEFT, padx=10, pady=10)

                frame_pneumatik = ttk.Frame(self.results_window)
                frame_pneumatik.pack(side=tk.RIGHT, padx=10, pady=10)

                ttk.Label(frame_elektrik, text=f"Wartungskosten Elektrik: {round(wartungskosten_elektrik, 2)}", font=("Helvetica", 16)).pack(anchor=tk.W)
                ttk.Label(frame_elektrik, text=f"Energiekosten Elektrik: {round(energiekosten_elektrik, 2)}", font=("Helvetica", 16)).pack(anchor=tk.W)
                ttk.Label(frame_elektrik, text=f"Installationskosten Elektrik: {round(anschaffungskosten_elektrik, 2)}", font=("Helvetica", 16)).pack(anchor=tk.W)
                ttk.Label(frame_elektrik, text=f"Gesamtkosten Elektrik: {round(gesamtkosten_elektrik, 2)}", font=("Helvetica", 16)).pack(anchor=tk.W)

                ttk.Label(frame_pneumatik, text=f"Wartungskosten Pneumatik: {round(wartungskosten_pneumatik, 2)}", font=("Helvetica", 16)).pack(anchor=tk.W)
                ttk.Label(frame_pneumatik, text=f"Energiekosten Pneumatik: {round(energiekosten_pneumatik, 2)}", font=("Helvetica", 16)).pack(anchor=tk.W)
                ttk.Label(frame_pneumatik, text=f"Installationskosten Pneumatik: {round(anschaffungskosten_pneumatik, 2)}", font=("Helvetica", 16)).pack(anchor=tk.W)
                ttk.Label(frame_pneumatik, text=f"Gesamtkosten Pneumatik: {round(gesamtkosten_pneumatik, 2)}", font=("Helvetica", 16)).pack(anchor=tk.W)


                # Create buttons for returning to main menu and changing component
                ttk.Button(self.results_window, text="Hauptmenü", command=self.back_to_main_menu).pack(pady=10)
                ttk.Button(self.results_window, text="Modify Data", command=self.modify_data).pack(pady=10)



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
