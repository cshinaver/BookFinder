import os


class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    # PostgreSQL configuration
    DATABASE_URL = os.environ.get("DATABASE_URL", None)


class DevelopmentConfig(Config):
    # PostgreSQL configuration
    DATABASE_URL = "localhost"
