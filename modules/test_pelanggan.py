import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.utilities import get_db_connection
from modules.tarif import update_tarif
from modules.pelanggan import add_pelanggan, delete_pelanggan, get_all_pelanggan

class TestAplikasiPascabayar(unittest.TestCase):
    
    # Test untuk fungsi add_pelanggan
    def test_add_pelanggan(self):
        pelanggan = {
            "nama": "Andi",
            "alamat": "Jl. Merdeka",
            "nomor_meter": "123456789",
            "tipe": "Rumah Tangga"
        }
        hasil = add_pelanggan(pelanggan)
        self.assertTrue(hasil, "Pelanggan berhasil diaddkan")

    # Test untuk fungsi update_tarif
    def test_update_tarif(self):
        tarif = {
            "daya": 450,
            "harga_per_kwh": 500
        }
        hasil = update_tarif(tarif)
        self.assertEqual(hasil, "Tarif berhasil diubah")

    # Test untuk fungsi delete_pelanggan
    def test_delete_pelanggan(self):
        nomor_meter = "123456789"
        hasil = delete_pelanggan(nomor_meter)
        self.assertTrue(hasil, "Pelanggan berhasil didelete")

    # Test untuk fungsi get_all_pelanggan
    def test_get_all_pelanggan(self):
        nomor_meter = "123456789"
        hasil = get_all_pelanggan(nomor_meter)
        self.assertIsNotNone(hasil, "Data pelanggan ditemukan")

if __name__ == '__main__':
    unittest.main()
