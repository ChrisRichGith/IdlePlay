#!/bin/bash

# Stellt sicher, dass das Skript bei einem Fehler abbricht
set -e

# Überprüft, ob die richtige Anzahl von Argumenten übergeben wurde (2 werden erwartet)
if [ "$#" -ne 2 ]; then
    echo "Benutzung: $0 <Pfad_zum_Ordner> \"<Commit-Nachricht>\""
    echo "Beispiel: ./upload_folder.sh ./mein_projekt \"Fügt das neue Projekt hinzu\""
    exit 1
fi

# Weist die Argumente Variablen mit aussagekräftigen Namen zu
FOLDER_PATH=$1
COMMIT_MESSAGE=$2

# Überprüft, ob der angegebene Pfad auch wirklich ein Ordner ist
if [ ! -d "$FOLDER_PATH" ]; then
    echo "Fehler: Der Ordner '$FOLDER_PATH' wurde nicht gefunden."
    exit 1
fi

# Schritt 1: Fügt den Ordner zum Git-Staging-Bereich hinzu
echo "Füge den Ordner '$FOLDER_PATH' zum Repository hinzu..."
git add "$FOLDER_PATH"

# Schritt 2: Erstellt einen Commit mit der übergebenen Nachricht
echo "Erstelle Commit mit der Nachricht: \"$COMMIT_MESSAGE\"..."
git commit -m "$COMMIT_MESSAGE"

# Schritt 3: Lädt die Änderungen in das Remote-Repository hoch
echo "Lade die Änderungen hoch (git push)..."
git push

echo "Fertig! Der Ordner wurde erfolgreich hochgeladen."
