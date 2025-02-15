from app import create_app, db
from app.services.init_data import init_db_data
import logging
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

# Nom du fichier de la base de données
DB_FILE = 'instance/project_manager.db'

if __name__ == '__main__':
    with app.app_context():
        try:
            # Vérifie si la base de données existe déjà
            db_exists = os.path.exists(DB_FILE)
            
            if not db_exists:
                logger.info("Base de données non trouvée, création initiale...")
                db.create_all()
                logger.info("Tables créées avec succès")
                
                logger.info("Initialisation avec les données de test...")
                init_db_data()
                logger.info("Données de test initialisées avec succès")
            else:
                logger.info("Base de données existante trouvée, conservation des données...")
        
        except Exception as e:
            logger.error(f"Une erreur est survenue : {str(e)}")
            raise e
        
    logger.info("Démarrage de l'application Flask...")
    app.run(debug=True)