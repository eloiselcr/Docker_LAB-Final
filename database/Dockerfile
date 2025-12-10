# database/Dockerfile

# On utilise l'image officielle légère
FROM postgres:16-alpine

# Métadonnées
LABEL maintainer="etudiant@esiea.fr"
LABEL description="Base de données PostgreSQL pour Todo App"

# Variables d'environnement par défaut
# (Elles seront écrasées par le docker-compose.yml, mais c'est bien d'avoir des défauts)
ENV POSTGRES_DB=app_db
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password_temp_insecure

# Copie du script d'initialisation
# Tout fichier .sql dans ce dossier est exécuté au premier démarrage
COPY init.sql /docker-entrypoint-initdb.d/

# Port standard
EXPOSE 5432

# Healthcheck (Vérifie si la base est prête à recevoir des requêtes)
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD pg_isready -U postgres || exit 1