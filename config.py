import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DATABASE_NAME = 'shoe_store_inventory.db'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'