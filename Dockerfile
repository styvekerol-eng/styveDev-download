# Image de base Linux légère avec Python 3.11
FROM python:3.11-slim

# Installation de FFmpeg pour la conversion audio et vidéo
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Dossier de travail dans le conteneur
WORKDIR /app

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des fichiers de l'application
COPY server.py .
COPY pwa/ ./pwa/

# Dossier temporaire pour les téléchargements
RUN mkdir -p /tmp/downloads && chmod 777 /tmp/downloads

# Port configurable par la plateforme cloud (Render, Railway, HuggingFace)
ENV PORT=8765
EXPOSE 8765

# Lancement du serveur FastAPI
CMD ["sh", "-c", "python server.py"]
