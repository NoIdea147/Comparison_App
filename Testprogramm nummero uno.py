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

        # Manuellen Daten der Komponenten
        self.selected_component = None
        self.manual_data = {
            "Schichtmodell": tk.StringVar(),
            "AnlagenGroesse": tk.StringVar(),
            "Anschaffungskosten": tk.DoubleVar(),
            "Betriebskosten": tk.DoubleVar(),
            "Wartungskosten": tk.DoubleVar(),
            "Nutzungsdauer": tk.IntVar(),
            "BerechnungStarten": tk.StringVar(value="Ja")
        }

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

    def modify_data(self):
        # Create a new window to modify manual data
        modify_window = tk.Toplevel(self.root)
        modify_window.geometry("1920x1080")
        modify_window.title("Modify Data")

        # Create entry fields for manual data
        ttk.Label(modify_window, text="Schichtmodell:").pack(pady=10)
        schichtmodell_dropdown = ttk.Combobox(modify_window, values=["Zweischichtbetrieb", "Dreibschichtbetrieb", "Dauerbetrieb"], textvariable=self.manual_data["Schichtmodell"])
        schichtmodell_dropdown.pack(pady=5)

        ttk.Label(modify_window, text="Anlagen Größe:").pack(pady=10)
        anlagen_groesse_dropdown = ttk.Combobox(modify_window, values=["Klein (10 Stück)", "Mittel (50 Stück)", "Groß (100 Stück)"], textvariable=self.manual_data["AnlagenGroesse"])
        anlagen_groesse_dropdown.pack(pady=5)

        ttk.Label(modify_window, text="Anschaffungskosten:").pack(pady=10)
        anschaffungskosten_entry = ttk.Entry(modify_window, textvariable=self.manual_data["Anschaffungskosten"])
        anschaffungskosten_entry.pack(pady=5)

        ttk.Label(modify_window, text="Betriebskosten:").pack(pady=10)
        betriebskosten_entry = ttk.Entry(modify_window, textvariable=self.manual_data["Betriebskosten"])
        betriebskosten_entry.pack(pady=5)

        ttk.Label(modify_window, text="Wartungskosten:").pack(pady=10)
        wartungskosten_entry = ttk.Entry(modify_window, textvariable=self.manual_data["Wartungskosten"])
        wartungskosten_entry.pack(pady=5)

        ttk.Label(modify_window, text="Nutzungsdauer (Jahre):").pack(pady=10)
        nutzungsdauer_entry = ttk.Entry(modify_window, textvariable=self.manual_data["Nutzungsdauer"])
        nutzungsdauer_entry.pack(pady=5)

        ttk.Button(modify_window, text="Confirm Data", command=self.change_data).pack(pady=10)


    def change_data(self):
        # Implement functionality to change manual data
        # Placeholder message for demonstration purposes
        messagebox.showinfo("Confirm Data", "Data confirmed successfully.")

        self.show_component_data()

    def calculate_and_display(self):
        if self.selected_component:
            data = self.component_data[self.selected_component]

            # Perform calculations using manual data
            schichtmodell = self.manual_data["Schichtmodell"].get()
            anlagen_groesse = self.manual_data["AnlagenGroesse"].get()
            anschaffungskosten = self.manual_data["Anschaffungskosten"].get()
            betriebskosten = self.manual_data["Betriebskosten"].get()
            wartungskosten = self.manual_data["Wartungskosten"].get()
            nutzungsdauer = self.manual_data["Nutzungsdauer"].get()

            # Optionally check if the calculation should start
            berechnung_starten = self.manual_data["BerechnungStarten"].get()
            if berechnung_starten == "Ja":
                # Perform calculations based on manual data
                # Replace with your actual calculations
                installation_cost = anschaffungskosten * 0.1
                operating_hours = 8

                maintenance_cost = wartungskosten
                operational_cost = betriebskosten * data["Wirkungsgrad"] * operating_hours
                total_cost = installation_cost + (maintenance_cost + operational_cost) * nutzungsdauer

                # Display results in a new window
                self.results_window = tk.Toplevel(self.root)
                self.results_window.geometry("1920x1080")
                self.results_window.title("Cost Analysis Results")

                # Create Matplotlib figures for graphs
                figure1 = Figure(figsize=(6, 4), tight_layout=True)
                subplot1 = figure1.add_subplot(111, projection='3d')
                subplot1.set_title('3D Graph')
                # Replace with your actual data for plotting
                subplot1.plot([1, 2, 3], [10, 20, 15], [5, 10, 8])

                figure2 = Figure(figsize=(3, 2), tight_layout=True)
                subplot2 = figure2.add_subplot(111)
                subplot2.set_title('Multiple Plots')
                # Replace with your actual data for plotting
                subplot2.plot([1, 2, 3], [10, 20, 15], label='Wartungskosten')
                subplot2.plot([1, 2, 3], [5, 8, 12], label='Betriebskosten')
                subplot2.legend()

                # Create FigureCanvasTkAgg widgets to display the graphs
                self.canvas1 = FigureCanvasTkAgg(figure1, master=self.results_window)
                self.canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

                self.canvas2 = FigureCanvasTkAgg(figure2, master=self.results_window)
                self.canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

                # Display cost values
                ttk.Label(self.results_window, text=f"Wartungskosten: {maintenance_cost}", font=("Helvetica", 16)).pack(pady=10)
                ttk.Label(self.results_window, text=f"Betriebskosten: {operational_cost}", font=("Helvetica", 16)).pack(pady=10)
                ttk.Label(self.results_window, text=f"Installationskosten: {installation_cost}", font=("Helvetica", 16)).pack(pady=10)
                ttk.Label(self.results_window, text=f"Gesamtkosten: {total_cost}", font=("Helvetica", 16)).pack(pady=10)

                # Create buttons for returning to main menu and changing component
                ttk.Button(self.results_window, text="Hauptmenü", command=self.back_to_main_menu).pack(pady=10)
                ttk.Button(self.results_window, text="Modify Data", command=self.modify_data).pack(pady=10)
                
    def back_to_main_menu(self):
        # Placeholder confirmation message
        user_response = messagebox.askyesno("Back to Hauptmenü", "Do you want to go back to Hauptmenü?")
        if user_response:
            self.root.destroy()
            root = tk.Tk()
            app = FullScreenApp(root)
            root.mainloop()

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


if __name__ == "__main__":
    root = tk.Tk()
    app = FullScreenApp(root)

root.mainloop()
