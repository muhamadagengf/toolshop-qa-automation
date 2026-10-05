# Technical Assessment QA Automation — Practice Software Testing

Repositori ini berisi pengerjaan Technical Assessment QA untuk web e-commerce [Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com). Pengujian mencakup perancangan test case (BDD), implementasi automation framework berbasis Robot Framework, dan laporan exploratory bug hunting.

---

## 📁 Struktur Repositori

Proyek ini menggunakan pola **Page Object Model (POM)** untuk memisahkan locator/interaksi UI dengan logika skenario pengujian:

```text
├── config/
│   └── env_config.robot            # Konfigurasi environment (URL, timeout, browser)
├── data/
│   └── login_test_data.json        # Data pengujian DDT untuk skenario login
├── docs/
│   ├── 01-test-design.md           # Bagian 1: Test Design & BDD Scenarios (Markdown)
│   ├── 01-test-design.xlsx         # Bagian 1: Versi Excel spreadsheet
│   ├── 01-test-design.pdf          # Bagian 1: Versi PDF
│   ├── 02-automation-result.md     # Bagian 2: Hasil eksekusi & detail otomasi
│   ├── 03-bug-report.md            # Bagian 3: Laporan bug hunting (Markdown)
│   ├── 03-bug-report.xlsx          # Bagian 3: Versi Excel dengan screenshot tertanam
│   └── evidence/                   # Screenshot bukti visual bug
├── features/
│   └── auth_profile_navigation.feature # 12 skenario Gherkin BDD
├── pages/                          # Komponen Page Object Model (POM)
│   ├── Common.robot                # Setup/teardown browser & helper global
│   ├── HomePage.robot              # Komponen navbar & katalog produk
│   ├── LoginPage.robot             # Form login & validasi error
│   ├── RegisterPage.robot          # Form pendaftaran akun
│   ├── ProfilePage.robot           # Halaman user profile & edit data
│   ├── ProductDetailPage.robot    # Detail produk & add to cart
│   └── CheckoutPage.robot          # Keranjang, alamat, payment, & invoice
├── resources/
│   └── DataHelper.py               # Helper Python untuk data unik (timestamp email)
├── results/                        # Output log & report eksekusi test
└── tests/                          # Test suite otomasi
    ├── 01_register.robot           # Test registrasi user baru (dinamis)
    ├── 02_login_data_driven.robot  # Test login data-driven (positif & negatif)
    ├── 03_edit_profile.robot       # Test update profil & verifikasi simpan
    └── 04_e2e_checkout.robot       # Test E2E checkout hingga invoice
```

---

## 📌 Pemetaan Deliverables

| Bagian | Item Tugas | Lokasi File |
| :--- | :--- | :--- |
| **Bagian 1 (35%)** | BDD Scenarios (`.feature`) | `features/auth_profile_navigation.feature` |
| | Test Case Document | `docs/01-test-design.md`, `.xlsx`, `.pdf` |
| **Bagian 2 (35%)** | Automation Script & Framework | `tests/` & `pages/` |
| | Laporan Hasil Otomasi | `docs/02-automation-result.md` |
| | Test Execution Report | `results/report.html` & `results/log.html` |
| **Bagian 3 (30%)** | Bug Hunting Report | `docs/03-bug-report.md` & `docs/03-bug-report.xlsx` |
| | Screenshot Evidence | `docs/evidence/` |

---

## ⚙️ Prasyarat & Versi Tool

- **Python**: Versi `3.10` atau `3.11`
- **Google Chrome**: Versi terbaru
- **Robot Framework**: `7.0`
- **SeleniumLibrary**: `6.2.0`
- **Selenium**: `4.32.0` (ChromeDriver dikelola otomatis via Selenium Manager bawaan, tidak perlu download driver manual)

---

## 🚀 Panduan Setup & Instalasi

1. **Clone repository dan masuk ke folder project:**
   ```bash
   git clone <URL_REPOSITORY>
   cd <NAMA_FOLDER_REPO>
   ```

2. **Buat dan aktifkan virtual environment:**
   - *Windows (PowerShell):*
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - *Linux / macOS:*
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Cara Menjalankan Test

### 1. Menjalankan Seluruh Test Suite (1-Command Run)
Secara default, test akan berjalan dalam mode **Headless** (cepat dan cocok untuk CI/CD):
```bash
robot -d results tests/
```

### 2. Menjalankan dalam Mode Headed (Browser Terlihat)
Ada dua cara mudah jika ingin melihat browser saat test berjalan:
- **Lewat CLI flag (tanpa ubah kode):**
  ```bash
  robot -v HEADLESS:false -d results tests/
  ```
- **Atau ubah setup di file test:**  
  Ubah `Test Setup    Open Application Browser` menjadi `Test Setup    CHROME` pada bagian `*** Settings ***` file test terkait.

### 3. Menjalankan Suite Spesifik
```bash
robot -d results tests/01_register.robot
robot -d results tests/02_login_data_driven.robot
robot -d results tests/03_edit_profile.robot
robot -d results tests/04_e2e_checkout.robot
```

### 4. Menjalankan Berdasarkan Tag
```bash
robot -i smoke -d results tests/
robot -i regression -d results tests/
robot -i e2e -d results tests/
```

---

## 📊 Cara Melihat Test Report

Setelah test selesai dieksekusi, Robot Framework akan otomatis membuat file report di folder `results/`:

- **Ringkasan Eksekutif (Report):** Buka file `results/report.html` di browser untuk melihat ringkasan status pass/fail dan durasi test.
- **Log Detail Step-by-Step (Log):** Buka file `results/log.html` untuk melihat detail tiap step keyword, value variabel, dan pesan error jika ada kegagalan.

Contoh buka langsung lewat terminal (Windows):
```powershell
start results/report.html
```

---

## 💡 Alasan Pemilihan Tools & Desain

1. **Robot Framework & SeleniumLibrary:**
   - Sintaks berbasis keyword membuat skenario mudah dibaca oleh non-programmer maupun tim produk.
   - Built-in reporting (`report.html` dan `log.html`) sudah sangat informatif dan lengkap tanpa butuh library reporter tambahan.
   - Selenium 4 memiliki driver management otomatis, sehingga siap dijalankan di mesin baru tanpa setup path ChromeDriver.
2. **Page Object Model (POM):**
   - Selector elemen dipusatkan di folder `pages/`. Jika ada perubahan selector pada web target, perbaikan hanya perlu dilakukan di satu file page terkait tanpa menyentuh file test.
3. **Data-Driven Testing (DDT):**
   - Skenario pengujian login negatif menggunakan data eksternal dari `data/login_test_data.json` agar mudah ditambah atau dimodifikasi tanpa mengubah alur script.
4. **Explicit & Dynamic Wait:**
   - Tidak menggunakan *hardcoded sleep* (`Sleep`). Semua interaksi menggunakan explicit wait (`Wait Until Element Is Visible`, `Wait Until Page Contains Element`) agar eksekusi stabil dan tidak flaky.

---

## 🔍 Asumsi & Keterbatasan

1. **Data Akun Registrasi:**  
   Karena server memvalidasi keunikan email pada database, email registrasi di-generate secara dinamis menggunakan timestamp presisi milidetik (`resources/DataHelper.py`) agar test dapat dijalankan berulang kali tanpa bentrok data.
2. **Alur Checkout E2E:**  
   Metode pembayaran yang dipilih pada skenario E2E adalah *Cash on Delivery* agar pesanan dapat diselesaikan sampai invoice terbentuk tanpa perlu input data kartu kredit live.
3. **Target Aplikasi Bagian 3:**  
   Exploratory testing (Bagian 3) dilakukan pada subdomain `https://with-bugs.practicesoftwaretesting.com` yang memang dikonfigurasi memiliki bug bawaan dari pembuat aplikasi demo.
