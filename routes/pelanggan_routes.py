# routes/pelanggan_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.pelanggan import get_all_pelanggan, add_pelanggan, update_pelanggan, delete_pelanggan
from modules.tarif import get_all_tarif   # Assuming you have this function to get all tariffs

pelanggan_bp = Blueprint('pelanggan_bp', __name__)

@pelanggan_bp.route('/manage_customers', methods=['GET', 'POST'])
def manage_customers():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama_pelanggan = request.form['nama_pelanggan']
        alamat = request.form['alamat']
        nomor_kwh = request.form['nomor_kwh']
        id_tarif = request.form['id_tarif']
        add_pelanggan(username, password, nama_pelanggan, alamat, nomor_kwh, id_tarif)
        return redirect(url_for('pelanggan_bp.manage_customers'))

    pelanggan_list = get_all_pelanggan()
    tarif_list = get_all_tarif()
    return render_template('manage_customers.html', pelanggan_list=pelanggan_list, tarif_list=tarif_list)

@pelanggan_bp.route('/update_customer', methods=['POST'])
def update_customer_route():
    id_pelanggan = request.form['id_pelanggan']
    nama_pelanggan = request.form['nama_pelanggan']
    alamat = request.form['alamat']
    nomor_kwh = request.form['nomor_kwh']
    update_pelanggan(id_pelanggan, nama_pelanggan, alamat, nomor_kwh)
    return redirect(url_for('pelanggan_bp.manage_customers'))

@pelanggan_bp.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer_route(id):
    delete_pelanggan(id)
    return redirect(url_for('pelanggan_bp.manage_customers'))