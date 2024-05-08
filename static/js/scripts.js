function openLuna(encodedPath) {
    // Zuerst den Pfad dekodieren
    const path = decodeURIComponent(encodedPath);

    fetch('/open_luna', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `path=${path}` // Sendet den Pfad uncodiert
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Projekt erfolgreich in Luna geöffnet.');
        } else {
            alert('Fehler: ' + data.message);
        }
    })
    .catch(error => alert('Fehler beim Senden der Anfrage: ' + error));
}

function openInFinder(encodedPath) {
    // Zuerst den Pfad dekodieren
    const path = decodeURIComponent(encodedPath);

    fetch('/open_in_finder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `path=${path}` // Sendet den Pfad uncodiert
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Ordner im Finder geöffnet.');
        } else {
            alert('Fehler: ' + data.message);
        }
    })
    .catch(error => alert('Fehler beim Senden der Anfrage: ' + error));
}
