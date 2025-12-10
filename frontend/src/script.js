// ============================================================
// CONFIGURATION API
// ============================================================
// Attention : Ton backend Python tourne sur le port 8000
// et l'endpoint défini dans app.py est "/items/"
const API_URL = 'http://localhost:8000/items'; 

const statusDiv = document.getElementById('status');
const taskList = document.getElementById('taskList');

// ============================================================
// FONCTIONS UTILITAIRES
// ============================================================

function updateStatus(message, isError = false) {
    statusDiv.innerHTML = `<i class="fas fa-info-circle"></i> ${message}`;
    statusDiv.style.color = isError ? '#e74c3c' : '#aaa';
}

// ============================================================
// 1. CHARGER LES TÂCHES (GET)
// ============================================================
async function loadTasks() {
    try {
        // Note : On ajoute un "/" à la fin car FastAPI est strict sur les slashes
        const response = await fetch(`${API_URL}/`);
        
        if (!response.ok) throw new Error("Erreur Backend");

        const items = await response.json();
        
        taskList.innerHTML = ''; // On vide la liste

        if (items.length === 0) {
            taskList.innerHTML = '<li style="justify-content:center; color:#ccc;">Aucune tâche pour le moment 🎉</li>';
        }

        // Ton API renvoie une liste d'objets : { "id": 1, "name": "Faire les courses", "description": ... }
        items.forEach(item => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${item.name}</span>
                <button onclick="deleteTask(${item.id})" class="delete-btn" title="Supprimer">
                    <i class="fas fa-trash-alt"></i>
                </button>
            `;
            taskList.appendChild(li);
        });
        updateStatus("Connecté au Backend Python (Port 8000)");

    } catch (error) {
        console.error('Erreur:', error);
        updateStatus("Impossible de joindre l'API (Backend éteint ?)", true);
    }
}

// ============================================================
// 2. AJOUTER UNE TÂCHE (POST)
// ============================================================
async function addTask() {
    const input = document.getElementById('taskInput');
    const nameValue = input.value;

    if (!nameValue.trim()) return;

    // Ton modèle Pydantic (ItemCreate) attend : { "name": "...", "description": "..." }
    const payload = {
        name: nameValue,
        description: "Ajouté depuis le Frontend Docker" // Optionnel
    };

    try {
        await fetch(`${API_URL}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        input.value = ''; // Vider le champ
        loadTasks(); // Recharger la liste
    } catch (error) {
        console.error(error);
        updateStatus("Erreur lors de l'ajout", true);
    }
}

// ============================================================
// 3. SUPPRIMER UNE TÂCHE (DELETE)
// ============================================================
async function deleteTask(id) {
    try {
        // Route Python : @app.delete("/items/{item_id}")
        await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        loadTasks();
    } catch (error) {
        console.error(error);
        updateStatus("Erreur lors de la suppression", true);
    }
}

// ============================================================
// ÉVÉNEMENTS
// ============================================================

// Permettre d'ajouter avec la touche "Entrée"
document.getElementById('taskInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') addTask();
});

// Charger au démarrage
loadTasks();