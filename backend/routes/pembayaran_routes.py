from flask import Blueprint, jsonify
from models import bayar_tagihan
from flask_jwt_extended import jwt_required, get_jwt_identity

pembayaran_routes = Blueprint('pembayaran_routes', __name__)

@pembayaran_routes.route('/api/pelanggan/bayar/<int:id_tagihan>', methods=['POST'])
@jwt_required()
def bayar(id_tagihan):
    id_pelanggan = get_jwt_identity()
    success = bayar_tagihan(id_tagihan, id_pelanggan)
    
    if success:
        return jsonify(success=True, message="Pembayaran berhasil"), 200
    return jsonify(success=False, message="Pembayaran gagal"), 400
