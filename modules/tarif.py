# modules/tarif.py
from flask import flash
from modules.utilities import get_db_connection

def get_all_tarif():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
    SELECT * FROM tarif
    """)
    tarif = cursor.fetchall()
    cursor.close()
    db.close()
    return tarif

def add_tarif(daya, tarifperkwh):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO tarif (daya, tarifperkwh) VALUES (%s, %s)", (daya, tarifperkwh))
    db.commit()
    cursor.close()
    db.close()
    flash('Tarif added successfully!', 'success')

def update_tarif(id_tarif, daya, tarifperkwh):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE tarif SET daya = %s, tarifperkwh = %s 
        WHERE id_tarif = %s
    """, (daya, tarifperkwh, id_tarif))
    db.commit()
    cursor.close()
    db.close()
    flash('Tarif updated successfully!', 'success')

def delete_tarif(id_tarif):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tarif WHERE id_tarif = %s", (id_tarif,))
    db.commit()
    cursor.close()
    db.close()
    flash('Tarif deleted successfully!', 'success')
