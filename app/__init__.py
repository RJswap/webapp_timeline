from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import DevelopmentConfig

db = SQLAlchemy()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from app.routes import main, project
    app.register_blueprint(main)
    app.register_blueprint(project)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app