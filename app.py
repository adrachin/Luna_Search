from flask import Flask, request, jsonify, render_template
import subprocess
import os
import urllib.parse

app = Flask(__name__, template_folder='templates')

class Project:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.size = self.calculate_size(path)  # Größe berechnen
        self.escaped_path = urllib.parse.quote(path)

    @staticmethod
    def calculate_size(path):
        """Berechnet die Größe des Verzeichnisses oder der Datei in Gigabytes."""
        total_size = 0
        if os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
        else:
            total_size = os.path.getsize(path)
        return total_size / (1024 ** 3)  # Bytes in Gigabytes umwandeln

def load_projects():
    """Lädt Projektdaten aus der Datei 'treffer.txt'."""
    project_paths = []
    try:
        # Verwenden des relativen Pfads zur Datei 'treffer.txt'
        with open('templates/treffer.txt', 'r', encoding='utf-8') as file:
            project_paths = file.read().splitlines()
    except FileNotFoundError:
        print("Die Datei 'treffer.txt' konnte nicht gefunden werden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

    return [Project(path) for path in project_paths if path.strip()]


@app.route("/")
def index():
    """Lädt die Hauptseite der Webanwendung."""
    projects = load_projects()  # Projekte laden
    return render_template('treffer.html', projects=projects)

@app.route("/open_luna", methods=['POST'])
def open_luna():
    """Öffnet ein Projekt in der Luna.app."""
    path = request.form['path']
    try:
        subprocess.run(['open', '-a', '/Applications/LUNA.app', path], check=True)
        return jsonify(success=True, message="Projekt erfolgreich geöffnet")
    except subprocess.CalledProcessError as e:
        return jsonify(success=False, message="Fehler beim Öffnen des Projekts")

@app.route("/open_in_finder", methods=['POST'])
def open_in_finder():
    """Öffnet den Finder am Speicherort des Projekts."""
    path = request.form['path']
    try:
        subprocess.run(['open', '-R', path], check=True)
        return jsonify(success=True, message="Ordner im Finder geöffnet")
    except subprocess.CalledProcessError as e:
        return jsonify(success=False, message="Fehler beim Öffnen im Finder")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
