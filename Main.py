#Main.py - main flask application for D-Money's Shoe World
from flask import Flask, Request, jsonify
from functools import wraps
from db_manager import DatabaseManager

import jwt
import datetime
import json
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = DatabaseManager()

# Initilize the database
db.init_db()

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
        if current_user[role] != 'admin':
            return jsonify({'message': 'Admin access required!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated
        

### Authorization Routes ###
@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message':'Username and Password required'}), 400
    
    role = data.get('role', 'customer')

    if role == 'admin':
        user = Admin(data['username'], data['password'], data.get('email')
    else:
        user = User(data['username'], data['password'], data.get('email')
                    
    user_id = db.create_user(user)

    if user_id:
        return jsonify({
            'message': 'User registered successfully!',
            'user_id': user_id
            'role': role
        }), 201
    else:
        return jsonify({'message': 'Username already exists!'}), 400
        
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
                })), 200
        else:
            return jsonify({'message': 'Invalid credentials!'}), 401

    if db.get_user_by_username(username):
        return jsonify({'message': 'Username already exists!'}), 400

    db.create_user(username, password, email, role)
    return jsonify({'message': 'User registered successfully!'}), 201       




@app.route('/shoes', methods=['Get'])
def get_shoes():
    """Get all the shoes in inventory"""
    shoes = db.get_all_shoes()
    return jsonify([shoe.to_dict() for shoe in shoes])

@app.route('/shoes', methods=['POST'])
def create_shoe():
    """add a new Shoe type to the inventory"""
    data = request.get_json()

    try:
        shoe_type = data.get('type', 'casual')