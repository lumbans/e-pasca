
-- Example data for level table
INSERT INTO level (nama_level) VALUES ('Admin'), ('Pelanggan');

-- Example data for user table
INSERT INTO user (username, password, nama_admin, id_level) 
VALUES 
('admin1', 'adminpass', 'Admin Satu', 1),
('pelanggan1', 'pass123', 'Pelanggan Satu', 2),
('pelanggan2', 'pass456', 'Pelanggan Dua', 2),
('pelanggan3', 'pass789', 'Pelanggan Tiga', 2);

-- Example data for tarif table
INSERT INTO tarif (daya, tarifperkwh) 
VALUES 
(450, 500),
(900, 1000),
(1300, 1500),
(2200, 2000);

-- Example data for pelanggan table
INSERT INTO pelanggan (username, password, nomor_kwh, nama_pelanggan, alamat, id_tarif) 
VALUES 
('pelanggan1', 'pass123', 'KW12345', 'Pelanggan Satu', 'Jalan A No. 1', 1),
('pelanggan2', 'pass456', 'KW54321', 'Pelanggan Dua', 'Jalan B No. 2', 2),
('pelanggan3', 'pass789', 'KW98765', 'Pelanggan Tiga', 'Jalan C No. 3', 3);

-- Example data for penggunaan table
INSERT INTO penggunaan (id_pelanggan, bulan, tahun, meter_awal, meter_ahir) 
VALUES 
(1, 1, 2024, 100, 150),
(1, 2, 2024, 150, 200),
(2, 1, 2024, 50, 80),
(3, 1, 2024, 200, 250),
(3, 2, 2024, 250, 300);

-- Example data for tagihan table
INSERT INTO tagihan (id_penggunaan, id_pelanggan, bulan, tahun, jumlah_meter, status)
VALUES 
(1, 1, 1, 2024, 50, 'Belum Dibayar'),
(2, 1, 2, 2024, 50, 'Belum Dibayar'),
(3, 2, 1, 2024, 30, 'Lunas'),
(4, 3, 1, 2024, 50, 'Belum Dibayar'),
(5, 3, 2, 2024, 50, 'Belum Dibayar');

-- Example data for pembayaran table
INSERT INTO pembayaran (id_tagihan, tanggal_pembayaran, bulan_bayar, biaya_admin, total, id_user)
VALUES 
(1, '2024-02-01', 2, 2500, 27500, 1),
(3, '2024-03-01', 3, 2500, 32500, 1);
