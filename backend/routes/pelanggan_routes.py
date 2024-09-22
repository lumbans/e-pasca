from flask import Blueprint, request, jsonify
from models import get_all_pelanggan, add_pelanggan

pelanggan_routes = Blueprint('pelanggan_routes', __name__)

@pelanggan_routes.route('/api/pelanggan', methods=['GET'])
def get_pelanggan():
    pelanggan = get_all_pelanggan()
    return jsonify(pelanggan)

@pelanggan_routes.route('/api/pelanggan', methods=['POST'])
def create_pelanggan():
    data = request.get_json()
    nama_pelanggan = data.get('nama_pelanggan')
    nomor_kwh = data.get('nomor_kwh')
    alamat = data.get('alamat')
    id_tarif = data.get('id_tarif')
    success = add_pelanggan(nama_pelanggan, nomor_kwh, alamat, id_tarif)
    return jsonify(success=success)
