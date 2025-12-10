const API_URL = 'http://localhost:8000/items'; 

const statusDiv = document.getElementById('status');
const taskList = document.getElementById('taskList');

// Gestion de l'affichage du statut (connexion ou erreur)
function updateStatus(message, isError = false) {
    statusDiv.innerHTML = `<i class="fas fa-info-circle"></i> ${message}`;
    statusDiv.style.color = isError ? '#e74c3c' : '#aaa';
}

// Fonction pour récupérer et afficher les taches
async function loadTasks() {
    try {
        const response = await fetch(`${API_URL}/`);
        
        if (!response.ok) throw new Error("Erreur Backend");

        const items = await response.json();
        
        taskList.innerHTML = ''; // On vide la liste avant affichage

        if (items.length === 0) {
            taskList.innerHTML = '<li style="justify-content:center; color:#ccc;">Aucune tâche pour le moment 🎉</li>';
        }

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
        updateStatus("API connectée");

    } catch (error) {
        console.error('Erreur:', error);
        updateStatus("Erreur de connexion API", true);
    }
}

// Fonction pour ajouter une nouvelle tâche
async function addTask() {
    const input = document.getElementById('taskInput');
    const nameValue = input.value;

    if (!nameValue.trim()) return;

    const payload = {
        name: nameValue,
        description: "Ajout via Frontend"
    };

    try {
        await fetch(`${API_URL}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        input.value = ''; 
        loadTasks(); // Rafraîchir la liste
    } catch (error) {
        console.error(error);
        updateStatus("Erreur lors de l'ajout", true);
    }
}

// Fonction pour supprimer une tâche
async function deleteTask(id) {
    try {
        await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        loadTasks();
    } catch (error) {
        console.error(error);
        updateStatus("Erreur lors de la suppression", true);
    }
}

// Ajout avec la touche Entrée
document.getElementById('taskInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') addTask();
});

// Chargement initial
loadTasks();