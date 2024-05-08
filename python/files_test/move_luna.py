import os
import shutil
import datetime
from tkinter import messagebox
import tkinter as tk

def load_file_paths(file_path):
    """Liest Dateipfade aus einer Datei."""
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def copy_files_with_date(source_paths, destination_folder):
    """Kopiert Dateien und fügt das Erstellungsdatum vor dem Dateinamen ein."""
    total_size_gb = 0
    for path in source_paths:
        try:
            folder_name = os.path.basename(path)
            creation_date = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%d.%m.%Y')
            new_folder_name = f"{creation_date}_{folder_name}"
            dest_path = os.path.join(destination_folder, new_folder_name)
            # Prüfen, ob das Zielverzeichnis bereits existiert und ggf. einen neuen Namen generieren
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(destination_folder, f"{new_folder_name}_{counter}")
                counter += 1
            shutil.copytree(path, dest_path)
            total_size_gb += get_directory_size(path) / (1024 ** 3)
        except Exception as e:
            print(f"Fehler beim Kopieren von {path}: {e}")
    return total_size_gb

def get_directory_size(directory):
    """Berechnet die Größe eines Verzeichnisses in Bytes."""
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

def main():
    root = tk.Tk()
    root.withdraw()  # Versteckt das Hauptfenster von tkinter

    input_file = '/Users/thomas/MyApps/Luna_Search/templates/treffer.txt'
    destination_folder = '/Volumes/SSD_500GB'

    paths = load_file_paths(input_file)
    total_size_gb = copy_files_with_date(paths, destination_folder)

    messagebox.showinfo("Kopierprozess abgeschlossen", f"Alle Dateien wurden erfolgreich kopiert.\nGesamtgröße: {total_size_gb:.2f} GB")
    root.destroy()

if __name__ == "__main__":
    main()
