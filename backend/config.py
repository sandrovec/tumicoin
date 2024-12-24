import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY no está configurada. Por favor, configura esta variable de entorno.")

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración del correo
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1', 'yes']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    if not MAIL_USERNAME or not MAIL_PASSWORD:
        raise ValueError("Las credenciales de correo no están configuradas. Por favor, configura MAIL_USERNAME y MAIL_PASSWORD.")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL no está configurada para el entorno de producción.")


# Selecciona automáticamente la configuración según la variable de entorno FLASK_ENV
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

current_config = config_by_name.get(os.environ.get("FLASK_ENV", "development"))

if current_config is None:
    raise ValueError("Configuración inválida para FLASK_ENV.")
