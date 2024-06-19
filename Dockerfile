# Verwenden Sie ein Python-Image als Basis
FROM python:3.9-slim

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die Anforderungen und die Anwendung in das Arbeitsverzeichnis
COPY requirements.txt requirements.txt
COPY . .

# Installieren Sie die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Exponieren Sie den Port, auf dem Flask läuft
EXPOSE 44555

# Starten Sie die Flask-Anwendung
CMD ["python", "server.py"]
