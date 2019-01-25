import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://postgres:@localhost:/'
dev_database_name = 'db_ireporter_api'
test_database_name = 'travis_ci_test'

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'totally_secret')
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    DATABASE_URI = postgres_local_base + dev_database_name

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DATABASE_URI = postgres_local_base +  test_database_name

class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'really_secret'
    DEBUG = False
    DATABASE_URI = 'postgresql:///example'
