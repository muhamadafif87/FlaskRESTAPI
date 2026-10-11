-- DISCLAIMER: INI CUMA DATA DUMMY YA GUYS, BUKAN DIAMBIL DARI DATA ASLI DI LAPANGAN

BEGIN;

-- 1. INSERT SEKOLAH
INSERT INTO embegeh.sekolah (id, nama_sekolah, jumlah_siswa, alamat_sekolah, jenjang, email_sekolah, nomor_telepon) VALUES
(1, 'SDN Menteng 01 Jakarta', 450, 'Jl. Besuki No. 1, Jakarta Pusat', 'SD', 'sdn_menteng01@jakarta.sch.id', '021-3141592'),
(2, 'SMPN 1 Bandung', 750, 'Jl. Kesturi No. 12, Bandung', 'SMP', 'info@smpn1bdg.sch.id', '022-4201234'),
(3, 'SMKN 2 Yogyakarta', 1200, 'Jl. AM Sangaji No. 47, Yogyakarta', 'SMK', 'contact@smkn2yogya.sch.id', '0274-513000'),
(4, 'SMA Kebon Jeruk 05', 380, 'Jl. Raya Kebon Jeruk No. 8, Jakarta Barat', 'SMA', 'smakebonjeruk05@gmail.com', '021-5321100');

-- 2. INSERT SPPG
INSERT INTO embegeh.sppg (id, nama_sppg, alamat, jumlah_karyawan, id_sekolah, kapasitas_produksi_harian, nomor_izin_edar, status_operasional, penanggung_jawab) VALUES
(1, 'SPPG Dapur Sehat Menteng', 'Jl. Surabaya No. 15, Jakarta Pusat', 18, 1, 1500, 'SLHS-JKT-2024-001', 'Aktif', 'Budi Santoso, S.Gz'),
(2, 'SPPG Catering Pasundan', 'Jl. Asia Afrika No. 88, Bandung', 25, 2, 2000, 'SLHS-BDG-2024-005', 'Aktif', 'Siti Aminah, M.Gz'),
(3, 'SPPG Mataram Nutrisi', 'Jl. Magelang Km 5, Yogyakarta', 30, 3, 3000, 'SLHS-YOG-2023-012', 'Aktif', 'Dr. Raden Mas Hendra'),
(4, 'SPPG Dapur Bersama Barat', 'Jl. Pemuda No. 120, Surakarta', 20, 4, 1800, 'SLHS-SKA-2024-022', 'Aktif', 'Dewi Lestari, S.TP');

-- 3. INSERT MENU
INSERT INTO embegeh.menu (id, nama_menu, rasa, id_sppg, kalori_kcal, biaya_per_porsi, is_halal, kategori_gizi) VALUES
(1, 'Nasi Kuning Ayam Suwir & Telur Dadar', 'Gurih', 1, 520, 15000.00, TRUE, 'Kombinasi Seimbang'),
(2, 'Nasi Timbel Ikan Lada Hitam + Sayur Asem', 'Gurih', 2, 580, 18000.00, TRUE, 'Protein Tinggi'),
(3, 'Gudeg Egg & Chicken Rice Box', 'Manis', 3, 610, 16500.00, TRUE, 'Tradisional Komplit'),
(4, 'Nasi Uduk Semur Daging & Tahu', 'Gurih', 4, 650, 17500.00, TRUE, 'Karbohidrat & Protein'),
(5, 'Nasi Goreng Sehat Sayuran & Rolade Ayam', 'Gurih', 4, 490, 14000.00, TRUE, 'Kalori Terkontrol'),
(6, 'Bubur Ayam Nutrisi Lengkap', 'Gurih', 1, 410, 12000.00, TRUE, 'Sarapan Gizi');

-- 4. INSERT PRODUKSI
INSERT INTO embegeh.produksi (id, batch_produksi, waktu_produksi, id_sppg, id_menu, jumlah_porsi, status_qc, suhu_simpan_celsius, waktu_distribusi) VALUES
(1, 101, '2026-03-01', 1, 1, 450, 'Lolos', 65.5, '2026-03-01 06:30:00+07'),
(2, 102, '2026-03-01', 2, 2, 750, 'Lolos', 68.0, '2026-03-01 06:45:00+07'),
(3, 103, '2026-03-01', 3, 3, 1200, 'Lolos', 62.0, '2026-03-01 06:15:00+07'),
(4, 104, '2026-03-02', 4, 4, 380, 'Gagal', 28.5, '2026-03-02 08:00:00+07'),
(5, 105, '2026-03-02', 4, 5, 900, 'Lolos', 67.2, '2026-03-02 06:30:00+07'),
(6, 106, '2026-03-03', 1, 6, 450, 'Lolos', 70.0, '2026-03-03 06:00:00+07');

-- Update tabel menu dengan id_produksi terbaru.
UPDATE embegeh.menu SET id_produksi = 1 WHERE id = 1;
UPDATE embegeh.menu SET id_produksi = 2 WHERE id = 2;
UPDATE embegeh.menu SET id_produksi = 3 WHERE id = 3;
UPDATE embegeh.menu SET id_produksi = 4 WHERE id = 4;
UPDATE embegeh.menu SET id_produksi = 5 WHERE id = 5;
UPDATE embegeh.menu SET id_produksi = 6 WHERE id = 6;

-- 5. INSERT DATA KERACUNAN
INSERT INTO embegeh.data_keracunan (id_sekolah, jumlah_siswa, id_sppg, waktu_kejadian, tingkat_keparahan, gejala_dominan, status_penanganan, catatan_medis) VALUES
(4, 35, 4, '2026-03-02 10:30:00+07', 'Sedang', 'Mual, Muntah, Pusing', 'Dalam Investigasi', 'Terjadi 2 jam setelah konsumsi Nasi Uduk Semur Daging. Diduga penanganan suhu makanan buruk.'),
(2, 3, 2, '2026-02-15 11:00:00+07', 'Ringan', 'Sakit Perut ringan', 'Selesai', 'Reaksi alergi individual terhadap bahan seafood/ikan pada 3 siswa.');

COMMIT;