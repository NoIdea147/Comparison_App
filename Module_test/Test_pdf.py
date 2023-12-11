# pdf_module.py

from reportlab.pdfgen import canvas

class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename

    def generate_pdf(self):
        c = canvas.Canvas(self.filename)
        c.drawString(100, 750, "Hello, this is a PDF")
