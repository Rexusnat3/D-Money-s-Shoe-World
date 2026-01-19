#Main.py the main flask application for the rest stop API
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from functools import wraps
from db_manager import DatabaseManager

import jwt
import datetime
import json
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app) #Enable CORS for all routes
db=DatabaseManager()

#initialize the database
db.initialize_database()

### Frontend Routes ###
@app.route('/')
def index():
    """Serve the main frontend page."""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files."""
    return send_from_directory('static', filename)

#authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token =  request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.get_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 401
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if current_user['role'] != 'admin':
            return jsonify({'message': 'Admin access required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

### Authorization Routes ###
@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user."""
    from models.user import User, Admin

    data=request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password required!'}), 400
    
    role = data.get('role', 'customer')

    if role == 'admin':
        user = Admin(data['username'], data['password'], email=data.get('email'))
    else:
        user = User(data['username'], data['password'], email=data.get('email'))

    user_id = db.create_user(user)
    
    if user_id:
        return jsonify({
            'message': 'User registered successfully!',
            'user_id': user_id,
            'role': role
        }), 201
    else:
        return jsonify({'message': 'Username already exists'}), 400
    
@app.route('/api/login', methods=['POST'])
def login():
    """Authenticate user and return token"""
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message':'Username and Password required'}), 400

    user_data = db.authenticate_user(data['username'], data['password'])

    if user_data:
        token = jwt.encode({
            'user_id': user_data['id'],
            'username': user_data['username'],
            'role': user_data['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({
            'message': 'Login successful!',
            'token': token,
            'user': {
                'id': user_data['id'],
                'username': user_data['username'],
                'role': user_data['role']
            }
        }), 200
    else:
        return jsonify({'message': 'Invalid credentials!'}), 401       




@app.route('/shoes', methods=['GET'])
def get_shoes():
    """Get all the shoes in inventory"""
    shoes = db.get_all_shoes()
    return jsonify([shoe.to_dict() for shoe in shoes])

@app.route('/api/shoes', methods=['POST'])
@app.route('/shoes', methods=['POST'])
@token_required
@admin_required
def create_shoe(current_user):
    """add a new Shoe type to the inventory (Admin only)"""
    from models.product import Shoe, AthleticShoe, CasualShoe, FormalShoe
    
    data = request.get_json()

    if not data or not data.get('name') or not data.get('price'):
        return jsonify({'message': 'Name and price are required'}), 400

    try:
        shoe_type = data.get('category', 'casual')
        
        # Create appropriate shoe type based on category
        if shoe_type == 'athletic':
            shoe = AthleticShoe(
                name=data['name'],
                brand=data.get('brand', 'Unknown'),
                price=float(data['price']),
                size=data.get('size', '10'),
                stock=int(data.get('stock', 0)),
                color=data.get('color', 'Black'),
                sport_type=data.get('sport_type', 'general')
            )
        elif shoe_type == 'formal':
            shoe = FormalShoe(
                name=data['name'],
                brand=data.get('brand', 'Unknown'),
                price=float(data['price']),
                size=data.get('size', '10'),
                stock=int(data.get('stock', 0)),
                color=data.get('color', 'Black'),
                material=data.get('material', 'leather')
            )
        else:
            shoe = CasualShoe(
                name=data['name'],
                brand=data.get('brand', 'Unknown'),
                price=float(data['price']),
                size=data.get('size', '10'),
                stock=int(data.get('stock', 0)),
                color=data.get('color', 'Black'),
                style=data.get('style', 'sneaker')
            )
        
        shoe_id = db.add_product(shoe)
        
        if shoe_id:
            return jsonify({
                'message': 'Shoe added successfully!',
                'shoe_id': shoe_id
            }), 201
        else:
            return jsonify({'message': 'Failed to add shoe'}), 500
            
    except (ValueError, KeyError) as e:
        return jsonify({'message': f'Invalid data: {str(e)}'}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)