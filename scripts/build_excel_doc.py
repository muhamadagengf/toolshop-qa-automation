import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# Define Palettes & Styles
HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid") # Deep Corporate Navy
SUBHEADER_FILL = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid") # Soft Blue
ACCENT_FILL = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
ZEBRA_FILL = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
HIGH_RISK_FILL = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid") # Soft Red/Orange
MED_RISK_FILL = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")  # Soft Yellow

FONT_TITLE = Font(name="Calibri", size=16, bold=True, color="1F4E79")
FONT_SECTION = Font(name="Calibri", size=12, bold=True, color="1F4E79")
FONT_HEADER = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
FONT_BOLD = Font(name="Calibri", size=10, bold=True, color="000000")
FONT_REGULAR = Font(name="Calibri", size=10, color="000000")

BORDER_THIN = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
BORDER_HEADER = Border(
    left=Side(style='thin', color='1F4E79'),
    right=Side(style='thin', color='1F4E79'),
    top=Side(style='medium', color='1F4E79'),
    bottom=Side(style='medium', color='1F4E79')
)

def auto_fit_columns(ws, min_col=1, max_col=None, max_width=45):
    if max_col is None:
        max_col = ws.max_column
    for col in range(min_col, max_col + 1):
        col_letter = get_column_letter(col)
        max_len = 0
        for cell in ws[col_letter]:
            if cell.value:
                val_str = str(cell.value)
                first_line = val_str.split("\n")[0]
                if len(first_line) > max_len:
                    max_len = len(first_line)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), max_width)

# =============================================================================
# SHEET 1: Summary & Cover
# =============================================================================
ws_cover = wb.active
ws_cover.title = "Overview"
ws_cover.views.sheetView[0].showGridLines = True

ws_cover.cell(row=2, column=2, value="TECHNICAL TEST QA - PT LOGIKA SARANA TEKNOLOGI").font = FONT_TITLE
ws_cover.cell(row=3, column=2, value="Bagian 1: Analytical & Test Design (35%)").font = FONT_SECTION

metadata = [
    ("Target Application", "Practice Software Testing (Toolshop)"),
    ("Target URL", "https://practicesoftwaretesting.com"),
    ("API Documentation", "https://api.practicesoftwaretesting.com/docs?api-docs.json"),
    ("Testing Scope", "User Registration, Login Authentication, Edit Profile, Change Password, Category Navigation"),
    ("Deliverable Assets", "01-test-design.xlsx, 01-test-design.pdf, 01-test-design.md, features/auth_profile_navigation.feature"),
    ("Author", "QA Automation Engineering Candidate")
]

for idx, (lbl, val) in enumerate(metadata, start=5):
    c1 = ws_cover.cell(row=idx, column=2, value=lbl)
    c1.font = FONT_BOLD
    c1.fill = SUBHEADER_FILL
    c1.border = BORDER_THIN
    c2 = ws_cover.cell(row=idx, column=3, value=val)
    c2.font = FONT_REGULAR
    c2.border = BORDER_THIN

ws_cover.column_dimensions["B"].width = 25
ws_cover.column_dimensions["C"].width = 75

# =============================================================================
# SHEET 2: Risk Analysis
# =============================================================================
ws_risk = wb.create_sheet(title="Risk_Analysis")
ws_risk.views.sheetView[0].showGridLines = True

ws_risk.cell(row=2, column=2, value="1. Risk Analysis & Mitigation Matrix").font = FONT_TITLE
ws_risk.cell(row=3, column=2, value="Formula Skor: Likelihood (1-3) x Impact (1-3). Diurutkan dari skor tertinggi.").font = FONT_REGULAR

risk_headers = ["Risk ID", "Area Risiko", "Likelihood (1-3)", "Impact (1-3)", "Risk Score", "Level", "Alasan & Potensi Dampak", "Strategi Mitigasi / Pengujian"]
for col_idx, h in enumerate(risk_headers, start=2):
    cell = ws_risk.cell(row=5, column=col_idx, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = BORDER_HEADER

risks_data = [
    ("R-01", "Autentikasi & Sesi (Session Hijacking / Broken Auth)", 2, 3, 6, "High", "Jika token otentikasi tidak diamankan atau sesi tidak dibatalkan pasca logout/ganti password, akun rentan dibajak.", "Uji pembatalan token saat logout dan ganti password, validasi route guards private."),
    ("R-02", "Validasi Batasan Usia (DOB Validation Bypass)", 3, 2, 6, "High", "Syarat usia 18-75 thn berpotensi hanya divalidasi di UI sehingga rentan dibypass via API payload langsung.", "Terapkan Boundary Value Analysis (BVA) pada field tanggal lahir baik di UI maupun API."),
    ("R-03", "Persistensi Data Pembaruan Profil (Data Loss)", 2, 3, 6, "High", "Pengguna update alamat/telepon berisiko gagal tersimpan permanen di database, memicu salah kirim pesanan.", "Uji skenario update, reload browser (F5), dan verifikasi sinkronisasi payload backend."),
    ("R-04", "Ganti Password Tanpa Verifikasi Password Lama", 2, 3, 6, "High", "Jika password lama salah namun diizinkan ganti, atau password baru terlalu lemah, akun mudah diambil alih.", "Uji penolakan saat password lama salah dan uji kompleksitas password baru (huruf besar, kecil, angka, simbol)."),
    ("R-05", "Duplikasi Email saat Registrasi (Duplicate Conflict)", 3, 2, 6, "High", "Registrasi dengan email yang sudah ada berisiko corrupt data jika backend tidak memiliki unique constraint.", "Uji negative registrasi dengan email terdaftar, validasi status code HTTP 422/409 dan feedback UI."),
    ("R-06", "Keamanan Input Form (Stored XSS / SQLi)", 2, 3, 6, "High", "Field nama/alamat yang tidak disanitasi dapat mengeksekusi script jahat di profil atau invoice PDF.", "Uji input karakter tag HTML/script (<script>, <b>), kutip satu/dua, serta verifikasi UI encoding."),
    ("R-07", "Inkonsistensi Filter & Navigasi Kategori Produk", 2, 2, 4, "Medium", "Jika query slug kategori putus atau state navigation rusak, katalog gagal menampilkan daftar produk.", "Uji routing dropdown navigasi, sinkronisasi URL slug, dan verifikasi relevansi produk.")
]

for row_idx, r in enumerate(risks_data, start=6):
    fill_to_use = HIGH_RISK_FILL if r[4] >= 6 else MED_RISK_FILL
    for col_idx, val in enumerate(r, start=2):
        cell = ws_risk.cell(row=row_idx, column=col_idx, value=val)
        cell.font = FONT_REGULAR
        cell.border = BORDER_THIN
        if col_idx in [2, 4, 5, 6, 7]: # ID, L, I, Score, Level
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if col_idx in [6, 7]:
                cell.fill = fill_to_use
                cell.font = FONT_BOLD
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

auto_fit_columns(ws_risk, min_col=2, max_col=9, max_width=45)
ws_risk.column_dimensions["C"].width = 30
ws_risk.column_dimensions["H"].width = 45
ws_risk.column_dimensions["I"].width = 45

# =============================================================================
# SHEET 3: Test Cases Detail
# =============================================================================
ws_tc = wb.create_sheet(title="Test_Cases_Detail")
ws_tc.views.sheetView[0].showGridLines = True

ws_tc.cell(row=2, column=2, value="2. Detailed Test Cases Specification").font = FONT_TITLE
ws_tc.cell(row=3, column=2, value="Daftar 9 test case komprehensif (positif & negatif) diturunkan dari skenario BDD dan analisis risiko.").font = FONT_REGULAR

tc_headers = ["ID", "Judul Test Case", "Precondition", "Test Data", "Steps (Langkah Pengujian)", "Expected Result", "Priority", "Teknik Test Design", "Link Scenario / Risk"]
for col_idx, h in enumerate(tc_headers, start=2):
    cell = ws_tc.cell(row=5, column=col_idx, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = BORDER_HEADER

tc_data = [
    (
        "TC-REG-01",
        "Registrasi user baru dengan data lengkap & valid",
        "Akses home page Toolshop, user dalam status belum login (guest).",
        "Nama: John Doe, DOB: 1995-05-20 (31 thn), Email: test_<dynamic>@auto.org, Password: Password@123, Alamat: Lengkap",
        "1. Klik menu 'Sign in' lalu klik tautan 'Register your account'.\n2. Isi seluruh field formulir pendaftaran dengan data valid.\n3. Klik tombol 'Register'.",
        "Pendaftaran berhasil, pengguna otomatis diredirect ke URL /auth/login, dan muncul pesan sukses registrasi.",
        "High",
        "Equivalence Partitioning (Valid)",
        "Scenario 1 / R-02"
    ),
    (
        "TC-REG-02",
        "Registrasi ditolak saat usia pendaftar di bawah 18 tahun",
        "Berada di halaman formulir /auth/register.",
        "DOB: tanggal hari ini dikurangi 17 tahun 364 hari (contoh: 2008-10-05), field lainnya valid.",
        "1. Isi semua field dengan data valid.\n2. Masukkan tanggal lahir dengan usia 17 tahun.\n3. Klik tombol 'Register'.",
        "Form menolak submit, tampil pesan error validasi bahwa pendaftar minimal harus berusia 18 tahun. Tidak ada akun terdaftar.",
        "High",
        "Boundary Value Analysis (Invalid Boundary)",
        "Scenario 2 / R-02"
    ),
    (
        "TC-REG-03",
        "Registrasi ditolak saat alamat email sudah terdaftar sebelumnya",
        "Akun dengan email target telah aktif dan terdaftar di database.",
        "Email: customer@practicesoftwaretesting.com, field lainnya valid.",
        "1. Akses halaman registrasi /auth/register.\n2. Isi field email dengan alamat email yang sudah ada.\n3. Lengkapi form dan klik tombol 'Register'.",
        "Registrasi gagal diproses, sistem menampilkan notifikasi error 'E-mail already exists' atau HTTP 422 Unprocessable Entity.",
        "High",
        "Error Guessing",
        "Scenario 1 / R-05"
    ),
    (
        "TC-LOG-01",
        "Login berhasil dengan kredensial valid",
        "User telah terdaftar dan akun berstatus aktif.",
        "Email: customer@practicesoftwaretesting.com, Password: welcome01",
        "1. Akses halaman /auth/login.\n2. Masukkan alamat email dan password yang benar.\n3. Klik tombol 'Login'.",
        "Otentikasi sukses, user diarahkan ke dashboard akun (/account), nama pengguna tampil pada header navigasi.",
        "High",
        "Decision Table (Rule 1)",
        "Scenario 3 / R-01"
    ),
    (
        "TC-LOG-02",
        "Login ditolak ketika password salah",
        "User telah terdaftar pada sistem.",
        "Email: customer@practicesoftwaretesting.com, Password: SalahPassword#99",
        "1. Buka halaman /auth/login.\n2. Masukkan email yang benar dan password yang salah.\n3. Klik tombol 'Login'.",
        "Otentikasi gagal, tetap di halaman login, muncul pesan alert 'Invalid email or password'. Token sesi tidak dibuat.",
        "High",
        "Decision Table (Rule 3)",
        "Scenario 3 / R-01"
    ),
    (
        "TC-LOG-03",
        "Validasi form ketika field email dan password dikosongkan",
        "Berada pada halaman login /auth/login.",
        "Email: \"\" (kosong), Password: \"\" (kosong)",
        "1. Klik field email lalu tinggalkan kosong.\n2. Klik field password lalu tinggalkan kosong.\n3. Klik tombol 'Login'.",
        "Muncul pesan error validasi client-side: 'E-mail is required' dan 'Password is required'. Request HTTP POST tidak dikirim.",
        "Medium",
        "Equivalence Partitioning (Empty Input)",
        "Scenario 3 / R-01"
    ),
    (
        "TC-PRF-01",
        "Update data profil (telepon & alamat) dan verifikasi persistensi reload",
        "Pengguna telah login dan berada pada halaman profil /account/profile.",
        "Phone: 081298765432, Address: Jl. Melati Raya No. 45, City: Jakarta",
        "1. Ubah nilai pada field Phone dan Address.\n2. Klik tombol 'Update Profile'.\n3. Lakukan reload halaman browser (F5).\n4. Periksa nilai pada form profil.",
        "Muncul feedback sukses 'Profile updated', dan setelah halaman di-reload data baru tetap tersimpan pada form.",
        "High",
        "State Transition Testing",
        "Scenario 4 / R-03"
    ),
    (
        "TC-PWD-01",
        "Ganti password ditolak jika password baru tidak memenuhi kompleksitas",
        "Pengguna telah login dan membuka tab Change Password.",
        "Current Password: welcome01, New Password: simplepass (tanpa angka/simbol)",
        "1. Buka menu profil -> tab Change Password.\n2. Masukkan current password yang valid.\n3. Masukkan new password yang tidak memenuhi syarat keamanan.\n4. Klik 'Save'.",
        "Sistem menolak update password, muncul pesan bahwa password harus memiliki huruf besar, huruf kecil, angka, dan simbol.",
        "High",
        "Boundary & Decision Table",
        "Scenario 5 / R-04"
    ),
    (
        "TC-NAV-01",
        "Navigasi menu kategori produk (Power Tools)",
        "User berada di halaman utama aplikasi Toolshop.",
        "Kategori: 'Power Tools' (Slug URL: /category/power-tools)",
        "1. Klik menu dropdown 'Categories' pada navigasi bar atas.\n2. Pilih sub-kategori 'Power Tools'.\n3. Verifikasi halaman katalog dan produk yang tampil.",
        "URL halaman berubah menjadi /category/power-tools, judul halaman menampilkan 'Power Tools', dan hanya produk kategori tersebut yang tampil.",
        "Medium",
        "State Transition Testing",
        "Scenario 7 / R-07"
    )
]

for row_idx, r in enumerate(tc_data, start=6):
    fill_to_use = ZEBRA_FILL if row_idx % 2 == 0 else PatternFill(fill_type=None)
    for col_idx, val in enumerate(r, start=2):
        cell = ws_tc.cell(row=row_idx, column=col_idx, value=val)
        cell.font = FONT_REGULAR
        cell.border = BORDER_THIN
        if fill_to_use.fill_type:
            cell.fill = fill_to_use
        
        if col_idx in [2, 8]: # ID, Priority
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if col_idx == 8:
                cell.font = FONT_BOLD
                cell.fill = HIGH_RISK_FILL if val == "High" else MED_RISK_FILL
        elif col_idx in [3, 9, 10]:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        else:
            cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)

ws_tc.column_dimensions["B"].width = 14
ws_tc.column_dimensions["C"].width = 28
ws_tc.column_dimensions["D"].width = 28
ws_tc.column_dimensions["E"].width = 32
ws_tc.column_dimensions["F"].width = 40
ws_tc.column_dimensions["G"].width = 35
ws_tc.column_dimensions["H"].width = 12
ws_tc.column_dimensions["I"].width = 28
ws_tc.column_dimensions["J"].width = 22

# =============================================================================
# SHEET 4: Test Design Techniques
# =============================================================================
ws_tech = wb.create_sheet(title="Test_Design_Techniques")
ws_tech.views.sheetView[0].showGridLines = True

ws_tech.cell(row=2, column=2, value="3. Penerapan Teknik Test Design Formal").font = FONT_TITLE
ws_tech.cell(row=3, column=2, value="Implementasi konkret 3 teknik pengujian: Equivalence Partitioning, Boundary Value Analysis, Decision Table, dan State Transition.").font = FONT_REGULAR

# --- 1. EP & BVA ---
ws_tech.cell(row=5, column=2, value="Teknik 1: Equivalence Partitioning (EP) - Field Tanggal Lahir (DOB: 18 - 75 Tahun)").font = FONT_SECTION

ep_headers = ["Kelas Partisi", "Rentang Nilai (Usia)", "Contoh Nilai Uji (DOB)", "Kategori Partisi", "Expected Result"]
for col_idx, h in enumerate(ep_headers, start=2):
    cell = ws_tech.cell(row=7, column=col_idx, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = BORDER_HEADER

ep_data = [
    ("P1", "Usia < 18 tahun (Minor)", "2012-05-10 (14 tahun)", "Invalid", "Ditolak: usia minimal pendaftar 18 tahun"),
    ("P2", "18 tahun <= Usia <= 75 tahun (Legal)", "1990-08-15 (36 tahun)", "Valid", "Diterima: registrasi dapat dilanjutkan"),
    ("P3", "Usia > 75 tahun (Senior di atas batas)", "1945-01-01 (81 tahun)", "Invalid", "Ditolak: usia maksimal pendaftar 75 tahun"),
    ("P4", "Tanggal masa depan (Future Date)", "2028-01-01 (-2 tahun)", "Invalid", "Ditolak: tanggal lahir tidak boleh di masa depan"),
    ("P5", "Format tanggal tidak valid / string", "abc-def-ghij", "Invalid", "Ditolak: format input tanggal harus YYYY-MM-DD")
]
for r_idx, row in enumerate(ep_data, start=8):
    for c_idx, val in enumerate(row, start=2):
        cell = ws_tech.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_REGULAR
        cell.border = BORDER_THIN
        cell.alignment = Alignment(horizontal="center" if c_idx in [2, 5] else "left", vertical="center")
        if c_idx == 5:
            cell.font = FONT_BOLD
            cell.fill = HIGH_RISK_FILL if val == "Invalid" else PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")

# BVA Table
ws_tech.cell(row=15, column=2, value="Teknik 1B: Boundary Value Analysis (BVA) - Titik Batas Umur Relatif thd 04-10-2026").font = FONT_SECTION
bva_headers = ["Titik Uji", "Nilai Uji (Tanggal Lahir)", "Representasi Batas", "Status", "Expected Output"]
for col_idx, h in enumerate(bva_headers, start=2):
    cell = ws_tech.cell(row=17, column=col_idx, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = BORDER_HEADER

bva_data = [
    ("BVA-01", "2008-10-05 (17 thn 364 hari)", "Just below minimum boundary (18 thn - 1 hari)", "Invalid", "Ditolak (Error: usia < 18 thn)"),
    ("BVA-02", "2008-10-04 (Tepat 18 tahun)", "Exact minimum valid boundary (18 thn)", "Valid", "Diterima"),
    ("BVA-03", "2008-10-03 (18 thn 1 hari)", "Just above minimum boundary (18 thn + 1 hari)", "Valid", "Diterima"),
    ("BVA-04", "1951-10-05 (74 thn 364 hari)", "Just below maximum boundary (75 thn - 1 hari)", "Valid", "Diterima"),
    ("BVA-05", "1951-10-04 (Tepat 75 tahun)", "Exact maximum valid boundary (75 thn)", "Valid", "Diterima"),
    ("BVA-06", "1951-10-03 (75 thn 1 hari)", "Just above maximum boundary (75 thn + 1 hari)", "Invalid", "Ditolak (Error: usia > 75 thn)")
]
for r_idx, row in enumerate(bva_data, start=18):
    for c_idx, val in enumerate(row, start=2):
        cell = ws_tech.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_REGULAR
        cell.border = BORDER_THIN
        cell.alignment = Alignment(horizontal="center" if c_idx in [2, 5] else "left", vertical="center")
        if c_idx == 5:
            cell.font = FONT_BOLD
            cell.fill = HIGH_RISK_FILL if val == "Invalid" else PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")

# Decision Table
ws_tech.cell(row=26, column=2, value="Teknik 2: Decision Table Testing - Logika Autentikasi Pengguna (Login)").font = FONT_SECTION
dt_headers = ["Kondisi & Aksi Sistem", "Rule 1", "Rule 2", "Rule 3", "Rule 4", "Rule 5", "Rule 6"]
for col_idx, h in enumerate(dt_headers, start=2):
    cell = ws_tech.cell(row=28, column=col_idx, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = BORDER_HEADER

dt_data = [
    ("C1: Format Email Valid", "Y", "Y", "Y", "T", "Y", "T"),
    ("C2: Email Terdaftar di Database", "Y", "Y", "T", "-", "Y", "-"),
    ("C3: Password Sesuai Hash DB", "Y", "T", "-", "-", "-", "-"),
    ("C4: Field Password Terisi", "Y", "Y", "Y", "Y", "T", "T"),
    ("--- AKSI SISTEM (ACTIONS) ---", "", "", "", "", "", ""),
    ("A1: Login Sukses & Buat Token Sesi", "X", "", "", "", "", ""),
    ("A2: Redirect ke Dashboard (/account)", "X", "", "", "", "", ""),
    ("A3: Tampilkan Pesan 'Invalid email or password'", "", "X", "X", "", "", ""),
    ("A4: Tampilkan Validasi 'Format e-mail tidak valid'", "", "", "", "X", "", ""),
    ("A5: Tampilkan Validasi 'Password is required'", "", "", "", "", "X", "X"),
    ("A6: Catat Audit Log Percobaan Gagal", "", "X", "X", "", "", "")
]
for r_idx, row in enumerate(dt_data, start=29):
    is_sep = "AKSI SISTEM" in row[0]
    for c_idx, val in enumerate(row, start=2):
        cell = ws_tech.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_BOLD if (c_idx == 2 or is_sep) else FONT_REGULAR
        cell.border = BORDER_THIN
        if is_sep:
            cell.fill = SUBHEADER_FILL
            cell.alignment = Alignment(horizontal="left", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="center" if c_idx > 2 else "left", vertical="center")
            if val == "X":
                cell.fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")

auto_fit_columns(ws_tech, min_col=2, max_col=8, max_width=45)

# =============================================================================
# SHEET 5: Out of Scope & Assumptions
# =============================================================================
ws_scope = wb.create_sheet(title="Out_of_Scope_&_Assumptions")
ws_scope.views.sheetView[0].showGridLines = True

ws_scope.cell(row=2, column=2, value="4. Out of Scope & Asumsi Pengujian").font = FONT_TITLE

# Out of scope table
ws_scope.cell(row=4, column=2, value="Item Out of Scope (Sengaja Tidak Dites)").font = FONT_SECTION
oos_headers = ["No", "Area / Fitur", "Alasan Eksklusi dari Lingkup Pengujian"]
for col_idx, h in enumerate(oos_headers, start=2):
    cell = ws_scope.cell(row=6, column=col_idx, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = BORDER_HEADER

oos_data = [
    (1, "Verifikasi Email SMTP / OTP Real Server", "Aplikasi demo Toolshop sengaja langsung mengaktifkan akun pendaftaran tanpa pengiriman tautan aktivasi email nyata."),
    (2, "Transaksi Real Payment Gateway Kartu Kredit", "Fokus Bagian 1 adalah manajemen akun dan navigasi. Modul pembayaran pihak ketiga diuji dalam mode simulasi transaksi belanja."),
    (3, "Social Login Integration (OAuth Google / FB)", "Fitur third-party social login tidak disediakan pada arsitektur aplikasi Toolshop."),
    (4, "Deep Penetration Testing (DAST / SQLi Injection)", "Pengujian berorientasi pada fungsionalitas dan test design BDD sesuai spesifikasi brief QA.")
]
for r_idx, row in enumerate(oos_data, start=7):
    for c_idx, val in enumerate(row, start=2):
        cell = ws_scope.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_REGULAR
        cell.border = BORDER_THIN
        cell.alignment = Alignment(horizontal="center" if c_idx == 2 else "left", vertical="center", wrap_text=True)

# Assumptions table
ws_scope.cell(row=13, column=2, value="Asumsi Pengujian").font = FONT_SECTION
assump_headers = ["No", "Aspek", "Deskripsi Asumsi"]
for col_idx, h in enumerate(assump_headers, start=2):
    cell = ws_scope.cell(row=15, column=col_idx, value=h)
    cell.font = FONT_HEADER
    cell.fill = HEADER_FILL
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = BORDER_HEADER

assump_data = [
    (1, "Lingkungan Server", "Aplikasi target diakses melalui domain resmi https://practicesoftwaretesting.com dalam kondisi server live dan stabil."),
    (2, "Isolasi Data Uji", "Setiap eksekusi registrasi menggunakan generator data unik (format test_<timestamp>@mail.com) guna mencegah tabrakan data unik."),
    (3, "Patokan Waktu Batas Usia", "Perhitungan batasan usia 18-75 tahun merujuk pada tanggal sistem saat pengujian dieksekusi."),
    (4, "Kompatibilitas Browser", "Pengujian dirancang optimal untuk browser berbasis Chromium (Google Chrome / Edge) versi terbaru.")
]
for r_idx, row in enumerate(assump_data, start=16):
    for c_idx, val in enumerate(row, start=2):
        cell = ws_scope.cell(row=r_idx, column=c_idx, value=val)
        cell.font = FONT_REGULAR
        cell.border = BORDER_THIN
        cell.alignment = Alignment(horizontal="center" if c_idx == 2 else "left", vertical="center", wrap_text=True)

auto_fit_columns(ws_scope, min_col=2, max_col=4, max_width=65)
ws_scope.column_dimensions["C"].width = 28
ws_scope.column_dimensions["D"].width = 65

# Save workbook
output_path = "c:/genesis-sage-automation/logique-qa-assessment/docs/01-test-design.xlsx"
wb.save(output_path)
print(f"Excel successfully created at: {output_path}")
