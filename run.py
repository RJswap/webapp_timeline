from app import create_app, db
from app.services.init_data import init_db_data
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        try:
            logger.info("Dropping all tables...")
            db.drop_all()
            logger.info("Tables dropped successfully")
            
            logger.info("Creating all tables...")
            db.create_all()
            logger.info("Tables created successfully")
            
            logger.info("Initializing database with sample data...")
            init_db_data()
            logger.info("Sample data initialized successfully")
            
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            raise e
        
    logger.info("Starting Flask application...")
    app.run(debug=True)