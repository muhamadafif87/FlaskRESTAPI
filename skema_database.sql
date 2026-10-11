-- ============================================================================
-- 1. HAPUS TABLE DAN DATABASE JIKA SEBELUMNYA KALIAN SUDAH COBA MEMBUAT
-- ============================================================================
-- DROP SCHEMA IF EXISTS embegeh;
-- DROP DATABASE IF EXISTS mbg;
-- DROP TABLE IF EXISTS data_keracunan CASCADE;
-- DROP TABLE IF EXISTS produksi CASCADE;
-- DROP TABLE IF EXISTS menu CASCADE;
-- DROP TABLE IF EXISTS sppg CASCADE;
-- DROP TABLE IF EXISTS sekolah CASCADE;
-- note: hilangkan tanda command jika kalian ingin mengeksekusi perintah di atas

-- =============================================================================
-- 2. MEMBUAT SCHEMA DAN DATABASE
-- =============================================================================
CREATE DATABASE mbg;
\c mbg; -- connect ke database mbg

CREATE SCHEMA embegeh;
SET search_path TO embegeh;

-- ============================================================================
-- 3. CREATE CUSTOM ENUM TYPES
-- ============================================================================
CREATE TYPE enum_rasa AS ENUM ('Gurih', 'Manis', 'Pedas', 'Asam', 'Netral');
CREATE TYPE enum_jenjang AS ENUM ('SD', 'SMP', 'SMA', 'SMK');
CREATE TYPE enum_status_qc AS ENUM ('Lolos', 'Gagal', 'Karantina');

-- ============================================================================
-- 4. CREATE TABLES WITH ATTRIBUTES & CONSTRAINTS
-- ============================================================================

-- A. TABEL SEKOLAH
CREATE TABLE sekolah (
    id BIGSERIAL PRIMARY KEY,
    nama_sekolah VARCHAR(150) NOT NULL,
    jumlah_siswa INT NOT NULL CHECK (jumlah_siswa > 0),
    alamat_sekolah VARCHAR(255) NOT NULL,
    jenjang enum_jenjang NOT NULL DEFAULT 'SD',
    email_sekolah VARCHAR(100),
    nomor_telepon VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- B. TABEL SPPG
CREATE TABLE sppg (
    id BIGSERIAL PRIMARY KEY,
    nama_sppg VARCHAR(150) NOT NULL,
    alamat VARCHAR(255) NOT NULL,
    jumlah_karyawan INT NOT NULL CHECK (jumlah_karyawan >= 0),
    id_sekolah BIGINT,
    kapasitas_produksi_harian INT DEFAULT 1000 CHECK (kapasitas_produksi_harian > 0),
    nomor_izin_edar VARCHAR(50) UNIQUE,
    status_operasional VARCHAR(20) DEFAULT 'Aktif' CHECK (status_operasional IN ('Aktif', 'Nonaktif', 'Dalam Investigasi')),
    penanggung_jawab VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sppg_sekolah FOREIGN KEY (id_sekolah) REFERENCES sekolah(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- C. TABEL MENU
CREATE TABLE menu (
    id BIGSERIAL PRIMARY KEY,
    nama_menu VARCHAR(150) NOT NULL,
    rasa enum_rasa NOT NULL DEFAULT 'Gurih',
    id_produksi BIGINT, -- Akan dihubungkan/dibiarkan nullable jika belum ada batch produksi spesifik
    id_sppg BIGINT NOT NULL,
    kalori_kcal INT CHECK (kalori_kcal > 0),
    biaya_per_porsi NUMERIC(10,2) CHECK (biaya_per_porsi >= 0),
    is_halal BOOLEAN DEFAULT TRUE,
    kategori_gizi VARCHAR(50) DEFAULT 'Kombinasi Seimbang',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_menu_sppg FOREIGN KEY (id_sppg) REFERENCES sppg(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- D. TABEL PRODUKSI
CREATE TABLE produksi (
    id BIGSERIAL PRIMARY KEY,
    batch_produksi INT NOT NULL CHECK (batch_produksi > 0),
    waktu_produksi DATE NOT NULL DEFAULT CURRENT_DATE,
    id_sppg BIGINT NOT NULL,
    id_menu BIGINT NOT NULL,
    jumlah_porsi INT NOT NULL CHECK (jumlah_porsi > 0),
    status_qc enum_status_qc NOT NULL DEFAULT 'Lolos',
    suhu_simpan_celsius NUMERIC(4,1) CHECK (suhu_simpan_celsius BETWEEN -20.0 AND 100.0),
    waktu_distribusi TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_produksi_sppg FOREIGN KEY (id_sppg) REFERENCES sppg(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_produksi_menu FOREIGN KEY (id_menu) REFERENCES menu(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Menambahkan FK Circular menu.id_produksi -> produksi.id secara terpisah
ALTER TABLE menu 
ADD CONSTRAINT fk_menu_produksi 
FOREIGN KEY (id_produksi) REFERENCES produksi(id) ON DELETE SET NULL ON UPDATE CASCADE;

-- E. TABEL DATA KERACUNAN
CREATE TABLE data_keracunan (
    id BIGSERIAL PRIMARY KEY,
    id_sekolah BIGINT NOT NULL,
    jumlah_siswa INT NOT NULL CHECK (jumlah_siswa >= 0),
    id_sppg BIGINT NOT NULL,
    waktu_kejadian TIMESTAMPTZ NOT NULL,
    tingkat_keparahan VARCHAR(20) DEFAULT 'Sedang' CHECK (tingkat_keparahan IN ('Ringan', 'Sedang', 'Berat')),
    gejala_dominan VARCHAR(150),
    status_penanganan VARCHAR(30) DEFAULT 'Dalam Investigasi',
    catatan_medis TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_keracunan_sekolah FOREIGN KEY (id_sekolah) REFERENCES sekolah(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_keracunan_sppg FOREIGN KEY (id_sppg) REFERENCES sppg(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================================
-- 5. INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================
CREATE INDEX idx_sppg_sekolah ON sppg(id_sekolah);
CREATE INDEX idx_menu_sppg ON menu(id_sppg);
CREATE INDEX idx_produksi_sppg_menu ON produksi(id_sppg, id_menu);
CREATE INDEX idx_produksi_waktu ON produksi(waktu_produksi);
CREATE INDEX idx_keracunan_sekolah_sppg ON data_keracunan(id_sekolah, id_sppg);
CREATE INDEX idx_keracunan_waktu ON data_keracunan(waktu_kejadian);