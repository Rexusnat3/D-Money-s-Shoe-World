from datetime import datetime


class OrderItem:
    """
    OrderItem class representing a single item in an order
    Demonstrates encapsulation
    """
    
    def __init__(self, product_id, product_name, quantity, price, item_id=None):
        """Initialize order item"""
        self._id = item_id
        self._product_id = product_id
        self._product_name = product_name
        self._quantity = int(quantity)
        self._price = float(price)
    
    @property
    def id(self):
        return self._id
    
    @property
    def product_id(self):
        return self._product_id
    
    @property
    def product_name(self):
        return self._product_name
    
    @property
    def quantity(self):
        return self._quantity
    
    @property
    def price(self):
        return self._price
    
    def get_subtotal(self):
        """Calculate subtotal for this item"""
        return self._quantity * self._price
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self._id,
            'product_id': self._product_id,
            'product_name': self._product_name,
            'quantity': self._quantity,
            'price': self._price,
            'subtotal': self.get_subtotal()
        }
    
    def __repr__(self):
        return f"OrderItem(product='{self._product_name}', qty={self._quantity}, price=${self._price})"

class Order:
    """
    Order class representing a customer order
    Demonstrates OOP with encapsulation and composition
    """
    
    def __init__(self, user_id, order_id=None, status='pending'):
        """Initialize an order"""
        self._id = order_id
        self._user_id = user_id
        self._items = []
        self._total = 0.0
        self._status = status  # pending, processing, completed, cancelled
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
        return self._items.copy()  # Return copy for encapsulation
    
    @property
    def total(self):
        return self._total
    
    @property
    def status(self):
        return self._status
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def updated_at(self):
        return self._updated_at
    
    def add_item(self, order_item):
        """Add an item to the order"""
        if not isinstance(order_item, OrderItem):
            raise TypeError("Item must be an OrderItem instance")
        self._items.append(order_item)
        self._calculate_total()
    
    def remove_item(self, product_id):
        """Remove an item from the order"""
        self._items = [item for item in self._items if item.product_id != product_id]
        self._calculate_total()
    
    def _calculate_total(self):
        """Private method to calculate order total"""
        self._total = sum(item.get_subtotal() for item in self._items)
        self._updated_at = datetime.now()
    
    def update_status(self, new_status):
        """Update order status"""
        valid_statuses = ['pending', 'processing', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        self._status = new_status
        self._updated_at = datetime.now()
    
    def get_item_count(self):
        """Get total number of items"""
        return sum(item.quantity for item in self._items)
    
    def is_empty(self):
        """Check if order is empty"""
        return len(self._items) == 0
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self._id,
            'user_id': self._user_id,
            'items': [item.to_dict() for item in self._items],
            'total': self._total,
            'status': self._status,
            'item_count': self.get_item_count(),
            'created_at': self._created_at.isoformat() if self._created_at else None,
            'updated_at': self._updated_at.isoformat() if self._updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Order from dictionary"""
        order = cls(
            user_id=data.get('user_id'),
            order_id=data.get('id'),
            status=data.get('status', 'pending')
        )
        
        # Restore items if they exist
        if 'items' in data:
            for item_data in data['items']:
                item = OrderItem(
                    product_id=item_data.get('product_id'),
                    product_name=item_data.get('product_name'),
                    quantity=item_data.get('quantity'),
                    price=item_data.get('price'),
                    item_id=item_data.get('id')
                )
                order._items.append(item)
        
        order._total = data.get('total', 0.0)
        
        if data.get('created_at'):
            order._created_at = datetime.fromisoformat(data['created_at'])
        if data.get('updated_at'):
            order._updated_at = datetime.fromisoformat(data['updated_at'])
        
        return order
    
    def __repr__(self):
        return f"Order(id={self._id}, user={self._user_id}, total=${self._total:.2f}, status='{self._status}')"






