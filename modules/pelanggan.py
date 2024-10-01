# modules/pelanggan.py
from modules.utilities import get_db_connection
from flask import flash
from modules.tarif import get_all_tarif

def get_all_pelanggan():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT id_pelanggan, nama_pelanggan, alamat, nomor_kwh FROM pelanggan")
    pelanggan_list = cursor.fetchall()
    cursor.close()
    db.close()
    return pelanggan_list

def add_pelanggan(username, password, nama_pelanggan, alamat, nomor_kwh, id_tarif):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO pelanggan (username, password, nama_pelanggan, alamat, nomor_kwh, id_tarif) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (username, password, nama_pelanggan, alamat, nomor_kwh, id_tarif))
    db.commit()
    cursor.close()
    db.close()
    flash('Pelanggan berhasil ditambahkan!', 'success')

def update_pelanggan(id_pelanggan, nama_pelanggan, alamat, nomor_kwh):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE pelanggan 
        SET nama_pelanggan = %s, alamat = %s, nomor_kwh = %s 
        WHERE id_pelanggan = %s
    """, (nama_pelanggan, alamat, nomor_kwh, id_pelanggan))
    db.commit()
    cursor.close()
    db.close()
    flash('Pelanggan berhasil diperbarui!', 'success')

def delete_pelanggan(id_pelanggan):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM pelanggan WHERE id_pelanggan = %s", (id_pelanggan,))
    db.commit()
    cursor.close()
    db.close()
    flash('Pelanggan berhasil dihapus!', 'success')