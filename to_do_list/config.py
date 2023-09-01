import os


class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    SECRET_KEY = os.environ["FLASK_SECRET_KEY"]


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["DEVELOPMENT_DATABASE_URL"]


class TestingConfig(Config):
    # create database in Postgres and
    # insert your database URI for testing config
    SQLALCHEMY_DATABASE_URI = os.environ["TESTING_DATABASE_URL"]
    TESTING = True
