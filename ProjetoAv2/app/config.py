import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:@localhost/bazar_temtudo')
    SQLALCHEMY_TRACK_MODIFICATIONS = False