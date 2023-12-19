import mysql.connector

def abfrage_kompressor_daten():
    # Verbindung zur MySQL-Datenbank herstellen
    db_connection = mysql.connector.connect(
        host="localhost",
        user="dev_user",
        passwd="^JB~_seip6Y%iuLV]V_.xmQn{nKA$Z",
        database="kompressor"
    )

    # Cursor-Objekt erstellen
    cursor = db_connection.cursor()

    # SQL-Abfrage ausführen
    query = "SELECT Kompressor, Druck, Volumenstrom, Leistung FROM kompressor"
    cursor.execute(query)

    # Alle Zeilen abrufen
    rows = cursor.fetchall()

    # Dictionary für die Variablen erstellen
    kompressor_variablen = {}

    # Daten in das Dictionary einfügen
    for row in rows:
        kompressor = row[0].lower()  # 'klein', 'mittel', 'groß'
        kompressor_variablen[f"{kompressor}_druck"] = row[1]
        kompressor_variablen[f"{kompressor}_volumenstrom"] = row[2]
        kompressor_variablen[f"{kompressor}_leistung"] = row[3]

    # Verbindung schließen
    cursor.close()
    db_connection.close()

    return kompressor_variablen