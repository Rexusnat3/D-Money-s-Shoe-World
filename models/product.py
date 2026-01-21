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
    
    def __repr__(self):
        return f"Shoe(id={self._id}, name='{self._name}', size={self._size}, color='{self._color}')"

class AthleticShoe(Shoe):
    """Athletic Shoe class - specialized shoe type"""
    
    def __init__(self, name, brand, price, size, stock=0, color='Black', 
                 sport_type='running', product_id=None, image=None):
        """Initialize athletic shoe with sport type"""
        super().__init__(name, brand, price, size, stock, color, 'athletic', product_id, image)
        self._sport_type = sport_type
    
    @property
    def sport_type(self):
        return self._sport_type
    
    def get_display_info(self):
        """Override to add sport-specific information"""
        info = super().get_display_info()
        info.update({
            'sport_type': self._sport_type,
            'category': 'athletic',
            'features': ['High Performance', 'Breathable', 'Durable']
        })
        return info
    
    def calculate_discount(self, percentage):
        """Athletic shoes get additional 5% discount"""
        base_discount = super().calculate_discount(percentage)
        return base_discount * 0.95
    
    def get_attributes(self):
        """Override to include sport type"""
        attrs = super().get_attributes()
        attrs['sport_type'] = self._sport_type
        return attrs
    
    def to_dict(self):
        """Override to include athletic-specific fields"""
        data = super().to_dict()
        data['attributes'] = json.dumps(self.get_attributes())
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create AthleticShoe from dictionary"""
        attributes = data.get('attributes', {})
        if isinstance(attributes, str):
            attributes = json.loads(attributes)
        
        shoe = cls(
            name=data.get('name'),
            brand=data.get('brand'),
            price=data.get('price'),
            size=data.get('size', attributes.get('size', '10')),
            stock=data.get('stock', 0),
            color=data.get('color', attributes.get('color', 'Black')),
            sport_type=attributes.get('sport_type', 'running'),
            product_id=data.get('id')
        )
        return shoe
    
    def __repr__(self):
        return f"AthleticShoe(name='{self._name}', sport_type='{self._sport_type}', size={self._size})"


class CasualShoe(Shoe):
    """Casual Shoe class - specialized shoe type"""
    
    def __init__(self, name, brand, price, size, stock=0, color='Black', 
                 style='sneaker', product_id=None, image=None):
        """Initialize casual shoe with style"""
        super().__init__(name, brand, price, size, stock, color, 'casual', product_id, image)
        self._style = style
    
    @property
    def style(self):
        return self._style
    
    def get_display_info(self):
        """Override to add casual shoe information"""
        info = super().get_display_info()
        info.update({
            'style': self._style,
            'category': 'casual',
            'features': ['Comfortable', 'Versatile', 'Everyday Wear']
        })
        return info
    
    def calculate_discount(self, percentage):
        """Casual shoes standard discount"""
        return super().calculate_discount(percentage)
    
    def get_attributes(self):
        """Override to include style"""
        attrs = super().get_attributes()
        attrs['style'] = self._style
        return attrs
    
    def to_dict(self):
        """Override to include casual-specific fields"""
        data = super().to_dict()
        data['attributes'] = json.dumps(self.get_attributes())
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create CasualShoe from dictionary"""
        attributes = data.get('attributes', {})
        if isinstance(attributes, str):
            attributes = json.loads(attributes)
        
        shoe = cls(
            name=data.get('name'),
            brand=data.get('brand'),
            price=data.get('price'),
            size=data.get('size', attributes.get('size', '10')),
            stock=data.get('stock', 0),
            color=data.get('color', attributes.get('color', 'Black')),
            style=attributes.get('style', 'sneaker'),
            product_id=data.get('id')
        )
        return shoe
    
    def __repr__(self):
        return f"CasualShoe(name='{self._name}', style='{self._style}', size={self._size})"


class FormalShoe(Shoe):
    """Formal Shoe class - specialized shoe type"""
    
    def __init__(self, name, brand, price, size, stock=0, color='Black', 
                 material='leather', product_id=None, image=None):
        """Initialize formal shoe with material"""
        super().__init__(name, brand, price, size, stock, color, 'formal', product_id, image)
        self._material = material
    
    @property
    def material(self):
        return self._material
    
    def get_display_info(self):
        """Override to add formal shoe information"""
        info = super().get_display_info()
        info.update({
            'material': self._material,
            'category': 'formal',
            'features': ['Premium Quality', 'Professional Look', 'Classic Design']
        })
        return info
    
    def calculate_discount(self, percentage):
        """Formal shoes have limited discount (max 10%)"""
        max_discount = min(percentage, 10)
        return super().calculate_discount(max_discount)
    
    def get_attributes(self):
        """Override to include material"""
        attrs = super().get_attributes()
        attrs['material'] = self._material
        return attrs
    
    def to_dict(self):
        """Override to include formal-specific fields"""
        data = super().to_dict()
        data['attributes'] = json.dumps(self.get_attributes())
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create FormalShoe from dictionary"""
        attributes = data.get('attributes', {})
        if isinstance(attributes, str):
            attributes = json.loads(attributes)
        
        shoe = cls(
            name=data.get('name'),
            brand=data.get('brand'),
            price=data.get('price'),
            size=data.get('size', attributes.get('size', '10')),
            stock=data.get('stock', 0),
            color=data.get('color', attributes.get('color', 'Black')),
            material=attributes.get('material', 'leather'),
            product_id=data.get('id')
        )
        return shoe
    
    def __repr__(self):
        return f"FormalShoe(name='{self._name}', material='{self._material}', size={self._size})"

    

    