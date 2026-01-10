#App.py - main flask application for D-Money's Shoe World
from flask import Flask, Request, jsonify
from functools import wraps

import jwt
import datetime
import json
from config import Config

app = Flask(__name__)
db = Database()

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