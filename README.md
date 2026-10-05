# Logique Digital Indonesia — QA Technical Assessment

[![Robot Framework](https://img.shields.io/badge/Framework-Robot%20Framework%207.0-blue.svg)](https://robotframework.org/)
[![SeleniumLibrary](https://img.shields.io/badge/Library-SeleniumLibrary%206.2.0-green.svg)](https://robotframework.org/SeleniumLibrary/)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-yellow.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Automation%20Status-5%2F5%20PASS%20(100%25)-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)]()

Repositori ini berisi solusi lengkap untuk **Technical Assessment QA Automation Engineer** di **PT. LOGIQUE Digital Indonesia**. Seluruh bagian teknis inti (**Bagian 1: Test Design**, **Bagian 2: Web Automation Framework**, dan **Bagian 3: Bug Hunting Report**) telah diselesaikan secara komprehensif, modular, dan mengikuti standar industri *quality engineering*.

---

## 📑 Daftar Isi
1. [Struktur Proyek](#-struktur-proyek)
2. [Pemetaan Deliverables](#-pemetaan-deliverables)
3. [Prasyarat & Lingkungan](#-prasyarat--lingkungan)
4. [Panduan Instalasi & Setup](#-panduan-instalasi--setup)
5. [Cara Menjalankan Test (1-Command Run)](#-cara-menjalankan-test-1-command-run)
6. [Fleksibilitas Headed vs Headless](#-fleksibilitas-headed-vs-headless)
7. [Cara Melihat Test Report](#-cara-melihat-test-report)
8. [Justifikasi Pemilihan Tools & Library](#-justifikasi-pemilihan-tools--library)
9. [Asumsi & Batasan (Assumptions & Limitations)](#-asumsi--batasan-assumptions--limitations)
10. [Checklist Verifikasi Sebelum Submit](#-checklist-verifikasi-sebelum-submit)

---

## 📂 Struktur Proyek

Arsitektur repositori dirancang dengan prinsip **Page Object Model (POM)** yang bersih dan pemisahan *concern* yang ketat:

```text
logique-qa-assessment/
│
├── .gitignore                      # Mengabaikan file temporary & build artifacts
├── README.md                       # Dokumentasi utama proyek & panduan eksekusi
├── requirements.txt                # Dependensi Python & library automation
│
├── config/                         # Konfigurasi environment & parameter global
│   └── env_config.robot            # URL web target, kredensial default, timeout global
│
├── data/                           # Data-driven test files
│   └── login_test_data.json        # Dataset pengujian login (skenario positif & negatif)
│
├── docs/                           # Dokumentasi deliverables resmi
│   ├── 01-test-design.md           # Bagian 1: Desain test case lengkap (Markdown)
│   ├── 01-test-design.xlsx         # Bagian 1: Desain test case format spreadsheet (Excel)
│   ├── 01-test-design.pdf          # Bagian 1: Desain test case format dokumen cetak (PDF)
│   ├── 02-automation-result.md     # Ringkasan metrik eksekusi otomasi Bagian 2
│   ├── 03-bug-report.md            # Bagian 3: Laporan 7 bug temuan exploratory testing (Markdown)
│   ├── 03-bug-report.xlsx          # Bagian 3: Laporan bug spreadsheet Excel (lengkap dengan screenshot tertanam)
│   └── evidence/                   # Screenshot bukti visual bug Bagian 3
│       ├── BUG-001-cart-subtotal-zero.png
│       ├── BUG-002-inverted-price-sorting.png
│       ├── BUG-003-swapped-country-state-labels.png
│       ├── BUG-004-future-date-of-birth.png
│       ├── BUG-005-duplicate-total-table-header.png
│       ├── BUG-006-broken-logo-asset-404.png
│       ├── BUG-007-typo-contact-massage.png
│       └── BUG-007-typos-related-products.png
│
├── features/                       # Skenario BDD / Gherkin
│   └── auth_profile_navigation.feature # 12 skenario Gherkin (Registrasi, Login, Profil, Navigasi)
│
├── pages/                          # Page Object Model (POM) Berbasis Keyword
│   ├── Common.robot                # Browser lifecycle, helper interaksi, headed switcher
│   ├── HomePage.robot              # Komponen halaman beranda, katalog produk & navigasi
│   ├── LoginPage.robot             # Form login, submit button, pesan validasi/error
│   ├── RegisterPage.robot          # Form registrasi komprehensif & validasi
│   ├── ProfilePage.robot           # Halaman akun pengguna, edit profil, update verifikasi
│   ├── ProductDetailPage.robot    # Detail produk, kuantitas, add-to-cart, toast alert
│   └── CheckoutPage.robot          # Keranjang belanja, stepper multi-step, payment & invoice
│
├── resources/                      # Library kustom & utility pendukung
│   └── DataHelper.py               # Generator data dinamis (timestamp email, unique data)
│
├── results/                        # Output hasil eksekusi Robot Framework (HTML & XML)
│   ├── log.html                    # Log hierarki keyword & step-by-step
│   ├── report.html                 # Ringkasan eksekutif status PASS/FAIL
│   └── output.xml                  # Machine-readable output untuk integrasi CI/CD
│
├── scripts/                        # Utility developer
│   └── generate_unified_test_design.py # Script sinkronisasi 100% paritas MD -> Excel & PDF
│
└── tests/                          # Test Suite Robot Framework
    ├── 01_register.robot           # Otomasi alur pendaftaran akun baru
    ├── 02_login_data_driven.robot  # Otomasi pengujian login data-driven (JSON)
    ├── 03_edit_profile.robot       # Otomasi alur modifikasi profil pengguna
    └── 04_e2e_checkout.robot       # Otomasi End-to-End (E2E) pencarian hingga checkout
```

---

## 🎯 Pemetaan Deliverables

Semua instruksi pada dokumen soal teknis telah dipenuhi pada lokasi file berikut:

| Bagian | Deskripsi Soal | File Deliverable | Status |
| :--- | :--- | :--- | :---: |
| **Bagian 1** (35%) | File Gherkin / BDD (`.feature`) | [`features/auth_profile_navigation.feature`](file:///c:/genesis-sage-automation/logique-qa-assessment/features/auth_profile_navigation.feature) | ✅ **100% Selesai** |
| **Bagian 1** (35%) | Test Case Document (Excel, PDF, MD) | [`docs/01-test-design.xlsx`](file:///c:/genesis-sage-automation/logique-qa-assessment/docs/01-test-design.xlsx)<br>[`docs/01-test-design.pdf`](file:///c:/genesis-sage-automation/logique-qa-assessment/docs/01-test-design.pdf)<br>[`docs/01-test-design.md`](file:///c:/genesis-sage-automation/logique-qa-assessment/docs/01-test-design.md) | ✅ **100% Selesai (Paritas Penuh)** |
| **Bagian 2** (35%) | Framework & Script Automation | [`tests/`](file:///c:/genesis-sage-automation/logique-qa-assessment/tests/) & [`pages/`](file:///c:/genesis-sage-automation/logique-qa-assessment/pages/) | ✅ **100% Selesai (5/5 PASS)** |
| **Bagian 2** (35%) | Test Report (HTML Report) | [`results/report.html`](file:///c:/genesis-sage-automation/logique-qa-assessment/results/report.html)<br>[`results/log.html`](file:///c:/genesis-sage-automation/logique-qa-assessment/results/log.html) | ✅ **Ter-generate Sempurna** |
| **Bagian 3** (30%) | Bug Hunting Report + Evidence | [`docs/03-bug-report.xlsx`](file:///c:/genesis-sage-automation/logique-qa-assessment/docs/03-bug-report.xlsx) *(Excel + Embedded Screenshots)*<br>[`docs/03-bug-report.md`](file:///c:/genesis-sage-automation/logique-qa-assessment/docs/03-bug-report.md)<br>[`docs/evidence/`](file:///c:/genesis-sage-automation/logique-qa-assessment/docs/evidence/) | ✅ **7 Bug Terverifikasi** |


---

## 💻 Prasyarat & Lingkungan

Pastikan sistem penguji memiliki komponen berikut:
- **Python**: Versi `3.10` atau `3.11` (direkomendasikan)
- **Google Chrome**: Versi stabil terbaru
- **ChromeDriver**: Tidak perlu diunduh manual; Selenium 4 / SeleniumLibrary 6.2.0 menggunakan Selenium Manager bawaan untuk mendeteksi dan mengunduh driver yang sesuai secara otomatis.

---

## 🚀 Panduan Instalasi & Setup

1. **Clone atau Buka Direktori Repositori:**
   ```bash
   cd c:/genesis-sage-automation/logique-qa-assessment
   ```

2. **Buat & Aktifkan Python Virtual Environment (Disarankan):**
   *Pada Windows (PowerShell):*
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   *Pada Linux / macOS:*
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚡ Cara Menjalankan Test (1-Command Run)

### 1. Menjalankan Seluruh Test Suite (Rekomendasi Default — Headless)
Jalankan satu perintah ini di root direktori project:
```bash
robot -d results tests/
```
*Perintah ini akan mengeksekusi 4 suite (5 skenario pengujian) secara otomatis dalam mode headless yang cepat, stabil, dan ramah lingkungan CI/CD.*

---

### 2. Menjalankan Test Suite Tertentu
Jika ingin menjalankan suite spesifik:
- **Registrasi Akun Baru:**
  ```bash
  robot -d results tests/01_register.robot
  ```
- **Login Data-Driven (Membaca file JSON):**
  ```bash
  robot -d results tests/02_login_data_driven.robot
  ```
- **Edit & Update Profil Pengguna:**
  ```bash
  robot -d results tests/03_edit_profile.robot
  ```
- **End-to-End (E2E) Pembelian Produk hingga Invoice:**
  ```bash
  robot -d results tests/04_e2e_checkout.robot
  ```

---

### 3. Menjalankan Berdasarkan Tag Pengujian
Framework dilengkapi dengan penandaan tag yang terstruktur:
- **Smoke Tests:**
  ```bash
  robot -i smoke -d results tests/
  ```
- **Regression Tests:**
  ```bash
  robot -i regression -d results tests/
  ```
- **E2E Flow:**
  ```bash
  robot -i e2e -d results tests/
  ```

---

## 🖥️ Fleksibilitas Headed vs Headless

Framework ini dirancang sangat fleksibel sehingga pengguna dapat berpindah antara mode **Headless** (tanpa browser visual) dan **Headed** (browser visual terlihat) dengan sangat mudah melalui 2 metode:

### Metode 1: Lewat Parameter Command-Line (Tanpa Mengubah Kode)
Cukup tambahkan flag `-v HEADLESS:false`:
```bash
robot -v HEADLESS:false -d results tests/
```
*Browser Chrome visual akan langsung terbuka di layar Anda selama pengujian berjalan.*

### Metode 2: Mengubah Keyword Setup di File Test
Pada bagian `*** Settings ***` di file test manapun, Anda dapat langsung mengetikkan `CHROME`:
```robot
*** Settings ***
# Ganti dari:
# Test Setup       Open Application Browser
# Menjadi:
Test Setup          CHROME
Test Teardown       Close Application Browser
```
*Keyword `CHROME` telah didefinisikan di `pages/Common.robot` untuk secara instan meluncurkan browser visual dengan window maximised.*

---

## 📊 Cara Melihat Test Report

Setelah eksekusi selesai, Robot Framework otomatis menghasilkan laporan interaktif di folder `results/`:

1. **Buka Laporan Ringkasan (Report):**
   - File: `results/report.html`
   - Berisi grafik ringkasan persentase PASS/FAIL, durasi pengujian, dan status per test suite.
   - Buka langsung di browser:
     ```powershell
     start results/report.html
     ```

2. **Buka Laporan Detail & Troubleshooting (Log):**
   - File: `results/log.html`
   - Berisi catatan hierarkis langkah per langkah, nilai variabel runtime, response interaksi DOM, dan screenshot kegagalan (jika ada).
   - Buka langsung di browser:
     ```powershell
     start results/log.html
     ```

---

## 💡 Justifikasi Pemilihan Tools & Library

Pemilihan teknologi otomasi didasarkan pada analisis mendalam terhadap kebutuhan teknis dan operasional:

1. **Robot Framework 7.0:**
   - **Keterbacaan Tinggi & Abstraksi Keyword-Driven:** Memungkinkan tim QA, Developer, dan Product Owner memahami skenario pengujian tanpa harus membaca detail implementasi kode internal.
   - **Laporan Bawaan yang Sangat Komprehensif:** Tidak memerlukan integrasi plugin pihak ketiga (seperti Allure) untuk mendapatkan grafik metrik dan log step-by-step yang rapi.
   - **Modular & Extensible:** Integrasi mulus antara sintaks Robot Framework dan modul logika Python kustom (`resources/DataHelper.py`).
   - **Adopsi Industri Luas:** Robot Framework merupakan standar de-facto yang telah terbukti kehandalannya di berbagai perusahaan multinasional dan digital agency.

2. **SeleniumLibrary 6.2.0 & Selenium 4:**
   - **Dukungan W3C WebDriver Baku:** Mendukung penanganan elemen web modern, AJAX rendering dinamis, modal backdrop, dan interaksi form kompleks.
   - **Zero-Config WebDriver:** Dilengkapi dengan driver management otomatis sehingga reviewer tidak perlu repot mencari versi ChromeDriver manual.

3. **Page Object Model (POM):**
   - Menjamin prinsip **DRY (Don't Repeat Yourself)** dan kemudahan pemeliharaan (*maintainability*). Perubahan selector locator pada halaman web hanya memerlukan perbaikan pada 1 file page terkait.

4. **Data-Driven Architecture:**
   - Pemisahan data pengujian dari kode skenario (menggunakan `data/login_test_data.json`) memudahkan penambahan *edge cases* baru tanpa risiko regresi skrip.

---

## 🔍 Asumsi & Batasan (Assumptions & Limitations)

1. **Lingkungan Pengujian Target:**
   - Pengujian otomasi Bagian 2 ditargetkan pada aplikasi stabil `https://practicesoftwaretesting.com`.
   - Bug hunting Bagian 3 ditargetkan khusus pada domain buggy `https://with-bugs.practicesoftwaretesting.com`.
2. **Penanganan Data Akun Registrasi:**
   - Sistem aplikasi target memvalidasi keunikan email pada proses registrasi. Framework menggunakan utility `Generate Unique Email` berbasis timestamp presisi milidetik agar eksekusi test bersifat idempoten dan tidak pernah gagal karena email terduplikasi.
3. **Simulasi Pembayaran E2E:**
   - Pada alur checkout, pengujian memilih metode pembayaran `Cash on Delivery` atau `Bank Transfer` untuk memvalidasi alur pesanan hingga terbentuk nomor invoice resmi tanpa membutuhkan integrasi gateway pihak ketiga yang sebenarnya.
4. **Latency Jaringan Publik:**
   - Mengingat server target adalah server publik demo, framework menerapkan timeout implisit dan eksplisit yang adaptif (10 - 15 detik) untuk menghindari *false negative* akibat fluktuasi jaringan.

---

## ✅ Checklist Verifikasi Sebelum Submit

Berdasarkan lembar panduan penilaian pada halaman 5 dokumen teknis:

- [x] **File Gherkin (.feature)** lengkap dan mengikuti format BDD yang benar (`features/auth_profile_navigation.feature`).
- [x] **Test Case Document** lengkap mencakup preconditions, steps, expected result, dan priority (`docs/01-test-design.md`, `.xlsx`, `.pdf`).
- [x] **100% Paritas Format** antara Markdown, Excel, dan PDF untuk dokumen Test Design.
- [x] **Framework automation** dapat dijalankan dengan 1 perintah tunggal (`robot -d results tests/`).
- [x] **Dukungan Headless & Headed** tersedia via command-line `-v HEADLESS:false` atau keyword `CHROME`.
- [x] **Semua test script PASS** saat dijalankan (5/5 PASS, 100% success rate).
- [x] **Test report** ter-generate dengan rapi dan lengkap (`results/report.html` dan `results/log.html`).
- [x] **Bug report** terdokumentasi lengkap dengan severity, priority, steps to reproduce, actual vs expected, dan bukti visual screenshot (`docs/03-bug-report.md`, `docs/03-bug-report.xlsx` & `docs/evidence/`).
- [x] **README.md** jelas, terstruktur, profesional, dan mudah dipahami.
- [x] **Riwayat Commit Git** granular, bertahap, dan deskriptif mengikuti konvensi Conventional Commits.

