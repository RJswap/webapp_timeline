from datetime import timedelta

class Config:
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project_manager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False