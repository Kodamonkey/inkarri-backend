from decouple import config

class Config():
    """Base configuration."""
    SECRET_KEY = config('SECRET_KEY')
    
    
class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}