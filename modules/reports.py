# modules/reports.py
from modules.utilities import get_db_connection
from flask import flash

def get_generate_report(pelanggan=None, bulan=None, tahun=None):
    """
    Retrieves electricity usage report based on given filters.
    :param pelanggan: Name of the customer (optional).
    :param bulan: Month (optional).
    :param tahun: Year (optional).
    :return: List of usage records.
    """
    db = get_db_connection()
    cursor = db.cursor()

    # Base query
    query = "SELECT * FROM view_penggunaan_listrik WHERE 1=1"
    params = []

    # Apply filters if provided
    if pelanggan:
        query += " AND nama_pelanggan LIKE %s"
        params.append(f"%{pelanggan}%")

    if bulan:
        query += " AND bulan = %s"
        params.append(bulan)

    if tahun:
        query += " AND tahun = %s"
        params.append(tahun)

    cursor.execute(query, params)
    usage_records = cursor.fetchall()
    cursor.close()
    db.close()
    return usage_records
    
def get_usage_report(pelanggan, bulan, tahun):
    db = get_db_connection()
    cursor = db.cursor()

    query = "SELECT * FROM view_penggunaan_listrik WHERE 1=1"
    params = []

    if pelanggan:
        query += " AND nama_pelanggan LIKE %s"
        params.append(f"%{pelanggan}%")

    if bulan:
        query += " AND bulan = %s"
        params.append(bulan)

    if tahun:
        query += " AND tahun = %s"
        params.append(tahun)

    cursor.execute(query, params)
    usage_records = cursor.fetchall()
    cursor.close()
    db.close()
    return usage_records

def get_payment_history(pelanggan_id):
    db = get_db_connection()
    cursor = db.cursor()
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
    payment_history = cursor.fetchall()
    cursor.close()
    db.close()
    return payment_history

def get_laporan_pembayaran(nama_pelanggan, bulan, tahun):
    db = get_db_connection()
    cursor = db.cursor()

    # Construct the SQL query to retrieve payment records with optional filters
    query = "SELECT * from view_laporan_pembayaran;"
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
    cursor.execute(query, params)
    pembayaran_list = cursor.fetchall()
    cursor.close()
    db.close()

    return pembayaran_list

def get_all_customers():
    db = get_db_connection()
    cursor = db.cursor()
    
    # Fetch all customer names for the filter dropdown
    cursor.execute("SELECT DISTINCT nama_pelanggan FROM pelanggan")
    pelanggan_list = [row[0] for row in cursor.fetchall()]

    cursor.close()
    db.close()

    return pelanggan_list