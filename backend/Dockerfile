# =============================================================================
# 🐍 Dockerfile Backend - Python/FastAPI
# =============================================================================

# Utilisation de 'alpine' pour éviter les erreurs avec PostgreSQL
FROM python:3.11-slim

# Métadonnées
LABEL maintainer="etudiant@esiea.fr"
LABEL description="Backend API pour projet microservices ESIEA"

# Répertoire de travail
WORKDIR /app

# =============================================================================
# 📦 INSTALLATION DES DÉPENDANCES
# =============================================================================

# Installation de curl pour le healthcheck (nécessaire sur l'image slim)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements.txt en premier
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# 📁 COPIE DU CODE SOURCE
# =============================================================================

# Copier tout le code source (main.py, etc.)
COPY . .

# =============================================================================
# 🔧 CONFIGURATION
# =============================================================================

# Port d'écoute
EXPOSE 8000

# Variables d'environnement par défaut
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# =============================================================================
# 🏥 HEALTH CHECK OBLIGATOIRE
# =============================================================================
# Vérifie toutes les 30s si l'API répond bien sur /health
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# =============================================================================
# 🚀 COMMANDE DE DÉMARRAGE
# =============================================================================

# Démarrage avec Uvicorn (Serveur pour FastAPI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]