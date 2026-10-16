# Image python
FROM python:3.11-slim

# Dossier de travail
WORKDIR /app

# Dépendances
COPY requirements.txt /app

# Installation des dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Code source
COPY movie.py /app
COPY resolvers.py /app
COPY movie.graphql /app

# Fichiers de données
COPY data/ /app/data/

# Port
EXPOSE 3001

# Commande d'exécution
CMD ["python", "-u", "movie.py"]