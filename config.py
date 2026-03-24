class Config:
    """Base config"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development config"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345678@localhost/library_db'


class ProductionConfig(Config):
    """Production config"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345678@localhost/library_db'
