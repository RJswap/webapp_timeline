from flask import Flask
from config import DevelopmentConfig

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Register blueprints
    from app.routes import main, project
    app.register_blueprint(main.bp)
    app.register_blueprint(project.bp)
    
    return app
