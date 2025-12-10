# 📁 Templates pour Projet Final Microservices

Ce dossier contient tous les fichiers templates pour vous aider à réaliser votre projet final de microservices avec Docker.

## 🎯 Objectif

Fournir une base structurée pour démarrer rapidement votre projet tout en vous obligeant à comprendre et adapter les concepts Docker selon vos besoins spécifiques.

## 📋 Contenu du dossier

### 🐳 Configuration Docker
- `docker-compose.template.yml` - Template d'orchestration avec health checks et réseau
- `.env.example` - Variables d'environnement à personnaliser

### 🔐 Sécurité  
- `secrets/db_password.example` - Template pour mot de passe sécurisé

### 🐍 Backend (Python/FastAPI)
- `backend/Dockerfile.template` - Image Docker optimisée pour API Python
- `backend/requirements.txt.template` - Dépendances Python avec alternatives
- `backend/main.py.template` - Code API FastAPI avec endpoints de base

### ⚛️ Frontend (React/Vite)
- `frontend/Dockerfile.template` - Build multi-étapes React optimisé  
- `frontend/package.json.template` - Configuration Vite/React basique

### 📚 Documentation
- `GETTING_STARTED.md` - Guide de démarrage pas à pas
- `PROJECT_CHECKLIST.md` - Checklist de validation complète (65 critères)

## 🚀 Comment utiliser ces templates

### 1. Préparation initiale
```bash
# Dans le répertoire de votre projet
cp templates/docker-compose.template.yml docker-compose.yml
cp templates/.env.example .env
cp templates/secrets/db_password.example secrets/db_password

# Personnalisez vos configurations
nano .env
nano secrets/db_password
```

### 2. Backend
```bash
# Copiez et adaptez les templates backend
mkdir backend
cp templates/backend/* backend/

# Renommez les fichiers
mv backend/Dockerfile.template backend/Dockerfile
mv backend/requirements.txt.template backend/requirements.txt  
mv backend/main.py.template backend/main.py

# Personnalisez selon votre projet
```

### 3. Frontend
```bash
# Copiez et adaptez les templates frontend
mkdir frontend
cp templates/frontend/* frontend/

# Renommez les fichiers
mv frontend/Dockerfile.template frontend/Dockerfile
mv frontend/package.json.template frontend/package.json

# Créez votre app React
cd frontend
npm install
npm create vite . -- --template react
```

### 4. Documentation
```bash
# Copiez les guides
cp templates/GETTING_STARTED.md .
cp templates/PROJECT_CHECKLIST.md .
```

## ✅ Points clés à retenir

### 🔧 À personnaliser obligatoirement
- Nom du projet dans `docker-compose.yml`
- Variables dans `.env` (DB_USER, DB_NAME, etc.)
- Mot de passe dans `secrets/db_password`
- Logique métier dans `backend/main.py`
- Interface utilisateur dans `frontend/src/`

### 🏥 Health checks obligatoires
- Endpoint `/health` sur backend ET frontend
- Configuration `healthcheck` dans docker-compose
- Vérification avec `docker compose ps` → tous `(healthy)`

### 🌐 Réseau Docker obligatoire
- Réseau personnalisé pour communication inter-services
- Pas d'exposition directe de la DB vers l'extérieur
- Variables d'environnement pour configuration réseau

## 💡 Conseils d'utilisation

1. **Commencez par les templates** - Ne partez pas de zéro
2. **Adaptez progressivement** - Modifiez selon vos besoins spécifiques  
3. **Testez fréquemment** - `docker compose up --build` après chaque modification
4. **Suivez la checklist** - Validez chaque critère avant soumission
5. **Documentez vos changements** - Expliquez vos choix techniques

## 🆘 Support

- Consultez `GETTING_STARTED.md` pour le guide détaillé
- Utilisez `PROJECT_CHECKLIST.md` pour l'auto-évaluation
- Référez-vous à l'implémentation complète dans `../` (dossier parent)
- Posez vos questions en cours ou sur le forum ESIEA

## ⚠️ Important

Ces templates sont une **aide au démarrage**, pas une solution complète. Vous devez :
- Comprendre chaque ligne de configuration
- Adapter le code à votre logique métier  
- Implémenter vos fonctionnalités spécifiques
- Respecter toutes les contraintes du projet

**Bon développement ! 🚀**