# routes/tagihan_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.utilities import get_db_connection
from modules.tagihan import get_all_tagihan, manage_tagihan, get_tagihan_pelanggan_list, add_tagihan, update_tagihan, delete_tagihan
from modules.pelanggan import get_all_pelanggan  # Assuming you have this function for fetching pelanggan

tagihan_bp = Blueprint('tagihan_bp', __name__)

@tagihan_bp.route('/manage_tagihan', methods=['GET', 'POST'])
def manage_tagihan():
    if request.method == 'POST':
        id_pelanggan = request.form['id_pelanggan']
        bulan = request.form['bulan']
        tahun = request.form['tahun']
        jumlah_meter = request.form['jumlah_meter']
        add_tagihan(id_pelanggan, bulan, tahun, jumlah_meter)
        return redirect(url_for('tagihan_bp.manage_tagihan'))

    tagihan_list = get_all_tagihan()
    pelanggan_list = get_all_pelanggan()
    return render_template('manage_tagihan.html', tagihan_list=tagihan_list, pelanggan_list=pelanggan_list)

@tagihan_bp.route('/tagihan_pelanggan', methods=['GET', 'POST'])
def tagihan_pelanggan_route():
    if request.method == 'POST':
        # Fetch data from the form
        id_pelanggan = request.form.get('id_pelanggan')
        nama_pelanggan = request.form.get('nama_pelanggan')
        bulan = request.form.get('bulan')
        tahun = request.form.get('tahun')
        jumlah_meter = request.form.get('jumlah_meter')
        tarifperkwh = request.form.get('tarifperkwh')

        # Calculate the total tagihan
        total_tagihan = (int(jumlah_meter) * float(tarifperkwh)) + 2500
        
        # Call the function to add this data to your database
        add_tagihan_pelanggan(id_pelanggan, nama_pelanggan, bulan, tahun, jumlah_meter, tarifperkwh, total_tagihan)
        
        flash('Tagihan pelanggan berhasil ditambahkan.', 'success')
        return redirect(url_for('tagihan_bp.tagihan_pelanggan_route'))

    # For the GET request, retrieve the id_pelanggan from query parameters or session
    id_pelanggan = request.args.get('id_pelanggan') or session.get('id_pelanggan')
    
    # Fetch data to display in the template for the specific pelanggan
    tagihan_pelanggan_list = get_tagihan_pelanggan_list(id_pelanggan)
    
    return render_template('manage_tagihan.html', tagihan_pelanggan_list=tagihan_pelanggan_list)

@tagihan_bp.route('/process_payment', methods=['POST'])
def process_payment():
    # Get the form data
    id_tagihan = request.form.get('id_tagihan')

    # Fetch the tagihan details from the database to calculate total payment
    db = get_db_connection()
    cursor = db.cursor()
    
    # Assuming tarif_per_kwh is stored in a related table (e.g., 'tarif'), join with that table to fetch it
    cursor.execute("""
        SELECT t.id_tagihan, t.bulan, t.tahun, t.jumlah_meter, t.status, p.id_pelanggan, tr.tarifperkwh
        FROM tagihan t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
        LEFT JOIN tarif tr ON p.id_tarif = tr.id_tarif
        WHERE t.id_tagihan = %s AND t.status = 'Belum Bayar'
    """, (id_tagihan,))
    
    tagihan = cursor.fetchone()
    
    if not tagihan:
        flash('Tagihan tidak ditemukan atau sudah dibayar.', 'danger')
        return redirect(url_for('tagihan_bp.tagihan_pelanggan_route'))

    # Extract the values correctly from the result
    id_tagihan, bulan, tahun, jumlah_meter, status, id_pelanggan, tarif_per_kwh = tagihan
    
    # Perform the payment logic
    user_id = session.get('user_id')  # Assuming user_id is stored in the session when logged in
    bayar(id_tagihan, jumlah_meter, tarif_per_kwh, user_id)
    
    flash('Pembayaran berhasil!', 'success')
    return redirect(url_for('tagihan_bp.tagihan_pelanggan_route'))

@tagihan_bp.route('/update_tagihan', methods=['POST'])
def update_tagihan_route():
    id_tagihan = request.form['id_tagihan']
    id_pelanggan = request.form['id_pelanggan']
    bulan = request.form['bulan']
    tahun = request.form['tahun']
    jumlah_meter = request.form['jumlah_meter']
    status = request.form['status']
    update_tagihan(id_tagihan, id_pelanggan, bulan, tahun, jumlah_meter, status)
    return redirect(url_for('tagihan_bp.manage_tagihan'))

@tagihan_bp.route('/delete_tagihan/<int:id>', methods=['POST'])
def delete_tagihan_route(id):
    delete_tagihan(id)
    return redirect(url_for('tagihan_bp.manage_tagihan'))