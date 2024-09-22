import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='db',
        user='root',
        password='example',
        database='pembayaran_listrik'
    )
    return conn

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_usage_by_pelanggan(id_pelanggan):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM penggunaan WHERE id_pelanggan = %s", (id_pelanggan,))
    usage_data = cursor.fetchall()
    conn.close()
    return usage_data

def get_tagihan_belum_dibayar(id_pelanggan):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tagihan WHERE id_pelanggan = %s AND status = 'Belum Dibayar'", (id_pelanggan,))
    tagihan_data = cursor.fetchall()
    conn.close()
    return tagihan_data

def bayar_tagihan(id_tagihan, id_pelanggan):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tagihan WHERE id_tagihan = %s AND id_pelanggan = %s AND status = 'Belum Dibayar'", 
                   (id_tagihan, id_pelanggan))
    tagihan = cursor.fetchone()
    
    if tagihan:
        cursor.execute("UPDATE tagihan SET status = 'Lunas' WHERE id_tagihan = %s", (id_tagihan,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_all_pelanggan():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pelanggan")
    pelanggan = cursor.fetchall()
    conn.close()
    return pelanggan

def add_pelanggan(nama_pelanggan, nomor_kwh, alamat, id_tarif):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pelanggan (nama_pelanggan, nomor_kwh, alamat, id_tarif) VALUES (%s, %s, %s, %s)", 
                   (nama_pelanggan, nomor_kwh, alamat, id_tarif))
    conn.commit()
    conn.close()
    return True
