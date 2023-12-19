import mysql.connector

# Verbindungsinformationen für die Datenbanken
db_config = {
    'host': 'localhost',
    'user': 'dev_user',
    'password': '^JB~_seip6Y%iuLV]V_.xmQn{nKA$Z'
}

# Funktion, um Daten aus einer bestimmten Datenbank und Tabelle zu holen
def fetch_data(database_name, table_name):
    connection = mysql.connector.connect(database=database_name, **db_config)
    cursor = connection.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# Daten aus den spezifischen Tabellen und Spalten holen
elektrik = fetch_data('elektrik', 'elektrik')
zylinder = fetch_data('zylinder', 'zylinder')
kompressor = fetch_data('kompressor', 'kompressor')

# Variablen für jede Spalte aus jeder Tabelle erstellen
# Beispiel für Tabelle1 aus Datenbank1 mit Spalten 'Spalte1', 'Spalte2', 'Spalte3'
for row in elektrik:
    Geschwindigkeit = row[0]
    Beschleunigug = row[1]
    # Verwenden Sie die Variablen wie benötigt
   #print("DB Elektrik") #Showcase
    print(Geschwindigkeit, Beschleunigug)


for row in zylinder:
    Hub = row[0]
    Kolbendurchmesser = row[1]
    Luftverbrauch = row[2]
    # Verwenden Sie die Variablen wie benötigt
    #print("DB Zylinder") #Showcase
    print(Hub, Kolbendurchmesser, Luftverbrauch)


for row in kompressor:
    Druck = row[1]
    Volumenstrom = row[2]
    Leistung = row[3]
    # Verwenden Sie die Variablen wie benötigt
    #print("DB Zylinder") #Showcase
    print(Druck, Volumenstrom, Leistung)
    

