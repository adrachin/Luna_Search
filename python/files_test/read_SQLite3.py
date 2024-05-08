import sqlite3
import pandas as pd
import subprocess
import os

def select_database_file():
    """ Nutzt AppleScript, um den macOS Dateidialog zu öffnen und eine Datei auszuwählen. """
    script = '''
    tell application "Finder"
        activate
        return POSIX path of (choose file with prompt "Wähle eine SQLite-Datenbankdatei" of type {"db"})
    end tell
    '''
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    file_path = result.stdout.strip()
    return file_path if file_path else None

def export_tables_to_csv(db_path):
    """ Exportiert jede Tabelle einer SQLite-Datenbank in eine separate CSV-Datei. """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table_name in tables:
        table = table_name[0]
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        output_path = os.path.join(os.path.expanduser('~'), f"{table}.csv")
        df.to_csv(output_path, index=False)
        print(f"Daten wurden exportiert: {output_path}")

    conn.close()

def main():
    db_file = select_database_file()
    if db_file:
        export_tables_to_csv(db_file)
    else:
        print("Keine Datenbankdatei ausgewählt.")

if __name__ == "__main__":
    main()
