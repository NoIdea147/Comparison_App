# Test_plot.py
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from Test_gui import GUI

class Graph:
    def plot_graph(ax, title):
        # Beispielplot für die Funktion
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 1, 5, 7]
        ax.plot(x, y)
        ax.set_title(title)
        ax.set_xlabel('X-Achse')
        ax.set_ylabel('Y-Achse')

    # Erstellen eines tkinter-Fensters
    root = tk.Tk()
    root.title("Anordnung von Graphen in tkinter")
    root.geometry("1920x1080")  # Passen Sie die Größe nach Bedarf an

    # Erstellen von drei Graphen
    fig1, ax1 = plt.subplots(figsize=(4, 4))
    fig2, ax2 = plt.subplots(figsize=(4, 4))
    fig3, ax3 = plt.subplots(figsize=(4, 4))

    # Zeichnen der Plots für jede Figur
    plot_graph(ax1, 'Graph 1')
    plot_graph(ax2, 'Graph 2')
    plot_graph(ax3, 'Graph 3')

    # Erstellen von Canvas-Widgets für die Graphen
    canvas1 = FigureCanvasTkAgg(fig1, master=root)
    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas3 = FigureCanvasTkAgg(fig3, master=root)

    # Platzierung der Canvas-Widgets mit pack
    canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Button, um die GUI zu öffnen
    open_gui_button = tk.Button(root, text="Zur GUI", command=GUI().run)
    open_gui_button.pack(side=tk.BOTTOM)

    # Starten der tkinter-Hauptloop
    root.mainloop()