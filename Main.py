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