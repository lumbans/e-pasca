
from flask import Blueprint, request, jsonify
from models import get_tagihan_belum_dibayar, bayar_tagihan
from flask_jwt_extended import jwt_required, get_jwt_identity

tagihan_routes = Blueprint('tagihan_routes', __name__)

@tagihan_routes.route('/api/pelanggan/tagihan/belum-dibayar', methods=['GET'])
@jwt_required()
def get_belum_dibayar():
    id_pelanggan = get_jwt_identity()
    tagihan_data = get_tagihan_belum_dibayar(id_pelanggan)
    return jsonify(tagihan_data)
