# Dokckerfile pour le service booking

# Utilisation image Python 3.12 slim comme base
FROM python:3.12-slim

# Installation dépenances 
WORKDIR /app

# Copie du fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installation dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie code source dans le conteneur
COPY . .

# Éxécution service booking
CMD ["python", "booking.py"]
