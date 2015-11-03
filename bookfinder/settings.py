import os
import urlparse


class Config(object):
    DEBUG = False
    DATABASE_USERNAME = "postgres"


class ProductionConfig(Config):
    # PostgreSQL configuration
    urlparse.uses_netloc.append("postgres")
    db_url = os.environ.get('DATABASE_URL', None)
    if db_url:
        url = urlparse.urlparse(db_url)
        DATABASE_NAME = url.path[1:]
        DATABASE_USERNAME = url.username
        DATABASE_PASSWORD = url.password
        DATABASE_HOST = url.hostname
        DATABASE_PORT = url.port


class DevelopmentConfig(Config):
    DEBUG = True
    # PostgreSQL configuration
    DATABASE_HOST = "localhost"
    DATABASE_PASSWORD = "test"
    DATABASE_NAME = "test"
    DATABASE_PORT = 5432
