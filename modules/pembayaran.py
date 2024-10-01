# modules/pembayaran.py
from flask import flash
from modules.utilities import get_db_connection

def get_unpaid_bills(pelanggan_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT id_tagihan, bulan, tahun, jumlah_meter, status
        FROM tagihan
        WHERE id_pelanggan = %s AND status = 'Belum Bayar'
    """, (pelanggan_id,))
    unpaid_bills = cursor.fetchall()
    cursor.close()
    db.close()
    return unpaid_bills

def bayar(id_tagihan, jumlah_meter, tarif_per_kwh, user_id):
    biaya_admin = 2500  # Fixed admin fee
    total_payment = (jumlah_meter * tarif_per_kwh) + biaya_admin

    db = get_db_connection()
    cursor = db.cursor()

    try:
        # Fetch id_pelanggan for the given id_tagihan
        cursor.execute("SELECT id_pelanggan FROM tagihan WHERE id_tagihan = %s", (id_tagihan,))
        result = cursor.fetchone()
        
        if not result:
            flash('Tagihan tidak ditemukan.', 'danger')
            return False
        
        id_pelanggan = result[0]

        # Insert the payment record into the pembayaran table, including id_pelanggan
        cursor.execute("""
            INSERT INTO pembayaran (id_tagihan, tanggal_pembayaran, bulan_bayar, biaya_admin, total, id_pelanggan)
            VALUES (%s, CURDATE(), MONTH(CURDATE()), %s, %s, %s)
        """, (id_tagihan, biaya_admin, total_payment, id_pelanggan))
        
        # Commit the payment insertion
        db.commit()

        # Update the tagihan status to 'Lunas'
        cursor.execute("UPDATE tagihan SET status = 'Lunas' WHERE id_tagihan = %s", (id_tagihan,))
        
        # Commit the status update
        db.commit()

        return True  # Successfully updated

    except Exception as e:
        db.rollback()  # Roll back if there's an error
        print(f"Error processing payment: {e}")
        flash('Terjadi kesalahan saat memproses pembayaran.', 'danger')
        return False
    finally:
        cursor.close()
        db.close()

def get_payment_history(pelanggan_id):
    db = get_db_connection()
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
    """, (pelanggan_id,))
    
    history = cursor.fetchall()
    cursor.close()
    db.close()
    return history