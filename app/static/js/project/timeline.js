// static/js/project/timeline.js

document.addEventListener('DOMContentLoaded', function() {
    const timelineContent = document.querySelector('.timeline-content');
    const projectRows = document.querySelectorAll('.project-row');
    const projectNames = document.querySelectorAll('.project-names .project-name');
    
    // Créer la barre de toggles
    const streamToggles = document.createElement('div');
    streamToggles.className = 'stream-toggles';
    
    // Créer un toggle pour chaque projet
    projectRows.forEach((row, index) => {
        const projectName = projectNames[index].textContent.trim();
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
            toggleProjectVisibility(row, projectNames[index], isVisible);
            updatePositions();
        });
    });
    
    // Insérer la barre de toggles avant la timeline
    const timelineContainer = document.querySelector('.timeline-container');
    timelineContainer.insertBefore(streamToggles, timelineContainer.querySelector('.timeline-grid'));
    
    function toggleProjectVisibility(row, nameElement, isVisible) {
        if (isVisible) {
            row.style.display = 'grid';
            row.style.height = 'auto';
            row.style.opacity = '1';
            nameElement.style.display = 'flex';
            nameElement.style.height = 'auto';
            nameElement.style.opacity = '1';
        } else {
            row.style.display = 'none';
            row.style.height = '0';
            row.style.opacity = '0';
            nameElement.style.display = 'none';
            nameElement.style.height = '0';
            nameElement.style.opacity = '0';
        }
    }
    
    function updatePositions() {
        // Mettre à jour la position des lignes visibles
        let visibleIndex = 0;
        projectRows.forEach((row, index) => {
            if (row.style.display !== 'none') {
                row.style.order = visibleIndex;
                projectNames[index].style.order = visibleIndex;
                visibleIndex++;
            }
        });
    }
});