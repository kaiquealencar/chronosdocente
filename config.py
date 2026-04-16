import os
from dotenv import load_dotenv

load_dotenv()

class Config:    
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-de-seguranca")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'sandbox.smtp.mailtrap.io')
    MAIL_PORT = int(os.getenv('MAIL_PORT')    
    MAIL_USE_TLS = True  
    MAIL_USE_SSL = False 
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = "no-reply@chronosdocente.com.br"

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):   
    DEBUG = False   

config = {
    'development': DevConfig,
    'production': ProdConfig,
    'default': DevConfig
}


    

