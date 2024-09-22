
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import get_usage_by_pelanggan

usage_routes = Blueprint('usage_routes', __name__)

@usage_routes.route('/api/pelanggan/usage', methods=['GET'])
@jwt_required()
def get_pelanggan_usage():
    id_pelanggan = get_jwt_identity()
    usage_data = get_usage_by_pelanggan(id_pelanggan)
    return jsonify(usage_data)
