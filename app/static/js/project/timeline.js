// Gestionnaire de la timeline
const TimelineManager = {
    init() {
        this.timelineRows = document.querySelectorAll('.timeline-row');
        this.setupStreamToggles();
        this.validateTaskPositions();
        this.setupProjectButtons();
        this.setupTaskButtons();
        this.calculateTaskPositions();
    },

    setupStreamToggles() {
        const streamToggles = document.createElement('div');
        streamToggles.className = 'stream-toggles';
        
        this.timelineRows.forEach((row) => {
            const toggleWrapper = this.createToggle(row);
            streamToggles.appendChild(toggleWrapper);
        });
        
        const timelineContainer = document.querySelector('.timeline-container');
        timelineContainer.insertBefore(streamToggles, timelineContainer.querySelector('.timeline-grid'));
    },

    setupProjectButtons() {
        // Gérer le bouton "Nouveau Projet"
        const addProjectBtn = document.getElementById('addProjectBtn');
        if (addProjectBtn) {
            addProjectBtn.addEventListener('click', () => {
                ModalManager.openNewProjectModal();
            });
        }

        // Gérer les clics sur les noms de projets
        document.querySelectorAll('.project-name').forEach(projectName => {
            projectName.addEventListener('click', (e) => {
                e.preventDefault();
                const projectId = projectName.closest('.timeline-row').dataset.projectId;
                const projectTitle = projectName.textContent.trim();
                const colorScheme = projectName.closest('.timeline-row').dataset.colorScheme || 'blue';
                ModalManager.openProjectEditModal(projectId, projectTitle, colorScheme);
            });
        });
    },

    createToggle(row) {
        const projectName = row.dataset.projectName;
        const toggleWrapper = document.createElement('div');
        toggleWrapper.className = 'stream-toggle';
        
        const label = document.createElement('label');
        label.className = 'switch';
        
        const input = document.createElement('input');
        input.type = 'checkbox';
        input.checked = true;
        
        const slider = document.createElement('span');
        slider.className = 'slider';
        
        label.appendChild(input);
        label.appendChild(slider);
        
        const nameLabel = document.createElement('span');
        nameLabel.textContent = projectName;
        
        toggleWrapper.appendChild(label);
        toggleWrapper.appendChild(nameLabel);
        
        input.addEventListener('change', () => {
            this.toggleRowVisibility(row, input.checked);
            this.updatePositions();
        });
        
        return toggleWrapper;
    },

    toggleRowVisibility(row, isVisible) {
        if (isVisible) {
            row.classList.remove('hidden');
            row.style.height = '';
            row.style.opacity = '1';
        } else {
            row.classList.add('hidden');
            row.style.height = '0';
            row.style.opacity = '0';
        }
    },

    calculateTaskPositions() {
        document.querySelectorAll('.timeline-row').forEach(row => {
            const tasks = Array.from(row.querySelectorAll('.task'));
            
            // Tri des tâches par date de début
            tasks.sort((a, b) => {
                const aStart = this.getTaskPosition(a).start;
                const bStart = this.getTaskPosition(b).start;
                return aStart - bStart;
            });

            // Initialisation des niveaux
            const levels = [];
            
            tasks.forEach(task => {
                const taskPos = this.getTaskPosition(task);
                let level = 0;

                // Trouver le premier niveau disponible pour la tâche
                while (this.isLevelOccupied(levels, level, taskPos)) {
                    level++;
                }

                // Ajouter la tâche au niveau trouvé
                if (!levels[level]) {
                    levels[level] = [];
                }
                levels[level].push(taskPos);

                // Appliquer la position verticale à la tâche
                task.style.top = `calc(${level} * (var(--task-base-height) + var(--task-margin)))`;
            });

            // Ajuster la hauteur du conteneur de projet
            const projectTasks = row.querySelector('.project-tasks');
            const totalLevels = levels.length;
            projectTasks.style.height = `calc(${totalLevels} * (var(--task-base-height) + var(--task-margin)) + 1rem)`;
        });
    },

    getTaskPosition(taskElement) {
        return {
            start: parseFloat(taskElement.style.left),
            end: parseFloat(taskElement.style.left) + parseFloat(taskElement.style.width),
            element: taskElement
        };
    },

    isLevelOccupied(levels, level, newTask) {
        if (!levels[level]) return false;
        
        return levels[level].some(existingTask => {
            // Vérifier si les tâches se chevauchent
            return !(
                newTask.start >= existingTask.end ||
                newTask.end <= existingTask.start
            );
        });
    },
    
    updatePositions() {
        let currentOffset = 0;
        this.timelineRows.forEach(row => {
            if (!row.classList.contains('hidden')) {
                currentOffset += row.offsetHeight + 16;
            }
        });
    },

    validateTaskPositions() {
        document.querySelectorAll('.task').forEach(task => {
            const left = task.style.left;
            const width = task.style.width;
            task.title = `Position: ${left} | Width: ${width}`;
        });
    },

    setupTaskButtons() {
        // Gestionnaire pour le bouton "Nouvelle Tâche"
        const addTaskBtn = document.getElementById('addTaskBtn');
        if (addTaskBtn) {
            addTaskBtn.addEventListener('click', () => {
                ModalManager.openNewTaskModal();
            });
        }     

        // Gestionnaire pour les tâches existantes
        document.querySelectorAll('.task').forEach(task => {
            task.addEventListener('click', (e) => {
                e.stopPropagation();
                const taskData = {
                    id: task.dataset.taskId,
                    projectId: task.closest('.timeline-row').dataset.projectId,
                    text: task.dataset.taskInfo,
                    comment: task.dataset.comment,
                    startDate: task.dataset.startDate,
                    endDate: task.dataset.endDate,
                    etp: task.dataset.etp
                };
                ModalManager.openEditTaskModal(taskData);
            });
        });
    }
};


// Gestionnaire des modals
const ModalManager = {
    init() {
        this.initElements();
        this.setupEventListeners();
        this.setupTaskHandlers(); 
        this.initializeDateInputs();
    },

    initElements() {
        this.elements = {
            newProjectModal: document.getElementById('newProjectModal'),
            newTaskModal: document.getElementById('newTaskModal'),
            editTaskModal: document.getElementById('editTaskModal'),
            projectForm: document.getElementById('projectForm'),
            taskForm: document.getElementById('newTaskForm'),
            editTaskForm: document.getElementById('editTaskForm'),
            deleteTaskBtn: document.getElementById('deleteTaskBtn'),
            deleteProjectBtn: document.getElementById('deleteProjectBtn'),
            projectModalTitle: document.getElementById('projectModalTitle'),
            submitProjectBtn: document.getElementById('submitProjectBtn'),
            taskProjectSelect: document.getElementById('taskProject'),
            editTaskProjectSelect: document.getElementById('editTaskProject'),
            deleteTaskBtn: document.getElementById('deleteTaskBtn')
        };
    },

    setupEventListeners() {
        // Gestionnaires de fermeture des modals
        document.querySelectorAll('.close, .close-modal').forEach(element => {
            element.addEventListener('click', () => this.closeAllModals());
        });

        // Gestionnaire du formulaire de projet
        if (this.elements.projectForm) {
            this.elements.projectForm.addEventListener('submit', (e) => this.handleProjectSubmit(e));
        }

        // Gestion des formulaires de tâches
        if (this.elements.taskForm) {
            this.elements.taskForm.addEventListener('submit', (e) => this.handleTaskSubmit(e));
        }

        if (this.elements.editTaskForm) {
            this.elements.editTaskForm.addEventListener('submit', (e) => this.handleEditTaskSubmit(e));
        }

        if (this.elements.deleteTaskBtn) {
            this.elements.deleteTaskBtn.addEventListener('click', () => this.handleTaskDelete());
        }

        // Gestionnaire du bouton de suppression de projet
        if (this.elements.deleteProjectBtn) {
            this.elements.deleteProjectBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleProjectDelete();
            });
        }
    },

    setupTaskHandlers() {
        // Assurer que les sélecteurs de projet sont initialisés au démarrage
        this.updateProjectSelect();

        // Gestionnaire pour le bouton "Nouvelle Tâche"
        const addTaskBtn = document.getElementById('addTaskBtn');
        if (addTaskBtn) {
            addTaskBtn.addEventListener('click', () => {
                this.openNewTaskModal();
            });
        }

        // Gestionnaire pour les tâches existantes
        document.querySelectorAll('.task').forEach(task => {
            task.addEventListener('click', (e) => {
                e.stopPropagation();
                const taskData = {
                    id: task.dataset.taskId,
                    projectId: task.closest('.timeline-row').dataset.projectId,
                    text: task.dataset.taskInfo,
                    comment: task.dataset.comment,
                    startDate: task.dataset.startDate,
                    endDate: task.dataset.endDate,
                    etp: task.dataset.etp
                };
                this.openEditTaskModal(taskData);
            });
        });
    },

    openNewProjectModal() {
        const modal = this.elements.newProjectModal;
        if (!modal) return;

        // Reset du formulaire
        this.elements.projectForm.reset();
        document.getElementById('projectId').value = '';
        
        // Mise à jour du titre et des boutons
        this.elements.projectModalTitle.textContent = 'Nouveau Projet';
        this.elements.submitProjectBtn.textContent = 'Créer';
        this.elements.deleteProjectBtn.style.display = 'none';

        modal.classList.add('show');
    },

    openProjectEditModal(projectId, projectName, colorScheme) {
        const modal = this.elements.newProjectModal;
        if (!modal) return;

        // Mise à jour du titre
        this.elements.projectModalTitle.textContent = 'Modifier le Projet';

        // Remplissage du formulaire
        document.getElementById('projectId').value = projectId;
        document.getElementById('projectName').value = projectName;
        document.getElementById('colorScheme').value = colorScheme;

        // Affichage du bouton de suppression et mise à jour du bouton de soumission
        this.elements.deleteProjectBtn.style.display = 'block';
        this.elements.submitProjectBtn.textContent = 'Modifier';

        modal.classList.add('show');
    },

    async handleProjectSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.elements.projectForm);
        const projectId = document.getElementById('projectId').value;
        const method = projectId ? 'PUT' : 'POST';
        const url = projectId ? `/project/api/projects/${projectId}` : '/project/api/projects';

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(Object.fromEntries(formData))
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Erreur lors de l\'opération sur le projet');
            }

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    },

    async handleProjectDelete() {
        const projectId = document.getElementById('projectId').value;
        const projectName = document.getElementById('projectName').value;

        if (confirm(`Êtes-vous sûr de vouloir supprimer le projet "${projectName}" ?\nCette action supprimera également toutes les tâches associées.`)) {
            try {
                const response = await fetch(`/project/api/projects/${projectId}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Erreur lors de la suppression du projet');
                }

                window.location.reload();
            } catch (error) {
                console.error('Error:', error);
                alert(error.message);
            }
        }
    },

    initializeDateInputs() {
        const dateInputs = document.querySelectorAll('input[type="date"]');
        const today = new Date().toISOString().split('T')[0];
        
        dateInputs.forEach(input => {
            input.min = today;
            
            // Pour les inputs de date de fin, mettre à jour le min quand la date de début change
            if (input.id.includes('End')) {
                const startInput = document.getElementById(input.id.replace('End', 'Start'));
                if (startInput) {
                    startInput.addEventListener('change', () => {
                        input.min = startInput.value;
                        if (input.value && input.value < startInput.value) {
                            input.value = startInput.value;
                        }
                    });
                }
            }
        });
    },

    openNewTaskModal() {
        const modal = this.elements.newTaskModal;
        if (!modal) return;

        this.elements.taskForm.reset();
        this.updateProjectSelect();
        modal.classList.add('show');
    },

    openEditTaskModal(taskData) {
        const modal = this.elements.editTaskModal;
        if (!modal) return;

        // Remplir le formulaire avec les données de la tâche
        document.getElementById('editTaskId').value = taskData.id;
        document.getElementById('editTaskProject').value = taskData.projectId;
        document.getElementById('editTaskText').value = taskData.text;
        document.getElementById('editTaskComment').value = taskData.comment || '';
        document.getElementById('editTaskStartDate').value = taskData.startDate;
        document.getElementById('editTaskEndDate').value = taskData.endDate;
        document.getElementById('editTaskEtp').value = taskData.etp;

        modal.classList.add('show');
    },

    async handleTaskSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.elements.taskForm);
        
        try {
            const response = await fetch('/project/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(Object.fromEntries(formData))
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Erreur lors de la création de la tâche');
            }

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    },

    async handleEditTaskSubmit(e) {
        e.preventDefault();
        const formData = new FormData(this.elements.editTaskForm);
        const taskId = formData.get('task_id');
        const newProjectId = formData.get('project_id');
        
        try {
            const response = await fetch(`/project/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    project_id: newProjectId,  // Ajout du project_id dans les données envoyées
                    text: formData.get('text'),
                    comment: formData.get('comment'),
                    start_date: formData.get('start_date'),
                    end_date: formData.get('end_date'),
                    etp: formData.get('etp')
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Erreur lors de la modification de la tâche');
            }

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
        }
    },

    async handleTaskDelete() {
        const taskId = document.getElementById('editTaskId').value;
        const taskText = document.getElementById('editTaskText').value;
        
        if (confirm(`Êtes-vous sûr de vouloir supprimer la tâche "${taskText}" ?`)) {
            try {
                const response = await fetch(`/project/api/tasks/${taskId}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Erreur lors de la suppression de la tâche');
                }

                window.location.reload();
            } catch (error) {
                console.error('Error:', error);
                alert(error.message);
            }
        }
    },

    async updateProjectSelect() {
        try {
            const response = await fetch('/project/api/projects');
            if (!response.ok) throw new Error('Erreur lors de la récupération des projets');
            
            const data = await response.json();
            
            [this.elements.taskProjectSelect, this.elements.editTaskProjectSelect].forEach(select => {
                if (select) {
                    select.innerHTML = '';
                    data.data.projects.forEach(project => {
                        const option = document.createElement('option');
                        option.value = project.id;
                        option.textContent = project.name;
                        select.appendChild(option);
                    });
                }
            });
        } catch (error) {
            console.error('Error updating project selects:', error);
            alert('Erreur lors de la mise à jour de la liste des projets');
        }
    },

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.classList.remove('show');
        });
    },

    // ... Le reste du code pour la gestion des tâches reste inchangé
};

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    TimelineManager.init();
    ModalManager.init();
});