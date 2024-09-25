from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import bcrypt
import csv
import calendar
from io import StringIO, BytesIO
from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'secret_key'

# Database configuration (Make sure this is placed here)
db_config = {
    'host': 'localhost',
    'user': 'root',        # Replace with your MySQL username
    'password': 'example', # Replace with your MySQL password
    'database': 'pembayaran_listrik' # Replace with your actual database name
}

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        
        # Retrieve user information
        cursor.execute("""
            SELECT id_user, username, password, id_level, nama_admin 
            FROM user 
            WHERE username = %s AND password = %s
        """, (username, password))
        user = cursor.fetchone()
        
        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_role'] = 'admin' if user[3] == 1 else 'customer'
            
            # Check the user's level and redirect accordingly
            if user[3] == 1:  # id_level 1 = Admin
                flash('Welcome, Admin!', 'success')
                return redirect(url_for('dashboard'))
            elif user[3] == 2:  # id_level 2 = Customer
                # Retrieve additional customer information if needed
                cursor.execute("SELECT nama_pelanggan, alamat FROM pelanggan WHERE id_pelanggan = %s", (user[0],))
                customer_info = cursor.fetchone()
                if customer_info:
                    session['user_name'] = customer_info[0]
                    session['user_address'] = customer_info[1]
                
                flash('Welcome, Customer!', 'success')
                return redirect(url_for('customer_dashboard'))
        
        else:
            flash('Invalid username or password. Please try again.', 'danger')
        
        cursor.close()
        db.close()

    return render_template('login.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    # Establish a connection to the database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    # Retrieve unpaid bills (status 'Belum Bayar' indicates unpaid)
    cursor.execute("""
        SELECT 
            tagihan.id_tagihan, 
            tagihan.id_penggunaan, 
            tagihan.id_pelanggan,
            penggunaan.meter_awal, 
            penggunaan.meter_ahir, 
            (penggunaan.meter_ahir - penggunaan.meter_awal) AS usage_kwh, 
            tagihan.jumlah_meter,
            tagihan.status
        FROM tagihan 
        JOIN penggunaan ON tagihan.id_penggunaan = penggunaan.id_penggunaan 
        WHERE tagihan.status = 'Belum Bayar'
    """)
    bills = cursor.fetchall()
    
    cursor.close()
    db.close()

    return render_template('dashboard.html', user_name=session['user_name'], bills=bills)

@app.route('/manage_customers', methods=['GET', 'POST'])
def manage_customers():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    # Retrieve all customers
    cursor.execute("SELECT id_pelanggan, nama_pelanggan, alamat, nomor_kwh FROM pelanggan")
    customers = cursor.fetchall()

    # Retrieve all tariffs for the dropdown
    cursor.execute("SELECT id_tarif, daya, tarifperkwh FROM tarif")
    tariffs = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('manage_customers.html', customers=customers, tariffs=tariffs)
    
# Feature: Add Customer
@app.route('/add_customer', methods=['POST'])
def add_customer():
    try:
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')
        nomor_kwh = request.form.get('nomor_kwh')
        nama_pelanggan = request.form.get('nama_pelanggan')
        alamat = request.form.get('alamat')
        id_tarif = request.form.get('id_tarif')

        if not username or not password or not nomor_kwh or not id_tarif:
            flash('Please provide all the required fields.', 'warning')
            return redirect(url_for('manage_customers'))

        # Hash the password for security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Insert the new customer
        cursor.execute("""
            INSERT INTO pelanggan (username, password, nomor_kwh, nama_pelanggan, alamat, id_tarif) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (username, hashed_password, nomor_kwh, nama_pelanggan, alamat, id_tarif))
        
        db.commit()
        cursor.close()
        db.close()
        
        flash('Customer added successfully!', 'success')
        return redirect(url_for('manage_customers'))

    except mysql.connector.Error as e:
        flash(f"Error adding customer: {str(e)}", 'danger')
        return redirect(url_for('manage_customers'))

# Feature: Pengelolaan User
@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if request.method == 'POST':
        # Handle adding or updating user
        username = request.form['username']
        password = request.form['password']
        nama_admin = request.form['nama_admin']
        id_level = request.form['id_level']

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("INSERT INTO user (username, password, nama_admin, id_level) VALUES (%s, %s, %s, %s)", 
                       (username, password, nama_admin, id_level))
        db.commit()
        cursor.close()
        db.close()
        flash('User berhasil ditambahkan!', 'success')
        return redirect(url_for('manage_users'))

    # Retrieve all users
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("SELECT id_user, username, nama_admin, id_level FROM user;")
    users = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('manage_users.html', users=users)

# Route to add a new user
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')
        nama_admin = request.form.get('nama_admin')
        id_level = request.form.get('id_level')

        # Validate if required fields are present
        if not (username and password and nama_admin and id_level):
            flash('All fields are required for adding a user!', 'danger')
            return redirect(url_for('manage_users'))

        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Insert the new user into the database
        cursor.execute("""
            INSERT INTO user (username, password, nama_admin, id_level) 
            VALUES (%s, %s, %s, %s)
        """, (username, password, nama_admin, id_level))
        db.commit()
        
        flash('User added successfully!', 'success')
    except Exception as e:
        flash(f"Error adding user: {str(e)}", 'danger')
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('manage_users'))

# Route to update a user
@app.route('/update_user', methods=['POST'])
def update_user():
    try:
        # Retrieve form data
        id_user = request.form.get('id_user')
        username = request.form.get('username')
        password = request.form.get('password')
        nama_admin = request.form.get('nama_admin')
        id_level = request.form.get('id_level')

        # Validate if required fields are present
        if not (id_user and username and password and nama_admin and id_level):
            flash('All fields are required for updating user!', 'danger')
            return redirect(url_for('manage_users'))
        
        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Update the user information
        cursor.execute("""
            UPDATE user 
            SET username = %s, password = %s, nama_admin = %s, id_level = %s 
            WHERE id_user = %s
        """, (username, password, nama_admin, id_level, id_user))
        db.commit()
        
        flash('User updated successfully!', 'success')
    except Exception as e:
        flash(f"Error updating user: {str(e)}", 'danger')
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('manage_users'))

# Route to delete a user
@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        
        # Delete the user based on the provided ID
        cursor.execute("DELETE FROM user WHERE id_user = %s", (id,))
        db.commit()
        
        flash('User berhasil dihapus!', 'success')
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", 'danger')
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('manage_users'))

# Feature: Pengelolaan Tarif
@app.route('/manage_tariff', methods=['GET', 'POST'])
def manage_tariff():
    if request.method == 'POST':
        # Handle adding or updating tariff
        daya = request.form.get('daya')
        tarifperkwh = request.form.get('tarifperkwh')

        if daya and tarifperkwh:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            cursor.execute("INSERT INTO tarif (daya, tarifperkwh) VALUES (%s, %s)", (daya, tarifperkwh))
            db.commit()
            cursor.close()
            db.close()
            flash('Tarif berhasil ditambahkan!', 'success')
            return redirect(url_for('manage_tariff'))  # Redirect after a successful POST request


    # Retrieve all tariffs (for GET request)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tarif")
    tariffs = cursor.fetchall()  # Fetch the data from the database
    cursor.close()
    db.close()

    return render_template('manage_tariff.html', tariffs=tariffs)

# Route for adding a new tariff
@app.route('/add_tariff', methods=['POST'])
def add_tariff():
    try:
        # Retrieve form data
        daya = request.form.get('daya')
        tarifperkwh = request.form.get('tarifperkwh')

        if daya and tarifperkwh:
            # Connect to the database
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            # Insert the new tariff
            cursor.execute("INSERT INTO tarif (daya, tarifperkwh) VALUES (%s, %s)", (daya, tarifperkwh))
            db.commit()
            cursor.close()
            db.close()
            flash('Tarif berhasil ditambahkan!', 'success')
        else:
            flash('Data tidak lengkap, mohon isi semua kolom.', 'warning')
    except Exception as e:
        flash(f"Error adding tariff: {str(e)}", 'danger')

    return redirect(url_for('manage_tariff'))

# Route for deleting a tariff
@app.route('/delete_tariff/<int:id>', methods=['POST'])
def delete_tariff(id):
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM tarif WHERE id_tarif = %s", (id,))
        db.commit()
        flash('Tarif berhasil dihapus!', 'success')
    except Exception as e:
        flash(f"Error deleting tariff: {str(e)}", 'danger')
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('manage_tariff'))

# Route for updating a tariff
@app.route('/update_tariff', methods=['POST'])
def update_tariff():
    try:
        # Retrieve form data
        id_tarif = request.form.get('id_tarif')
        daya = request.form.get('daya')
        tarifperkwh = request.form.get('tarifperkwh')

        if id_tarif and daya and tarifperkwh:
            # Connect to the database
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            # Update the tariff data
            cursor.execute("""
                UPDATE tarif 
                SET daya = %s, tarifperkwh = %s 
                WHERE id_tarif = %s
            """, (daya, tarifperkwh, id_tarif))
            db.commit()
            cursor.close()
            db.close()
            flash('Tarif berhasil diperbarui!', 'success')
        else:
            flash('Data tidak lengkap, mohon isi semua kolom.', 'warning')
    except Exception as e:
        flash(f"Error updating tariff: {str(e)}", 'danger')

    return redirect(url_for('manage_tariff'))

# Adjust the manage_tagihan route to include the "Nama Pelanggan" dropdown list
@app.route('/manage_tagihan', methods=['GET'])
def manage_tagihan():
    nama_pelanggan = request.args.get('nama_pelanggan', '')
    bulan = request.args.get('bulan', '')
    status = request.args.get('status', '')

    # Construct the query with filters
    query = """
        SELECT t.id_tagihan, p.nama_pelanggan, t.bulan, t.tahun, t.jumlah_meter, t.status, 
               COALESCE(tr.daya, 0) AS daya, COALESCE(tr.tarifperkwh, 0) AS tarifperkwh, 
               COALESCE((t.jumlah_meter * tr.tarifperkwh) + 2500, 0) AS total_tagihan
        FROM tagihan t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
        LEFT JOIN tarif tr ON p.id_tarif = tr.id_tarif
        WHERE 1=1
    """
    params = []

    if nama_pelanggan:
        query += " AND p.nama_pelanggan LIKE %s"
        params.append(nama_pelanggan)
    if bulan:
        query += " AND t.bulan = %s"
        params.append(bulan)
    if status:
        query += " AND t.status = %s"
        params.append(status)

    # Execute the query to fetch tagihan list
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(query, tuple(params))
    tagihan_list = cursor.fetchall()

    # Fetch the list of all unique "Nama Pelanggan" for the dropdown
    cursor.execute("SELECT nama_pelanggan FROM pelanggan")
    pelanggan_list = cursor.fetchall()
    
    cursor.close()
    db.close()

    # Pass 'pelanggan_list' to the template along with 'tagihan_list'
    return render_template('manage_tagihan.html', tagihan_list=tagihan_list, pelanggan_list=pelanggan_list)

# Update Tagihan
@app.route('/update_tagihan', methods=['POST'])
def update_tagihan():
    try:
        # Retrieve the form data
        id_tagihan = request.form.get('id_tagihan')
        id_pelanggan = request.form.get('id_pelanggan')
        bulan = request.form.get('bulan')
        tahun = request.form.get('tahun')
        jumlah_meter = request.form.get('jumlah_meter')
        status = request.form.get('status')

        # Validate form data
        if not (id_tagihan and id_pelanggan and bulan and tahun and jumlah_meter and status):
            flash('Data tidak lengkap. Silakan isi semua kolom.', 'warning')
            return redirect(url_for('manage_tagihan'))

        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Update the tagihan record
        cursor.execute("""
            UPDATE tagihan
            SET id_pelanggan = %s, bulan = %s, tahun = %s, jumlah_meter = %s, status = %s
            WHERE id_tagihan = %s
        """, (id_pelanggan, bulan, tahun, jumlah_meter, status, id_tagihan))

        db.commit()
        cursor.close()
        db.close()

        flash('Tagihan berhasil diperbarui!', 'success')
    except Exception as e:
        flash(f"Terjadi kesalahan saat memperbarui tagihan: {str(e)}", 'danger')
    
    return redirect(url_for('manage_tagihan'))

# Hapus Tagihan
@app.route('/delete_tagihan/<int:id>', methods=['POST'])
def delete_tagihan(id):
    try:
        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Execute delete query
        cursor.execute("DELETE FROM tagihan WHERE id_tagihan = %s", (id,))
        db.commit()

        # Close connections
        cursor.close()
        db.close()

        flash('Tagihan berhasil dihapus!', 'success')
    except Exception as e:
        flash(f"Terjadi kesalahan: {str(e)}", 'danger')
    
    return redirect(url_for('manage_tagihan'))

# Feature: Laporan
@app.route('/generate_report')
def generate_report():
    # Example: Retrieve data for the report
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.nama_pelanggan, t.bulan, t.tahun, t.jumlah_meter, t.status 
        FROM tagihan t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
    """)
    reports = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('report.html', reports=reports)

@app.route('/usage_report')
def usage_report():
    # Retrieve query parameters
    pelanggan = request.args.get('pelanggan', '').strip()
    bulan = request.args.get('bulan', '').strip()
    tahun = request.args.get('tahun', '').strip()

    # Establish a connection to the database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    # Retrieve distinct pelanggan names for the dropdown
    cursor.execute("SELECT DISTINCT nama_pelanggan FROM view_penggunaan_listrik")
    pelanggan_list = cursor.fetchall()

    # Base query
    query = "SELECT * FROM view_penggunaan_listrik WHERE 1=1"
    query_params = []

    # Add filtering conditions if parameters are provided
    if pelanggan:
        query += " AND nama_pelanggan LIKE %s"
        query_params.append(f"%{pelanggan}%")

    if bulan:
        query += " AND bulan = %s"
        query_params.append(bulan)

    if tahun:
        query += " AND tahun = %s"
        query_params.append(tahun)

    # Execute the query with filtering parameters
    cursor.execute(query, query_params)
    usage_records = cursor.fetchall()
    cursor.close()
    db.close()

    # Render the template with the filtered data and query parameters
    return render_template('usage_report.html', usage_records=usage_records, pelanggan_list=pelanggan_list, bulan=bulan, tahun=tahun)

@app.route('/bill_report')
def bill_report():
    # Retrieve all bill records (tagihan)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("""
        SELECT t.id_tagihan, p.nama_pelanggan, t.bulan, t.tahun, t.jumlah_meter, t.status
        FROM tagihan t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
    """)
    bill_records = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('bill_report.html', bill_records=bill_records)

@app.route('/customer_report')
def customer_report():
    # Retrieve all customer records (pelanggan)
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.id_pelanggan, p.username, p.nama_pelanggan, p.nomor_kwh, p.alamat, t.daya
        FROM pelanggan p
        JOIN tarif t ON p.id_tarif = t.id_tarif
    """)
    customer_records = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('customer_report.html', customer_records=customer_records)

@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/customer_dashboard')
def customer_dashboard():
    if 'logged_in' in session and session['user_role'] == 'customer':
        return render_template('customer_dashboard.html', user_name=session['user_name'])
    else:
        flash('Please log in to access your dashboard.', 'warning')
        return redirect(url_for('login'))

@app.route('/view_bills')
def view_bills():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("""
        SELECT tagihan.id_tagihan, tagihan.bulan, tagihan.tahun, tagihan.jumlah_meter, tagihan.status 
        FROM tagihan 
        WHERE tagihan.id_pelanggan = %s
    """, (session['user_id'],))
    bills = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('view_bills.html', bills=bills)

# Example route for customer_bills
# Example route for customer_bills
@app.route('/customer/bills', methods=['GET'])
def customer_bills():
    # Fetch the bill details for the customer from the database
    db = mysql.connector.connect(**db_config)
    try:
        user_id = session.get('user_id')  # Assuming user_id is stored in session
        cursor = db.cursor()
        
        query = """
            SELECT 
                t.id_tagihan, 
                t.bulan, 
                t.tahun, 
                t.jumlah_meter, 
                t.status, 
                (t.jumlah_meter * tr.tarifperkwh + 2500) AS total_tagihan, -- Calculate total including admin fee
                tr.daya, 
                tr.tarifperkwh
            FROM tagihan t
            JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
            JOIN tarif tr ON p.id_tarif = tr.id_tarif
            WHERE p.id_pelanggan = %s
        """
        cursor.execute(query, (user_id,))
        bills = cursor.fetchall()
        
        # Convert month numbers to month names
        bills_with_month_names = [
            (
                bill[0],
                calendar.month_name[bill[1]],  # Convert month number to name
                bill[2],
                bill[3],
                bill[4],
                bill[5],
                bill[6],
                bill[7]
            ) for bill in bills
        ]
        
        return render_template('customer_bills.html', bills=bills_with_month_names)
    except Exception as e:
        flash(f"Error fetching bills: {str(e)}", "danger")
        return redirect(url_for('customer_dashboard'))
    finally:
        if cursor: cursor.close()
        if db: db.close()

# Feature: Delete Customer
@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("DELETE FROM pelanggan WHERE id_pelanggan = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        flash('Pelanggan berhasil dihapus!', 'success')
    except Exception as e:
        flash(f"Error deleting customer: {str(e)}", 'danger')
    return redirect(url_for('manage_customers'))

# Feature: Update Customer
@app.route('/update_customer', methods=['POST'])
def update_customer():
    try:
        # Retrieve the form data
        id_pelanggan = request.form.get('id_pelanggan')
        nama = request.form.get('nama')
        alamat = request.form.get('alamat')

        if not id_pelanggan or not nama or not alamat:
            flash('Please provide all the necessary fields for updating.', 'warning')
            return redirect(url_for('manage_customers'))

        # Connect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        
        # Update the customer record
        cursor.execute("""
            UPDATE pelanggan 
            SET nama_pelanggan = %s, alamat = %s 
            WHERE id_pelanggan = %s
        """, (nama, alamat, id_pelanggan))
        
        db.commit()
        cursor.close()
        db.close()
        
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('manage_customers'))

    except Exception as e:
        flash(f"Error updating customer: {str(e)}", 'danger')
        return redirect(url_for('manage_customers'))

@app.route('/pay_bill/<int:bill_id>', methods=['GET', 'POST'])
def pay_bill(bill_id):
    if request.method == 'POST':
        amount_paid = request.form['amount_paid']
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO pembayaran (id_tagihan, jumlah_bayar) VALUES (%s, %s)
        """, (bill_id, amount_paid))
        cursor.execute("""
            UPDATE tagihan SET status = 'Lunas' WHERE id_tagihan = %s
        """, (bill_id,))
        db.commit()
        cursor.close()
        db.close()
        flash('Bill payment successful.', 'success')
        return redirect(url_for('view_bills'))
    return render_template('pay_bill.html', bill_id=bill_id)

@app.route('/customer/make_payment', methods=['GET', 'POST'])
def make_payment():
    if request.method == 'POST':
        try:
            # Retrieve the form data
            id_tagihan = request.form.get('id_tagihan')
            jumlah_meter = request.form.get('jumlah_meter')
            tarif_per_kwh = request.form.get('tarif_per_kwh')
            biaya_admin = 2500  # Assume fixed admin fee, adjust as needed
            user_id = session['user_id']

            if not id_tagihan or not jumlah_meter or not tarif_per_kwh:
                flash('Some form data is missing. Please try again.', 'warning')
                return redirect(url_for('make_payment'))

            # Convert the values to the appropriate data types
            id_tagihan = int(id_tagihan)
            jumlah_meter = int(jumlah_meter)
            tarif_per_kwh = int(tarif_per_kwh)
            total_payment = (jumlah_meter * tarif_per_kwh) + biaya_admin

            # Connect to the database and process the payment
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()

            # Insert the payment into the database
            cursor.execute("""
                INSERT INTO pembayaran (id_tagihan, tanggal_pembayaran, bulan_bayar, biaya_admin, total, id_user)
                VALUES (%s, CURDATE(), MONTH(CURDATE()), %s, %s, %s)
            """, (id_tagihan, biaya_admin, total_payment, user_id))
            db.commit()

            # Update the status of the bill to 'Sudah Dibayar'
            cursor.execute("UPDATE tagihan SET status = 'Sudah Dibayar' WHERE id_tagihan = %s", (id_tagihan,))
            db.commit()

            flash('Payment successful!', 'success')
            return redirect(url_for('customer_dashboard'))
        
        except Exception as e:
            flash(f"Error during payment: {str(e)}", 'danger')
            return redirect(url_for('make_payment'))
        finally:
            if cursor: 
                cursor.close()
            if db: 
                db.close()

    # Fetch unpaid bills for the customer to display in the payment form
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("""
        SELECT t.id_tagihan, t.bulan, t.tahun, t.jumlah_meter, tf.tarifperkwh
        FROM tagihan t 
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan 
        JOIN tarif tf ON p.id_tarif = tf.id_tarif 
        WHERE p.id_pelanggan = %s AND t.status = 'Belum Dibayar'
    """, (session['user_id'],))
    unpaid_bills = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template('make_payment.html', unpaid_bills=unpaid_bills)

@app.route('/payment_history')
def payment_history():
    if 'logged_in' in session and session['user_role'] == 'customer':
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Query to fetch payment history
        cursor.execute("""
            SELECT 
                pembayaran.id_pembayaran, 
                tagihan.bulan, 
                tagihan.tahun, 
                pembayaran.tanggal_pembayaran, 
                pembayaran.bulan_bayar, 
                pembayaran.biaya_admin, 
                pembayaran.total
            FROM pembayaran 
            JOIN tagihan ON pembayaran.id_tagihan = tagihan.id_tagihan
            WHERE tagihan.id_pelanggan = %s
        """, (session['user_id'],))

        history = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('payment_history.html', history=history)
    else:
        flash('You need to be logged in as a customer to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        new_name = request.form['name']
        new_address = request.form['address']
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        cursor.execute("""
            UPDATE pelanggan SET nama_pelanggan = %s, alamat = %s WHERE id_pelanggan = %s
        """, (new_name, new_address, session['user_id']))
        db.commit()
        cursor.close()
        db.close()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('customer_dashboard'))
    return render_template('update_profile.html')


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'logged_in' not in session or session['user_role'] != 'customer':
        flash('You need to be logged in as a customer to access this page.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Password baru dan konfirmasi password tidak cocok.', 'danger')
            return redirect(url_for('change_password'))

        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        try:
            # Fetch the current password hash from the database
            cursor.execute("SELECT password FROM user WHERE id_user = %s", (session['user_id'],))
            result = cursor.fetchone()

            if result and bcrypt.checkpw(current_password.encode('utf-8'), result[0].encode('utf-8')):
                # Hash the new password
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                # Update the password in the database
                cursor.execute("UPDATE user SET password = %s WHERE id_user = %s", (hashed_password.decode('utf-8'), session['user_id']))
                db.commit()
                
                flash('Password berhasil diubah.', 'success')
                return redirect(url_for('customer_dashboard'))
            else:
                flash('Password saat ini tidak benar.', 'danger')
                return redirect(url_for('change_password'))
        except Exception as e:
            flash(f"Terjadi kesalahan: {str(e)}", 'danger')
            return redirect(url_for('change_password'))
        finally:
            cursor.close()
            db.close()
    
    return render_template('change_password.html')

@app.route('/customer_logout')
def customer_logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/total_penggunaan/<int:bulan>/<int:tahun>')
def total_penggunaan(bulan, tahun):
    if 'logged_in' in session and session['user_role'] == 'customer':
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            
            # Memanggil fungsi total_penggunaan_bulanan untuk pelanggan yang sedang login
            cursor.execute("SELECT total_penggunaan_bulanan(%s, %s, %s)", (session['user_id'], bulan, tahun))
            total_usage = cursor.fetchone()[0]
            
            cursor.close()
            db.close()
            
            return render_template('total_penggunaan.html', total_usage=total_usage, bulan=bulan, tahun=tahun)
        except Exception as e:
            flash(f"Error fetching total usage: {str(e)}", "danger")
            return redirect(url_for('customer_dashboard'))
    else:
        flash('You need to be logged in as a customer to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/pelanggan_900_watt')
def pelanggan_900_watt():
    if 'logged_in' in session and session['user_role'] == 'admin':
        try:
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()
            
            # Memanggil stored procedure get_pelanggan_900_watt
            cursor.callproc('get_pelanggan_900_watt')
            
            for result in cursor.stored_results():
                customers = result.fetchall()
            
            cursor.close()
            db.close()
            
            return render_template('pelanggan_900_watt.html', customers=customers)
        except Exception as e:
            flash(f"Error fetching data: {str(e)}", "danger")
            return redirect(url_for('dashboard'))
    else:
        flash('You need to be logged in as an admin to access this page.', 'warning')
        return redirect(url_for('login'))

@app.route('/laporan_penggunaan')
def laporan_penggunaan():
    if 'logged_in' in session:
        try:
            daya_filter = request.args.get('daya')
            db = mysql.connector.connect(**db_config)
            cursor = db.cursor()

            # Jika ada filter daya yang dipilih
            if daya_filter:
                cursor.execute("""
                    SELECT p.nama_pelanggan, pg.bulan, pg.tahun, pg.meter_awal, pg.meter_ahir, 
                           (pg.meter_ahir - pg.meter_awal) AS total_meter, t.daya,
                           ((pg.meter_ahir - pg.meter_awal) * t.tarifperkwh) AS total_tagihan
                    FROM penggunaan pg
                    JOIN pelanggan p ON pg.id_pelanggan = p.id_pelanggan
                    JOIN tarif t ON p.id_tarif = t.id_tarif
                    WHERE t.daya = %s
                """, (daya_filter,))
            else:
                # Jika tidak ada filter daya
                cursor.execute("""
                    SELECT p.nama_pelanggan, pg.bulan, pg.tahun, pg.meter_awal, pg.meter_ahir, 
                           (pg.meter_ahir - pg.meter_awal) AS total_meter, t.daya,
                           ((pg.meter_ahir - pg.meter_awal) * t.tarifperkwh) AS total_tagihan
                    FROM penggunaan pg
                    JOIN pelanggan p ON pg.id_pelanggan = p.id_pelanggan
                    JOIN tarif t ON p.id_tarif = t.id_tarif
                """)

            penggunaan_data = cursor.fetchall()
            
            cursor.close()
            db.close()
            
            return render_template('laporan_penggunaan.html', penggunaan_data=penggunaan_data)
        except Exception as e:
            flash(f"Error fetching data: {str(e)}", "danger")
            return redirect(url_for('dashboard'))
    else:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

# Add this to your existing Flask app
@app.route('/laporan_pembayaran', methods=['GET'])
def laporan_pembayaran():
    # Retrieve filters if available
    nama_pelanggan = request.args.get('nama_pelanggan', '')
    bulan = request.args.get('bulan', '')
    tahun = request.args.get('tahun', '')

    # Construct the SQL query to retrieve payment records with optional filters
    query = """
        SELECT p.nama_pelanggan, t.bulan, t.tahun, b.tanggal_pembayaran, 
               b.total, b.biaya_admin, b.total + b.biaya_admin AS total_bayar
        FROM pembayaran b
        JOIN tagihan t ON b.id_tagihan = t.id_tagihan
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
        WHERE 1=1
    """
    params = []

    if nama_pelanggan:
        query += " AND p.nama_pelanggan LIKE %s"
        params.append(f"%{nama_pelanggan}%")
    if bulan:
        query += " AND t.bulan = %s"
        params.append(bulan)
    if tahun:
        query += " AND t.tahun = %s"
        params.append(tahun)

    # Execute the query
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(query, tuple(params))
    pembayaran_list = cursor.fetchall()
    cursor.close()
    db.close()

    # Fetch all customer names for the filter dropdown
    pelanggan_list_query = "SELECT DISTINCT nama_pelanggan FROM pelanggan"
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute(pelanggan_list_query)
    pelanggan_list = [row[0] for row in cursor.fetchall()]
    cursor.close()
    db.close()

    return render_template('laporan_pembayaran.html', pembayaran_list=pembayaran_list, pelanggan_list=pelanggan_list)

# Route to export data as CSV
@app.route('/export_usage_csv')
def export_usage_csv():
    # Retrieve data from your database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.nama_pelanggan, penggunaan.bulan, penggunaan.tahun, penggunaan.meter_awal, penggunaan.meter_ahir,
               (penggunaan.meter_ahir - penggunaan.meter_awal) as total_usage
        FROM penggunaan
        JOIN pelanggan p ON penggunaan.id_pelanggan = p.id_pelanggan
    """)
    usage_records = cursor.fetchall()
    cursor.close()
    db.close()

    # Create a CSV response
    si = StringIO()
    csv_writer = csv.writer(si)
    csv_writer.writerow(['Nama Pelanggan', 'Bulan', 'Tahun', 'Meter Awal', 'Meter Akhir', 'Total Penggunaan'])
    for record in usage_records:
        csv_writer.writerow(record)

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=daftar_penggunaan.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# Route to export data as PDF
@app.route('/export_usage_pdf')
def export_usage_pdf():
    # Retrieve data from your database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("""
        SELECT p.nama_pelanggan, penggunaan.bulan, penggunaan.tahun, penggunaan.meter_awal, penggunaan.meter_ahir,
               (penggunaan.meter_ahir - penggunaan.meter_awal) as total_usage
        FROM penggunaan
        JOIN pelanggan p ON penggunaan.id_pelanggan = p.id_pelanggan
    """)
    usage_records = cursor.fetchall()
    cursor.close()
    db.close()

    # Create PDF response
    pdf_buffer = BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    pdf.setTitle("Daftar Penggunaan")

    # Write table header
    pdf.drawString(30, 750, "Nama Pelanggan")
    pdf.drawString(150, 750, "Bulan")
    pdf.drawString(200, 750, "Tahun")
    pdf.drawString(250, 750, "Meter Awal")
    pdf.drawString(320, 750, "Meter Akhir")
    pdf.drawString(400, 750, "Total Penggunaan")

    y = 730
    for record in usage_records:
        pdf.drawString(30, y, str(record[0]))
        pdf.drawString(150, y, str(record[1]))
        pdf.drawString(200, y, str(record[2]))
        pdf.drawString(250, y, str(record[3]))
        pdf.drawString(320, y, str(record[4]))
        pdf.drawString(400, y, str(record[5]))
        y -= 20
        if y < 40:  # Prevent writing off the page
            pdf.showPage()
            y = 750

    pdf.save()

    output = make_response(pdf_buffer.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=daftar_penggunaan.pdf"
    output.headers["Content-type"] = "application/pdf"
    return output

# Ensure this is the last line
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
