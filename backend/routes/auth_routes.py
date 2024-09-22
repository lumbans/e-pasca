from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import authenticate_user

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = authenticate_user(username, password)
    
    if user:
        access_token = create_access_token(identity=user['id'])
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401
