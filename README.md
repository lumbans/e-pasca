
# Aplikasi Pembayaran Listrik Pasca Bayar

Aplikasi Pembayaran Listrik Pasca Bayar adalah sebuah aplikasi berbasis web yang dibangun menggunakan HTML, CSS, JavaScript, Python (Flask), dan MySQL. Aplikasi ini dibuat untuk memudahkan pengguna dalam mengelola dan membayar tagihan listrik pasca bayar secara online.

Proyek ini dikembangkan sebagai bagian dari Sertifikasi Kompetensi di Universitas Nusa Mandiri (UNM).

## Fitur Utama
- **Login & Logout**: Pengguna dapat login dan logout menggunakan peran sebagai Pelanggan, Admin, dan Operator.
- **Pengelolaan Tagihan**: Pelanggan dapat melihat tagihan listrik mereka dan melakukan pembayaran.
- **Riwayat Pembayaran**: Pelanggan dapat melihat riwayat pembayaran yang telah dilakukan.
- **Manajemen Pengguna**: Admin dapat mengelola data pengguna, termasuk menambahkan, mengedit, dan menghapus pengguna.
- **Pengelolaan Tarif & Tagihan**: Admin dapat mengelola tarif listrik dan tagihan pelanggan.
- **Laporan Penggunaan & Pembayaran**: Admin dapat melihat laporan penggunaan listrik dan pembayaran.

## Teknologi yang Digunakan
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Template Engine**: Jinja2
- **Framework**: AdminLTE untuk tampilan dasbor

## Prasyarat
Sebelum memulai, pastikan Anda telah menginstal perangkat lunak berikut:
- [Python 3.7+](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/mysql/)
- [Git](https://git-scm.com/) (opsional jika ingin mengkloning dari repository)

## Langkah-Langkah Instalasi

1. **Clone Repository (Opsional)**
   ```bash
   git clone https://github.com/username/aplikasi-pembayaran-listrik-pasca-bayar.git
   cd aplikasi-pembayaran-listrik-pasca-bayar
   ```

2. **Buat Virtual Environment dan Aktifkan**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   venv\Scripts\activate     # Untuk Windows
   ```

3. **Instal Dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Database**
   - Buat database baru di MySQL:
     ```sql
     CREATE DATABASE pembayaran_listrik;
     ```
   - Sesuaikan konfigurasi database di file `config.py`:
     ```python
     db_config = {
         'host': 'localhost',
         'user': 'root',
         'password': 'your_mysql_password',
         'database': 'pembayaran_listrik'
     }
     ```

5. **Inisialisasi Database**
   - Jalankan file `init_db.py` untuk membuat tabel-tabel yang diperlukan:
     ```bash
     python init_db.py
     ```

6. **Menjalankan Aplikasi**
   ```bash
   flask run
   ```
   Aplikasi akan berjalan di `http://127.0.0.1:5000`.

## Cara Menggunakan Aplikasi
1. Buka browser dan akses `http://127.0.0.1:5000`.
2. Login menggunakan salah satu role:
   - **Admin**: username `admin` dengan password `admin123` (default)
   - **Operator**: username `operator` dengan password `operator123` (default)
   - **Pelanggan**: dapat dibuat melalui role Admin atau Operator
3. Mulai gunakan fitur-fitur seperti melihat tagihan, pembayaran, pengelolaan pengguna, dan laporan.

## Struktur Proyek
```
aplikasi-pembayaran-listrik-pasca-bayar/
│
├── app.py                    # File utama aplikasi Flask
├── config.py                 # Konfigurasi database
├── requirements.txt          # Daftar dependensi Python
├── templates/                # Folder untuk template HTML
│   ├── base.html             # Template dasar
│   ├── home.html             # Halaman utama
│   ├── customer_dashboard.html  # Halaman dashboard pelanggan
│   └── ...                   # Template lainnya
├── static/                   # Folder untuk file statis (CSS, JS, gambar)
│   ├── css/
│   ├── js/
│   └── images/
└── README.md                 # Dokumentasi proyek
```

## Informasi Tambahan
Aplikasi ini dikembangkan sebagai bagian dari **Sertifikasi Kompetensi** di Universitas Nusa Mandiri (UNM).

## Catatan
- Pastikan Anda telah mengaktifkan virtual environment saat menjalankan aplikasi.
- Ganti `SECRET_KEY` pada file `config.py` dengan kunci yang lebih aman untuk keperluan produksi.
- Jangan lupa untuk menutup aplikasi dengan `CTRL + C` di terminal saat sudah selesai.

## Kontribusi
Jika Anda ingin berkontribusi dalam pengembangan aplikasi ini, silakan buat pull request atau hubungi pengembang.

---

**© 2024 Aplikasi Pembayaran Listrik Pasca Bayar - Sertifikasi Kompetensi UNM**
