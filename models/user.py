"""User Models for D-Money's Shoe World, here we demonstrate Inheritance.
and Polymorphism with different user roles."""

import hashlib
from datetime import datetime

class User:
    """Base User class representing a generic user with common attributes
    and methods."""

    def __init__(self, username, password, email=None, user_id=None, role='customer'):
        self.user_id = user_id
        self._username = username
        self._password_hash = self._hash_password(password)
        self._email = email
        self._role = role
        self._created_at = datetime.now()
    
    #Proprties for encapsulation

    @property
    def id(self):
        """to get the user ID"""
    
        return self.user_id
    @property
    def username(self):
        """to get the username"""
        return self._username
    
    @property
    def password_hash(self):
        """to get the password hash"""
        return self._password_hash
    
    @property
    def email(self):
        """to get the email"""
        return self._email
    
    @property
    def role(self):
        """to get the user role"""
        return self._role
    
    @property
    def created_at(self):
        """to get the account creation timestamp"""
        return self._created_at
    
    def _hash_password(self, password):
        """Hash the password using SHA-256. This demonstrates encapsulation by
        keeping the hashing logic private."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password):
        """verify if the password written by the user matches the one stored by hash"""
        return self._hash_password(password) == self.password_hash
    
    def display_dashboard(self):
        """Display a generic user dashboard which will be overridden by subclasses.
        This demonstrates polymorphism."""
        return {
            'type': 'customer',
            'username': self.username,
            'message':' Welcome to the shop!',
            'features':['Browse Products', 'View Cart', 'Place Orders']
        }
    
    def get_permissions(self):
        """Get the permissions for the user. This method can be overridden by
        subclasses to provide specific permissions."""
        return ['view_products', 'add_to cart', 'place_order', 'view_own_orders']
    
    def to_dict(self):
        """convert user object into a dictionary for JSON serialization"""
        return {
            'id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self._created_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a User object from a dictionary.
        the User is used for deserialization from database records or JSON payloads.
        """
        user = cls.__new__(cls)  # Create an uninitialized instance
        user.user_id = data.get('id')
        user._username = data.get('username')
        user._password_hash = data.get('password_hash')
        user._email = data.get('email')
        user._role = data.get('role', 'customer')
        user._created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else None
        return user
    
    def __repr__(self):
        """string representation of the User object"""
        return f"User(id={self.user_id}, username='{self._username}', role='{self._role}')"

class Admin(User):
    """Admin class inheriting from User,
    with elevated privileges and additional methods.
    this demonstrates inheritance and polymorphism in the code"""

    def __init__(self, username, password, email=None, user_id=None):
        super().__init__(username, password, email, user_id, role='admin')  
        self._admin_level = 'Super' # this is an additional attribute for Admins

    @property
    def admin_level(self):
        return self._admin_level
    
    def display_dashboard(self):
        """Override the parent method to display an 
        admin specific dashboard."""
        return {
            'type': 'admin',
            'username': self.username,
            'message':'Admin Control Panel - D-Money\'s Shoe World',
            'features': [
                'Manage Inventory',
                'View All Orders',
                'Manage Users',
                'Sales Analytics',
                'Product Management',
                'System Settings'
            ],
            'admin_level': self.admin_level
        }
    
    def get_permissions(self):
        """Override to provide admin specific permissions. Polymorphism in action."""
        return [
            'view_products', 'add_to_cart', 'place_order', 'view_own_orders',
            'manage_inventory', 'add_products', 'edit_products', 'delete_products',
            'view_all_orders', 'manage_orders', 'view_analytics',
            'manage_users', 'system_settings'
        ]
    
    def manage_inventory(self, action, product_id=None, **kwargs):
        """Admin only method to manage inventory."""
        return {
            'action': action,
            'product_id': product_id,
            'admin': self._username,
            'timestamp': datetime.now().isoformat(),
            'data': kwargs
        }
    
    def view_analytics(self):
        """Admin-specific method to view sales analytics."""
        return {
            'admin': self._username,
            'report_type': 'Sales Analytics',
            'access_granted': True
        }
    
    def __repr__(self):
        """String representation of the Admin"""
        return f"Admin(id={self.user_id}, username='{self._username}', admin_level='{self._admin_level}')"
    
class Customer(User):
    """Customer class inheriting from User with customer-specific features."""
    def __init__(self, username, password, email=None, user_id=None):
        super().__init__(username, password, email, user_id, role='customer')
        self._loyalty_points = 0  # Additional attribute for Customers
        self._shipping_address = None

    @property
    def loyalty_points(self):
        """Get Loyalte Points"""
        return self._loyalty_points
    
    @property
    def shipping_address(self, address):
        """Get Shipping Address"""
        self._shipping_address = address

    def display_dashboard(self):
        """Override the parent method to display a 
        customer specific dashboard."""
        return { 
            'type': 'customer',
            'username': self._username,
            'message': f'Welcome back, {self._username}!',
            'features': [ 
                'Browse Shoes',
                'My Cart',
                'Order History',
                'Track Orders',
                'My Profile'
            ],
            'loyalty_points': self.loyalty_points
        }
    
    def get_permissions(self):
        """ Override the parent method to provide customer-specific permissions."""
        return [
            'view_products','search_products',
            'add_to_cart','manage_cart',
            'place_order','view_own_orders','track_orders',
            'update_profile', 'view_loyalty_points'
        ]
    
    def add_loyalty_points(self, points):
        """Customer-specific Method to add loyalty points to the customer account."""
        self._loyalty_points += points
        return self._loyalty_points
    
    def redeem_loyalty_points(self, points):
        """method to redeem loyalty points."""
        if points <=self._loyalty_points:
            self._loyalty_points -= points
            return True
        return False
    
    def update_shipping_address(self, address):
        """
        Customer-specific method to update shipping address
        """
        self._shipping_address = address
        return True
    
    def to_dict(self):
        """Override to include customer-specific fields"""
        data = super().to_dict()
        data['loyalty_points'] = self._loyalty_points
        data['shipping_address'] = self._shipping_address
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create Customer object from dictionary"""
        customer = super(Customer, cls).from_dict(data)
        customer._loyalty_points = data.get('loyalty_points', 0)
        customer._shipping_address = data.get('shipping_address')
        return customer
    
    def __repr__(self):
        """String representation of Customer"""
        return f"Customer(id={self.user_id}, username='{self._username}', points={self._loyalty_points})"

