import os
class Config:
    SECRET_KEY = os.inviron.get('SECRET_KEY')
    DATABASE_NAME = 'shoe_store_inventory.db'