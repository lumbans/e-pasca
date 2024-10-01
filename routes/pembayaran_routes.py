# routes/pembayaran_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from modules.pembayaran import get_unpaid_bills, bayar, get_payment_history as fetch_payment_history

pembayaran_bp = Blueprint('pembayaran_bp', __name__)

# Route to display unpaid bills for the customer
@pembayaran_bp.route('/unpaid_bills', methods=['GET'])
def unpaid_bills():
    user_id = session.get('user_id')
    bills = get_unpaid_bills(user_id)
    return render_template('unpaid_bills.html', bills=bills)

# Route to process a payment
@pembayaran_bp.route('/bayar/<int:id_tagihan>', methods=['POST'])
def process_payment(id_tagihan):
    try:
        # Retrieve form data
        jumlah_meter = request.form.get('jumlah_meter', '').strip()
        tarif_per_kwh = request.form.get('tarif_per_kwh', '').strip()

        # Check if values are provided
        if not jumlah_meter or not tarif_per_kwh:
            flash("Jumlah meter atau tarif per kWh tidak boleh kosong.", "danger")
            return redirect(url_for('tagihan_bp.tagihan_pelanggan_route'))

        # Convert to appropriate numeric types
        jumlah_meter = int(jumlah_meter)
        tarif_per_kwh = float(tarif_per_kwh)

        user_id = session.get('user_id')  # Assuming user_id is stored in session

        # Call the bayar function
        if bayar(id_tagihan, jumlah_meter, tarif_per_kwh, user_id):
            flash("Pembayaran berhasil!", "success")
        else:
            flash("Gagal melakukan pembayaran!", "danger")

    except ValueError as ve:
        # Handle conversion errors
        flash("Data jumlah meter atau tarif per kWh tidak valid.", "danger")
        print(f"Error: {ve}")
    except Exception as e:
        flash("Terjadi kesalahan saat memproses pembayaran.", "danger")
        print(f"Unexpected error: {e}")

    return redirect(url_for('tagihan_bp.tagihan_pelanggan_route'))

@pembayaran_bp.route('/payment_history')
def get_payment_history():
    if 'logged_in' in session and session['user_role'] == 'pelanggan':
        history = fetch_payment_history(session['user_id']) # Use the new module function
        return render_template('payment_history.html', history=history)
    else:
        flash('You need to be logged in as a customer to access this page.', 'warning')
        return redirect(url_for('auth.login'))