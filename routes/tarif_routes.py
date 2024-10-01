# routes/tarif_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from modules.tarif import get_all_tarif, add_tarif, update_tarif, delete_tarif

tarif_bp = Blueprint('tarif_bp', __name__)

@tarif_bp.route('/manage_tarif', methods=['GET', 'POST'])
def manage_tarif():
    if request.method == 'POST':
        # Handle adding or updating a tarif
        daya = request.form.get('daya')
        tarifperkwh = request.form.get('tarifperkwh')
        add_tarif(daya, tarifperkwh)
        return redirect(url_for('tarif_bp.manage_tarif'))
    
    # Fetch all tarif data
    tarif_list = get_all_tarif()  # This function should return data like [(1, 450, 500.00), (2, 900, 1000.00), ...]

    return render_template('manage_tarif.html', tarif_list=tarif_list)

@tarif_bp.route('/add_tarif', methods=['GET', 'POST'])
def add_tarif_route():
    if request.method == 'POST':
        # Handle adding a new tarif
        daya = request.form['daya']
        tarifperkwh = request.form['tarifperkwh']
        add_tarif(daya, tarifperkwh)
        return redirect(url_for('tarif_bp.manage_tarif'))
    
    tarif = all_tarif()
    print("Tarif Data:", tarif)  # Debugging line
    return render_template('manage_tarif.html', tarif=tarif)

@tarif_bp.route('/update_tarif', methods=['POST'])
def update_tarif_route():
    id_tarif = request.form['id_tarif']
    daya = request.form['daya']
    tarifperkwh = request.form['tarifperkwh']
    update_tarif(id_tarif, daya, tarifperkwh)
    return redirect(url_for('tarif_bp.manage_tarif'))

@tarif_bp.route('/delete_tarif/<int:id>', methods=['POST'])
def delete_tarif_route(id):
    delete_tarif(id)
    return redirect(url_for('tarif_bp.manage_tarif'))
