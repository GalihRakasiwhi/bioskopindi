from .default import Config

# setting for development staging
class Development(Config):
    DEBUG=True
    ENV='development'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:bandungbandung@localhost/bioskopindi_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True
