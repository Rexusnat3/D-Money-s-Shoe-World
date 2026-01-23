import os
from pathlib import Path

# Resolve project root based on this file's location
BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Store DB file alongside the project (not a hardcoded absolute path)
    DATABASE_NAME = str(BASE_DIR / 'shoe_store_inventory.db')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'