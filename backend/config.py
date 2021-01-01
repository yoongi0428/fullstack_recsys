import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.getenv('SECRET_KEY', 'ITS-SECRET')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DEBUG = False

key = Config.SECRET_KEY