-- database/init.sql

-- 1. Création de la table 'items' (Correspond à ton modèle Backend)
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- On a enlevé updated_at pour simplifier
);

-- 2. Optimisation (Bonus pour le rapport technique)
CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);

-- 3. Données de démarrage (Pour ne pas avoir une liste vide au début)
INSERT INTO items (name, description) VALUES 
    ('Faire le backend', 'Coder les endpoints avec FastAPI'),
    ('Faire la base de données', 'Nettoyer le Dockerfile et le init.sql'),
    ('Tester le tout', 'Vérifier avec le Swagger UI')
ON CONFLICT DO NOTHING;