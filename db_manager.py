import sqlite3
import json
from config import Config

class DatabaseManager:
    """This class manages all the database operations for my store"""

    def __init__(self):
        self.db_name = Config.DATABASE_NAME

    def get_connection(self):
        """get the database connected"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def initi_db(self):
        """Initialize the database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                pasword_hash TEXT NOT NULL,
                email TEXT,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        
        # Products Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL
                       brand TEXT NOT NULL,
                       price REAL NOT NULL
                       size TEXT NOT NULL
                       stock INTEGER NOT NULL
                       color TEXT,
                       category TEXT NOT NULL,
                       attributes TEXT
                       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )
                       ''')