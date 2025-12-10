# =============================================================================
# BACKEND - CONTAINER POUR LA DATABASE (PostgreSQL)
# =============================================================================

# -- image de PostegreSQL 16 Alpine
FROM postgres:16-alpine 

# -- imétadonnées du container (pour la documentation)
LABEL maintainer="etudiant@esiea.fr"
LABEL description="Base de données PostgreSQL pour Todo App"

# -- ivariables d'environnement par défaut
ENV POSTGRES_DB=app_db
ENV POSTGRES_USER=postgres
# note : pas de password car dans /secrets 

# -- copie du script d'initialisation (exécuté au 1er démarrage du container)
COPY init.sql /docker-entrypoint-initdb.d/

# -- définition du port de la db
EXPOSE 5432

# -- healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD pg_isready -U postgres || exit 1