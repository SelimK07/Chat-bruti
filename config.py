"""
Configuration file for Flask application.
Separates environment-specific settings.
"""
import os
from datetime import timedelta


class Config:
    """Base configuration"""
    # Flask
    JSON_SORT_KEYS = False
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # API Limits
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1MB max request size
    
    # Conversation limits
    MAX_CONVERSATION_HISTORY = 20
    MAX_MESSAGE_LENGTH = 1000
    MAX_RESPONSE_TOKENS = 300
    

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False


def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'production').lower()
    
    if env == 'development':
        return DevelopmentConfig
    elif env == 'testing':
        return TestingConfig
    else:
        return ProductionConfig
