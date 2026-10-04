import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import subprocess
import os

# =============================================================================
# SINGLE SOURCE OF TRUTH DATA MODEL
# =============================================================================

DOC_INFO = {
    "title": "TECHNICAL TEST - QA",
    "subtitle": "PT Logika Sarana Teknologi (Logique)",
    "section": "Bagian 1: Analytical & Test Design (35%)",
    "target_app": "Practice Software Testing (Toolshop)",
    "target_url": "https://practicesoftwaretesting.com",
    "api_doc": "https://api.practicesoftwaretesting.com/docs?api-docs.json",
    "scope": "Register, Login, Edit Profile (termasuk Ganti Password), Navigasi Menu",
    "author": "QA Automation Engineering Candidate",
    "date": "Oktober 2026",
    "deliverables": "01-test-design.xlsx, 01-test-design.pdf, 01-test-design.md, features/auth_profile_navigation.feature"
}

RISKS = [
    {
        "id": "R-01",
        "area": "Autentikasi & Penyimpanan Sesi (Session Hijacking / Broken Auth)",
        "likelihood": 2,
        "impact": 3,
        "score": 6,
        "level": "High",
        "reason": "Jika token autentikasi tidak diamankan dengan benar atau sesi tidak dibatalkan saat logout/ganti password, akun pengguna rentan diambil alih.",
        "mitigation": "Uji ketahanan sesi, verifikasi pembatalan token pasca logout dan ganti password, validasi proteksi route private."
    },
    {
        "id": "R-02",
        "area": "Validasi Aturan Bisnis Batasan Usia (DOB Validation Bypass)",
        "likelihood": 3,
        "impact": 2,
        "score": 6,
        "level": "High",
        "reason": "Toolshop mensyaratkan pengguna berusia 18–75 tahun. Seringkali validasi hanya di UI sehingga rentan dibypass via API payload langsung.",
        "mitigation": "Terapkan Boundary Value Analysis (BVA) pada field tanggal lahir baik melalui UI form maupun integrasi API backend."
    },
    {
        "id": "R-03",
        "area": "Persistensi Data Pembaruan Profil (Data Loss / Desynchronization)",
        "likelihood": 2,
        "impact": 3,
        "score": 6,
        "level": "High",
        "reason": "Pengguna yang memperbarui alamat pengiriman atau nomor telepon dapat mengalami kegagalan simpan, berakibat salah alamat pengiriman saat checkout.",
        "mitigation": "Uji skenario update, refresh browser (F5), verifikasi data tersimpan di backend, dan lakukan pemesanan dengan data baru."
    },
    {
        "id": "R-04",
        "area": "Penggantian Password Tanpa Validasi Password Lama yang Kuat",
        "likelihood": 2,
        "impact": 3,
        "score": 6,
        "level": "High",
        "reason": "Jika endpoint ganti password tidak memvalidasi kecocokan password lama atau mengizinkan password baru yang lemah, akun mudah dikompromikan.",
        "mitigation": "Uji penolakan ketika password lama salah, serta uji aturan kompleksitas password baru (huruf besar, kecil, angka, simbol)."
    },
    {
        "id": "R-05",
        "area": "Duplikasi Email & Pendaftaran Akun Bersamaan (Race Condition)",
        "likelihood": 3,
        "impact": 2,
        "score": 6,
        "level": "High",
        "reason": "Registrasi dengan email yang sama secara bersamaan berisiko menyebabkan data corrupt atau akun ganda jika tidak ada unique constraint di DB.",
        "mitigation": "Uji negative pendaftaran dengan email terdaftar, uji respon status HTTP 422/409, dan feedback pesan error pada UI."
    },
    {
        "id": "R-06",
        "area": "Keamanan Input Form (Cross-Site Scripting / SQLi pada Profile)",
        "likelihood": 2,
        "impact": 3,
        "score": 6,
        "level": "High",
        "reason": "Field profil (nama, alamat, kota) yang tidak disanitasi dapat menjadi celah Stored XSS saat ditampilkan di dashboard atau invoice.",
        "mitigation": "Uji karakter spesial, tag HTML (<script>, <b>), kutip tunggal/ganda, dan verifikasi enkoding karakter pada UI."
    },
    {
        "id": "R-07",
        "area": "Inkonsistensi Filter & Navigasi Kategori Produk (Broken Routing)",
        "likelihood": 2,
        "impact": 2,
        "score": 4,
        "level": "Medium",
        "reason": "Jika routing kategori (Hand Tools, Power Tools) bermasalah atau state kategori tidak sync dengan URL query, katalog produk gagal tampil.",
        "mitigation": "Uji navigasi menu bertingkat, verifikasi sinkronisasi URL slug, validasi jumlah dan relevansi produk yang terfilter."
    }
]

BDD_SCENARIOS = [
    {
        "id": "SCN-01",
        "feature": "User Authentication",
        "type": "Scenario",
        "tags": "@auth @register @smoke @positive",
        "title": "Successful customer registration with valid personal details",
        "steps": [
            "Given the customer navigates to the registration page",
            "When the customer submits the registration form with valid and complete personal information",
            "Then the system should register the new account successfully",
            "And the customer should be redirected to the login page with a success confirmation"
        ],
        "examples": None
    },
    {
        "id": "SCN-02",
        "feature": "User Authentication",
        "type": "Scenario",
        "tags": "@auth @register @negative",
        "title": "Registration rejected when applicant is under legal age (under 18 years old)",
        "steps": [
            "Given the customer navigates to the registration page",
            "When the customer attempts to register with a date of birth indicating age younger than 18 years",
            "Then the system should reject the registration submission",
            "And an age validation error stating that the customer must be at least 18 years old should be displayed"
        ],
        "examples": None
    },
    {
        "id": "SCN-03",
        "feature": "User Authentication",
        "type": "Scenario Outline",
        "tags": "@auth @login @data-driven",
        "title": "Customer login attempts with various credential states",
        "steps": [
            "Given the customer navigates to the login page",
            "When the customer attempts to sign in with email \"<email>\" and password \"<password>\"",
            "Then the authentication outcome should be \"<status>\"",
            "And the customer should receive the expected message \"<expected_message>\""
        ],
        "examples": [
            {"email": "customer@practicesoftwaretesting.com", "password": "welcome01", "status": "SUCCESS", "expected_message": "User dashboard displayed"},
            {"email": "customer@practicesoftwaretesting.com", "password": "WrongPassword99!", "status": "FAILED", "expected_message": "Invalid email or password"},
            {"email": "unregistered.user.2026@test.com", "password": "ValidPass#2026", "status": "FAILED", "expected_message": "Invalid email or password"},
            {"email": "", "password": "ValidPass#2026", "status": "FAILED", "expected_message": "E-mail is required"},
            {"email": "customer@practicesoftwaretesting.com", "password": "", "status": "FAILED", "expected_message": "Password is required"}
        ]
    },
    {
        "id": "SCN-04",
        "feature": "Profile Management",
        "type": "Scenario",
        "tags": "@profile @positive",
        "title": "Successful update of customer profile details",
        "steps": [
            "Given the customer is authenticated with an active account",
            "And the customer accesses the account profile settings",
            "When the customer updates the phone number and residential address with new details",
            "Then the updated profile should be saved successfully",
            "And the new information should persist upon reloading the profile page"
        ],
        "examples": None
    },
    {
        "id": "SCN-05",
        "feature": "Profile Management",
        "type": "Scenario",
        "tags": "@profile @password @negative",
        "title": "Password change rejected when new password does not satisfy security complexity",
        "steps": [
            "Given the customer is authenticated with an active account",
            "And the customer accesses the change password page",
            "When the customer attempts to set a weak new password lacking numbers or special characters",
            "Then the system should reject the password update request",
            "And a password complexity warning should prompt the customer to fulfill security requirements"
        ],
        "examples": None
    },
    {
        "id": "SCN-06",
        "feature": "Profile Management",
        "type": "Scenario",
        "tags": "@profile @password @positive",
        "title": "Successful password change and re-authentication with new password",
        "steps": [
            "Given the customer is authenticated with an active account",
            "And the customer accesses the change password page",
            "When the customer submits the correct current password and a valid new compliant password",
            "Then the account password should be updated successfully",
            "And the customer should be able to log in with the new password in a new session"
        ],
        "examples": None
    },
    {
        "id": "SCN-07",
        "feature": "Navigation Menu",
        "type": "Scenario",
        "tags": "@navigation @catalog @positive",
        "title": "Targeted product catalog filtering through header category menu",
        "steps": [
            "When the customer navigates to \"Power Tools\" via the top categories navigation menu",
            "Then the product catalog view should display only products classified under \"Power Tools\"",
            "And the page header and breadcrumb should display \"Power Tools\""
        ],
        "examples": None
    }
]

TEST_CASES = [
    {
        "id": "TC-REG-01",
        "title": "Registrasi user baru dengan data lengkap & valid",
        "precondition": "Berada di halaman utama Toolshop, user belum login",
        "test_data": "Nama: John Doe, DOB: 1995-05-20 (31 thn), Email: test_<timestamp>@auto.org, Password: Password@123, Alamat lengkap terisi",
        "steps": "1. Buka menu Sign in -> Klik link Register.\n2. Isi seluruh field dengan data valid.\n3. Klik tombol 'Register'.",
        "expected": "Berhasil register, redirect otomatis ke URL /auth/login, dan menampilkan pesan sukses pendaftaran.",
        "priority": "High",
        "technique": "Equivalence Partitioning (Valid)",
        "link": "Scenario 1 / R-02"
    },
    {
        "id": "TC-REG-02",
        "title": "Registrasi ditolak saat usia pendaftar di bawah 18 tahun",
        "precondition": "Berada di halaman /auth/register",
        "test_data": "DOB dihitung hari ini - 17 tahun 364 hari (contoh: 2008-10-05), field lain valid",
        "steps": "1. Lengkapi form registrasi dengan data valid.\n2. Input DOB dengan usia 17 tahun.\n3. Klik tombol 'Register'.",
        "expected": "Tombol Register diblokir atau form memunculkan pesan validasi: usia minimal pendaftar adalah 18 tahun. Tidak ada user yang tersimpan di DB.",
        "priority": "High",
        "technique": "Boundary Value Analysis (Invalid Boundary)",
        "link": "Scenario 2 / R-02"
    },
    {
        "id": "TC-REG-03",
        "title": "Registrasi ditolak saat email sudah terdaftar sebelumnya",
        "precondition": "Akun dengan email target sudah aktif di sistem",
        "test_data": "Email: customer@practicesoftwaretesting.com, field lain valid",
        "steps": "1. Buka form registrasi.\n2. Isi field email dengan email yang sudah ada.\n3. Klik tombol 'Register'.",
        "expected": "Pendaftaran gagal, sistem menampilkan pesan error bahwa alamat email sudah digunakan (E-mail already exists).",
        "priority": "High",
        "technique": "Error Guessing",
        "link": "Scenario 1 / R-05"
    },
    {
        "id": "TC-LOG-01",
        "title": "Login berhasil dengan kredensial valid",
        "precondition": "User sudah terdaftar dan berstatus aktif",
        "test_data": "Email: customer@practicesoftwaretesting.com, Password: welcome01",
        "steps": "1. Akses halaman /auth/login.\n2. Input email dan password yang benar.\n3. Klik tombol 'Login'.",
        "expected": "Berhasil terotentikasi, redirect ke halaman akun/dashboard (/account), nama user muncul di header navigasi.",
        "priority": "High",
        "technique": "Decision Table (Rule 1)",
        "link": "Scenario 3 / R-01"
    },
    {
        "id": "TC-LOG-02",
        "title": "Login ditolak ketika password salah",
        "precondition": "User sudah terdaftar",
        "test_data": "Email: customer@practicesoftwaretesting.com, Password: SalahPassword#99",
        "steps": "1. Akses /auth/login.\n2. Input email valid dan password yang salah.\n3. Klik tombol 'Login'.",
        "expected": "Tetap di halaman login, muncul pesan peringatan: 'Invalid email or password', token sesi tidak dibuat.",
        "priority": "High",
        "technique": "Decision Table (Rule 3)",
        "link": "Scenario 3 / R-01"
    },
    {
        "id": "TC-LOG-03",
        "title": "Validasi client-side ketika field email dan password dikosongkan",
        "precondition": "Berada di halaman /auth/login",
        "test_data": "Email: \"\" (kosong), Password: \"\" (kosong)",
        "steps": "1. Klik input email lalu tinggalkan kosong.\n2. Klik input password lalu tinggalkan kosong.\n3. Periksa feedback UI.",
        "expected": "Muncul pesan error validasi: 'E-mail is required' dan 'Password is required', tombol login tidak menjalankan proses POST.",
        "priority": "Medium",
        "technique": "Equivalence Partitioning (Empty Input)",
        "link": "Scenario 3 / R-01"
    },
    {
        "id": "TC-PRF-01",
        "title": "Update data profil (alamat & nomor telepon) dan verifikasi persistensi",
        "precondition": "User login dan berada di halaman /account/profile",
        "test_data": "Phone: 081298765432, Address: Jl. Melati No. 45, City: Jakarta",
        "steps": "1. Ubah nomor telepon dan alamat rumah.\n2. Klik tombol 'Update Profile'.\n3. Reload browser page (F5).\n4. Periksa isi field form.",
        "expected": "Muncul notifikasi profil berhasil diperbarui, dan setelah reload data yang baru tetap tersimpan pada field form.",
        "priority": "High",
        "technique": "State Transition Testing",
        "link": "Scenario 4 / R-03"
    },
    {
        "id": "TC-PWD-01",
        "title": "Penggantian password gagal jika password baru tidak memenuhi kompleksitas",
        "precondition": "User login dan berada di halaman ganti password",
        "test_data": "Current Pass: welcome01, New Pass: simplepass (tanpa angka/simbol)",
        "steps": "1. Buka tab Change Password.\n2. Masukkan password lama yang valid.\n3. Masukkan password baru yang lemah.\n4. Klik tombol simpan.",
        "expected": "Sistem menolak perubahan password, muncul indikator atau pesan bahwa password harus memiliki huruf besar, kecil, angka, dan simbol.",
        "priority": "High",
        "technique": "Boundary & Decision Table",
        "link": "Scenario 5 / R-04"
    },
    {
        "id": "TC-NAV-01",
        "title": "Navigasi menu kategori produk (Power Tools)",
        "precondition": "User berada di beranda situs",
        "test_data": "Kategori: Power Tools (Slug: power-tools)",
        "steps": "1. Klik menu dropdown 'Categories'.\n2. Pilih 'Power Tools'.\n3. Verifikasi halaman katalog produk yang ditampilkan.",
        "expected": "URL berubah menjadi /category/power-tools, judul halaman menampilkan 'Power Tools', dan seluruh kartu produk yang tampil sesuai kategori.",
        "priority": "Medium",
        "technique": "State Transition Testing",
        "link": "Scenario 7 / R-07"
    }
]

TECH_EP = [
    {"partisi": "P1", "rentang": "Usia < 18 tahun (Minor)", "contoh": "2012-05-10 (14 tahun)", "status": "Invalid", "expected": "Ditolak dengan pesan: usia minimal 18 tahun"},
    {"partisi": "P2", "rentang": "18 tahun <= Usia <= 75 tahun (Legal)", "contoh": "1990-08-15 (36 tahun)", "status": "Valid", "expected": "Diterima, registrasi dapat dilanjutkan"},
    {"partisi": "P3", "rentang": "Usia > 75 tahun (Senior di atas batas)", "contoh": "1945-01-01 (81 tahun)", "status": "Invalid", "expected": "Ditolak dengan pesan: usia maksimal 75 tahun"},
    {"partisi": "P4", "rentang": "Tanggal di masa depan (Future Date)", "contoh": "2028-01-01 (-2 tahun)", "status": "Invalid", "expected": "Ditolak dengan pesan: tanggal lahir tidak valid"},
    {"partisi": "P5", "rentang": "Format tanggal tidak sesuai / string acak", "contoh": "abc-def-ghij", "status": "Invalid", "expected": "Validasi format input YYYY-MM-DD"}
]

TECH_BVA = [
    {"titik": "BVA-01", "nilai": "2008-10-05 (17 thn 364 hari)", "representasi": "Just below minimum boundary (18 - 1 hari)", "status": "Invalid", "expected": "Ditolak (Error: usia < 18 thn)"},
    {"titik": "BVA-02", "nilai": "2008-10-04 (Tepat 18 tahun hari ini)", "representasi": "Exact minimum valid boundary (18)", "status": "Valid", "expected": "Diterima"},
    {"titik": "BVA-03", "nilai": "2008-10-03 (18 thn 1 hari)", "representasi": "Just above minimum boundary (18 + 1 hari)", "status": "Valid", "expected": "Diterima"},
    {"titik": "BVA-04", "nilai": "1951-10-05 (74 thn 364 hari)", "representasi": "Just below maximum boundary (75 - 1 hari)", "status": "Valid", "expected": "Diterima"},
    {"titik": "BVA-05", "nilai": "1951-10-04 (Tepat 75 tahun hari ini)", "representasi": "Exact maximum valid boundary (75)", "status": "Valid", "expected": "Diterima"},
    {"titik": "BVA-06", "nilai": "1951-10-03 (75 thn 1 hari)", "representasi": "Just above maximum boundary (75 + 1 hari)", "status": "Invalid", "expected": "Ditolak (Error: usia > 75 thn)"}
]

TECH_DT = {
    "conditions": [
        ("C1: Format Email Valid", ["Y", "Y", "Y", "T", "Y", "T"]),
        ("C2: Email Terdaftar di Database", ["Y", "Y", "T", "-", "Y", "-"]),
        ("C3: Password Cocok dengan Hash", ["Y", "T", "-", "-", "-", "-"]),
        ("C4: Field Password Terisi", ["Y", "Y", "Y", "Y", "T", "T"])
    ],
    "actions": [
        ("A1: Otentikasi Berhasil & Buat Token Sesi", ["X", "", "", "", "", ""]),
        ("A2: Redirect ke /account Dashboard", ["X", "", "", "", "", ""]),
        ("A3: Tampilkan Pesan 'Invalid email or password'", ["", "X", "X", "", "", ""]),
        ("A4: Tampilkan Validasi 'Format e-mail tidak valid'", ["", "", "", "X", "", ""]),
        ("A5: Tampilkan Validasi 'Password is required'", ["", "", "", "", "X", "X"]),
        ("A6: Catat Percobaan Gagal (Security Audit Log)", ["", "X", "X", "", "", ""])
    ]
}

TECH_ST = [
    {"current": "S0: Guest (Unauthenticated)", "trigger": "Input data valid & klik Register", "action": "Kirim data registrasi ke API /users/register, simpan data", "next": "S1: Registered"},
    {"current": "S1: Registered", "trigger": "Redirect ke /auth/login", "action": "Render form login dengan notifikasi pendaftaran", "next": "S0: Guest"},
    {"current": "S0: Guest", "trigger": "Masukkan kredensial valid & klik Login", "action": "Validasi DB, terbitkan JWT token, simpan ke sessionStorage", "next": "S2: Authenticated"},
    {"current": "S2: Authenticated", "trigger": "Ubah data profil & klik Update", "action": "Kirim PUT /users/me, update database", "next": "S3: Profile Updated"},
    {"current": "S3: Profile Updated", "trigger": "Refresh halaman browser (F5)", "action": "Ambil data terbaru dari GET /users/me", "next": "S3: Profile Updated"},
    {"current": "S2: Authenticated", "trigger": "Masukkan password lama + baru & klik Simpan", "action": "Kirim POST /users/change-password, enkripsi password baru", "next": "S4: Password Changed"},
    {"current": "S2: Authenticated", "trigger": "Klik tombol 'Sign Out'", "action": "Hapus JWT token dan info akun dari browser storage", "next": "S0: Guest"}
]

OUT_OF_SCOPE = [
    {"no": 1, "fitur": "Verifikasi Email via Tautan SMTP / OTP", "alasan": "Aplikasi demo Toolshop secara sengaja langsung mengaktifkan akun saat form registrasi di-submit tanpa mengirimkan email verifikasi nyata ke inbox."},
    {"no": 2, "fitur": "Transaksi Kartu Kredit / Payment Gateway Riil", "alasan": "Lingkup Bagian 1 difokuskan pada manajemen pengguna (Register, Login, Edit Profile, Navigasi). Pemrosesan pembayaran berada di luar modul autentikasi akun."},
    {"no": 3, "fitur": "Integrasi Social Login (OAuth 2.0 via Google / Facebook)", "alasan": "Fitur social login tidak diimplementasikan pada aplikasi Toolshop ini."},
    {"no": 4, "fitur": "Security Penetration Testing Mendalam (DAST / SQL Injection Payload Injection)", "alasan": "Pengujian pada Bagian 1 berfokus pada fungsionalitas dan test design berbasis BDD, bukan automated security auditing."}
]

ASSUMPTIONS = [
    {"no": 1, "aspek": "Lingkungan Pengujian", "deskripsi": "Aplikasi target diakses melalui domain resmi https://practicesoftwaretesting.com yang berjalan pada environment staging/demo publik yang stabil."},
    {"no": 2, "aspek": "Kemandirian Data Uji (Test Data Isolation)", "deskripsi": "Setiap eksekusi registrasi menggunakan generator data unik (misalnya email berformat user_<timestamp>@mailslurp.biz) guna mencegah kegagalan akibat bentrok email unik yang sudah terdaftar sebelumnya."},
    {"no": 3, "aspek": "Waktu Server & Lokasi", "deskripsi": "Perhitungan batasan usia 18–75 tahun mengacu pada tanggal sistem saat pengujian dijalankan."},
    {"no": 4, "aspek": "Kompatibilitas Browser", "deskripsi": "Pengujian dirancang untuk kompatibilitas browser berbasis Chromium modern (Google Chrome, Microsoft Edge)."}
]

# =============================================================================
# 1. EXCEL BUILDER (openpyxl)
# =============================================================================

def build_excel(file_path):
    wb = openpyxl.Workbook()
    
    # Styles
    HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    SUBHEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    ZEBRA_FILL = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    HIGH_FILL = PatternFill(start_color="FED7D7", end_color="FED7D7", fill_type="solid")
    MED_FILL = PatternFill(start_color="FEFCBF", end_color="FEFCBF", fill_type="solid")
    VALID_FILL = PatternFill(start_color="C6F6D5", end_color="C6F6D5", fill_type="solid")

    FONT_TITLE = Font(name="Calibri", size=14, bold=True, color="1F4E79")
    FONT_SECTION = Font(name="Calibri", size=11, bold=True, color="1F4E79")
    FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    FONT_BOLD = Font(name="Calibri", size=9, bold=True, color="000000")
    FONT_REGULAR = Font(name="Calibri", size=9, color="000000")

    BORDER_THIN = Border(
        left=Side(style='thin', color='CBD5E0'),
        right=Side(style='thin', color='CBD5E0'),
        top=Side(style='thin', color='CBD5E0'),
        bottom=Side(style='thin', color='CBD5E0')
    )
    BORDER_HEADER = Border(
        left=Side(style='thin', color='1F4E79'),
        right=Side(style='thin', color='1F4E79'),
        top=Side(style='medium', color='1F4E79'),
        bottom=Side(style='medium', color='1F4E79')
    )

    def style_header(ws, row, headers):
        for col_idx, h in enumerate(headers, start=2):
            cell = ws.cell(row=row, column=col_idx, value=h)
            cell.font = FONT_HEADER
            cell.fill = HEADER_FILL
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = BORDER_HEADER

    # --- Sheet 1: Overview ---
    ws1 = wb.active
    ws1.title = "1. Overview"
    ws1.views.sheetView[0].showGridLines = True
    ws1.cell(row=2, column=2, value=DOC_INFO["title"]).font = FONT_TITLE
    ws1.cell(row=3, column=2, value=f"{DOC_INFO['subtitle']} — {DOC_INFO['section']}").font = FONT_SECTION

    items = [
        ("Aplikasi Target", DOC_INFO["target_app"]),
        ("Target URL", DOC_INFO["target_url"]),
        ("API Documentation", DOC_INFO["api_doc"]),
        ("Lingkup Pengujian", DOC_INFO["scope"]),
        ("Tanggal Pengujian", DOC_INFO["date"]),
        ("Kandidat QA", DOC_INFO["author"]),
        ("File Deliverables", DOC_INFO["deliverables"])
    ]
    for idx, (lbl, val) in enumerate(items, start=5):
        c1 = ws1.cell(row=idx, column=2, value=lbl)
        c1.font = FONT_BOLD
        c1.fill = SUBHEADER_FILL
        c1.border = BORDER_THIN
        c2 = ws1.cell(row=idx, column=3, value=val)
        c2.font = FONT_REGULAR
        c2.border = BORDER_THIN
    ws1.column_dimensions["B"].width = 24
    ws1.column_dimensions["C"].width = 75

    # --- Sheet 2: Risk Analysis ---
    ws2 = wb.create_sheet(title="2. Risk_Analysis")
    ws2.views.sheetView[0].showGridLines = True
    ws2.cell(row=2, column=2, value="1. Risk Analysis & Mitigation Matrix").font = FONT_TITLE
    ws2.cell(row=3, column=2, value="Skor = Likelihood (1-3) x Impact (1-3). Diurutkan dari skor tertinggi.").font = FONT_REGULAR

    risk_h = ["No", "Risk ID", "Area Risiko", "Likelihood (1–3)", "Impact (1–3)", "Risk Score", "Tingkat Risiko", "Alasan & Potensi Dampak", "Strategi Mitigasi / Pengujian"]
    style_header(ws2, 5, risk_h)

    for idx, r in enumerate(RISKS, start=1):
        row_num = 5 + idx
        vals = [idx, r["id"], r["area"], r["likelihood"], r["impact"], r["score"], r["level"], r["reason"], r["mitigation"]]
        for col_idx, val in enumerate(vals, start=2):
            cell = ws2.cell(row=row_num, column=col_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = BORDER_THIN
            if col_idx in [2, 3, 5, 6, 7, 8]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if col_idx == 8:
                    cell.font = FONT_BOLD
                    cell.fill = HIGH_FILL if val == "High" else MED_FILL
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    ws2.column_dimensions["B"].width = 6
    ws2.column_dimensions["C"].width = 10
    ws2.column_dimensions["D"].width = 32
    ws2.column_dimensions["E"].width = 14
    ws2.column_dimensions["F"].width = 14
    ws2.column_dimensions["G"].width = 12
    ws2.column_dimensions["H"].width = 14
    ws2.column_dimensions["I"].width = 45
    ws2.column_dimensions["J"].width = 45

    # --- Sheet 3: BDD Scenarios ---
    ws3 = wb.create_sheet(title="3. BDD_Scenarios")
    ws3.views.sheetView[0].showGridLines = True
    ws3.cell(row=2, column=2, value="2. Test Scenarios (Gherkin / BDD)").font = FONT_TITLE
    ws3.cell(row=3, column=2, value="Skenario berorientasi bisnis (declarative). Tersimpan juga di features/auth_profile_navigation.feature.").font = FONT_REGULAR

    bdd_h = ["Scenario ID", "Feature Group", "Type", "Tags", "Scenario Title", "Gherkin Specification Steps"]
    style_header(ws3, 5, bdd_h)

    cur_row = 6
    for scn in BDD_SCENARIOS:
        steps_text = "\n".join(scn["steps"])
        if scn["examples"]:
            steps_text += "\n\nExamples:\n"
            steps_text += " | ".join(scn["examples"][0].keys()) + "\n"
            for ex in scn["examples"]:
                steps_text += " | ".join(str(v) for v in ex.values()) + "\n"

        vals = [scn["id"], scn["feature"], scn["type"], scn["tags"], scn["title"], steps_text]
        for c_idx, val in enumerate(vals, start=2):
            cell = ws3.cell(row=cur_row, column=c_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = BORDER_THIN
            if c_idx in [2, 4]:
                cell.alignment = Alignment(horizontal="center", vertical="top")
            elif c_idx == 7:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                cell.font = Font(name="Consolas", size=8.5)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
        cur_row += 1

    ws3.column_dimensions["B"].width = 14
    ws3.column_dimensions["C"].width = 22
    ws3.column_dimensions["D"].width = 16
    ws3.column_dimensions["E"].width = 26
    ws3.column_dimensions["F"].width = 36
    ws3.column_dimensions["G"].width = 65

    # --- Sheet 4: Test Cases Detail ---
    ws4 = wb.create_sheet(title="4. Test_Cases_Detail")
    ws4.views.sheetView[0].showGridLines = True
    ws4.cell(row=2, column=2, value="3. Detailed Test Cases Specification").font = FONT_TITLE
    ws4.cell(row=3, column=2, value="Daftar 9 test case komprehensif lengkap dengan 9 atribut wajib.").font = FONT_REGULAR

    tc_h = ["ID", "Judul Test Case", "Precondition", "Test Data", "Steps (Langkah Pengujian)", "Expected Result", "Priority", "Teknik Test Design", "Link ke Scenario / Risk"]
    style_header(ws4, 5, tc_h)

    for idx, tc in enumerate(TEST_CASES, start=1):
        row_num = 5 + idx
        fill_zebra = ZEBRA_FILL if idx % 2 == 0 else PatternFill(fill_type=None)
        vals = [tc["id"], tc["title"], tc["precondition"], tc["test_data"], tc["steps"], tc["expected"], tc["priority"], tc["technique"], tc["link"]]
        for col_idx, val in enumerate(vals, start=2):
            cell = ws4.cell(row=row_num, column=col_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = BORDER_THIN
            if fill_zebra.fill_type:
                cell.fill = fill_zebra
            
            if col_idx in [2, 8]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if col_idx == 8:
                    cell.font = FONT_BOLD
                    cell.fill = HIGH_FILL if val == "High" else MED_FILL
            elif col_idx in [3, 9, 10]:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            else:
                cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

    ws4.column_dimensions["B"].width = 14
    ws4.column_dimensions["C"].width = 28
    ws4.column_dimensions["D"].width = 26
    ws4.column_dimensions["E"].width = 32
    ws4.column_dimensions["F"].width = 40
    ws4.column_dimensions["G"].width = 36
    ws4.column_dimensions["H"].width = 12
    ws4.column_dimensions["I"].width = 28
    ws4.column_dimensions["J"].width = 22

    # --- Sheet 5: Test Design Techniques ---
    ws5 = wb.create_sheet(title="5. Test_Design_Techniques")
    ws5.views.sheetView[0].showGridLines = True
    ws5.cell(row=2, column=2, value="4. Penerapan Teknik Test Design Formal").font = FONT_TITLE
    ws5.cell(row=3, column=2, value="Implementasi konkret 3 teknik: Equivalence Partitioning, Boundary Value Analysis, Decision Table, dan State Transition.").font = FONT_REGULAR

    # 1. EP
    ws5.cell(row=5, column=2, value="4.1. Equivalence Partitioning (EP) - Aturan Batas Usia Tanggal Lahir (18 - 75 Tahun)").font = FONT_SECTION
    ep_h = ["Partisi", "Rentang Nilai (Usia)", "Contoh Input Tanggal Lahir", "Status Partisi", "Expected Result"]
    style_header(ws5, 7, ep_h)
    for idx, item in enumerate(TECH_EP, start=1):
        row_num = 7 + idx
        vals = [item["partisi"], item["rentang"], item["contoh"], item["status"], item["expected"]]
        for col_idx, val in enumerate(vals, start=2):
            cell = ws5.cell(row=row_num, column=col_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = BORDER_THIN
            if col_idx in [2, 5]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if col_idx == 5:
                    cell.font = FONT_BOLD
                    cell.fill = VALID_FILL if val == "Valid" else HIGH_FILL
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    # 2. BVA
    bva_start = 15
    ws5.cell(row=bva_start, column=2, value="4.2. Boundary Value Analysis (BVA) - Titik Batas Umur Relatif terhadap Tanggal Sistem (04-10-2026)").font = FONT_SECTION
    bva_h = ["Titik Uji", "Nilai Uji (Tanggal Lahir)", "Representasi Batas", "Status", "Expected Result"]
    style_header(ws5, bva_start + 2, bva_h)
    for idx, item in enumerate(TECH_BVA, start=1):
        row_num = bva_start + 2 + idx
        vals = [item["titik"], item["nilai"], item["representasi"], item["status"], item["expected"]]
        for col_idx, val in enumerate(vals, start=2):
            cell = ws5.cell(row=row_num, column=col_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = BORDER_THIN
            if col_idx in [2, 5]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if col_idx == 5:
                    cell.font = FONT_BOLD
                    cell.fill = VALID_FILL if val == "Valid" else HIGH_FILL
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    # 3. Decision Table
    dt_start = 26
    ws5.cell(row=dt_start, column=2, value="4.3. Decision Table Testing - Logika Autentikasi Pengguna (Login Validation)").font = FONT_SECTION
    dt_h = ["Kondisi & Aksi Sistem", "Rule 1", "Rule 2", "Rule 3", "Rule 4", "Rule 5", "Rule 6"]
    style_header(ws5, dt_start + 2, dt_h)
    
    dt_rows = []
    for cond, rules in TECH_DT["conditions"]:
        dt_rows.append((cond, rules, False))
    dt_rows.append(("--- AKSI SISTEM (ACTIONS) ---", ["", "", "", "", "", ""], True))
    for act, rules in TECH_DT["actions"]:
        dt_rows.append((act, rules, False))

    for idx, (label, rules, is_sep) in enumerate(dt_rows, start=1):
        row_num = dt_start + 2 + idx
        c_label = ws5.cell(row=row_num, column=2, value=label)
        c_label.font = FONT_BOLD if is_sep else FONT_REGULAR
        c_label.border = BORDER_THIN
        if is_sep:
            c_label.fill = SUBHEADER_FILL
        for r_idx, val in enumerate(rules, start=3):
            cell = ws5.cell(row=row_num, column=r_idx, value=val)
            cell.font = FONT_BOLD if val == "X" else FONT_REGULAR
            cell.border = BORDER_THIN
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if is_sep:
                cell.fill = SUBHEADER_FILL
            elif val == "X":
                cell.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")

    # 4. State Transition
    st_start = dt_start + 3 + len(dt_rows) + 2
    ws5.cell(row=st_start, column=2, value="4.4. State Transition Testing - Siklus Hidup Akun Pelanggan (User Account Lifecycle)").font = FONT_SECTION
    st_h = ["Current State", "Trigger / Event", "Action yang Dijalankan", "Next State"]
    style_header(ws5, st_start + 2, st_h)
    for idx, item in enumerate(TECH_ST, start=1):
        row_num = st_start + 2 + idx
        vals = [item["current"], item["trigger"], item["action"], item["next"]]
        for col_idx, val in enumerate(vals, start=2):
            cell = ws5.cell(row=row_num, column=col_idx, value=val)
            cell.font = FONT_BOLD if col_idx in [2, 5] else FONT_REGULAR
            cell.border = BORDER_THIN
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

    ws5.column_dimensions["B"].width = 28
    ws5.column_dimensions["C"].width = 30
    ws5.column_dimensions["D"].width = 38
    ws5.column_dimensions["E"].width = 28
    ws5.column_dimensions["F"].width = 12
    ws5.column_dimensions["G"].width = 12
    ws5.column_dimensions["H"].width = 12

    # --- Sheet 6: Out of Scope & Assumptions ---
    ws6 = wb.create_sheet(title="6. Out_of_Scope_&_Assumptions")
    ws6.views.sheetView[0].showGridLines = True
    ws6.cell(row=2, column=2, value="5. Out of Scope & Asumsi Pengujian").font = FONT_TITLE

    ws6.cell(row=4, column=2, value="Item Out of Scope (Sengaja Tidak Dites)").font = FONT_SECTION
    oos_h = ["No", "Area / Fitur", "Alasan Eksklusi dari Lingkup Pengujian"]
    style_header(ws6, 6, oos_h)
    for idx, item in enumerate(OUT_OF_SCOPE, start=1):
        row_num = 6 + idx
        vals = [item["no"], item["fitur"], item["alasan"]]
        for col_idx, val in enumerate(vals, start=2):
            cell = ws6.cell(row=row_num, column=col_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = BORDER_THIN
            cell.alignment = Alignment(horizontal="center" if col_idx == 2 else "left", vertical="center", wrap_text=True)

    assump_start = 6 + len(OUT_OF_SCOPE) + 3
    ws6.cell(row=assump_start, column=2, value="Asumsi Pengujian").font = FONT_SECTION
    assump_h = ["No", "Aspek", "Deskripsi Asumsi"]
    style_header(ws6, assump_start + 2, assump_h)
    for idx, item in enumerate(ASSUMPTIONS, start=1):
        row_num = assump_start + 2 + idx
        vals = [item["no"], item["aspek"], item["deskripsi"]]
        for col_idx, val in enumerate(vals, start=2):
            cell = ws6.cell(row=row_num, column=col_idx, value=val)
            cell.font = FONT_REGULAR
            cell.border = BORDER_THIN
            cell.alignment = Alignment(horizontal="center" if col_idx == 2 else "left", vertical="center", wrap_text=True)

    ws6.column_dimensions["B"].width = 8
    ws6.column_dimensions["C"].width = 30
    ws6.column_dimensions["D"].width = 75

    wb.save(file_path)
    print(f"Excel saved successfully at: {file_path}")


# =============================================================================
# 2. PDF BUILDER (HTML -> Chrome Headless)
# =============================================================================

def build_pdf(html_path, pdf_path):
    import html as html_lib
    def esc(s):
        return html_lib.escape(str(s)) if s is not None else ""

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>01 - Analytical & Test Design (QA Technical Test)</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 14mm 10mm 14mm 10mm;
    }}
    body {{
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
      font-size: 8.5pt;
      line-height: 1.4;
      color: #2D3748;
      background-color: #FFFFFF;
      margin: 0;
      padding: 0;
    }}
    .header-banner {{
      border-bottom: 3px solid #1F4E79;
      padding-bottom: 8px;
      margin-bottom: 14px;
    }}
    .company-title {{
      font-size: 16pt;
      font-weight: 800;
      color: #1F4E79;
      margin: 0;
    }}
    .doc-subtitle {{
      font-size: 11pt;
      font-weight: 600;
      color: #4A5568;
      margin-top: 3px;
    }}
    .meta-box {{
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-left: 4px solid #1F4E79;
      padding: 8px 12px;
      border-radius: 4px;
      margin-bottom: 16px;
      font-size: 8pt;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: 130px 1fr 130px 1fr;
      gap: 4px 10px;
    }}
    .meta-label {{
      font-weight: 700;
      color: #1A202C;
    }}
    h2 {{
      font-size: 12pt;
      color: #1F4E79;
      border-bottom: 1.5px solid #CBD5E0;
      padding-bottom: 3px;
      margin-top: 20px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }}
    h3 {{
      font-size: 10pt;
      color: #2B6CB0;
      margin-top: 14px;
      margin-bottom: 6px;
      page-break-after: avoid;
    }}
    p {{
      margin: 0 0 8px 0;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 14px;
      font-size: 8pt;
      page-break-inside: auto;
    }}
    tr {{
      page-break-inside: avoid;
    }}
    th {{
      background-color: #1F4E79;
      color: #FFFFFF;
      font-weight: 700;
      text-align: left;
      padding: 6px 7px;
      border: 1px solid #1A365D;
    }}
    td {{
      padding: 5px 7px;
      border: 1px solid #CBD5E0;
      vertical-align: top;
    }}
    tr:nth-child(even) td {{
      background-color: #F8FAFC;
    }}
    .badge {{
      display: inline-block;
      padding: 2px 6px;
      font-size: 7pt;
      font-weight: 700;
      border-radius: 3px;
      text-align: center;
    }}
    .badge-high {{ background-color: #FED7D7; color: #9B2C2C; border: 1px solid #FEB2B2; }}
    .badge-med {{ background-color: #FEFCBF; color: #975A16; border: 1px solid #F6E05E; }}
    .badge-valid {{ background-color: #C6F6D5; color: #22543D; border: 1px solid #9AE6B4; }}
    .badge-invalid {{ background-color: #FED7D7; color: #9B2C2C; border: 1px solid #FEB2B2; }}
    .text-center {{ text-align: center; }}
    .text-bold {{ font-weight: 700; }}
    .code-block {{
      background-color: #1A202C;
      color: #E2E8F0;
      font-family: 'Consolas', monospace;
      font-size: 7.5pt;
      padding: 10px;
      border-radius: 4px;
      margin-bottom: 12px;
      white-space: pre-wrap;
      line-height: 1.35;
      page-break-inside: avoid;
    }}
    .page-break {{
      page-break-before: always;
      break-before: page;
    }}
  </style>
</head>
<body>

  <div class="header-banner">
    <h1 class="company-title">{esc(DOC_INFO["title"])}</h1>
    <div class="doc-subtitle">{esc(DOC_INFO["subtitle"])} — {esc(DOC_INFO["section"])}</div>
  </div>

  <div class="meta-box">
    <div class="meta-grid">
      <div class="meta-label">Aplikasi Target:</div><div>{esc(DOC_INFO["target_app"])}</div>
      <div class="meta-label">Target URL:</div><div>{esc(DOC_INFO["target_url"])}</div>
      <div class="meta-label">Lingkup Pengujian:</div><div>{esc(DOC_INFO["scope"])}</div>
      <div class="meta-label">Tanggal Pengujian:</div><div>{esc(DOC_INFO["date"])}</div>
      <div class="meta-label">Kandidat QA:</div><div>{esc(DOC_INFO["author"])}</div>
      <div class="meta-label">File Deliverables:</div><div>{esc(DOC_INFO["deliverables"])}</div>
    </div>
  </div>

  <h2>1. Risk Analysis & Mitigation Matrix</h2>
  <p>Analisis risiko terhadap 7 area kritis dengan formula <strong>Likelihood (1–3) &times; Impact (1–3)</strong>. Diurutkan dari skor tertinggi:</p>

  <table>
    <thead>
      <tr>
        <th style="width: 5%;" class="text-center">No</th>
        <th style="width: 9%;" class="text-center">Risk ID</th>
        <th style="width: 25%;">Area Risiko</th>
        <th style="width: 6%;" class="text-center">L (1-3)</th>
        <th style="width: 6%;" class="text-center">I (1-3)</th>
        <th style="width: 7%;" class="text-center">Skor</th>
        <th style="width: 8%;" class="text-center">Level</th>
        <th style="width: 34%;">Alasan & Potensi Dampak</th>
      </tr>
    </thead>
    <tbody>
"""
    for idx, r in enumerate(RISKS, start=1):
        badge = "badge-high" if r["score"] >= 6 else "badge-med"
        html += f"""      <tr>
        <td class="text-center">{idx}</td>
        <td class="text-center text-bold">{esc(r["id"])}</td>
        <td class="text-bold">{esc(r["area"])}</td>
        <td class="text-center">{r["likelihood"]}</td>
        <td class="text-center">{r["impact"]}</td>
        <td class="text-center text-bold">{r["score"]}</td>
        <td class="text-center"><span class="badge {badge}">{esc(r["level"])}</span></td>
        <td>{esc(r["reason"])}<br><strong>Mitigasi:</strong> {esc(r["mitigation"])}</td>
      </tr>
"""
    html += """    </tbody>
  </table>

  <div class="page-break"></div>

  <h2>2. Test Scenarios (Gherkin / BDD)</h2>
  <p>Format spesifikasi BDD ditulis dengan bahasa bisnis (<strong>declarative</strong>), tersimpan di <code>features/auth_profile_navigation.feature</code>:</p>
"""
    for scn in BDD_SCENARIOS:
        steps_str = "\n".join(scn["steps"])
        ex_str = ""
        if scn["examples"]:
            ex_str = "\n\n    Examples:\n      | " + " | ".join(scn["examples"][0].keys()) + " |\n"
            for ex in scn["examples"]:
                ex_str += "      | " + " | ".join(str(v) for v in ex.values()) + " |\n"
        html += f"""  <div class="code-block"><span style="color:#FAF089;">{esc(scn["tags"])}</span>
<span style="color:#63B3ED; font-weight:bold;">{esc(scn["type"])}:</span> {esc(scn["title"])}
{esc(steps_str)}{esc(ex_str)}</div>
"""

    html += """  <div class="page-break"></div>

  <h2>3. Detailed Test Cases Specification</h2>
  <p>Daftar 9 test case komprehensif (positif dan negatif) dengan 9 atribut wajib:</p>

  <table>
    <thead>
      <tr>
        <th style="width: 9%;" class="text-center">ID</th>
        <th style="width: 17%;">Judul Test Case</th>
        <th style="width: 18%;">Precondition & Test Data</th>
        <th style="width: 22%;">Steps (Langkah Pengujian)</th>
        <th style="width: 20%;">Expected Result</th>
        <th style="width: 7%;" class="text-center">Priority</th>
        <th style="width: 7%;">Teknik</th>
      </tr>
    </thead>
    <tbody>
"""
    for tc in TEST_CASES:
        p_badge = "badge-high" if tc["priority"] == "High" else "badge-med"
        steps_formatted = esc(tc["steps"]).replace("\n", "<br>")
        html += f"""      <tr>
        <td class="text-center text-bold">{esc(tc["id"])}</td>
        <td class="text-bold">{esc(tc["title"])}</td>
        <td><strong>Precondition:</strong> {esc(tc["precondition"])}<br><strong>Data:</strong> {esc(tc["test_data"])}</td>
        <td>{steps_formatted}</td>
        <td>{esc(tc["expected"])}</td>
        <td class="text-center"><span class="badge {p_badge}">{esc(tc["priority"])}</span></td>
        <td>{esc(tc["technique"])}<br><small style="color:#718096;">{esc(tc["link"])}</small></td>
      </tr>
"""
    html += """    </tbody>
  </table>

  <div class="page-break"></div>

  <h2>4. Penerapan Teknik Test Design Formal</h2>

  <h3>4.1. Equivalence Partitioning (EP) — Field Tanggal Lahir (Batas Usia 18–75 Tahun)</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 10%;" class="text-center">Partisi</th>
        <th style="width: 28%;">Rentang Nilai (Usia)</th>
        <th style="width: 22%;">Contoh Nilai Uji (DOB)</th>
        <th style="width: 12%;" class="text-center">Status</th>
        <th style="width: 28%;">Expected Result</th>
      </tr>
    </thead>
    <tbody>
"""
    for ep in TECH_EP:
        b_class = "badge-valid" if ep["status"] == "Valid" else "badge-invalid"
        html += f"""      <tr>
        <td class="text-center text-bold">{esc(ep["partisi"])}</td>
        <td>{esc(ep["rentang"])}</td>
        <td>{esc(ep["contoh"])}</td>
        <td class="text-center"><span class="badge {b_class}">{esc(ep["status"])}</span></td>
        <td>{esc(ep["expected"])}</td>
      </tr>
"""
    html += """    </tbody>
  </table>

  <h3>4.2. Boundary Value Analysis (BVA) — Titik Batas Umur (Tanggal Sistem: 04-10-2026)</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 12%;" class="text-center">Titik Uji</th>
        <th style="width: 26%;">Nilai Uji (Tanggal Lahir)</th>
        <th style="width: 32%;">Representasi Batas</th>
        <th style="width: 10%;" class="text-center">Status</th>
        <th style="width: 20%;">Expected Result</th>
      </tr>
    </thead>
    <tbody>
"""
    for bva in TECH_BVA:
        b_class = "badge-valid" if bva["status"] == "Valid" else "badge-invalid"
        html += f"""      <tr>
        <td class="text-center text-bold">{esc(bva["titik"])}</td>
        <td>{esc(bva["nilai"])}</td>
        <td>{esc(bva["representasi"])}</td>
        <td class="text-center"><span class="badge {b_class}">{esc(bva["status"])}</span></td>
        <td>{esc(bva["expected"])}</td>
      </tr>
"""
    html += """    </tbody>
  </table>

  <h3>4.3. Decision Table Testing — Logika Autentikasi Pengguna (Login)</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 40%;">Kondisi Input & Aksi Sistem</th>
        <th class="text-center">Rule 1</th>
        <th class="text-center">Rule 2</th>
        <th class="text-center">Rule 3</th>
        <th class="text-center">Rule 4</th>
        <th class="text-center">Rule 5</th>
        <th class="text-center">Rule 6</th>
      </tr>
    </thead>
    <tbody>
"""
    for cond, rules in TECH_DT["conditions"]:
        html += f"""      <tr>
        <td class="text-bold">{esc(cond)}</td>
""" + "".join(f"<td class='text-center'>{esc(r)}</td>" for r in rules) + """
      </tr>
"""
    html += """      <tr style="background-color: #E2E8F0;">
        <td colspan="7" class="text-bold" style="color: #1F4E79;">AKSI SISTEM (ACTIONS)</td>
      </tr>
"""
    for act, rules in TECH_DT["actions"]:
        cells = ""
        for r in rules:
            if r == "X":
                cells += "<td class='text-center text-bold' style='background:#D9E1F2;'>X</td>"
            else:
                cells += "<td class='text-center'></td>"
        html += f"""      <tr>
        <td>{esc(act)}</td>{cells}
      </tr>
"""
    html += """    </tbody>
  </table>

  <h3>4.4. State Transition Testing — Siklus Hidup Akun Pelanggan</h3>
  <table>
    <thead>
      <tr>
        <th style="width: 25%;">Current State</th>
        <th style="width: 25%;">Trigger / Event</th>
        <th style="width: 25%;">Action yang Dijalankan</th>
        <th style="width: 25%;">Next State</th>
      </tr>
    </thead>
    <tbody>
"""
    for st in TECH_ST:
        html += f"""      <tr>
        <td class="text-bold">{esc(st["current"])}</td>
        <td>{esc(st["trigger"])}</td>
        <td>{esc(st["action"])}</td>
        <td class="text-bold">{esc(st["next"])}</td>
      </tr>
"""
    html += """    </tbody>
  </table>

  <h2>5. Out of Scope & Asumsi Pengujian</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
    <div>
      <h3 style="margin-top: 0;">Item Out of Scope (Sengaja Tidak Dites)</h3>
      <table style="margin-bottom: 0;">
        <thead>
          <tr>
            <th style="width: 10%;" class="text-center">No</th>
            <th style="width: 35%;">Area / Fitur</th>
            <th style="width: 55%;">Alasan Eksklusi</th>
          </tr>
        </thead>
        <tbody>
"""
    for item in OUT_OF_SCOPE:
        html += f"""          <tr>
            <td class="text-center">{item["no"]}</td>
            <td class="text-bold">{esc(item["fitur"])}</td>
            <td>{esc(item["alasan"])}</td>
          </tr>
"""
    html += """        </tbody>
      </table>
    </div>
    <div>
      <h3 style="margin-top: 0;">Asumsi Pengujian</h3>
      <table style="margin-bottom: 0;">
        <thead>
          <tr>
            <th style="width: 10%;" class="text-center">No</th>
            <th style="width: 35%;">Aspek</th>
            <th style="width: 55%;">Deskripsi Asumsi</th>
          </tr>
        </thead>
        <tbody>
"""
    for item in ASSUMPTIONS:
        html += f"""          <tr>
            <td class="text-center">{item["no"]}</td>
            <td class="text-bold">{esc(item["aspek"])}</td>
            <td>{esc(item["deskripsi"])}</td>
          </tr>
"""
    html += """        </tbody>
      </table>
    </div>
  </div>

</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    from selenium import webdriver
    import base64
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    
    abs_url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    driver.get(abs_url)
    
    pdf_params = {
        'printBackground': True,
        'paperWidth': 8.27,
        'paperHeight': 11.69,
        'marginTop': 0.3,
        'marginBottom': 0.3,
        'marginLeft': 0.3,
        'marginRight': 0.3,
        'preferCSSPageSize': True
    }
    result = driver.execute_cdp_cmd('Page.printToPDF', pdf_params)
    with open(pdf_path, 'wb') as f:
        f.write(base64.b64decode(result['data']))
    driver.quit()
    print(f"PDF saved successfully via Selenium CDP at: {pdf_path}")
    if os.path.exists(html_path):
        os.remove(html_path)

if __name__ == "__main__":
    excel_path = "c:/genesis-sage-automation/logique-qa-assessment/docs/01-test-design.xlsx"
    html_temp = "c:/genesis-sage-automation/logique-qa-assessment/docs/temp_print.html"
    pdf_path = "c:/genesis-sage-automation/logique-qa-assessment/docs/01-test-design.pdf"
    
    print("Building unified Excel...")
    build_excel(excel_path)
    
    print("Building unified PDF...")
    build_pdf(html_temp, pdf_path)
    print("Both Excel and PDF are now 100% synchronized and identical!")
