#!/bin/bash

# Dynamisch das Basisverzeichnis bestimmen, in dem das Skript ausgeführt wird
BASE_DIR=$(dirname "$(realpath "$0")")

# Pfad zur Flask-Anwendung
FLASK_APP="$BASE_DIR/app.py"

echo "Basisverzeichnis: $BASE_DIR"

# Überprüfe, ob der Port 8000 bereits verwendet wird
PORT=8000
echo "Überprüfung des Ports $PORT..."
if lsof -i:$PORT > /dev/null; then
    echo "Port $PORT ist bereits belegt."
    read -p "Möchten Sie den laufenden Server beenden? (ja/nein): " answer
    if [[ "$answer" = "ja" ]]; then
        echo "Beende laufenden Prozess auf Port $PORT..."
        lsof -t -i:$PORT | xargs kill -9
        echo "Prozess auf Port $PORT wurde beendet."
    else
        echo "Vorgang abgebrochen."
        exit 1
    fi
else
    echo "Port $PORT ist frei."
fi

# Starten des Flask-Servers
echo "Starte Flask Server auf Port $PORT..."
export FLASK_APP="$FLASK_APP"
flask run --port=$PORT

echo "Flask Server läuft auf http://localhost:$PORT"
