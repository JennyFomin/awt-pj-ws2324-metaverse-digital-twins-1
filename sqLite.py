import sqlite3

def execute_sql_script(script_path):
    with open(script_path, 'r') as script_file:
        sql_script = script_file.read()
    # SQLite-Datenbankverbindung herstellen (wenn die Datei nicht existiert, wird sie erstellt)
    db_connection = sqlite3.connect("energy_data.db")

    # SQLite-Cursor erstellen
    cursor = db_connection.cursor()

    # Tabelle erstellen, wenn sie noch nicht existiert
    cursor.executescript(sql_script)

    # Änderungen in der Datenbank bestätigen
    db_connection.commit()

    # Verbindung schließen
    db_connection.close()

# Aufruf der Funktion mit dem Pfad zum SQL-Skript
execute_sql_script('create_tables.sql')
