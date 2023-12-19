from DB_Test import abfrage_kompressor_daten

# Daten aus der Datenbank abrufen
kompressor_daten = abfrage_kompressor_daten()

# Variablen aus dem Dictionary verwenden
klein_druck = kompressor_daten['klein_druck']
klein_volumenstrom = kompressor_daten['klein_volumenstrom']
klein_leistung = kompressor_daten['klein_leistung']

mittel_druck = kompressor_daten['mittel_druck']
mittel_volumenstrom = kompressor_daten['mittel_volumenstrom']
mittel_leistung = kompressor_daten['mittel_leistung']

groß_druck = kompressor_daten['groß_druck']
groß_volumenstrom = kompressor_daten['groß_volumenstrom']
groß_leistung = kompressor_daten['groß_leistung']

print(klein_leistung)
