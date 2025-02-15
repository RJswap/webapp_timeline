// static/js/project/timeline.js

document.addEventListener('DOMContentLoaded', function() {
    const timelineRows = document.querySelectorAll('.timeline-row');
    
    // Créer la barre de toggles
    const streamToggles = document.createElement('div');
    streamToggles.className = 'stream-toggles';
    
    // Créer un toggle pour chaque projet
    timelineRows.forEach((row) => {
        const projectName = row.dataset.projectName;
        const toggleWrapper = document.createElement('div');
        toggleWrapper.className = 'stream-toggle';
        
        // Créer le switch
        const label = document.createElement('label');
        label.className = 'switch';
        
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = true;
        
        const slider = document.createElement('span');
        slider.className = 'slider';
        
        label.appendChild(input);
        label.appendChild(slider);
        
        // Ajouter le label du projet
        const nameLabel = document.createElement('span');
        nameLabel.textContent = projectName;
        
        toggleWrapper.appendChild(label);
        toggleWrapper.appendChild(nameLabel);
        streamToggles.appendChild(toggleWrapper);
        
        // Gestionnaire d'événements pour le toggle
        input.addEventListener('change', function() {
            const isVisible = this.checked;
            toggleRowVisibility(row, isVisible);
            updatePositions();
        });
    });
    
    // Insérer la barre de toggles avant la timeline
    const timelineContainer = document.querySelector('.timeline-container');
    timelineContainer.insertBefore(streamToggles, timelineContainer.querySelector('.timeline-grid'));
    
    function toggleRowVisibility(row, isVisible) {
        if (isVisible) {
            row.classList.remove('hidden');
            row.style.height = '';
            row.style.opacity = '1';
        } else {
            row.classList.add('hidden');
            row.style.height = '0';
            row.style.opacity = '0';
        }
    }
    
    function updatePositions() {
        let currentOffset = 0;
        timelineRows.forEach(row => {
            if (!row.classList.contains('hidden')) {
                currentOffset += row.offsetHeight + 16; // 16px pour le gap
            }
        });
    }

    document.querySelectorAll('.task').forEach(task => {
        const left = task.style.left;
        const width = task.style.width;
        
        console.log(`Task: ${task.textContent.trim()}`);
        console.log(`Position CSS - left: ${left}, width: ${width}`);
        console.log(`Container width: ${task.parentElement.offsetWidth}px`);
        console.log('---');
        
        // Valider visuellement les positions
        task.title = `Position: ${left} | Width: ${width}`;
    });
    
});




document.addEventListener('DOMContentLoaded', function() {
    // Éléments du DOM
    const newProjectModal = document.getElementById('newProjectModal');
    const newTaskModal = document.getElementById('newTaskModal');
    const addProjectBtn = document.getElementById('addProjectBtn');
    const addTaskBtn = document.getElementById('addTaskBtn');
    const projectForm = document.getElementById('newProjectForm');
    const taskForm = document.getElementById('newTaskForm');
    
    // Gestionnaires d'ouverture des modals
    addProjectBtn.addEventListener('click', () => openModal(newProjectModal));
    addTaskBtn.addEventListener('click', async () => {
        await updateProjectSelect();
        openModal(newTaskModal);
    });
    
    // Fermeture des modals
    document.querySelectorAll('.close, .close-modal').forEach(element => {
        element.addEventListener('click', () => {
            newProjectModal.classList.remove('show');
            newTaskModal.classList.remove('show');
        });
    });
    
    // Soumission du formulaire de projet
    projectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(projectForm);
        
        try {
            const response = await fetch('/project/api/projects', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(Object.fromEntries(formData))
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Recharger la page pour afficher le nouveau projet
                window.location.reload();
            } else {
                alert(data.error || 'Erreur lors de la création du projet');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Erreur lors de la création du projet');
        }
    });
    
    // Soumission du formulaire de tâche
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(taskForm);
        const data = Object.fromEntries(formData);
        
        try {
            console.log('Sending task data:', data);
            const response = await fetch('/project/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            console.log('Server response:', result);
            
            if (response.ok) {
                // Fermer le modal
                document.getElementById('newTaskModal').classList.remove('show');
                
                // Recharger la page pour afficher la nouvelle tâche
                window.location.reload();
            } else {
                alert(result.error || 'Erreur lors de la création de la tâche');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Erreur lors de la création de la tâche');
        }
    });
    
    // Validation des dates
    const startDateInput = document.getElementById('taskStartDate');
    const endDateInput = document.getElementById('taskEndDate');
    
    startDateInput.addEventListener('change', () => {
        endDateInput.min = startDateInput.value;
        if (endDateInput.value && endDateInput.value < startDateInput.value) {
            endDateInput.value = startDateInput.value;
        }
    });
    
    // Fonctions utilitaires
    function openModal(modal) {
        modal.classList.add('show');
        // Réinitialiser le formulaire
        const form = modal.querySelector('form');
        if (form) form.reset();
    }
    
    async function updateProjectSelect() {
        const select = document.getElementById('taskProject');
        select.innerHTML = '';
        
        try {
            const response = await fetch('/project/api/projects');
            const data = await response.json();
            
            if (response.ok) {
                data.projects.forEach(project => {
                    const option = document.createElement('option');
                    option.value = project.id;
                    option.textContent = project.name;
                    select.appendChild(option);
                });
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    // Fermer les modals si on clique en dehors
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            e.target.classList.remove('show');
        }
    });
    
    // Initialiser les dates min/max
    const today = new Date().toISOString().split('T')[0];
    startDateInput.min = today;
    endDateInput.min = today;
});