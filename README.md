# 👟 D-Money's Shoe World

A comprehensive full-stack e-commerce web application for a shoe store, built with Python Flask backend and modern JavaScript frontend. This project demonstrates advanced Object-Oriented Programming (OOP) concepts, database management, RESTful API design, and JWT authentication.

**Student**: Daniel Rabago  
**Course**: Advanced Coding  
**Date**: January 2026

---

## 📋 Table of Contents

- [Features](#-features)
- [Technologies Used](#️-technologies-used)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [OOP Concepts](#-oop-concepts-demonstrated)
- [Database Schema](#-database-schema)
- [Security](#-security)
- [Screenshots](#-screenshots)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

## ✨ Features

### User Features
- 🔐 **User Authentication** - Secure registration and login with JWT tokens
- 🛍️ **Product Browsing** - View shoes by category (Athletic, Casual, Formal)
- 🛒 **Shopping Cart** - Add, update, and remove items from cart
- 📦 **Order Management** - Place orders and view order history
- 👤 **User Profile** - Manage account information
- 📱 **Responsive Design** - Seamless experience across all devices

### Admin Features
- ➕ **Product Management** - Create, read, update, and delete products
- 📊 **Inventory Control** - Track stock levels for each product
- 👥 **User Management** - View registered users
- 🔒 **Role-Based Access Control** - Admin-only operations protected

### Technical Features
- 🎯 **RESTful API** - Clean, organized API endpoints
- 🔄 **Real-time Updates** - Dynamic content without page refresh
- 💾 **SQLite Database** - Persistent data storage
- 🎨 **Modern UI/UX** - Beautiful, intuitive interface

---

## 🛠️ Technologies Used

### Backend
- **Python 3.13** - Programming language
- **Flask 2.3.3** - Lightweight web framework
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **PyJWT 2.8.0** - JWT token authentication
- **SQLite3** - Embedded database (built-in)
- **Werkzeug 2.3.7** - WSGI utilities and password hashing

### Frontend
- **HTML5** - Semantic markup structure
- **CSS3** - Modern styling with gradients, animations, and flexbox
- **Vanilla JavaScript (ES6+)** - No frameworks, pure JavaScript
- **Fetch API** - Asynchronous HTTP requests

### Development Tools
- **Git** - Version control
- **VS Code** - IDE
- **Unsplash** - Product images CDN
- **Python-docx** - Documentation generation

---

## 📁 Project Structure

```
D-Money-s-Shoe-World/
├── Main.py                    # Flask application entry point
├── config.py                  # Configuration settings
├── db_manager.py              # Database operations and queries
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── generate_documentation.py  # Word doc generator
├── shoe_store_inventory.db    # SQLite database (generated)
│
├── models/                    # Data models (OOP)
│   ├── __init__.py
│   ├── product.py            # Product class hierarchy
│   ├── user.py               # User authentication classes
│   ├── cart.py               # Shopping cart logic
│   └── order.py              # Order management
│
├── templates/                 # HTML templates
│   └── index.html            # Main single-page application
│
└── static/                    # Static assets
    ├── style.css             # Application styles
    └── script.js             # Frontend JavaScript
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd D-Money-s-Shoe-World
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python Main.py
   ```

5. **Access the application**
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

### Default Credentials

The application seeds with sample data on first run:

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Customer Account:**
- Username: `customer`
- Password: `customer123`

---

## 💻 Usage

### For Customers

1. **Register/Login**
   - Create a new account or login with existing credentials
   - JWT token is stored in browser localStorage

2. **Browse Products**
   - View all available shoes
   - Filter by category (Athletic, Casual, Formal)
   - View detailed product information

3. **Shopping Cart**
   - Add products to cart
   - Update quantities
   - Remove items
   - View total price

4. **Place Orders**
   - Checkout with items in cart
   - View order history
   - Track order status

### For Administrators

1. **Login with Admin Account**
   - Use admin credentials to access admin features

2. **Manage Products**
   - Add new products with details
   - Edit existing products
   - Delete products
   - Update inventory stock

3. **View Users**
   - See registered customers
   - Monitor user activity

---

## 🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/register` | Register new user | No |
| POST | `/api/login` | Login and get JWT token | No |

### Product Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/products` | Get all products | No |
| GET | `/api/products/<id>` | Get product by ID | No |
| POST | `/api/products` | Create new product | Admin |
| PUT | `/api/products/<id>` | Update product | Admin |
| DELETE | `/api/products/<id>` | Delete product | Admin |

### Cart Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/cart` | Get user's cart | User |
| POST | `/api/cart` | Add item to cart | User |
| DELETE | `/api/cart/<id>` | Remove item from cart | User |
| PUT | `/api/cart/<id>` | Update cart item quantity | User |

### Order Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/orders` | Create new order | User |
| GET | `/api/orders` | Get user's orders | User |
| GET | `/api/orders/<id>` | Get specific order | User |

### Example API Request

```javascript
// Login example
fetch('http://localhost:5000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'customer',
    password: 'customer123'
  })
})
.then(response => response.json())
.then(data => {
  localStorage.setItem('token', data.token);
});

// Get products with authentication
fetch('http://localhost:5000/api/products', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  }
})
.then(response => response.json())
.then(data => console.log(data));
```

---

## 🎓 OOP Concepts Demonstrated

### 1. **Inheritance**
The project implements class hierarchies demonstrating inheritance:

```python
# Product Hierarchy
Product (Base Class)
├── AthleticShoe
├── CasualShoe
└── FormalShoe

# User Hierarchy
User (Base Class)
├── Customer
└── Admin
```

**Example:**
```python
class Product:
    def __init__(self, name, brand, price, stock=0):
        self._name = name
        self._brand = brand
        self._price = price
        self._stock = stock

class AthleticShoe(Product):
    def __init__(self, name, brand, price, stock=0, sport_type='general'):
        super().__init__(name, brand, price, stock)
        self._sport_type = sport_type
```

### 2. **Encapsulation**
Private attributes with property decorators for controlled access:

```python
class Product:
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)
```

### 3. **Polymorphism**
Method overriding in subclasses:

```python
class Product:
    def to_dict(self):
        return {'name': self._name, 'price': self._price}

class AthleticShoe(Product):
    def to_dict(self):
        data = super().to_dict()
        data['sport_type'] = self._sport_type
        return data
```

### 4. **Abstraction**
Database operations abstracted through `DatabaseManager` class:

```python
class DatabaseManager:
    def add_product(self, product):
        # Implementation details hidden
        pass
    
    def get_product(self, product_id):
        # Implementation details hidden
        pass
```

### 5. **Composition**
Cart and Order objects contain Product objects:

```python
class Cart:
    def __init__(self, user_id):
        self._items = []  # List of CartItem objects
    
class Order:
    def __init__(self, user_id):
        self._items = []  # List of OrderItem objects
```

---

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    role TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Products Table
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    price REAL NOT NULL,
    size TEXT NOT NULL,
    stock INTEGER NOT NULL,
    color TEXT,
    category TEXT NOT NULL,
    attributes TEXT,  -- JSON for category-specific attributes
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Cart Table
```sql
CREATE TABLE cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);
```

---

## 🔒 Security

### Authentication & Authorization
- **JWT Tokens**: Secure token-based authentication
- **Password Hashing**: SHA-256 hashing for password storage
- **Role-Based Access**: Admin and customer role separation
- **Token Decorators**: `@token_required` and `@admin_required` decorators

### Security Best Practices
- **SQL Injection Prevention**: Parameterized queries
- **CORS Protection**: Configured to allow specific origins
- **Input Validation**: Server-side validation of all inputs
- **Secure Headers**: Proper HTTP headers set
- **Environment Variables**: Sensitive data in environment variables

### Example Security Implementation
```python
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], 
                            algorithms=["HS256"])
            current_user = db.get_user_by_id(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated
```

---

## 📸 Screenshots

### Home Page - Product Catalog
![Product Catalog](https://via.placeholder.com/800x400?text=Product+Catalog)

### Shopping Cart
![Shopping Cart](https://via.placeholder.com/800x400?text=Shopping+Cart)

### Admin Dashboard
![Admin Panel](https://via.placeholder.com/800x400?text=Admin+Dashboard)

### Order History
![Order History](https://via.placeholder.com/800x400?text=Order+History)

---

## 🚀 Future Enhancements

Potential features for future development:

- [ ] **Payment Integration** - Stripe or PayPal integration
- [ ] **Email Notifications** - Order confirmation emails
- [ ] **Product Reviews** - Customer rating and review system
- [ ] **Wishlist Feature** - Save products for later
- [ ] **Advanced Search** - Filter by size, color, price range
- [ ] **Product Recommendations** - AI-based suggestions
- [ ] **Order Tracking** - Real-time delivery status
- [ ] **Admin Analytics** - Sales reports and statistics
- [ ] **Social Login** - OAuth integration (Google, Facebook)
- [ ] **Multi-language Support** - Internationalization (i18n)
- [ ] **Mobile App** - React Native or Flutter mobile version
- [ ] **Image Upload** - Allow admins to upload product images

---

## 🐛 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError: No module named 'flask'`**
- Solution: Install dependencies with `pip install -r requirements.txt`

**Issue: Database errors on first run**
- Solution: Delete `shoe_store_inventory.db` and restart application

**Issue: Port 5000 already in use**
- Solution: Change port in `Main.py` or kill process using port 5000

**Issue: CORS errors in browser console**
- Solution: Ensure Flask-CORS is installed and configured properly

---

## 📝 License

This project is created for educational purposes as part of an Advanced Coding course.

**Copyright © 2026 Daniel Rabago**

---

## 👨‍💻 Author

**Daniel Rabago**
- Course: Advanced Coding
- Project: D-Money's Shoe World E-Commerce Platform
- Date: January 2026

---

## 🙏 Acknowledgments

- Flask documentation and community
- Unsplash for product images
- VS Code for development environment
- Advanced Coding course instructors

---

## 📞 Contact & Support

For questions or support regarding this project, please contact through your course platform or raise an issue in the repository.

---

**Made with ❤️ and Python**

