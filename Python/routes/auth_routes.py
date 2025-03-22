from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth', __name__)

def init_auth_routes(auth_service):
    
    @auth_bp.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email and password are required"}), 400
        
        token, error = auth_service.register_user(
            data['email'], 
            data['password'], 
            data.get('profile')
        )
        
        if error:
            return jsonify({"error": error}), 409
            
        return jsonify({"message": "User registered successfully", "token": token}), 201
    
    @auth_bp.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email and password are required"}), 400
        
        token, error = auth_service.login_user(data['email'], data['password'])
        
        if error:
            return jsonify({"error": error}), 401
            
        return jsonify({"token": token}), 200
    
    @auth_bp.route('/logout', methods=['POST'])
    @jwt_required()
    def logout():
        # With JWT, logout is handled client-side
        return jsonify({"message": "Logged out successfully"}), 200
    
    return auth_bp