#!/bin/bash

# --- KONFIGURATION ---
# Die URL deines GitHub-Repositorys.
REPO_URL="https://github.com/ChrisRichGith/IdlePlay.git"
# Der Name des Ordners, in den das Repository lokal geklont wird.
REPO_DIR="IdlePlay"
# --------------------

# Bricht das Skript ab, wenn ein Befehl fehlschlägt.
set -e

# Überprüft, ob die richtige Anzahl von Argumenten übergeben wurde.
if [ "$#" -ne 2 ]; then
    echo "Benutzung: $0 <Pfad_zum_Quellordner> \"<Commit-Nachricht>\""
    echo "Beispiel: ./sync_project.sh /home/user/ZeroPlay \"Projekt-Update\""
    exit 1
fi

# Weist die Argumente Variablen zu.
SOURCE_DIR=$1
COMMIT_MESSAGE=$2

# Überprüft, ob der Quellordner existiert.
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Fehler: Der Quellordner '$SOURCE_DIR' wurde nicht gefunden."
    exit 1
fi

# --- SCHRITT 1: Repository vorbereiten ---
# Prüft, ob der Repository-Ordner bereits existiert.
if [ ! -d "$REPO_DIR" ]; then
    # Wenn nicht, wird das Repository von GitHub geklont.
    echo "Klone das Repository '$REPO_URL'..."
    git clone "$REPO_URL" "$REPO_DIR"
else
    # Wenn es existiert, wechsle in das Verzeichnis und hole die neuesten Änderungen.
    echo "Aktualisiere das lokale Repository..."
    cd "$REPO_DIR"
    # Setzt den lokalen Branch zurück, falls er durch den fehlerhaften rsync beschädigt wurde
    git reset --hard origin/main || git reset --hard origin/master
    git pull
    cd ..
fi

# --- SCHRITT 2: Dateien synchronisieren ---
echo "Synchronisiere den Inhalt von '$SOURCE_DIR' nach '$REPO_DIR'..."
# rsync ist ein leistungsstarkes Werkzeug zum Synchronisieren von Ordnern.
# --exclude='.git': Dieser neue Teil ist die KORREKTUR. Er verhindert, dass der .git-Ordner im Ziel gelöscht wird.
# --delete: Löscht Dateien im Ziel, die in der Quelle nicht mehr existieren.
# -av: Archivmodus (behält Berechtigungen, etc.) und ausführliche Ausgabe.
# Der Schrägstrich am Ende von SOURCE_DIR ist wichtig, er kopiert den *Inhalt*.
rsync -av --delete --exclude='.git' "$SOURCE_DIR/" "$REPO_DIR/"

# --- SCHRITT 3: Änderungen hochladen ---
# Wechsle in das Verzeichnis des Repositorys.
cd "$REPO_DIR"

# Prüft, ob es überhaupt Änderungen gibt, die committet werden können.
if git diff-index --quiet HEAD --; then
    echo "Keine Änderungen zum Hochladen. Dein Repository ist bereits aktuell."
else
    # Wenn es Änderungen gibt, werden sie hochgeladen.
    echo "Füge alle neuen und geänderten Dateien hinzu..."
    git add .

    echo "Erstelle Commit mit der Nachricht: \"$COMMIT_MESSAGE\"..."
    git commit -m "$COMMIT_MESSAGE"

    echo "Lade die Änderungen nach GitHub hoch..."
    git push

    echo "Fertig! Dein Projekt wurde erfolgreich synchronisiert und hochgeladen."
fi

# Kehrt zum ursprünglichen Verzeichnis zurück.
cd ..

exit 0
