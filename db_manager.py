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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
        
conn.commit()
conn.close

### USER TABLES ###

"""Function to create a new user"""
def create_user(self, user):
    """Create a new user"""
    try:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO users (username, password_hash, email, role)
            VALUES (?, ?, ?, ?)
        ''', (user.username, user.password_hash, user.email, user.role))

        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        return None
    
def get_user_by_id(self, user_id):
    """Get the user by unique ID"""
    conn = self.get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row =cursor.fetschone()
    conn.close

    if row:
        return dict(row)
    return None

#Function to Authenticate the user and return data
def authenticate_user(self, username, password):
    from models.user import User