
-- Schema for Aplikasi Pembayaran Listrik Pascabayar
USE pembayaran_listrik;

-- Tabel level
CREATE TABLE level (
    id_level INT PRIMARY KEY AUTO_INCREMENT,
    nama_level VARCHAR(50) NOT NULL
);

-- Tabel user
CREATE TABLE user (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    nama_admin VARCHAR(100),
    id_level INT,
    FOREIGN KEY (id_level) REFERENCES level(id_level)
);

-- Tabel pelanggan
CREATE TABLE pelanggan (
    id_pelanggan INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    nomor_kwh VARCHAR(20) NOT NULL,
    nama_pelanggan VARCHAR(100),
    alamat VARCHAR(200),
    id_tarif INT,
    FOREIGN KEY (id_tarif) REFERENCES tarif(id_tarif)
);

-- Tabel tarif
CREATE TABLE tarif (
    id_tarif INT PRIMARY KEY AUTO_INCREMENT,
    daya INT NOT NULL,
    tarifperkwh DECIMAL(10, 2) NOT NULL
);

-- Tabel penggunaan
CREATE TABLE penggunaan (
    id_penggunaan INT PRIMARY KEY AUTO_INCREMENT,
    id_pelanggan INT,
    bulan INT,
    tahun INT,
    meter_awal INT NOT NULL,
    meter_ahir INT NOT NULL,
    FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id_pelanggan)
);

-- Tabel tagihan
CREATE TABLE tagihan (
    id_tagihan INT PRIMARY KEY AUTO_INCREMENT,
    id_penggunaan INT,
    id_pelanggan INT,
    bulan INT,
    tahun INT,
    jumlah_meter INT NOT NULL,
    status VARCHAR(20),
    FOREIGN KEY (id_penggunaan) REFERENCES penggunaan(id_penggunaan),
    FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id_pelanggan)
);

-- Tabel pembayaran
CREATE TABLE pembayaran (
    id_pembayaran INT PRIMARY KEY AUTO_INCREMENT,
    id_tagihan INT,
    tanggal_pembayaran DATE,
    bulan_bayar INT,
    biaya_admin DECIMAL(10, 2),
    total DECIMAL(10, 2),
    id_user INT,
    FOREIGN KEY (id_tagihan) REFERENCES tagihan(id_tagihan),
    FOREIGN KEY (id_user) REFERENCES user(id_user)
);
