import os
from dotenv import load_dotenv

load_dotenv()

class Config:    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-de-seguranca")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):   
    DEBUG = False   

config = {
    'development': DevConfig,
    'production': ProdConfig,
    'default': DevConfig
}
    
