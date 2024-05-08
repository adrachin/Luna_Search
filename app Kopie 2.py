from flask import Flask, request, render_template, jsonify
import subprocess
import os
import urllib.parse

app = Flask(__name__, template_folder='templates')

class Project:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.size = self.calculate_size(path)
        self.escaped_path = urllib.parse.quote(path)

    @staticmethod
    def calculate_size(path):
        total_size = 0
        if os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total_size += os.path.getsize(fp)
        else:
            total_size = os.path.getsize(path)
        return total_size / (1024 ** 3)  # Konvertierung von Bytes in Gigabytes

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        directory = request.form['directory']
        if directory:
            projects = search_files(directory, '.luna')
            return render_template('treffer.html', projects=projects)
    return render_template('index.html')

def search_files(directory, extension):
    result = subprocess.run(['find', directory, '-name', f"*{extension}"], capture_output=True, text=True)
    file_paths = result.stdout.strip().split('\n')
    return [Project(path) for path in file_paths if path.strip()]

@app.route("/open_luna", methods=['POST'])
def open_luna():
    path = request.form['path']
    try:
        subprocess.run(['open', '-a', '/Applications/LUNA.app', path], check=True)
        return jsonify(success=True, message="Projekt erfolgreich geöffnet")
    except subprocess.CalledProcessError as e:
        return jsonify(success=False, message="Fehler beim Öffnen des Projekts")

@app.route("/open_in_finder", methods=['POST'])
def open_in_finder():
    path = request.form['path']
    try:
        subprocess.run(['open', '-R', path], check=True)
        return jsonify(success=True, message="Ordner im Finder geöffnet")
    except subprocess.CalledProcessError as e:
        return jsonify(success=False, message="Fehler beim Öffnen im Finder")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
