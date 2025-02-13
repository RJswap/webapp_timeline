// static/js/project/etp_table.js

document.addEventListener('DOMContentLoaded', function() {
    const table = document.querySelector('.etp-table');
    let activeInput = null;

    // Gérer le clic sur une cellule éditable
    document.addEventListener('click', function(e) {
        // Vérifier si on clique sur une cellule éditable ou son contenu
        const cell = e.target.closest('.editable-cell');
        if (!cell) return; // Si on n'a pas cliqué sur une cellule éditable
        if (cell.querySelector('input')) return; // Si la cellule est déjà en mode édition

        // Récupérer la valeur actuelle
        const valueSpan = cell.querySelector('.etp-value');
        const currentValue = valueSpan.textContent.trim();

        // Créer l'input
        const input = document.createElement('input');
        input.type = 'number';
        input.step = '0.1';
        input.min = '0';
        input.value = currentValue;
        input.className = 'etp-input';

        // Cacher la valeur et ajouter l'input
        valueSpan.style.display = 'none';
        cell.appendChild(input);
        input.focus();
        activeInput = input;

        // Sélectionner tout le texte
        input.select();
    });

    // Gérer la validation des modifications
    async function saveChange(cell, newValue) {
        const project = cell.closest('tr').dataset.project;
        const period = cell.dataset.period;

        try {
            const response = await fetch('/project/api/update_etp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    project,
                    period,
                    etp: newValue
                })
            });

            if (!response.ok) throw new Error('Failed to update ETP');

            // Mettre à jour l'affichage
            const valueSpan = cell.querySelector('.etp-value');
            valueSpan.textContent = parseFloat(newValue).toFixed(2);
            valueSpan.style.display = '';
            valueSpan.classList.add('updated');
            
            // Supprimer l'input
            if (cell.querySelector('input')) {
                cell.querySelector('input').remove();
            }

            // Mettre à jour les totaux
            updateTotals();
            
        } catch (error) {
            console.error('Error updating ETP:', error);
            alert('Failed to update ETP');
        }
    }

    // Gérer les touches clavier pendant l'édition
    document.addEventListener('keydown', function(e) {
        if (!activeInput) return;
        
        if (e.key === 'Enter') {
            e.preventDefault();
            const newValue = activeInput.value;
            if (newValue && !isNaN(newValue)) {
                const cell = activeInput.closest('.editable-cell');
                saveChange(cell, newValue);
            }
            activeInput = null;
        } else if (e.key === 'Escape') {
            const cell = activeInput.closest('.editable-cell');
            cell.querySelector('.etp-value').style.display = '';
            activeInput.remove();
            activeInput = null;
        }
    });

    // Gérer la perte de focus
    document.addEventListener('click', function(e) {
        if (activeInput && !activeInput.contains(e.target) && !e.target.closest('.editable-cell')) {
            const newValue = activeInput.value;
            if (newValue && !isNaN(newValue)) {
                const cell = activeInput.closest('.editable-cell');
                saveChange(cell, newValue);
            }
            activeInput = null;
        }
    });

    // Fonction pour mettre à jour tous les totaux
    function updateTotals() {
        // Totaux par période
        const periods = ['2024 Q3-Q4', '2025 Q1-Q2', '2025 Q3-Q4', '2026-2027'];
        
        periods.forEach(period => {
            const cells = table.querySelectorAll(`td[data-period="${period}"] .etp-value`);
            const total = Array.from(cells)
                .reduce((sum, cell) => sum + parseFloat(cell.textContent || 0), 0);
            const totalCell = table.querySelector(`.period-total[data-period="${period}"]`);
            if (totalCell) {
                totalCell.textContent = total.toFixed(2);
                totalCell.classList.add('updated');
            }
        });

        // Totaux par ligne (max ETP)
        const projectRows = table.querySelectorAll('tr[data-project]');
        projectRows.forEach(row => {
            const etpCells = row.querySelectorAll('.etp-value');
            const maxEtp = Array.from(etpCells)
                .reduce((max, cell) => Math.max(max, parseFloat(cell.textContent || 0)), 0);
            const totalCell = row.querySelector('.row-total');
            if (totalCell) {
                totalCell.textContent = maxEtp.toFixed(2);
                totalCell.classList.add('updated');
            }
        });

        // Total général (somme des max ETP)
        const rowTotals = Array.from(table.querySelectorAll('.row-total'))
            .map(cell => parseFloat(cell.textContent || 0));
        const grandTotal = rowTotals.reduce((sum, val) => sum + val, 0);
        const grandTotalCell = table.querySelector('.grand-total');
        if (grandTotalCell) {
            grandTotalCell.textContent = grandTotal.toFixed(2);
            grandTotalCell.classList.add('updated');
        }

        // Retirer les classes 'updated' après l'animation
        setTimeout(() => {
            table.querySelectorAll('.updated').forEach(el => {
                el.classList.remove('updated');
            });
        }, 1000);
    }
});