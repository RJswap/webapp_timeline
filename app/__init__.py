from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import DevelopmentConfig

db = SQLAlchemy()
migrate_manager = Migrate()  # Renommé pour éviter le conflit

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize Flask-Migrate
    migrate_manager.init_app(app, db)
    
    # Register blueprints
    from app.routes import main, project
    app.register_blueprint(main)
    app.register_blueprint(project)
    
    return app