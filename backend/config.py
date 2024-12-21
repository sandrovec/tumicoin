import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///blockchain.db")
    DEBUG = os.environ.get("DEBUG", "False").lower() in ["true", "1", "yes"]
    TOKEN_EXPIRATION = int(os.environ.get("TOKEN_EXPIRATION", 3600))  # En segundos (1 hora)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Selecciona automáticamente la configuración según la variable de entorno FLASK_ENV
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

current_config = config_by_name.get(os.environ.get("FLASK_ENV", "development"))
