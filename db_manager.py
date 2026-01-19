import sqlite3
import json
from config import Config

class DatabaseManager:
    """This class manages all the database operations for my store"""

    def __init__(self):
        self.db_name = Config.DATABASE_NAME

    def get_connection(self):
        """get the database connected"""
        conn = sqlite3.connect(self.db_name, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize the database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        
        # Products Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       brand TEXT NOT NULL,
                       price REAL NOT NULL,
                       size TEXT NOT NULL,
                       stock INTEGER NOT NULL,
                       color TEXT,
                       category TEXT NOT NULL,
                       attributes TEXT,
                       image TEXT,
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
        conn.close()

    ### USER OPERATIONS ###

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
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def authenticate_user(self, username, password):
        """Authenticate user and return user data"""
        from models.user import User

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            user_dict = dict(row)
            user = User.from_dict(user_dict)
            if user.verify_password(password):
                return user_dict
        
        return None

    ### PRODUCT OPERATIONS ###

    def add_product(self, product):
        """Add a new product to the inventory"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Serialize attributes dictionary to JSON string
        attributes = json.dumps(product.get_attributes())
        image = product.image if hasattr(product, 'image') else None

        cursor.execute('''
            INSERT INTO products (name, brand, price, size, stock, color, category, attributes, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (product.name, product.brand, product.price, product.size, 
              product.stock, product.color, product.category, attributes, image))

        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return product_id

    def get_all_shoes(self):
        """Get all shoes from the inventory"""
        from models.product import Shoe
        
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()
        conn.close()

        shoes = []
        for row in rows:
            shoe_dict = dict(row)
            if shoe_dict.get('attributes'):
                shoe_dict['attributes'] = json.loads(shoe_dict['attributes'])
            shoe = Shoe.from_dict(shoe_dict)
            # Ensure image is set from database
            if 'image' in shoe_dict and shoe_dict['image']:
                shoe._image = shoe_dict['image']
            shoes.append(shoe)
        
        return shoes

    def get_user_by_username(self, username):
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None