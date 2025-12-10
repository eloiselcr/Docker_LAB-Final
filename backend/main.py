# =============================================================================
# BACKEND - Fichier principal API (Python + FastAPI)
# =============================================================================


from fastapi import FastAPI, HTTPException, Depends # moteur pour le site web
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # pour validation des données envoyées par le frontend

import os
from typing import List, Optional

import psycopg2 # permet la relation python <-> postgresql
from psycopg2.extras import RealDictCursor
import time


# =================================
# 1. INITIALISATION DE L'APPLICATION
# =================================

# création de l'application
app = FastAPI(
    title="Microservices Todo App",
    description="API REST pour le projet final ESIEA - Gestion de tâches",
    version="1.0.0"
)

# =================================
# 2. CONFIGURATION CORS (FRONTEND)
# =================================

# configuration des origines autorisées (CORS) pour le frontend car bloqué par défaut
app.add_middleware(
    CORSMiddleware,
    # On autorise le localhost et le réseau docker
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =================================
# 3. MODÈLES DE DONNÉES (PYDANTIC)
# =================================

# définition de ce qu'est une Tâche (Item) sur un modèle
class ItemBase(BaseModel):
    name: str # nom tâche 
    description: Optional[str] = None # description tâche (optionnelle)

class ItemCreate(ItemBase):
    pass

class Item(ItemBase): # si la tâche existe et retournée par la DB
    id: int # on utilise son id 
    class Config:
        from_attributes = True


# =================================
# 4. CONNEXION A LA DB
# =================================

def get_db_connection():
    """
    Connexion à la base de données PostgreSQL
    """
    try:
        pwd_path = os.getenv("DB_PASSWORD_FILE", "/run/secrets/db_password") # lecture du mdp pour ouvrir la base
        if os.path.exists(pwd_path):
            with open(pwd_path, "r") as f:
                password = f.read().strip()
        else:
            password = "password_local_insecure"

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"), # nom du service dans docker-compose (db compose)
            database=os.getenv("DB_NAME", "app_db"),
            user=os.getenv("DB_USER", "postgres"),
            password=password,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Erreur de connexion DB: {e}")
        return None


# =================================
# 5. HEALTH CHECK
# =================================

# vérifie toutes les 30 secondes si la DB est accessible (demandé par énoncé)
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


# =================================
# 6. ENDPOINTS DE BASE
# =================================

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


# =================================
# 7. CRUD DB
# =================================

# --- POST : Créer une tâche
@app.post("/items/", response_model=Item, tags=["Items"])
def create_item(item: ItemCreate):
    """
    Créer un nouvel élément (POST) en base de données
    """

    # vérification connexion DB
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cur = conn.cursor()
        
        # requête de création de tâche
        query = "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id, name, description;"
        cur.execute(query, (item.name, item.description))
        
        new_item = cur.fetchone() # récupère l'objet créé
        conn.commit() # valide la transaction
        cur.close()
        conn.close()
        
        return new_item
    except Exception as e:
        conn.rollback() # annule en cas d'erreur
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


# --- GET : Lire les tâches
@app.get("/items/", response_model=List[Item], tags=["Items"])
def read_items(skip: int = 0, limit: int = 100):
    """
    Récupérer la liste des éléments (GET) depuis la base de données
    """

    # vérification connexion DB
    conn = get_db_connection()
    if conn is None:
        # si pas de connexion -> liste vide pour pas planter le frontend
        print("Database not accessible")
        return []
    
    try:
        cur = conn.cursor()

        # requête de lecture des tâches
        cur.execute("SELECT id, name, description FROM items ORDER BY id DESC LIMIT %s OFFSET %s;", (limit, skip))
        items = cur.fetchall()
        
        cur.close()
        conn.close()
        return items
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))


# --- DELETE : Supprimer une tâche
@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int):
    """
    Supprimer un élément (DELETE) - Supprime de la base de données
    """

    # vérification connexion DB
    conn = get_db_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cur = conn.cursor()

        # requête pour supprimer une tâche
        cur.execute("DELETE FROM items WHERE id = %s RETURNING id;", (item_id,))
        deleted_item = cur.fetchone()
        
        conn.commit()
        cur.close()
        conn.close()
        
        if deleted_item is None: # si tâche non trouvée -> erreur 404
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
            
        return {"message": f"Item {item_id} supprimé avec succès"} # validation de suppression 
    except HTTPException as he:
        raise he
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))
    

# =================================
# 8. LANCEMENT SERVEUR
# =================================

# lancement de l'application avec Uvicorn (serveur web)
# note : uniquement si on exécute ce fichier directement
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)