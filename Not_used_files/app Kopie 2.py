from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    """Lädt die Hauptseite der Webanwendung."""
    return render_template('treffer.html')

@app.route("/test")
def test():
    """Lädt die Testseite."""
    return render_template('test.html')

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
