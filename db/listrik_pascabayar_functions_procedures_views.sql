
-- Function to calculate total usage per month
DELIMITER $$
CREATE FUNCTION total_penggunaan_bulanan(id_pelanggan INT, bulan INT, tahun INT) 
RETURNS INT
BEGIN
    DECLARE total INT;
    SELECT (meter_ahir - meter_awal) INTO total
    FROM penggunaan
    WHERE id_pelanggan = id_pelanggan AND bulan = bulan AND tahun = tahun;
    RETURN total;
END$$
DELIMITER ;


-- Stored Procedure to show customers using 900 watt power
DELIMITER $$
CREATE PROCEDURE get_pelanggan_900_watt()
BEGIN
    SELECT p.nama_pelanggan, p.nomor_kwh, t.daya
    FROM pelanggan p
    JOIN tarif t ON p.id_tarif = t.id_tarif
    WHERE t.daya = 900;
END$$
DELIMITER ;


-- View to show electricity usage information
CREATE VIEW view_penggunaan_listrik AS
SELECT p.nama_pelanggan, pg.bulan, pg.tahun, pg.meter_awal, pg.meter_ahir, 
       (pg.meter_ahir - pg.meter_awal) AS total_meter
FROM penggunaan pg
JOIN pelanggan p ON pg.id_pelanggan = p.id_pelanggan;


-- Trigger to save bill data after inserting electricity usage data
DELIMITER $$
CREATE TRIGGER after_insert_penggunaan
AFTER INSERT ON penggunaan
FOR EACH ROW
BEGIN
    DECLARE jumlah_meter INT;
    SET jumlah_meter = NEW.meter_ahir - NEW.meter_awal;

    INSERT INTO tagihan (id_penggunaan, id_pelanggan, bulan, tahun, jumlah_meter, status)
    VALUES (NEW.id_penggunaan, NEW.id_pelanggan, NEW.bulan, NEW.tahun, jumlah_meter, 'Belum Dibayar');
END$$
DELIMITER ;
