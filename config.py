import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY','secrets976767!')
    SQLALCHEMY_DATABASE_URI = "mysql://gema:Soleil-20G3ma@localhost/campaign"
    SQLALCHEMY_TRACK_MODIFICATIONS = False