from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

from config import Config
from routes.auth_routes import init_auth_routes
from routes.user_routes import init_user_routes
from services.auth_service import AuthService
from services.user_service import UserService

def create_app():
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Add a test route right here, after configuring the app
    @app.route('/test', methods=['GET'])
    def test():
        return jsonify({"message": "Test route works!"}), 200

    # Setup JWT
    jwt = JWTManager(app)

    # Connect to MongoDB
    client = MongoClient(Config.MONGO_URI)
    db = client[Config.DB_NAME]

    # Create indexes
    db.users.create_index('email', unique=True)

    # Initialize services
    auth_service = AuthService(db)
    user_service = UserService(db)

    # Register blueprints
    app.register_blueprint(init_auth_routes(auth_service), url_prefix='/api/auth')
    app.register_blueprint(init_user_routes(user_service), url_prefix='/api/user')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)