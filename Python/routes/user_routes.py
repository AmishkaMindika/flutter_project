from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

def init_user_routes(user_service):
    
    @user_bp.route('/profile', methods=['GET'])
    @jwt_required()
    def get_profile():
        current_user_email = get_jwt_identity()
        
        user = user_service.get_user_profile(current_user_email)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify(user), 200
    
    @user_bp.route('/profile', methods=['PUT'])
    @jwt_required()
    def update_profile():
        current_user_email = get_jwt_identity()
        data = request.get_json()
        
        if not data or not data.get('profile'):
            return jsonify({"error": "Profile data is required"}), 400
            
        success, error = user_service.update_user_profile(
            current_user_email, 
            data['profile']
        )
        
        if not success:
            return jsonify({"error": error}), 404
            
        return jsonify({"message": "Profile updated successfully"}), 200
    
    return user_bp