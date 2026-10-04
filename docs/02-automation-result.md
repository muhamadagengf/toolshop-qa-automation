# Laporan Hasil Otomasi Pengujian Web (Bagian 2)
**Kandidat:** Ageng QA  
**Posisi:** QA Engineer / Automation QA  
**SUT (System Under Test):** [Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com)  
**Teknologi / Framework:** Robot Framework 7.0, SeleniumLibrary 6.2.0, Python 3.11  

---

## 1. Ringkasan Eksekutif (Executive Summary)

Pengujian otomatisasi Web pada Bagian 2 dibangun menggunakan **Robot Framework 7.0** dan **SeleniumLibrary**, dengan arsitektur **Page Object Model (POM)**, pemisahan konfigurasi environment, pembuatan test data dinamis mandiri, serta pengujian berbasis data (**Data-Driven Testing**) menggunakan file JSON eksternal.

Seluruh 4 skenario inti yang diwajibkan telah diimplementasikan, dieksekusi secara headless menggunakan Google Chrome, dan mencapai **100% Pass Rate**.

| Metrik | Nilai | Keterangan |
| :--- | :--- | :--- |
| **Total Test Suites** | 4 Suite | Registrasi, Login, Edit Profil, E2E Checkout |
| **Total Test Cases** | 5 Test Case | 1 Positif Reg, 1 Positif Log, 1 Negatif DDT (4 iterasi), 1 Positif Profil, 1 Positif E2E |
| **Total Passed** | **5 / 5 (100%)** | Seluruh asersi fungsional & verifikasi UI terpenuhi |
| **Total Failed** | **0 (0%)** | Bebas failure dan error |
| **Browser Execution** | Chrome Headless | Resolusi 1920x1080 (Desktop standard) |
| **Report File** | `results/report.html` | Laporan interaktif bawaan Robot Framework |

---

## 2. Struktur Repositori & Arsitektur Framework

Framework diorganisir secara modular agar mudah dipelihara (*maintainable*), mudah diperluas (*scalable*), dan memisahkan dengan jelas antara locator, logic, data, dan test spec:

```text
logique-qa-assessment/
├── config/
│   └── env.robot                  # Konfigurasi environment (URL, Browser, Timeout, Headless flag)
├── data/
│   └── login_test_data.json       # Dataset eksternal untuk pengujian Data-Driven login negatif
├── pages/
│   ├── BasePage.robot             # Setup browser, teardown, dan utilitas explicit wait
│   ├── RegisterPage.robot         # Page Object untuk pendaftaran akun customer baru
│   ├── LoginPage.robot            # Page Object untuk autentikasi dan validasi error login
│   ├── ProfilePage.robot          # Page Object untuk update profil dan verifikasi persistensi
│   ├── ProductCatalogPage.robot   # Page Object untuk katalog produk dan pencarian
│   ├── ProductDetailPage.robot    # Page Object untuk detail produk dan penambahan ke keranjang
│   └── CheckoutPage.robot         # Page Object untuk multi-step checkout dan pembayaran COD
├── resources/
│   └── DataHelper.py              # Custom Python Library: generator data user unik & loader JSON
├── tests/
│   ├── 01_register.robot          # Skenario 1: Registrasi user baru dengan data unik dinamis
│   ├── 02_login_data_driven.robot # Skenario 2: Login sukses & validasi negatif berbasis JSON
│   ├── 03_edit_profile.robot      # Skenario 3: Update nomor HP & alamat serta cek data persistence
│   └── 04_e2e_checkout.robot      # Skenario 4: End-to-End checkout belanja produk hingga selesai
├── results/                       # Direktori artefak output (report.html, log.html, output.xml)
└── docs/
    ├── 01-test-design.md          # Dokumen Analisis Risiko & Desain Pengujian (Bagian 1)
    └── 02-automation-result.md    # Dokumen Laporan Hasil Eksekusi Otomasi (Bagian 2)
```

---

## 3. Keputusan Teknis & Rekayasa Solusi Asinkronus (SPA Challenges)

Selama proses otomasi pada aplikasi web modern berbasis Single Page Application (Angular), ditemukan beberapa tantangan teknis spesifik yang diselesaikan melalui pendekatan *engineering* yang kokoh:

### A. Kemandirian Akun & Proteksi Kebocoran Password (Data Leak Defense)
- **Tantangan:** Akun demo publik (`customer@practicesoftwaretesting.com`) terkunci (*"Account locked, too many failed attempts"*) akibat serangan brute-force dari pengguna publik lain. Selain itu, backend API Toolshop menerapkan validasi integritas password terhadap database kebocoran publik (*Have I Been Pwned*), sehingga password umum seperti `SecurePass123!` ditolak dengan HTTP 422 (*"The given password has appeared in a data leak"*). Karakter `#` juga ditolak oleh regex validator aplikasi.
- **Solusi:** `resources/DataHelper.py` meng-generate email unik berbasis timestamp (`ageng_qa_{timestamp}@toolshop-test.org`) serta password acak kuat yang memenuhi aturan kompleksitas namun aman dari daftar kebocoran publik (`Logique{timestamp}!Zx9`). Setiap rangkaian tes mendaftarkan user mandiri sehingga 100% independen dan terisolasi dari gangguan lingkungan bersama.

### B. Race Condition & SPA Form Hydration pada Halaman Profil & Checkout
- **Tantangan:** Pada framework SPA seperti Angular, elemen form input langsung dirender ke DOM dalam keadaan kosong, kemudian sesaat setelahnya Angular mengambil data dari API backend dan meng-hydrate/menimpa nilai form. Jika script otomasi langsung mengetikkan data sebelum proses hidrasi selesai, nilai baru akan tertimpa kembali oleh data lama dari server.
- **Solusi:** Diterapkan keyword explicit polling `Wait Until Keyword Succeeds ${TIMEOUT} 500ms Element Value Should Not Be Empty ${LOCATOR}` pada field acuan (`id=phone` atau `id=street`). Script hanya akan mengisi data baru setelah form selesai melakukan sinkronisasi data awal dari server.

### C. Penanganan Sticky Elements & Floating Widgets
- **Tantangan:** Bottom navigation bar dan widget chat floating pada resolusi tertentu berpotensi menutupi tombol konfirmasi langkah checkout di bagian bawah layar.
- **Solusi:** Menggunakan scroll eksplisit yang dikombinasikan dengan eksekusi event native/JS click yang aman untuk memastikan form submission terpicu tanpa terganggu overlapping layer CSS.

---

## 4. Matriks Hasil Eksekusi Pengujian

Hasil eksekusi test suite per skenario yang dijalankan secara otomatis:

| Suite / File | Test Case ID | Deskripsi Skenario | Tipe Test | Status | Durasi | Validasi Kunci yang Diverifikasi |
| :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| `01_register.robot` | `TC_REG_001` | Registrasi akun baru dengan data dinamis | Positive / Smoke | **PASS** | ~8s | Redirect otomatis ke `/auth/login`, keberadaan form login |
| `02_login_data_driven.robot` | `TC_LOG_001` | Login customer dengan kredensial baru | Positive / Smoke | **PASS** | ~11s | Redirect ke `/account`, menu navigasi profil pengguna muncul |
| `02_login_data_driven.robot` | `TC_LOG_002` | Validasi login negatif data-driven (4 variasi data JSON) | Negative / Regression | **PASS** | ~14s | Pesan error sesuai: *"Invalid email or password"*, *"Email is required"*, *"Password is required"*, tetap di `/auth/login` |
| `03_edit_profile.robot` | `TC_PROF_001` | Edit informasi nomor HP & alamat jalan | Positive / Regression | **PASS** | ~16s | Alert sukses *"Your profile is successfully updated!"*, data persisten setelah refresh halaman (F5) |
| `04_e2e_checkout.robot` | `TC_E2E_001` | End-to-End transaksi pembelian produk (COD) | Positive / E2E | **PASS** | ~22s | Pencarian produk, detail harga, cart badge, multi-step checkout (1-4), konfirmasi *"Payment was successful"* |

---

## 5. Cara Menjalankan Otomasi Pengujian

### Prasyarat
- Python 3.10+ terinstal
- Google Chrome terinstal
- Dependensi Python terinstal:
  ```bash
  pip install robotframework selenium robotframework-seleniumlibrary
  ```

### Perintah Eksekusi

1. **Menjalankan Seluruh Test Suite (Rekomendasi):**
   ```bash
   robot -d results tests/
   ```

2. **Menjalankan per File Skenario Spesifik:**
   ```bash
   # Skenario 1: Registrasi
   robot -d results tests/01_register.robot

   # Skenario 2: Login Positif & Data-Driven
   robot -d results tests/02_login_data_driven.robot

   # Skenario 3: Edit Profil & Cek Data Persistence
   robot -d results tests/03_edit_profile.robot

   # Skenario 4: E2E Checkout Belanja
   robot -d results tests/04_e2e_checkout.robot
   ```

3. **Menjalankan Berdasarkan Tag:**
   ```bash
   # Menjalankan smoke test
   robot -d results -i smoke tests/

   # Menjalankan regression test
   robot -d results -i regression tests/
   ```

4. **Membuka Laporan Hasil Pengujian:**
   Buka file laporan HTML pada browser:
   - `results/report.html` (Ringkasan statistik grafis eksekusi)
   - `results/log.html` (Detail langkah eksekusi per keyword, nilai variabel, dan screenshot otomatis jika terjadi kegagalan)
