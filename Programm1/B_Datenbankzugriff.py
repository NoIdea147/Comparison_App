import sqlite3
class Datenbankzugriff:
    def __init__(self, hauptprogramm):
        self.hauptprogramm = hauptprogramm
    # Verbindung zur Datenbank herstellen (oder erstellen, falls nicht vorhanden)
    conn = sqlite3.connect('datenbank.db')

    # Cursor erstellen, um SQL-Operationen durchzuführen
    cursor = conn.cursor()

    # Tabelle erstellen (wenn sie nicht vorhanden ist)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bauteile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            antriebsart TEXT,
            installationskosten INTEGER,
            wartungskosten INTEGER
        )
    ''')

    # Beispielwerte einfügen
    cursor.execute("INSERT INTO bauteile (name, antriebsart, installationskosten, wartungskosten) VALUES (?, ?, ?, ?)",
                ('Staurollenförderer', 'Elektrik', 5000, 200))
    cursor.execute("INSERT INTO bauteile (name, antriebsart, installationskosten, wartungskosten) VALUES (?, ?, ?, ?)",
                ('Staurollenförderer', 'Pneumatik', 3000, 150))

    cursor.execute("INSERT INTO bauteile (name, antriebsart, installationskosten, wartungskosten) VALUES (?, ?, ?, ?)",
                ('Gurtumsetzer', 'Elektrik', 8000, 300))
    cursor.execute("INSERT INTO bauteile (name, antriebsart, installationskosten, wartungskosten) VALUES (?, ?, ?, ?)",
                ('Gurtumsetzer', 'Pneumatik', 6000, 250))

    # Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()

    def __init__(self, hauptprogramm):
        self.hauptprogramm = hauptprogramm
