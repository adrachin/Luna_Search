import subprocess
import os
import tkinter as tk
from tkinter import messagebox

# Statische Erweiterung für die Suche
extension = ".luna"

def get_directory():
    """Fragt den Benutzer nach einem Verzeichnis mithilfe eines Finder-Popup-Fensters."""
    script = """
    tell application "Finder"
        activate
        set selectedFolder to POSIX path of (choose folder with prompt "Wähle ein Verzeichnis aus")
    end tell
    selectedFolder
    """
    # Führe das AppleScript aus und erhalte den ausgewählten Ordnerpfad
    try:
        directory = subprocess.run(['osascript', '-e', script], capture_output=True, text=True).stdout.strip()
        return directory
    except subprocess.CalledProcessError:
        return None

def validate_directory(directory):
    """Überprüft, ob der eingegebene Pfad gültig ist."""
    return os.path.isdir(directory)

def search_files(directory, extension):
    """Sucht nach Dateien mit der angegebenen Erweiterung im Verzeichnis."""
    result = subprocess.run(['find', directory, '-name', f"*{extension}"], capture_output=True, text=True)
    file_paths = result.stdout.strip().split('\n')
    return file_paths

def get_directory_size(directory):
    """Berechnet die Größe eines Verzeichnisses in Gigabytes."""
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / (1024 ** 3)  # Convert Bytes to Gigabytes

def write_to_file(file_paths, output_file):
    """Schreibt die gefundenen Dateipfade in eine Ausgabedatei."""
    with open(output_file, 'a') as file:  # Ändere 'w' zu 'a' für Append-Modus
        for file_path in file_paths:
            file.write(file_path + '\n')

def show_summary(num_projects, total_size_gb):
    """Zeigt eine Zusammenfassung der gefundenen Projekte an."""
    root = tk.Tk()
    root.withdraw()  # Verhindert, dass das Tkinter-Fenster angezeigt wird
    messagebox.showinfo("Zusammenfassung", f"Anzahl der gefundenen Projekte: {num_projects}\nGesamtgröße der Projekte: {total_size_gb:.2f} GB")
    root.destroy()

def main():
    total_projects = 0
    total_size_gb = 0
    while True:
        # Frage den Benutzer nach einem Verzeichnis
        directory = get_directory()
        if not directory or not validate_directory(directory):
            show_summary(total_projects, total_size_gb)
            print("Kein gültiges Verzeichnis eingegeben oder Abbruch durch den Benutzer.")
            break

        # Suche nach Dateien mit der .luna-Erweiterung im angegebenen Verzeichnis
        file_paths = search_files(directory, extension)
        total_projects += len(file_paths)
        for path in file_paths:
            total_size_gb += get_directory_size(path)

        # Zeige die Suchergebnisse im Terminal an
        print("Suchergebnisse:")
        for file_path in file_paths:
            print(file_path)

        # Stelle sicher, dass der Output-Ordner existiert
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'treffer.txt')
        write_to_file(file_paths, output_file)

        # Zeige die Anzahl der Fundstellen und den Pfad der Ausgabedatei an
        print(f"Anzahl der Fundstellen: {len(file_paths)}")
        print(f"Die Treffer wurden in die Datei {output_file} geschrieben.")

if __name__ == "__main__":
    main()
