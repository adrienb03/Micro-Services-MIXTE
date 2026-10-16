# Image python
FROM python:3.11-slim

# Dossier de travail
WORKDIR /app

# Dépendances
COPY requirements.txt /app

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Code source
COPY booking.py /app

# Fichiers de données
COPY data/ /app/data/

# Port
EXPOSE 3003

# Commande d'exécution
CMD ["python", "-u", "booking.py"]