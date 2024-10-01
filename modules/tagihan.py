# modules/tagihan.py
from modules.utilities import get_db_connection
from flask import flash

def get_all_tagihan():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            t.id_tagihan, 
            p.nama_pelanggan, 
            t.bulan, 
            t.tahun, 
            t.jumlah_meter, 
            t.status, 
            COALESCE(tr.daya, 0) AS daya, 
            COALESCE(tr.tarifperkwh, 0) AS tarifperkwh, 
            COALESCE((t.jumlah_meter * tr.tarifperkwh) + 2500, 0) AS total_tagihan
        FROM tagihan t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
        LEFT JOIN tarif tr ON p.id_tarif = tr.id_tarif
        WHERE 1=1
    """)
    tagihan_list = cursor.fetchall()
    cursor.close()
    db.close()
    return tagihan_list

def get_tagihan_pelanggan_list(id_pelanggan):
    db = get_db_connection()
    cursor = db.cursor()

    # Retrieve unpaid bills (status 'Belum Dibayar' indicates unpaid)
    query = """
        SELECT 
            t.id_pelanggan,
            p.nama_pelanggan, 
            t.bulan, 
            t.tahun, 
            t.jumlah_meter, 
            t.status, 
            COALESCE(tr.daya, 0) AS daya, 
            COALESCE(tr.tarifperkwh, 0) AS tarifperkwh, 
            COALESCE((t.jumlah_meter * tr.tarifperkwh) + 2500, 0) AS total_tagihan
        FROM tagihan t
        JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
        LEFT JOIN tarif tr ON p.id_tarif = tr.id_tarif
        WHERE t.status = 'Belum Dibayar' AND t.id_pelanggan = %s
    """
    
    # Execute the query with the parameter passed as a tuple
    cursor.execute(query, (id_pelanggan,))
    tagihan_pelanggan_list = cursor.fetchall()
    cursor.close()
    db.close()
    return tagihan_pelanggan_list

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

def add_tagihan(id_pelanggan, bulan, tahun, jumlah_meter):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO tagihan (id_pelanggan, bulan, tahun, jumlah_meter, status) 
        VALUES (%s, %s, %s, %s, %s)
    """, (id_pelanggan, bulan, tahun, jumlah_meter, 'Belum Bayar'))
    db.commit()
    cursor.close()
    db.close()
    flash('Tagihan berhasil ditambahkan!', 'success')

def update_tagihan(id_tagihan, id_pelanggan, bulan, tahun, jumlah_meter, status):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE tagihan 
        SET id_pelanggan = %s, bulan = %s, tahun = %s, jumlah_meter = %s, status = %s 
        WHERE id_tagihan = %s
    """, (id_pelanggan, bulan, tahun, jumlah_meter, status, id_tagihan))
    db.commit()
    cursor.close()
    db.close()
    flash('Tagihan berhasil diperbarui!', 'success')

def delete_tagihan(id_tagihan):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tagihan WHERE id_tagihan = %s", (id_tagihan,))
    db.commit()
    cursor.close()
    db.close()
    flash('Tagihan berhasil dihapus!', 'success')