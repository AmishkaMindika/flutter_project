from flask import Blueprint, request, jsonify
from flask_cors import CORS
from werkzeug.security import check_password_hash
from app.models import create_user, get_user_by_email

auth = Blueprint('auth', __name__)
CORS(auth)  # Enable Cross-Origin Requests

@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if get_user_by_email(email):
        return jsonify({'message': 'User Already Exists'}), 400

    create_user(email, password)
    return jsonify({'message': 'User Registered Successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = get_user_by_email(email)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid Credentials'}), 401

    return jsonify({'message': 'Login Successfully'}), 200
