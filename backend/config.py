import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración del correo
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'tu_correo@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'tu_contraseña')


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
