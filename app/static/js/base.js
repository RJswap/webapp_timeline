// base.js - Fonctionnalités communes à toute l'application

document.addEventListener('DOMContentLoaded', function() {
    // Configuration des variables globales
    window.APP = {
        config: {
            animationDuration: 300,
            dateFormat: 'DD/MM/YYYY',
            apiEndpoint: '/api'
        }
    };

    // Gestion de la navigation active
    const handleActiveNavigation = () => {
        const currentPath = window.location.pathname;
        document.querySelectorAll('.nav-links a').forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    };

    // Gestion des notifications
    const notifications = {
        container: null,
        
        init() {
            this.container = document.createElement('div');
            this.container.className = 'notifications-container';
            document.body.appendChild(this.container);
        },

        show(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.textContent = message;
            
            this.container.appendChild(notification);
            
            // Animation d'entrée
            setTimeout(() => {
                notification.classList.add('show');
            }, 10);

            // Auto-suppression après 5 secondes
            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => {
                    notification.remove();
                }, 300);
            }, 5000);
        }
    };

    // Gestion du thème
    const themeManager = {
        init() {
            const savedTheme = localStorage.getItem('theme') || 'light';
            this.setTheme(savedTheme);
            
            // Écouteur pour le bouton de changement de thème (si présent)
            const themeToggle = document.querySelector('.theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    const newTheme = document.body.classList.contains('dark-theme') ? 'light' : 'dark';
                    this.setTheme(newTheme);
                });
            }
        },

        setTheme(theme) {
            document.body.classList.remove('light-theme', 'dark-theme');
            document.body.classList.add(`${theme}-theme`);
            localStorage.setItem('theme', theme);
        }
    };

    // Utilitaires pour les dates
    const dateUtils = {
        formatDate(date) {
            return new Intl.DateTimeFormat('fr-FR').format(date);
        },

        formatDateTime(date) {
            return new Intl.DateTimeFormat('fr-FR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            }).format(date);
        }
    };

    // Gestion des formulaires
    const formManager = {
        init() {
            document.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', this.handleSubmit.bind(this));
            });
        },

        handleSubmit(event) {
            const form = event.target;
            
            // Désactiver le bouton submit pendant le traitement
            const submitButton = form.querySelector('[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
            }

            // Réactiver le bouton après le traitement
            setTimeout(() => {
                if (submitButton) {
                    submitButton.disabled = false;
                }
            }, 1000);
        },

        validateForm(form) {
            let isValid = true;
            const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    this.showError(input, 'Ce champ est requis');
                } else {
                    this.clearError(input);
                }
            });

            return isValid;
        },

        showError(input, message) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'form-error';
            errorDiv.textContent = message;
            input.classList.add('error');
            input.parentNode.appendChild(errorDiv);
        },

        clearError(input) {
            input.classList.remove('error');
            const errorDiv = input.parentNode.querySelector('.form-error');
            if (errorDiv) {
                errorDiv.remove();
            }
        }
    };

    // Gestion des erreurs globales
    //window.onerror = function(msg, url, lineNo, columnNo, error) {
        //console.error('Error: ', msg, url, lineNo, columnNo, error);
        //notifications.show('Une erreur est survenue', 'error');
        //return false;
    //};

    // Initialisation des composants
    const init = () => {
        handleActiveNavigation();
        notifications.init();
        themeManager.init();
        formManager.init();
        
        // Exposer les utilitaires globalement
        window.APP = {
            ...window.APP,
            notifications,
            dateUtils,
            formManager
        };
    };

    // Lancer l'initialisation
    init();
});