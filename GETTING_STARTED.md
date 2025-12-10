# 🚀 Guide de démarrage rapide - Projet Microservices ESIEA

## 📋 Pré-requis

- Docker et Docker Compose installés
- Git pour le versionnement
- Éditeur de code (VS Code recommandé)

## 🛠️ Installation et configuration

### 1. Préparation des fichiers de configuration

```bash
# Copier les templates vers les fichiers de configuration
cp docker-compose.template.yml docker-compose.yml
cp .env.example .env
cp secrets/db_password.example secrets/db_password

# Personnaliser la configuration
nano .env  # Adapter les variables selon votre projet
nano secrets/db_password  # Changer le mot de passe
```

### 2. Adapter les templates selon votre projet

1. **Backend** : 
   - Copiez `backend/main.py.template` vers `backend/main.py`
   - Copiez `backend/requirements.txt.template` vers `backend/requirements.txt` 
   - Copiez `backend/Dockerfile.template` vers `backend/Dockerfile`
   - Adaptez le code selon votre logique métier

2. **Frontend** :
   - Copiez `frontend/package.json.template` vers `frontend/package.json`
   - Copiez `frontend/Dockerfile.template` vers `frontend/Dockerfile`
   - Créez votre application React dans `frontend/src/`

3. **Docker Compose** :
   - Personnalisez `docker-compose.yml` selon votre stack technique
   - Adaptez les noms de services et variables

### 3. Développement

```bash
# Construction et démarrage de tous les services
docker compose up --build -d

# Vérifier que tous les services sont healthy
docker compose ps

# Voir les logs en temps réel
docker compose logs -f

# Logs d'un service spécifique
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db
```

### 4. Tests des endpoints

```bash
# Health check du backend
curl http://localhost:8000/health

# Health check du frontend  
curl http://localhost:3000/

# Test des endpoints API (à adapter selon votre API)
curl -X GET http://localhost:8000/items/
curl -X POST http://localhost:8000/items/ -H "Content-Type: application/json" -d '{"name":"test","description":"test item"}'
```

## ✅ Checklist de validation

### Architecture Docker ✅
- [ ] `Dockerfile` pour chaque service (backend, frontend, database si custom)
- [ ] `docker-compose.yml` fonctionnel avec réseau personnalisé
- [ ] Variables d'environnement dans `.env`
- [ ] Secrets Docker pour les mots de passe
- [ ] Volumes pour persistance des données

### Health Checks ✅  
- [ ] Endpoint `/health` implémenté sur le backend
- [ ] Health check configuré pour le frontend
- [ ] Configuration `healthcheck` dans docker-compose.yml
- [ ] Commande `docker compose ps` affiche tous les services comme `(healthy)`

### API REST ✅
- [ ] Au moins 3 endpoints implémentés : POST, GET, DELETE
- [ ] Connexion à la base de données fonctionnelle
- [ ] CORS configuré pour permettre les requêtes frontend
- [ ] Documentation API accessible (ex: FastAPI /docs)

### Frontend ✅
- [ ] Interface utilisateur interactive
- [ ] Formulaire pour créer des données (POST)
- [ ] Liste/tableau pour afficher des données (GET)
- [ ] Bouton/action pour supprimer des données (DELETE)
- [ ] Communication avec l'API backend

### Documentation ✅
- [ ] `README.md` avec instructions d'installation
- [ ] Documentation des endpoints API
- [ ] Captures d'écran de l'interface
- [ ] Guide de déploiement

## 🐛 Dépannage

### Problèmes courants

1. **Services pas healthy** :
   ```bash
   docker compose logs [nom_service]
   ```

2. **Erreurs de connexion DB** :
   - Vérifiez les variables d'environnement
   - Vérifiez le mot de passe dans `secrets/db_password`
   - Attendez que la DB soit complètement initialisée

3. **CORS errors** :
   - Vérifiez la configuration CORS dans votre backend
   - Vérifiez l'URL de l'API dans `VITE_API_URL`

4. **Build errors** :
   ```bash
   docker compose build --no-cache
   ```

## 🔗 Accès aux services

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs (si FastAPI)
- **Health checks** : 
  - Backend: http://localhost:8000/health
  - Frontend: http://localhost:3000/

## 📚 Ressources utiles

- [Documentation Docker Compose](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)

---

**Bon développement ! 🚀**