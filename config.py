import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'postgresql://postgres:@localhost:/'
#heroku_base = 'postgres://pwnanpdbdxhouu:0d0fa27f64c27e6753f00c1022a6360a63f7541d4372cbd6c04e22c651936e5e@ec2-54-227-246-152.compute-1.amazonaws.com:5432/'
#dev_database_name = 'dfluufvoinldmi'
test_database_name = 'travis_ci_test'
database_url = os.getenv('DATABASE_URL')

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'totally_secret')
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    DATABASE_URL = database_url

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    DATABASE_URL = postgres_local_base +  test_database_name

class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'really_secret'
    DEBUG = False
    DATABASE_URL = 'postgresql:///example'
