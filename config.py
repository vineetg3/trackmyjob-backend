#https://pythonise.com/series/learning-flask/flask-configuration-files
#https://github.com/pallets/flask/issues/3307
# class Config(object):
#     #Debug and Testing boolean seem to have no effect
#     DEBUG = True
#     TESTING = False
#     SECRET_KEY = b"F2'\x94\xf0\x9a\x82}\x8f\xd0\x87\xd0\xda;\xa1\xc9J*\xdc\x1b"
#     DATABASE_URI="postgresql://vineet:admin123@localhost:5432/job_project_api"
#     #postgresql://<username>:<password>@<server>:5432/<db_name>
#     SESSION_COOKIE_SECURE = True

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


