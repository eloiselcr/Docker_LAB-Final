-- =============================================================================
-- BACKEND - SCRIPT DE LA BASE DE DONNÉES (PostgreSQL)
-- =============================================================================


-- création de la table 'items' 
CREATE TABLE IF NOT EXISTS items (
    id SERIAL PRIMARY KEY, -- id tâche
    name VARCHAR(100) NOT NULL, -- nom tâche 
    description TEXT, -- description tâche
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- date de création tâche (actuelle)
);

-- pour rechercher une tâche sans avoir à tout parcourir (optimisation)
CREATE INDEX IF NOT EXISTS idx_items_name ON items(name);


-- données initiales (3 tâches d'exemples) 
INSERT INTO items (name, description) VALUES 
    ('Faire le backend', 'Coder les endpoints avec FastAPI'), -- ex tâche 1
    ('Faire la base de données', 'Nettoyer le Dockerfile et le init.sql'), -- ex tâche 2
    ('Tester le tout', 'Vérifier avec le Swagger UI') -- ex tâche 3
ON CONFLICT DO NOTHING;