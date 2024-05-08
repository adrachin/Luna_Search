from flask import Flask, request, jsonify, render_template
import subprocess
import os
from urllib.parse import unquote

app = Flask(__name__, template_folder='templates')

class Project:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.size = self.calculate_size(path)
        self.escaped_path = path  # Keine Notwendigkeit für URL-Kodierung hier

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
        return format(total_size / (1024 ** 3), '.2f')  # Konvertierung von Bytes in Gigabytes

@app.route("/open_luna", methods=['POST'])
def open_luna():
    path = unquote(request.form['path'])
    if not os.path.exists(path):
        return jsonify(success=False, message="Die Datei existiert nicht: " + path)
    try:
        subprocess.run(['open', '-a', '/Applications/LUNA.app', path], check=True)
        return jsonify(success=True, message="Projekt erfolgreich in Luna geöffnet")
    except subprocess.CalledProcessError as e:
        return jsonify(success=False, message="Fehler beim Öffnen in Luna: " + str(e))

@app.route("/open_in_finder", methods=['POST'])
def open_in_finder():
    path = unquote(request.form['path'])
    if not os.path.exists(path):
        return jsonify(success=False, message="Die Datei existiert nicht: " + path)
    try:
        subprocess.run(['open', '-R', path], check=True)
        return jsonify(success=True, message="Ordner im Finder geöffnet")
    except subprocess.CalledProcessError as e:
        return jsonify(success=False, message="Fehler beim Öffnen im Finder: " + str(e))

if __name__ == "__main__":
    app.run(debug=True, port=8000)
