#https://pythonise.com/series/learning-flask/flask-configuration-files
#https://github.com/pallets/flask/issues/3307
class Config(object):
    #Debug and Testing boolean seem to have no effect
    DEBUG = True
    TESTING = False
    SECRET_KEY = b"F2'\x94\xf0\x9a\x82}\x8f\xd0\x87\xd0\xda;\xa1\xc9J*\xdc\x1b"
    DATABASE_URI="postgresql://vineet:admin123@localhost:5432/job_project_api"
    #postgresql://<username>:<password>@<server>:5432/<db_name>
    SESSION_COOKIE_SECURE = True

# class ProductionConfig(Config):
#     pass

# class DevelopmentConfig(Config):
#     DEBUG = True
#     DB_NAME = "job_project_api"
#     DB_USERNAME = "vineet"
#     DB_PASSWORD = "admin123"
#     @property
#     def DATABASE_URI(self):
#         return f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost:5432/{DB_NAME}"



