import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gold-prediction-secret-key-change-me'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'goldpred.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

