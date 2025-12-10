# =============================================================================
# 🐍 Backend API Template - FastAPI
# Fichier principal de l'API REST
# =============================================================================

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional

# IMPORTS AJOUTÉS POUR LA BASE DE DONNÉES
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# =============================================================================
# 🚀 INITIALISATION DE L'APPLICATION
# =============================================================================

app = FastAPI(
    title="Microservices Todo App",
    description="API REST pour le projet final ESIEA - Gestion de tâches",
    version="1.0.0"
)

# =============================================================================
# 🌐 CONFIGURATION CORS (OBLIGATOIRE POUR FRONTEND)
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    # On autorise le localhost et le réseau docker
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# 📊 MODÈLES DE DONNÉES (PYDANTIC)
# =============================================================================

# Définition de ce qu'est une Tâche (Item)
class ItemBase(BaseModel):
    name: str               # Titre de la tâche
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    # On ajoute created_at pour l'affichage si besoin, sinon optionnel
    
    class Config:
        from_attributes = True

# =============================================================================
# 🗃️ FONCTION DE CONNEXION (DÉPLACÉE ICI POUR ÊTRE UTILISÉE PLUS BAS)
# =============================================================================

def get_db_connection():
    """
    Connexion à la base de données PostgreSQL
    """
    try:
        # On lit le mot de passe depuis le secret Docker (Sécurité)
        # Si le fichier secret n'existe pas (dev local), on met un mot de passe par défaut
        pwd_path = os.getenv("DB_PASSWORD_FILE", "/run/secrets/db_password")
        if os.path.exists(pwd_path):
            with open(pwd_path, "r") as f:
                password = f.read().strip()
        else:
            password = "password_local_insecure" # Juste pour éviter le crash en test hors docker

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),        # Nom du service dans docker-compose
            database=os.getenv("DB_NAME", "app_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=password,
            cursor_factory=RealDictCursor           # Pour avoir des résultats {clé: valeur}
        )
        return conn
    except Exception as e:
        print(f"Erreur de connexion DB: {e}")
        return None

# =============================================================================
# 🏥 HEALTH CHECK (OBLIGATOIRE)
# =============================================================================

@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint - OBLIGATOIRE pour Docker health check
    """
    return {
        "status": "healthy",
        "service": "backend-api",
        "version": "1.0.0"
    }

# =============================================================================
# 🔧 ENDPOINTS DE BASE
# =============================================================================

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint racine - Information sur l'API
    """
    return {
        "message": "Bienvenue sur votre API microservices",
        "project": "ESIEA Final Project",
        "docs": "/docs"
    }

# =============================================================================
# 📝 ENDPOINTS CRUD (IMPLÉMENTATION RÉELLE)
# =============================================================================

# 1. POST : Créer une tâche
@app.post("/items/", response_model=Item, tags=["Items"])
def create_item(item: ItemCreate):
    """
    Créer un nouvel élément (POST) - Enregistre en base de données
    """
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cur = conn.cursor()
        # Requete SQL d'insertion
        query = "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id, name, description;"
        cur.execute(query, (item.name, item.description))
        
        new_item = cur.fetchone() # Récupère l'objet créé
        conn.commit()             # Valide la transaction
        cur.close()
        conn.close()
        
        return new_item
    except Exception as e:
        conn.rollback() # Annule en cas d'erreur
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# 2. GET : Lire les tâches
@app.get("/items/", response_model=List[Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100):
    """
    Récupérer la liste des éléments (GET) - Lit depuis la base de données
    """
    conn = get_db_connection()
    if conn is None:
        # En cas d'erreur de connexion, on renvoie une liste vide pour ne pas casser le front
        print("Database not accessible")
        return []
    
    try:
        cur = conn.cursor()
        # Requete SQL de sélection
        cur.execute("SELECT id, name, description FROM items ORDER BY id DESC LIMIT %s OFFSET %s;", (limit, skip))
        items = cur.fetchall()
        
        cur.close()
        conn.close()
        return items
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# 3. DELETE : Supprimer une tâche
@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int):
    """
    Supprimer un élément (DELETE) - Supprime de la base de données
    """
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cur = conn.cursor()
        # Requete SQL de suppression
        cur.execute("DELETE FROM items WHERE id = %s RETURNING id;", (item_id,))
        deleted_item = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        
        if deleted_item is None:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
            
        return {"message": f"Item {item_id} supprimé avec succès"}
    except HTTPException as he:
        raise he
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# 🚀 POINT D'ENTRÉE
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)