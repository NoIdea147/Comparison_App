from reportlab.pdfgen import canvas

class PDFExport:
    def __init__(self, dateiname, hauptprogramm):
        self.hauptprogramm=hauptprogramm
        self.dateiname = dateiname

    def erstelle_pdf(self, elektrik_ergebnisse, pneumatik_ergebnisse):
        pdf = canvas.Canvas(self.dateiname)
        
        pdf.drawString(100, 800, "Ergebnisse - Elektrik:")
        pdf.drawString(100, 780, f"Gesamtkosten: {elektrik_ergebnisse['gesamtkosten']} Euro")

        pdf.drawString(100, 750, "Ergebnisse - Pneumatik:")
        pdf.drawString(100, 730, f"Gesamtkosten: {pneumatik_ergebnisse['gesamtkosten']} Euro")

        # Hier können weitere Informationen hinzugefügt werden

        pdf.save()



if __name__ == "__main__":
    # Beispielaufruf für das Modul
    pdf_export = PDFExport("ergebnisse.pdf")
    pdf_export.erstelle_pdf({"gesamtkosten": 10000}, {"gesamtkosten": 8000})
