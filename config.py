from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY')
    MYSQL_HOST = environ.get('MYSQL_HOST')
    MYSQL_USER= environ.get('MYSQL_USER')
    MYSQL_PASSWORD= environ.get('MYSQL_PASSWORD')
    MYSQL_DB= environ.get('MYSQL_DB')

class DevelopmentConfig(Config):
    DEBUG = True 