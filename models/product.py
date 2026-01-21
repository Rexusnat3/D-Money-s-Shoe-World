"""" all the product related models """

from datetime import datetime
import json

from matplotlib import category

class Product:
    """base class for all products"""
    def __init__(self, name, brand, price, stock=0, product_id=None):
        self._id = product_id
        self._name = name
        self._brand = brand
        self._price = float(price)
        self._stock = int(stock)
        self._created_at = datetime.now()

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def brand(self):
        return self._brand
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        self._price
        """Set the price of the product"""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)

    @property 
    def stock(self):
        return self._stock
    
    @stock.setter
    def stock(self, value):
        """Set the stock of the product"""
        if value < 0:
            raise ValueError("Stock cannot be negative")
        self._stock = int(value)

    @property
    def created_at(self):
        return self._created_at
    
    def update_stock(self, quantity):
        """Update stock quantity"""
        self._stock += quantity
        return self._stock
    
    def shoe_in_stock(self):
        """Check if the product is in stock"""
        return self._stock > 0
    
    def get_display_info(self):
        """Get product display information"""
        return {
            'id': self._id,
            'name': self._name,
            'brand': self._brand,
            'price': self._price,
            'stock': self._stock,
            'available': self.shoe_in_stock(),
        }
    
    def get_attributes(self):
        """get product attributes as a dictionary"""
        return{}
    
    def to_dict(self):
        """convert product to dictionary for JSON serialization"""
        return {
            'id': self._id,
            'name': self._name,
            'brand': self._brand,
            'price': self._price,
            'stock': self._stock,
            'created_at': self._created_at.isoformat() if self._created_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """create product instance from dictionary"""
        return cls(
            name=data['name'],
            brand=data['brand'],
            price=float(data['price']),
            stock=int(data.get('stock', 0)),
            product_id=data.get('id')
        )
    
    def __repr__(self):
        return f"<Product id={self._id} name={self._name} brand={self._brand} price=${self._price} stock={self._stock}>"
    
class Shoe(Product):
    """Shoe class inheriting the Product base class"""

    def __init__(self, name, brand, price, size, stock=0, color='Black', 
                 category='casual',product_id=None, image=None):
        super().__init__(name, brand, price, stock, product_id)
        self._size = size
        self._color = color
        self._category = category
        self._image = image

    @property
    def size(self):
        return self._size
    
    @property
    def color(self):
        return self._color
    
    @property
    def category(self):
        return self._category
    
    @property
    def image(self):
        return self._image
    
    def get_display_info(self):
        """Override the base method to include shoe-specific info"""
        info = super().get_display_info()
        info.update({
            'size': self._size,
            'color': self._color,
            'category': self._category,
            'image': self._image,
            'type': 'Shoe'
            })
        return info
    
    def get_attributes(self):
        """Get shoe-specific attributes as a dictionary"""
        return {
            'size': self._size,
            'color': self._color,
            'category': self._category,
            'image': self._image
        }
    
    def to_dict(self):
        """Convert shoe to dictionary for JSON serialization"""
        data = super().to_dict()
        data.update({
            'size': self._size,
            'color': self._color,
            'category': self._category,
            'image': self._image ,
            'attributes': json.dumps(self.get_attributes())
             })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create shoe Object from dictionary"""
        attributes = data.get('attributes', {})
        if isinstance(attributes, str):
            attributes = json.loads(attributes)

        shoe = cls(
            name=data.get('name'),
            brand=data.get('brand'),
            price=float(data.get('price')),
            size=data.get('size', attributes.get('size', '10')),
            stock=int(data.get('stock', 0)),
            color=data.get('color', attributes.get('color', 'Black')),
            category=data.get('category', attributes.get('category', 'casual')),
            product_id=data.get('id'),
            image=data.get('image')
        )
        return shoe

    

    