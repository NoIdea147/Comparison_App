import mysql.connector

# Erstellen Sie eine Verbindung zur Datenbank
# Ersetzen Sie 'hostname', 'user', 'password' und 'database' mit Ihren eigenen Daten
conn = mysql.connector.connect(
    host='localhost',
    port = '3306',
    user='dev_user',
    password='^JB~_seip6Y%iuLV]V_.xmQn{nKA$Z',
    database='sys'
)

# Erstellen Sie ein Cursor-Objekt
cursor = conn.cursor()

# SQL-Abfrage, um alle Zeilen aus der Tabelle Bauteile zu erhalten
query = "SELECT * FROM Bauteile"

try:
    # Führen Sie die Abfrage aus
    cursor.execute(query)

    # Holen Sie alle Zeilen
    rows = cursor.fetchall()

    # Dictionary, um die Werte zu speichern
    bauteile_dict = {}

    # Schleife durch die Ergebnisse und speichern Sie die Werte im Dictionary
    for i, row in enumerate(rows, start=1):
        bauteile_dict[f'bauteil{i}_luftverbrauch'] = row[1]
        bauteile_dict[f'bauteil{i}_hub'] = row[2]
        bauteile_dict[f'bauteil{i}_zykluszeit'] = row[3]
        bauteile_dict[f'bauteil{i}_positionierungszeit'] = row[4]
        bauteile_dict[f'bauteil{i}_durchschnittliche_wartungskosten'] = row[5]

    # Beispiel, um zu zeigen, wie auf die Werte zugegriffen wird
    for key, value in bauteile_dict.items():
        print(f'{key}: {value}')

except mysql.connector.Error as err:
    print(f"Fehler: {err}")

finally:
    # Schließen Sie die Verbindung
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL Verbindung ist geschlossen")