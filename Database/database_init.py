import mysql.connector

# Verbindungsdetails für die MySQL-Datenbank
config = {
    'user': 'dev_user',
    'password': '^JB~_seip6Y%iuLV]V_.xmQn{nKA$Z',
    'host': '127.0.0.1',
    'port': '3306',  # Standard-MySQL-Port ist 3306
    'database': 'sys',
    'raise_on_warnings': True
}

try:
    # Verbindung zur Datenbank herstellen
    conn = mysql.connector.connect(**config)
    print("Verbindung zur Datenbank erfolgreich hergestellt!")
    
    # Einen Cursor erstellen
    cursor = conn.cursor()
    
    # SQL-Abfrage, um alle Werte aller Spalten für alle Zeilen zu erhalten
    query = "SELECT * FROM Bauteile"
    cursor.execute(query)
    
    # Alle Ergebnisse der Abfrage holen
    results = cursor.fetchall()
    
    if results:
        for row in results:
            # Jeden Wert in einer Variablen speichern
            bauteil = row[0]
            luftverbrauch = row[1]
            hub = row[2]
            zykluszeit = row[3]
            positionierungszeit = row[4]
            durchschnittliche_wartungskosten = row[5]
            

    else:
        print("Keine Einträge in der Tabelle Bauteile gefunden.")
    
    # Cursor und Verbindung schließen
    cursor.close()
    conn.close()
except mysql.connector.Error as e:
    print(f"Fehler bei der Verbindung zur Datenbank: {e}")
