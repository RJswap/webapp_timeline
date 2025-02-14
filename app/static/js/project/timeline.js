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
});