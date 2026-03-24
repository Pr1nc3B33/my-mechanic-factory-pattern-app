import os


class Config:
    """Base config"""

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
