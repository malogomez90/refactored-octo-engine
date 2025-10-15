"""
Configuración del proyecto - Variables de entorno y configuración
"""
import os
from typing import Optional


class Config:
    """Configuración base"""
    
    # Bot de Telegram
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '8343722743:AAEmNl5sea6rFotwUKfQqowMEwPFkUjIO6g')
    BOT_USERNAME: str = os.getenv('BOT_USERNAME', 'antiviralbot')
    
    # Flask
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV: str = os.getenv('FLASK_ENV', 'development')
    
    # Base de datos
    DATABASE_URL: str = os.getenv('DATABASE_URL', 'sqlite:///bot.db')
    
    # Webhook
    WEBHOOK_URL: Optional[str] = os.getenv('WEBHOOK_URL', None)
    WEBHOOK_SECRET: str = os.getenv('WEBHOOK_SECRET', 'mi-token-super-secreto-123')
    
    # Servidor
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', 5000))
    
    # Logs
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Admin
    ADMIN_USER_IDS: list = [int(x) for x in os.getenv('ADMIN_USER_IDS', '').split(',') if x.strip()]
    
    @classmethod
    def is_development(cls) -> bool:
        """Verificar si estamos en desarrollo"""
        return cls.FLASK_ENV == 'development'
    
    @classmethod
    def is_production(cls) -> bool:
        """Verificar si estamos en producción"""
        return cls.FLASK_ENV == 'production'
    
    @classmethod
    def get_database_url(cls) -> str:
        """Obtener URL de base de datos con fallback"""
        url = cls.DATABASE_URL
        if url.startswith('postgres://'):
            # Render.com usa postgres:// pero SQLAlchemy necesita postgresql://
            url = url.replace('postgres://', 'postgresql://', 1)
        return url


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    FLASK_ENV = 'production'


# Seleccionar configuración basada en el entorno
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtener configuración actual"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])