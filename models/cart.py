"""
Cart model for shopping cart functionality
Demonstrates OOP with encapsulation and composition

OOP CONCEPTS DEMONSTRATED IN THIS MODULE:
==========================================

1. ENCAPSULATION:
   - All attributes are PROTECTED (single underscore prefix: _user_id, _items, etc.)
   - Protected attributes are not directly accessible from outside; accessed via @property decorators
   - This prevents unauthorized modification and allows validation/control
   - Example: _quantity is protected, but accessed via cart_item.quantity

2. PROPERTY DECORATORS (@property):
   - Convert methods into read-only attributes for clean access
   - Provides controlled access to protected variables
   - Example: @property def quantity(self) allows item.quantity instead of item.get_quantity()
   - Can add @setter to allow controlled modification with validation

3. COMPOSITION:
   - Cart class CONTAINS CartItem objects (has-a relationship)
   - Cart manages a collection of CartItem instances
   - This is composition: one object contains other objects as parts
   - Dictionary storage: self._items = {product_id: CartItem}

4. DATA VALIDATION:
   - Setter methods validate data before assignment
   - Example: quantity setter raises ValueError if value < 0
   - Ensures data integrity throughout object lifecycle

5. SERIALIZATION/DESERIALIZATION:
   - to_dict() method: Converts objects to dictionary for JSON/database storage
   - from_dict() class method: Reconstructs objects from dictionary data
   - Essential for data persistence and API responses

6. SPECIAL METHODS:
   - __init__: Constructor to initialize object state
   - __repr__: String representation for debugging (appears in print())
   
7. TYPE CONVERSION:
   - float(price): Ensures price is always a float
   - int(quantity): Ensures quantity is always an integer
   - Prevents type errors and ensures data consistency

8. CLASS vs INSTANCE METHODS:
   - Regular methods (def add_item): Operate on instance data
   - @classmethod (def from_dict): Create new instances, work with class itself
   - cls parameter in class methods refers to the class, not instance
"""

from datetime import datetime


class CartItem:
    """
    CartItem class representing a single item in cart
    
    CONCEPTS IN THIS CLASS:
    ---------------------------
    - ENCAPSULATION: All attributes are protected (_product_id, _product_name, etc.)
    - PROPERTY DECORATORS: Clean read access via @property (product_id, quantity, etc.)
    - PROPERTY SETTER: Controlled write access with validation (@quantity.setter)
    - DATA VALIDATION: Setter validates quantity cannot be negative
    - TYPE SAFETY: Enforces float for price, int for quantity
    - SERIALIZATION: to_dict() converts object to dictionary for JSON/database
    
    Protected Attributes:
        _product_id (int): Product identifier
        _product_name (str): Name of the product
        _price (float): Price per unit (always converted to float)
        _quantity (int): Quantity of items (always converted to int, validated >= 0)
    """
    
    def __init__(self, product_id, product_name, price, quantity=1):
        """Initialize cart item"""
        self._product_id = product_id
        self._product_name = product_name
        self._price = float(price)
        self._quantity = int(quantity)
    
    @property
    def product_id(self):
        """
        PROPERTY DECORATOR: Provides read-only access to protected _product_id
        Usage: item.product_id (no parentheses needed, looks like an attribute)
        """
        return self._product_id
    
    @property
    def product_name(self):
        """
        PROPERTY DECORATOR: Provides read-only access to protected _product_name
        """
        return self._product_name
    
    @property
    def price(self):
        """
        PROPERTY DECORATOR: Provides read-only access to protected _price
        """
        return self._price
    
    @property
    def quantity(self):
        """
        PROPERTY DECORATOR: Provides read access to protected _quantity
        Note: This has a setter, so it's readable AND writable (with validation)
        """
        return self._quantity
    
    @quantity.setter
    def quantity(self, value):
        """
        PROPERTY SETTER: Allows controlled modification with validation
        
        Usage: item.quantity = 5  (looks like simple assignment, but runs validation)
        
        Demonstrates:
        - DATA VALIDATION: Checks value >= 0
        - ENCAPSULATION: Direct access to _quantity blocked, must use this setter
        - TYPE SAFETY: Converts to int automatically
        """
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = int(value)
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self._quantity * self._price
    
    def to_dict(self):
        """
        SERIALIZATION: Convert object to dictionary for JSON/database storage
        
        Returns all data in a simple dict format that can be:
        - Converted to JSON for API responses
        - Stored in databases
        - Sent over network
        - Saved to files
        
        Demonstrates data persistence pattern
        """
        return {
            'product_id': self._product_id,
            'product_name': self._product_name,
            'price': self._price,
            'quantity': self._quantity,
            'subtotal': self.get_subtotal()
        }
    
    def __repr__(self):
        """
        SPECIAL METHOD: String representation for debugging
        
        Called when you print() the object or view it in debugger
        Returns a string showing the object's current state
        """
        return f"CartItem(product='{self._product_name}', qty={self._quantity}, price=${self._price})"


class Cart:
    """
    Shopping Cart class
    Demonstrates OOP with encapsulation and data persistence capabilities
    
    OOP CONCEPTS IN THIS CLASS:
    ---------------------------
    1. COMPOSITION: 
       - Cart CONTAINS CartItem objects (has-a relationship)
       - self._items dictionary stores CartItem instances
       - Cart manages the lifecycle of its CartItem objects
    
    2. ENCAPSULATION:
       - All attributes protected: _id, _user_id, _items, _created_at, _updated_at
       - Access controlled through @property decorators
       - Internal state hidden from external manipulation
    
    3. PROPERTY DECORATORS:
       - Read-only access to: id, user_id, created_at, updated_at
       - items property returns COPY of items list (protects internal dictionary)
    
    4. DATA STRUCTURES:
       - Dictionary for efficient lookup: {product_id: CartItem}
       - Allows O(1) time complexity for finding items by product_id
    
    5. SERIALIZATION/DESERIALIZATION:
       - to_dict(): Convert entire cart to dictionary
       - from_dict(): Reconstruct cart from dictionary (class method)
    
    6. BUSINESS LOGIC METHODS:
       - add_item, remove_item, update_quantity, clear
       - get_total, get_item_count, is_empty, has_item
       - Each method maintains data integrity
    
    Protected Attributes:
        _id (int): Cart identifier
        _user_id (int): User who owns this cart
        _items (dict): Dictionary mapping product_id to CartItem objects
        _created_at (datetime): When cart was created
        _updated_at (datetime): Last modification time
    """
    
    def __init__(self, user_id, cart_id=None):
        """Initialize shopping cart for a user"""
        self._id = cart_id
        self._user_id = user_id
        self._items = {}  # Dictionary: product_id -> CartItem
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    @property
    def id(self):
        return self._id
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def items(self):
        """
        Return list of cart items
        
        ENCAPSULATION PROTECTION:
        Returns a COPY of the items list, not the original dictionary
        This prevents external code from modifying the internal _items dictionary
        
        Example:
            cart.items.append(something)  # Won't affect cart._items (it's a copy!)
            Must use cart.add_item() to properly modify cart
        """
        return list(self._items.values())
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def updated_at(self):
        return self._updated_at
    
    def add_item(self, product_id, product_name, price, quantity=1):
        """
        Add item to cart or update quantity if exists
        
        COMPOSITION DEMONSTRATION:
        - Creates CartItem object and stores it in this Cart
        - Cart "has-a" CartItem relationship
        - Cart manages the CartItem lifecycle
        
        BUSINESS LOGIC:
        - If item exists: increment quantity (update)
        - If new item: create new CartItem object (create)
        - Updates modification timestamp
        
        Args:
            product_id: Unique product identifier
            product_name: Display name
            price: Price per unit
            quantity: Number of items to add (default: 1)
        
        Returns:
            CartItem: The added/updated item
        """
        if product_id in self._items:
            # Update quantity if item already in cart
            self._items[product_id].quantity += quantity
        else:
            # Add new item - COMPOSITION: Cart creates and contains CartItem
            cart_item = CartItem(product_id, product_name, price, quantity)
            self._items[product_id] = cart_item
        
        self._updated_at = datetime.now()
        return self._items[product_id]
    
    def remove_item(self, product_id):
        """Remove item from cart"""
        if product_id in self._items:
            del self._items[product_id]
            self._updated_at = datetime.now()
            return True
        return False
    
    def update_quantity(self, product_id, quantity):
        """Update quantity of an item"""
        if product_id in self._items:
            if quantity <= 0:
                self.remove_item(product_id)
            else:
                self._items[product_id].quantity = quantity
                self._updated_at = datetime.now()
            return True
        return False
    
    def clear(self):
        """Clear all items from cart"""
        self._items = {}
        self._updated_at = datetime.now()
    
    def get_total(self):
        """Calculate total price of all items in cart"""
        return sum(item.get_subtotal() for item in self._items.values())
    
    def get_item_count(self):
        """Get total number of items (sum of quantities)"""
        return sum(item.quantity for item in self._items.values())
    
    def is_empty(self):
        """Check if cart is empty"""
        return len(self._items) == 0
    
    def has_item(self, product_id):
        """Check if product is in cart"""
        return product_id in self._items
    
    def get_item(self, product_id):
        """Get specific item from cart"""
        return self._items.get(product_id)
    
    def to_dict(self):
        """
        Convert cart to dictionary for JSON serialization
        
        SERIALIZATION PATTERN:
        - Converts entire cart object graph to dictionary
        - Recursively serializes contained CartItem objects
        - Converts datetime objects to ISO format strings
        - Result can be saved to database or sent as JSON API response
        
        COMPOSITION SERIALIZATION:
        - Calls to_dict() on each CartItem (composition objects serialized too)
        - List comprehension: [item.to_dict() for item in self._items.values()]
        
        Returns:
            dict: Complete cart data ready for JSON/storage
        """
        return {
            'id': self._id,
            'user_id': self._user_id,
            'items': [item.to_dict() for item in self._items.values()],  # Serialize all CartItems
            'total': self.get_total(),
            'item_count': self.get_item_count(),
            'created_at': self._created_at.isoformat() if self._created_at else None,
            'updated_at': self._updated_at.isoformat() if self._updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create Cart from dictionary (for deserialization)
        
        CLASS METHOD (@classmethod):
        - Works with the class itself, not an instance
        - 'cls' parameter refers to the Cart class
        - Used for alternative constructors (factory pattern)
        
        DESERIALIZATION PATTERN:
        - Reconstructs object from stored dictionary data
        - Creates new Cart instance with cls()
        - Recreates all CartItem objects by calling add_item()
        - Restores datetime objects from ISO format strings
        
        Usage:
            saved_data = cart.to_dict()  # Serialize
            restored_cart = Cart.from_dict(saved_data)  # Deserialize
        
        Args:
            data (dict): Dictionary containing cart data
        
        Returns:
            Cart: Fully reconstructed Cart object with all items
        """
        # Create new Cart instance using the class (cls)
        cart = cls(
            user_id=data.get('user_id'),
            cart_id=data.get('id')
        )
        
        # Restore items - recreates all CartItem objects (COMPOSITION)
        if 'items' in data:
            for item_data in data['items']:
                cart.add_item(
                    product_id=item_data.get('product_id'),
                    product_name=item_data.get('product_name'),
                    price=item_data.get('price'),
                    quantity=item_data.get('quantity', 1)
                )
        
        # Restore datetime objects from ISO format strings
        if data.get('created_at'):
            cart._created_at = datetime.fromisoformat(data['created_at'])
        if data.get('updated_at'):
            cart._updated_at = datetime.fromisoformat(data['updated_at'])
        
        return cart
    
    def __repr__(self):
        """
        SPECIAL METHOD: String representation for debugging
        
        Called automatically when:
        - print(cart) is used
        - Object appears in debugger
        - Object is displayed in interactive shell
        
        Returns human-readable summary of cart state
        """
        return f"Cart(user={self._user_id}, items={len(self._items)}, total=${self.get_total():.2f})"
