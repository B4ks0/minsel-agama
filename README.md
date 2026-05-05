# Kemenag Minsel - Sistem Informasi Data Lembaga Keagamaan

Aplikasi web Django untuk mengelola data lembaga keagamaan (Gereja Kristen & Masjid/Mushollah) di Kabupaten Minahasa Selatan, Provinsi Sulawesi Utara, Indonesia.

![Django](https://img.shields.io/badge/Django-4.2%2B-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-blueviolet)
![Status](https://img.shields.io/badge/Status-Development-yellow)

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Tech Stack](#tech-stack)
- [Prasyarat Sistem](#prasyarat-sistem)
- [Instalasi & Setup](#instalasi--setup)
- [Konfigurasi Database](#konfigurasi-database)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Struktur Proyek](#struktur-proyek)
- [Dokumentasi URL & Views](#dokumentasi-url--views)
- [Dokumentasi Database](#dokumentasi-database)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Troubleshooting](#troubleshooting)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

---

## 🎯 Fitur Utama

### 1. **Manajemen Data Kecamatan**
- ✅ CRUD lengkap (Create, Read, Update, Delete) data kecamatan
- ✅ Tampilan daftar dengan pencarian
- ✅ Edit dan hapus data kecamatan
- ✅ Total 17 kecamatan di Minahasa Selatan

### 2. **Manajemen Data Gereja (Lembaga Kristen)**
- ✅ Database 594 gereja dengan data lengkap
- ✅ Pencarian berdasarkan nama gereja & kecamatan
- ✅ Filter per kecamatan
- ✅ Tracking jumlah umat (laki-laki & perempuan)
- ✅ Information status bangunan (Permanen/Semi Permanen/Darurat/Sewa)
- ✅ Data pimpinan dan jumlah pendeta
- ✅ CRUD dan operasi lengkap

### 3. **Manajemen Data Masjid & Mushollah**
- ✅ Database 32 masjid/mushollah
- ✅ Pencarian dan filter berdasarkan KUA (Kantor Urusan Agama)
- ✅ Data imam dan ketua BKM
- ✅ Tracking ada tidaknya mushollah
- ✅ CRUD lengkap

### 4. **Dashboard & Analytics**
- ✅ Dashboard ringkasan statistik
- ✅ View rekapitulasi gereja per kecamatan
- ✅ View rekapitulasi masjid per KUA
- ✅ Tampilan total data keseluruhan

### 5. **User Interface**
- ✅ Responsif dan mobile-friendly (Bootstrap 5)
- ✅ Sidebar navigasi
- ✅ Topbar dengan informasi
- ✅ DataTables untuk manajemen data
- ✅ Form dengan validasi Bootstrap
- ✅ Konfirmasi delete yang aman

---

## 🛠 Tech Stack

| Komponen | Teknologi | Versi |
|----------|-----------|-------|
| Backend | Django | 4.2+ |
| Database | MySQL | 8.0+ |
| Python | Python | 3.8+ |
| Frontend | Bootstrap | 5.3.3 |
| Frontend | DataTables | 1.13.8 |
| Frontend | Bootstrap Icons | Latest |
| Web Server | Gunicorn/Laragon | - |
| Adapter DB | mysqlclient | Latest |

---

## ⚙️ Prasyarat Sistem

### Software yang Perlu Diinstal:
1. **Python** 3.8 atau lebih baru
   ```
   python --version
   ```

2. **MySQL** 8.0 atau lebih baru
   ```
   mysql --version
   ```

3. **Git** (opsional, untuk version control)
   ```
   git --version
   ```

4. **Laragon** atau Web Server Python (Django dev server juga bisa)

### Hardware Minimum:
- RAM: 2GB
- Storage: 500MB
- Processor: Dual Core

---

## 📦 Instalasi & Setup

### 1. Clone atau Download Proyek

```bash
# Jika menggunakan git
git clone <repository-url>
cd minsel-agama

# Atau copy folder proyek ke folder yang diinginkan
cd c:\laragon\www\minsel-agama
```

### 2. Buat Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install Django dan requirements
pip install Django==4.2.0
pip install mysqlclient
pip install python-dotenv

# Atau jika ada requirements.txt
pip install -r requirements.txt
```

**Buat `requirements.txt`** (jika belum ada):
```
Django==4.2.0
mysqlclient==2.2.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

```bash
pip freeze > requirements.txt
```

### 4. Konfigurasi Environment Variables

Buat file `.env` di root project:

```env
# Database Configuration
DB_NAME=db_kemenag_minsel
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306

# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-&3ak@9rxphdeijwbji^lnv4u_3x3%z4&xywlqy&itk*rl9)7a7
ALLOWED_HOSTS=127.0.0.1,localhost

# Language & Timezone
LANGUAGE_CODE=id
TIME_ZONE=Asia/Makassar
```

---

## 🗄️ Konfigurasi Database

### 1. Import Database SQL

Pastikan MySQL/MariaDB sudah berjalan, kemudian:

```bash
# Command line MySQL
mysql -u root -p < db_kemenag_minsel.sql

# Atau lewat MySQL client GUI
# - Buka file db_kemenag_minsel.sql
# - Browse dan select semua
# - Execute
```

**Verifikasi Database:**
```bash
mysql -u root
> SHOW DATABASES;
> USE db_kemenag_minsel;
> SHOW TABLES;
> SELECT COUNT(*) FROM gereja;
> SELECT COUNT(*) FROM masjid_bkm;
> SELECT COUNT(*) FROM kecamatan;
```

**Expected Output:**
- `kecamatan`: 17 records
- `gereja`: 594 records
- `masjid_bkm`: 32 records
- **Total**: 643 records

### 2. Jalankan Migrations Django (jika ada)

```bash
python manage.py migrate
```

### 3. Buat Superuser (untuk Django Admin) - Optional

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@admin.com
# Password: ****
```

---

## 🚀 Menjalankan Aplikasi

### Opsi 1: Django Development Server

```bash
# Navigate ke project directory
cd c:\laragon\www\minsel-agama

# Pastikan venv sudah activate (jika menggunakan)
venv\Scripts\activate

# Jalankan development server
python manage.py runserver

# Atau specify host dan port
python manage.py runserver 0.0.0.0:8000
```

**Output:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Opsi 2: Laragon

1. Buka Laragon
2. Klik "Start All"
3. Project akan accessible di `http://minsel-agama.local` (jika sudah dikonfigurasi)
4. Atau gunakan `http://localhost/minsel-agama`

### Opsi 3: Production dengan Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Jalankan dengan Gunicorn
gunicorn kemenag_minsel.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## 📁 Struktur Proyek

```
minsel-agama/
│
├── manage.py                          # Django CLI utility
├── db_kemenag_minsel.sql              # Database schema SQL
├── database_erd.json                  # Database ERD documentation
│
├── kemenag_minsel/                    # Django Project Settings
│   ├── __init__.py
│   ├── settings.py                    # ⚙️ Django settings (DATABASE, INSTALLED_APPS, etc)
│   ├── urls.py                        # 🔗 Root URL routing
│   ├── asgi.py                        # ASGI server config (async)
│   ├── wsgi.py                        # WSGI server config (production)
│   └── __pycache__/
│
├── main/                              # Main Django App (Business Logic)
│   ├── migrations/                    # Database migrations
│   │   ├── __init__.py
│   │   └── __pycache__/
│   │
│   ├── templates/main/                # 🎨 HTML Templates
│   │   ├── base.html                  # Base layout (sidebar + navbar)
│   │   ├── dashboard.html             # Dashboard/Home page
│   │   ├── kecamatan/
│   │   │   ├── list.html              # Daftar kecamatan
│   │   │   ├── form.html              # Form tambah/edit kecamatan
│   │   │   └── confirm_delete.html    # Konfirmasi hapus
│   │   ├── gereja/
│   │   │   ├── list.html              # Daftar gereja
│   │   │   ├── form.html              # Form tambah/edit gereja
│   │   │   └── confirm_delete.html    # Konfirmasi hapus
│   │   └── masjid/
│   │       ├── list.html              # Daftar masjid
│   │       ├── form.html              # Form tambah/edit masjid
│   │       └── confirm_delete.html    # Konfirmasi hapus
│   │
│   ├── __init__.py
│   ├── admin.py                       # 🛠️ Django admin configuration
│   ├── apps.py                        # App configuration
│   ├── models.py                      # 📊 Database models (ORM)
│   ├── views.py                       # 🔧 View functions (Business logic)
│   ├── urls.py                        # 🔗 App URL routing
│   ├── forms.py                       # 📝 Django forms
│   ├── tests.py                       # ✅ Unit tests
│   ├── __pycache__/
│   └── __pycache__/
│
├── static/                            # 📦 Static files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── images/
│
├── requirements.txt                   # Python dependencies list
├── .env                               # Environment variables (gitignore)
├── .gitignore                         # Git ignore rules
└── README.md                          # 📖 Documentation (file ini)
```

### Penjelasan File Penting:

| File | Fungsi |
|------|--------|
| `settings.py` | Konfigurasi Django (DB, INSTALLED_APPS, STATIC, dll) |
| `urls.py` | Routing URL ke views |
| `models.py` | Definisi model database (ORM) |
| `views.py` | Logic untuk handle request HTTP |
| `forms.py` | Form validasi dan rendering |
| `admin.py` | Konfigurasi Django admin panel |
| `base.html` | Template layout utama (inheritance) |
| `database_erd.json` | Dokumentasi skema database |

---

## 🔗 Dokumentasi URL & Views

### URL Routing Map

#### **Dashboard & Home**
```
GET  /                          → views.dashboard
```

#### **Kecamatan Management**
```
GET  /kecamatan/               → views.kecamatan_list (List + Search)
GET  /kecamatan/<id>/          → views.kecamatan_detail (Detail view)
GET  /kecamatan/tambah/        → views.kecamatan_form (Form)
POST /kecamatan/tambah/        → views.kecamatan_form (Save create)
GET  /kecamatan/<id>/edit/     → views.kecamatan_form (Edit form)
POST /kecamatan/<id>/edit/     → views.kecamatan_form (Save edit)
POST /kecamatan/<id>/hapus/    → views.kecamatan_delete (Delete)
```

#### **Gereja Management**
```
GET  /gereja/                  → views.gereja_list (List + Filter)
GET  /gereja/<id>/             → views.gereja_detail (Detail)
GET  /gereja/tambah/           → views.gereja_form (Form)
POST /gereja/tambah/           → views.gereja_form (Save create)
GET  /gereja/<id>/edit/        → views.gereja_form (Edit form)
POST /gereja/<id>/edit/        → views.gereja_form (Save edit)
POST /gereja/<id>/hapus/       → views.gereja_delete (Delete)
```

#### **Masjid Management**
```
GET  /masjid/                  → views.masjid_list (List + Filter)
GET  /masjid/<id>/             → views.masjid_detail (Detail)
GET  /masjid/tambah/           → views.masjid_form (Form)
POST /masjid/tambah/           → views.masjid_form (Save create)
GET  /masjid/<id>/edit/        → views.masjid_form (Edit form)
POST /masjid/<id>/edit/        → views.masjid_form (Save edit)
POST /masjid/<id>/hapus/       → views.masjid_delete (Delete)
```

#### **Admin & Utilities**
```
GET  /admin/                   → Django admin panel
GET  /static/...               → Static files (CSS, JS, etc)
```

---

## 🗄️ Dokumentasi Database

### Database: `db_kemenag_minsel`

**Charset**: utf8mb4 | **Collation**: utf8mb4_unicode_ci

### 1. Table: `kecamatan` (Kecamatan/Districts)

```sql
CREATE TABLE kecamatan (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  nama       VARCHAR(100) NOT NULL,
  kabupaten  VARCHAR(100) DEFAULT 'Minahasa Selatan',
  provinsi   VARCHAR(100) DEFAULT 'Sulawesi Utara'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Fields:**
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | INT | PK, AUTO_INCREMENT | Unique identifier |
| nama | VARCHAR(100) | NOT NULL | Nama kecamatan |
| kabupaten | VARCHAR(100) | DEFAULT | Nama kabupaten |
| provinsi | VARCHAR(100) | DEFAULT | Nama provinsi |

**Sample Data:**
- Kec. Tumpaan
- Kec. Tatapaan
- Kec. Tenga
- ... (17 kecamatan total)

---

### 2. Table: `gereja` (Churches/Gereja Kristen)

```sql
CREATE TABLE gereja (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  kecamatan        VARCHAR(100) NOT NULL,
  nama_gereja      VARCHAR(200) NOT NULL,
  kelurahan_desa   VARCHAR(150),
  jumlah_umat_l    INT DEFAULT 0,
  jumlah_umat_p    INT DEFAULT 0,
  jumlah_umat      INT DEFAULT 0,
  nama_pimpinan    VARCHAR(200),
  status_bangunan  ENUM('Permanen','Semi Permanen','Darurat','Sewa/Kontrak') DEFAULT 'Permanen',
  jumlah_pdt       INT DEFAULT 0,
  jumlah_pdm       INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Fields:**
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | INT | PK | Unique identifier |
| kecamatan | VARCHAR(100) | NOT NULL, FK | Nama kecamatan |
| nama_gereja | VARCHAR(200) | NOT NULL | Nama gereja |
| kelurahan_desa | VARCHAR(150) | - | Lokasi kelurahan/desa |
| jumlah_umat_l | INT | DEFAULT 0 | Jumlah umat laki-laki |
| jumlah_umat_p | INT | DEFAULT 0 | Jumlah umat perempuan |
| jumlah_umat | INT | DEFAULT 0 | Total jumlah umat |
| nama_pimpinan | VARCHAR(200) | - | Nama pendeta/pimpinan |
| status_bangunan | ENUM | DEFAULT 'Permanen' | Status kondisi bangunan |
| jumlah_pdt | INT | DEFAULT 0 | Jumlah pendeta |
| jumlah_pdm | INT | DEFAULT 0 | Jumlah pendeta muda/pekerja |

**Status Bangunan Enum:**
- `Permanen` - Bangunan permanen
- `Semi Permanen` - Bangunan semi permanen
- `Darurat` - Bangunan darurat
- `Sewa/Kontrak` - Pakai bangunan sewa

**Total Records**: 594 gereja

---

### 3. Table: `masjid_bkm` (Mosques/Masjid & BKM)

```sql
CREATE TABLE masjid_bkm (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  no_urut      INT,
  wilayah_kua  VARCHAR(100),
  desa         VARCHAR(150),
  nama_masjid  VARCHAR(200),
  ada_musholla TINYINT(1) DEFAULT 0 COMMENT '1=Ada, 0=Tidak',
  nama_imam    VARCHAR(200),
  ketua_btm    VARCHAR(200),
  keterangan   VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Fields:**
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | INT | PK | Unique identifier |
| no_urut | INT | - | Nomor urut |
| wilayah_kua | VARCHAR(100) | FK | Wilayah KUA (Kantor Urusan Agama) |
| desa | VARCHAR(150) | - | Nama desa |
| nama_masjid | VARCHAR(200) | - | Nama masjid |
| ada_musholla | TINYINT(1) | DEFAULT 0 | Ada mushollah? (1=Ya, 0=Tidak) |
| nama_imam | VARCHAR(200) | - | Nama imam masjid |
| ketua_btm | VARCHAR(200) | - | Nama ketua BKM |
| keterangan | VARCHAR(255) | - | Keterangan tambahan |

**Total Records**: 32 masjid

---

### 4. Views (Read-Only)

#### `v_rekap_gereja_per_kecamatan`
Ringkasan statistik gereja per kecamatan.

```sql
SELECT
  kecamatan,
  COUNT(*) AS jumlah_gereja,
  SUM(jumlah_umat_l) AS total_umat_laki,
  SUM(jumlah_umat_p) AS total_umat_perempuan,
  SUM(jumlah_umat) AS total_umat,
  SUM(jumlah_pdt) AS total_pendeta,
  SUM(jumlah_pdm) AS total_pdm
FROM gereja
GROUP BY kecamatan
ORDER BY kecamatan;
```

#### `v_rekap_masjid_per_kua`
Ringkasan statistik masjid per KUA.

```sql
SELECT
  wilayah_kua,
  COUNT(*) AS jumlah_masjid,
  SUM(ada_musholla) AS jumlah_musholla
FROM masjid_bkm
GROUP BY wilayah_kua
ORDER BY wilayah_kua;
```

---

### 5. Database Statistics

| Entitas | Jumlah |
|---------|--------|
| Kecamatan | 17 |
| Gereja | 594 |
| Masjid/BKM | 32 |
| **Total** | **643** |

### Entity Relationship Diagram (ERD)

```
┌──────────────┐
│  KECAMATAN   │
├──────────────┤
│ id (PK)      │
│ nama         │
│ kabupaten    │
│ provinsi     │
└──────────────┘
       │
       │ 1:N
       ├─────────────────────┬─────────────────────┐
       │                     │                     │
┌──────────────────────┐   ┌──────────────────────┐
│      GEREJA          │   │   MASJID_BKM         │
├──────────────────────┤   ├──────────────────────┤
│ id (PK)              │   │ id (PK)              │
│ kecamatan (FK)       │   │ wilayah_kua (FK)     │
│ nama_gereja          │   │ desa                 │
│ kelurahan_desa       │   │ nama_masjid          │
│ jumlah_umat_l        │   │ ada_musholla         │
│ jumlah_umat_p        │   │ nama_imam            │
│ jumlah_umat          │   │ ketua_btm            │
│ nama_pimpinan        │   │ keterangan           │
│ status_bangunan      │   └──────────────────────┘
│ jumlah_pdt           │
│ jumlah_pdm           │
└──────────────────────┘
```

---

## 📖 Panduan Penggunaan

### Akses Aplikasi

1. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

2. **Buka browser** dan akses:
   ```
   http://127.0.0.1:8000
   atau
   http://localhost:8000
   ```

### 📊 Dashboard

- **Halaman utama** menampilkan:
  - Total jumlah kecamatan
  - Total jumlah gereja
  - Total jumlah umat (gereja)
  - Total jumlah masjid
  - Ringkasan per kecamatan
  - Ringkasan per KUA

### 🏛️ Manajemen Kecamatan

**1. Lihat Daftar Kecamatan:**
- Klik menu "Kecamatan" di sidebar
- Semua kecamatan akan ditampilkan dalam tabel

**2. Cari Kecamatan:**
- Gunakan search box di atas tabel
- Filter berdasarkan nama kecamatan

**3. Tambah Kecamatan Baru:**
- Klik tombol "+ Tambah Kecamatan"
- Isi form dengan data kecamatan
- Klik "Simpan"

**4. Edit Kecamatan:**
- Klik tombol "Edit" pada baris kecamatan
- Ubah data yang diperlukan
- Klik "Simpan Perubahan"

**5. Hapus Kecamatan:**
- Klik tombol "Hapus" pada baris kecamatan
- Konfirmasi penghapusan
- Kecamatan akan dihapus dari database

### ⛪ Manajemen Gereja

**1. Lihat Daftar Gereja:**
- Klik menu "Gereja" di sidebar
- Semua gereja akan ditampilkan

**2. Filter Gereja:**
- Pilih kecamatan dari dropdown "Filter Kecamatan"
- Tabel akan menampilkan gereja di kecamatan tersebut

**3. Cari Gereja:**
- Gunakan search box
- Cari berdasarkan nama gereja

**4. Tambah Gereja:**
- Klik "+ Tambah Gereja"
- Isi data:
  - Pilih kecamatan
  - Nama gereja
  - Kelurahan/desa
  - Jumlah umat (laki-laki & perempuan)
  - Nama pimpinan
  - Status bangunan
  - Jumlah pendeta
- Klik "Simpan"

**5. Edit/Hapus:**
- Sama seperti kecamatan

### 🕌 Manajemen Masjid

**1. Lihat Daftar Masjid:**
- Klik menu "Masjid" di sidebar

**2. Filter Masjid:**
- Pilih wilayah KUA dari dropdown
- Lihat masjid di wilayah tersebut

**3. Tambah Masjid:**
- Klik "+ Tambah Masjid"
- Isi data masjid lengkap
- Klik "Simpan"

**4. Edit/Hapus:**
- Klik tombol "Edit" atau "Hapus"
- Lakukan perubahan atau konfirmasi penghapusan

---

## 🐛 Troubleshooting

### Error 1: "No module named 'django'"
**Solusi:**
```bash
pip install Django==4.2.0
```

### Error 2: "No module named 'mysqlclient'"
**Solusi:**
```bash
pip install mysqlclient
```

### Error 3: "Access denied for user 'root'@'localhost'"
**Solusi:**
- Pastikan MySQL service berjalan
- Check kredensial di `.env`
- Pastikan username dan password super

```bash
# Check MySQL service
mysql -u root -p
# Tekan enter jika password kosong
```

### Error 4: "Database 'db_kemenag_minsel' doesn't exist"
**Solusi:**
```bash
# Import database SQL
mysql -u root < db_kemenag_minsel.sql

# Atau create database manual
mysql -u root
> CREATE DATABASE db_kemenag_minsel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> exit
```

### Error 5: "Port 8000 already in use"
**Solusi:**
```bash
# Use different port
python manage.py runserver 0.0.0.0:8001

# Atau kill process yang menggunakan port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Error 6: Static files not loading (CSS/JS)
**Solusi:**
```bash
# Collect static files
python manage.py collectstatic

# Atau pastikan DEBUG=True di settings.py
```

### Error 7: Form validation error
**Solusi:**
- Check browser console (F12) untuk error detail
- Ensure semua required field sudah diisi
- Pastikan format data sesuai (misal: number untuk jumlah umat)

### Error 8: CSRF token missing
**Solusi:**
```html
<!-- Ensure form memiliki CSRF token -->
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>
```

---

## 📝 Development Notes

### Membuat Model Baru

Jika perlu menambah model baru:

```python
# di models.py
from django.db import models

class NamaModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField(default=0)
    
    class Meta:
        managed = False  # Jika table sudah ada di database
        db_table = 'nama_table_di_db'
    
    def __str__(self):
        return self.field1
```

### Membuat View Baru

```python
# di views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import NamaModel

def nama_list(request):
    items = NamaModel.objects.all()
    return render(request, 'main/nama/list.html', {'items': items})

def nama_form(request, id=None):
    item = get_object_or_404(NamaModel, id=id) if id else None
    if request.method == 'POST':
        # Handle form submission
        pass
    return render(request, 'main/nama/form.html', {'item': item})
```

### Routing URL

```python
# di urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('nama/', views.nama_list, name='nama_list'),
    path('nama/tambah/', views.nama_form, name='nama_form'),
    path('nama/<int:id>/edit/', views.nama_form, name='nama_edit'),
]
```

---

## 💡 Best Practices

1. ✅ **Always use Django ORM** untuk database operations
2. ✅ **Validate all form inputs** di forms.py
3. ✅ **Use get_object_or_404()** untuk safe object retrieval
4. ✅ **Cache expensive queries** jika diperlukan
5. ✅ **Use transactions** untuk multi-table updates
6. ✅ **Add CSRF token** di semua POST forms
7. ✅ **Use slugify()** untuk URL-safe strings
8. ✅ **Write unit tests** untuk critical functions
9. ✅ **Keep settings.py secure** (use .env untuk secrets)
10. ✅ **Log errors properly** untuk debugging

---

## 🔒 Security Checklist

- [ ] Ubah `SECRET_KEY` ke value yang aman
- [ ] Set `DEBUG=False` di production
- [ ] Update `ALLOWED_HOSTS` dengan domain yang tepat
- [ ] Enable HTTPS di production
- [ ] Use environment variables untuk credentials
- [ ] Set strong password untuk database
- [ ] Regular backup database
- [ ] Update Django & dependencies secara berkala
- [ ] Implement rate limiting untuk API
- [ ] Add input validation & sanitization

---

## 🤝 Kontribusi

Untuk berkontribusi pada proyek ini:

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Coding Standards:
- Follow PEP 8 style guide
- Add comments untuk logic yang kompleks
- Write unit tests untuk new features
- Update documentation

---

## 📄 Lisensi

Proyek ini berlisensikan di bawah **MIT License** - lihat file LICENSE untuk detail.

---

## 📞 Kontak & Support

- **Project Owner**: Kementerian Agama Kabupaten Minahasa Selatan
- **Email**: support@kemenag-minsel.local
- **Documentation**: Lihat `database_erd.json` untuk schema detail
- **Issues**: Report bugs via GitHub Issues

---

## 📚 Referensi & Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
- [DataTables Documentation](https://datatables.net/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)

---

## 🎉 Changelog

### Version 1.0.0 (Current)
- ✅ Initial release
- ✅ CRUD operations untuk Kecamatan, Gereja, Masjid
- ✅ Dashboard dengan statistik
- ✅ Database views untuk rekapitulasi
- ✅ Responsive Bootstrap UI
- ✅ Search & filter functionality

### Planned Features (v1.1.0)
- 🔄 REST API endpoints
- 🔄 Export to Excel/PDF
- 🔄 Advanced reporting & analytics
- 🔄 Multi-user support dengan authentication
- 🔄 Audit logging
- 🔄 Data validation rules
- 🔄 Mobile app

---

**Last Updated**: May 5, 2026  
**Version**: 1.0.0  
**Status**: Development ✅

---

_Dokumentasi lengkap untuk Sistem Informasi Data Lembaga Keagamaan Kab. Minahasa Selatan_
