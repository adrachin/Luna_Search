import os
import http.server
import socketserver

# Verzeichnis, das Sie hosten möchten (hier das Verzeichnis der HTML-Datei)
directory = '/Users/thomas/110_days_python/Test_Scripts/templates'

# Portnummer für den Server
port = 8000

os.chdir(directory)  # Ändern Sie das Arbeitsverzeichnis auf das zu hostende Verzeichnis

# Erstellen Sie einen einfachen HTTP-Server
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", port), Handler) as httpd:
    print("Server läuft auf dem Port:", port)
    # Warten Sie auf Anforderungen
    httpd.serve_forever()
