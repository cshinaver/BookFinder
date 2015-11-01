import os


class Config(object):
    DEBUG = False
    DATABASE_USERNAME = "postgres"
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'

class ProductionConfig(Config):
    # PostgreSQL configuration
    DATABASE_URL = os.environ.get("DATABASE_URL", None)


class DevelopmentConfig(Config):
    DEBUG = True
    # PostgreSQL configuration
    DATABASE_URL = "localhost"
    DATABASE_PASSWORD = "test"
    DATABASE_NAME = "test"
    DATABASE_PORT = 5432

