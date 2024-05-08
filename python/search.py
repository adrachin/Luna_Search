import subprocess
import os

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
    directory = subprocess.run(['osascript', '-e', script], capture_output=True, text=True).stdout.strip()
    return directory

def validate_directory(directory):
    """Überprüft, ob der eingegebene Pfad gültig ist."""
    return True if directory else False

def search_files(directory, extension):
    """Sucht nach Dateien mit der angegebenen Erweiterung im Verzeichnis."""
    result = subprocess.run(['find', directory, '-name', f"*{extension}"], capture_output=True, text=True)
    file_paths = result.stdout.strip().split('\n')
    return file_paths

def write_to_file(file_paths, output_file):
    """Schreibt die gefundenen Dateipfade in eine Ausgabedatei."""
    with open(output_file, 'w') as file:
        for file_path in file_paths:
            file.write(file_path + '\n')

def main():
    # Frage den Benutzer nach einem Verzeichnis
    directory = get_directory()

    # Überprüfe den eingegebenen Pfad
    if not validate_directory(directory):
        print("Der eingegebene Pfad ist ungültig oder leer.")
        return

    # Suche nach Dateien mit der .luna-Erweiterung im angegebenen Verzeichnis
    file_paths = search_files(directory, extension)

    # Zeige die Suchergebnisse im Terminal an
    print("Suchergebnisse:")
    for file_path in file_paths:
        print(file_path)

    # Relativer Pfad zum 'templates' Ordner vom Wurzelverzeichnis
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, 'treffer.txt')
    write_to_file(file_paths, output_file)

    # Zeige die Anzahl der Fundstellen und den Pfad der Ausgabedatei an
    print(f"Anzahl der Fundstellen: {len(file_paths)}")
    print(f"Die Treffer wurden in die Datei {output_file} geschrieben.")

if __name__ == "__main__":
    main()
