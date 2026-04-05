import os


class Config:
    """Base config"""

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///my_mechanic.db',
    )


class DevelopmentConfig(Config):
    """Development config"""

    DEBUG = True


class ProductionConfig(Config):
    """Production config"""

    DEBUG = False


class TestingConfig(Config):
    """Testing config"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    RATELIMIT_ENABLED = False
    CACHE_TYPE = 'NullCache'
    CACHE_NO_NULL_WARNING = True
