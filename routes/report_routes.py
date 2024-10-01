# routes/report_routes.py
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from modules.reports import get_usage_report, get_payment_history, get_generate_report, get_laporan_pembayaran
from modules.utilities import get_db_connection

report_bp = Blueprint('report_bp', __name__)

@report_bp.route('/generate_report')
def generate_report():
    # Get data from the module
    reports = get_generate_report()
    
    # Pass data to a template or return as needed
    return render_template('generate_report.html', reports=reports)

@report_bp.route('/usage_report', methods=['GET'])
def usage_report():
    pelanggan = request.args.get('pelanggan', '').strip()
    bulan = request.args.get('bulan', '').strip()
    tahun = request.args.get('tahun', '').strip()
    
    usage_records = get_usage_report(pelanggan, bulan, tahun)
    return render_template('usage_report.html', usage_records=usage_records)

@report_bp.route('/payment_history', methods=['GET'])
def payment_history():
    if 'user_id' in session:
        history = get_payment_history(session['user_id'])
        return render_template('payment_history.html', history=history)
    else:
        flash('You need to be logged in to access this page.', 'warning')
        return redirect(url_for('auth_bp.login'))

@report_bp.route('/laporan_pembayaran', methods=['GET'], endpoint='laporan_pembayaran')
def laporan_pembayaran_view():
    # Retrieve filters from the request
    nama_pelanggan = request.args.get('nama_pelanggan', '')
    bulan = request.args.get('bulan', '')
    tahun = request.args.get('tahun', '')

    # Fetch payment report using the correct function
    pembayaran_list = get_laporan_pembayaran(nama_pelanggan, bulan, tahun)

    # Fetch all customer names for the filter dropdown
    db = get_db_connection()
    cursor = db.cursor()
    pelanggan_list_query = "SELECT DISTINCT nama_pelanggan FROM pelanggan"
    cursor.execute(pelanggan_list_query)
    pelanggan_list = [row[0] for row in cursor.fetchall()]
    cursor.close()
    db.close()

    # Return data to the template
    return render_template('laporan_pembayaran.html', pembayaran_list=pembayaran_list, pelanggan_list=pelanggan_list)