"""
Script: generate_bug_report_excel.py
Deskripsi: Menghasilkan dokumen Excel resmi 'docs/03-bug-report.xlsx' untuk hasil
           Bug Hunting (Bagian 3) pada target https://with-bugs.practicesoftwaretesting.com.
Fitur:
  1. Sheet 1: Ringkasan & Metrik (Executive Dashboard, KPI Cards, Severity Matrix, Summary Table).
  2. Sheet 2: Detail Bug & Bukti Screenshot (Form kartu bug terstruktur dengan gambar screenshot tertanam).
  3. Sheet 3: Grid Database (Format flat tabular untuk kemudahan integrasi Jira/ALM).
"""

import os
from PIL import Image as PILImage
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as OpenpyxlImage

def create_bug_report_excel():
    wb = openpyxl.Workbook()
    # Hapus default sheet
    wb.remove(wb.active)

    # -------------------------------------------------------------
    # Palet Warna & Styling Standar Logique
    # -------------------------------------------------------------
    NAVY_DARK = "1A365D"
    BLUE_PRIMARY = "2B6CB0"
    BLUE_LIGHT = "EBF8FF"
    GRAY_HEADER = "EDF2F7"
    GRAY_BG = "F7FAFC"
    BORDER_COLOR = "CBD5E0"

    COLOR_CRITICAL = "9B2C2C" # Dark Red
    BG_CRITICAL = "FED7D7"    # Soft Red
    COLOR_MAJOR = "C05621"    # Dark Orange
    BG_MAJOR = "FEEBC8"       # Soft Orange
    COLOR_MINOR = "975A16"    # Dark Yellow
    BG_MINOR = "FEFCBF"       # Soft Yellow
    COLOR_TRIVIAL = "4A5568"  # Slate Gray
    BG_TRIVIAL = "E2E8F0"     # Soft Gray

    thin_border = Border(
        left=Side(style='thin', color=BORDER_COLOR),
        right=Side(style='thin', color=BORDER_COLOR),
        top=Side(style='thin', color=BORDER_COLOR),
        bottom=Side(style='thin', color=BORDER_COLOR)
    )

    header_font_white = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_font_dark = Font(name="Calibri", size=11, bold=True, color=NAVY_DARK)
    cell_font = Font(name="Calibri", size=10)
    bold_font = Font(name="Calibri", size=10, bold=True)
    small_font = Font(name="Calibri", size=9, italic=True, color="718096")

    # -------------------------------------------------------------
    # Data 7 Bug Hasil Hunting
    # -------------------------------------------------------------
    bugs_data = [
        {
            "id": "BUG-001",
            "title": "Subtotal Baris Keranjang Belanja Terhitung $00.00 (Kalkulasi Finansial Rusak)",
            "area": "Checkout & Cart",
            "severity": "Critical",
            "priority": "P1",
            "status": "OPEN",
            "environment": "Google Chrome v134.0 (Desktop 1920x1080), Windows 11 Pro 64-bit",
            "steps": (
                "1. Buka halaman utama https://with-bugs.practicesoftwaretesting.com.\n"
                "2. Klik salah satu produk (misalnya: Combination Pliers seharga $14.15).\n"
                "3. Pastikan kuantitas produk minimal 1, lalu klik tombol 'Add to cart'.\n"
                "4. Buka halaman keranjang belanja melalui ikon Cart di navbar (/#/checkout).\n"
                "5. Perhatikan nilai kolom 'Total' pada baris produk pertama."
            ),
            "expected": (
                "Kolom 'Total' pada baris produk menghitung hasil perkalian harga satuan dan kuantitas "
                "secara akurat (misal: $14.15 × 1 = $14.15)."
            ),
            "actual": (
                "Kolom 'Total' pada baris produk menampilkan nilai '$00.00', sedangkan baris ringkasan "
                "Grand Total di bagian bawah menampilkan nilai '$14.15'. Terdapat ketidaksinkronan kalkulasi finansial."
            ),
            "impact": (
                "Merusak integritas data transaksi dan faktur belanja. Berpotensi dieksploitasi pengguna "
                "untuk melakukan pembayaran gratis jika backend menerima data baris item."
            ),
            "evidence": ["docs/evidence/BUG-001-cart-subtotal-zero.png"],
            "sev_color": COLOR_CRITICAL,
            "sev_bg": BG_CRITICAL
        },
        {
            "id": "BUG-002",
            "title": "Pengurutan Produk Terbalik (Opsi 'Price Low - High' Mengurutkan dari Tertinggi)",
            "area": "Catalog & Sorting",
            "severity": "Major",
            "priority": "P2",
            "status": "OPEN",
            "environment": "Google Chrome v134.0 (Desktop 1920x1080), Windows 11 Pro 64-bit",
            "steps": (
                "1. Akses katalog produk di https://with-bugs.practicesoftwaretesting.com.\n"
                "2. Buka dropdown pengurutan pada sidebar kiri yang berlabel 'Sorth'.\n"
                "3. Pilih opsi 'Price (Low - High)'.\n"
                "4. Amati urutan harga produk yang ditampilkan pada grid katalog."
            ),
            "expected": (
                "Produk termurah ($10.00 - $15.00) ditampilkan di awal urutan, kemudian meningkat secara bertahap."
            ),
            "actual": (
                "Produk termahal justru ditampilkan pertama kali (Cordless Drill 20V seharga $125.23, "
                "Cordless Drill 18V seharga $119.24). Network tab membuktikan parameter terbalik: sort=price,desc."
            ),
            "impact": (
                "Menyesatkan calon pembeli yang mencari produk ekonomis dan menurunkan kepuasan pengguna (UX)."
            ),
            "evidence": ["docs/evidence/BUG-002-inverted-price-sorting.png"],
            "sev_color": COLOR_MAJOR,
            "sev_bg": BG_MAJOR
        },
        {
            "id": "BUG-003",
            "title": "Label dan Form Input Tertukar pada Kolom 'Country' dan 'State' di Registrasi",
            "area": "Customer Registration",
            "severity": "Major",
            "priority": "P2",
            "status": "OPEN",
            "environment": "Google Chrome v134.0 (Desktop 1920x1080), Windows 11 Pro 64-bit",
            "steps": (
                "1. Buka formulir pendaftaran pelanggan https://with-bugs.practicesoftwaretesting.com/#/auth/register.\n"
                "2. Gulir ke bagian alamat pelanggan (Address information).\n"
                "3. Perhatikan pasangan label teks dan elemen input field untuk negara dan provinsi/negara bagian."
            ),
            "expected": (
                "Label 'Country' memayungi dropdown negara, dan label 'State' memayungi text field input state."
            ),
            "actual": (
                "Label 'Country' berada di atas text input dengan placeholder 'Your state *'. "
                "Sedangkan label 'State' berada di atas elemen dropdown 'Select your country *'."
            ),
            "impact": (
                "Data alamat pelanggan tersimpan terbalik di database (Country tersimpan sebagai State dan sebaliknya), "
                "berakibat gagal kirim kurir fisik dan kalkulasi ongkos kirim keliru."
            ),
            "evidence": ["docs/evidence/BUG-003-swapped-country-state-labels.png"],
            "sev_color": COLOR_MAJOR,
            "sev_bg": BG_MAJOR
        },
        {
            "id": "BUG-004",
            "title": "Validasi Tanggal Lahir (DOB) Mengizinkan Tanggal di Masa Depan (Future Date)",
            "area": "Customer Registration",
            "severity": "Major",
            "priority": "P2",
            "status": "OPEN",
            "environment": "Google Chrome v134.0 (Desktop 1920x1080), Windows 11 Pro 64-bit",
            "steps": (
                "1. Buka form registrasi https://with-bugs.practicesoftwaretesting.com/#/auth/register.\n"
                "2. Pada kolom 'Date of birth', ketikkan tanggal di masa depan (contoh: 2099-12-31).\n"
                "3. Isi seluruh field lainnya dengan data valid, lalu klik tombol 'Register'."
            ),
            "expected": (
                "Sistem memunculkan error validasi: 'Date of birth cannot be in the future' atau "
                "menerapkan batas usia minimum legal (misal: 18 tahun)."
            ),
            "actual": (
                "Formulir menerima tanggal masa depan '2099-12-31' dan berhasil submit tanpa penolakan validasi sama sekali."
            ),
            "impact": (
                "Integritas data profil rusak dan melanggar kepatuhan batas usia hukum transaksi online (compliance)."
            ),
            "evidence": ["docs/evidence/BUG-004-future-date-of-birth.png"],
            "sev_color": COLOR_MAJOR,
            "sev_bg": BG_MAJOR
        },
        {
            "id": "BUG-005",
            "title": "Duplikasi Nama Header Kolom 'Total' pada Tabel Keranjang Belanja",
            "area": "Checkout & Cart Table",
            "severity": "Minor",
            "priority": "P3",
            "status": "OPEN",
            "environment": "Google Chrome v134.0 (Desktop 1920x1080), Windows 11 Pro 64-bit",
            "steps": (
                "1. Tambahkan item apapun ke dalam cart.\n"
                "2. Navigasikan ke halaman Checkout https://with-bugs.practicesoftwaretesting.com/#/checkout.\n"
                "3. Amati susunan header tabel keranjang: Item | Quantity | Price | Total | Total."
            ),
            "expected": (
                "Header kolom kelima berlabel 'Action' atau dibiarkan kosong karena berisi tombol ikon hapus."
            ),
            "actual": (
                "Kolom keempat dan kelima keduanya menggunakan label yang identik: 'Total'."
            ),
            "impact": (
                "Menurunkan estetika antarmuka dan membingungkan screen reader untuk aksesibilitas pengguna difabel."
            ),
            "evidence": ["docs/evidence/BUG-005-duplicate-total-table-header.png"],
            "sev_color": COLOR_MINOR,
            "sev_bg": BG_MINOR
        },
        {
            "id": "BUG-006",
            "title": "Asset Logo Toolshop pada Header Aplikasi Mengalami Broken Image (HTTP 404)",
            "area": "Global Navigation Header",
            "severity": "Minor",
            "priority": "P3",
            "status": "OPEN",
            "environment": "Google Chrome v134.0 (Desktop 1920x1080), Windows 11 Pro 64-bit",
            "steps": (
                "1. Buka halaman manapun di situs https://with-bugs.practicesoftwaretesting.com.\n"
                "2. Perhatikan logo Toolshop di sudut kiri atas navbar.\n"
                "3. Buka browser Developer Tools (F12) -> Tab Console & Network."
            ),
            "expected": (
                "Gambar logo brand Toolshop termuat sempurna dengan status HTTP 200 OK."
            ),
            "actual": (
                "Elemen gambar menampilkan ikon broken image. Console mencatat: "
                "GET /broken.png net::ERR_HTTP_RESPONSE_CODE_FAILURE 404 (Not Found)."
            ),
            "impact": (
                "Menurunkan reputasi profesionalitas brand toko online di mata calon pelanggan baru."
            ),
            "evidence": ["docs/evidence/BUG-006-broken-logo-asset-404.png"],
            "sev_color": COLOR_MINOR,
            "sev_bg": BG_MINOR
        },
        {
            "id": "BUG-007",
            "title": "Berbagai Kesalahan Ejaan (Typo) pada Komponen Kunci UI Aplikasi",
            "area": "Global UI & Copywriting",
            "severity": "Trivial",
            "priority": "P4",
            "status": "OPEN",
            "environment": "Google Chrome v134.0 (Desktop 1920x1080), Windows 11 Pro 64-bit",
            "steps": (
                "1. Header navbar: Amati menu 'Contakt' (seharusnya 'Contact').\n"
                "2. Filter sidebar: Amati label pengurutan 'Sorth' (seharusnya 'Sort').\n"
                "3. Tombol pencarian: Amati tombol search bertuliskan 'Serch' (seharusnya 'Search').\n"
                "4. Detail produk: Amati judul section 'Reltded products' (seharusnya 'Related products').\n"
                "5. Halaman Contact: Amati placeholder textarea 'Massage' (seharusnya 'Message')."
            ),
            "expected": (
                "Seluruh teks antarmuka menggunakan kosa kata bahasa Inggris yang baku dan benar secara gramatikal."
            ),
            "actual": (
                "Ditemukan banyak kesalahan ketik (Contakt, Sorth, Serch, Reltded products, Massage)."
            ),
            "impact": (
                "Mengurangi kredibilitas visual aplikasi tanpa memblokir fungsionalitas teknis apapun."
            ),
            "evidence": [
                "docs/evidence/BUG-007-typos-related-products.png",
                "docs/evidence/BUG-007-typo-contact-massage.png"
            ],
            "sev_color": COLOR_TRIVIAL,
            "sev_bg": BG_TRIVIAL
        }
    ]

    # =============================================================
    # SHEET 1: RINGKASAN & METRIK (EXECUTIVE DASHBOARD)
    # =============================================================
    ws1 = wb.create_sheet(title="Ringkasan & Metrik")
    ws1.views.sheetView[0].showGridLines = True

    # Header Judul
    ws1.merge_cells("A1:H1")
    ws1["A1"] = "LOGIQUE DIGITAL INDONESIA — QA TECHNICAL ASSESSMENT"
    ws1["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    ws1["A1"].fill = PatternFill(start_color=NAVY_DARK, end_color=NAVY_DARK, fill_type="solid")
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[1].height = 32

    ws1.merge_cells("A2:H2")
    ws1["A2"] = "LAPORAN BUG HUNTING & EXPLORATORY TESTING (BAGIAN 3)"
    ws1["A2"].font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
    ws1["A2"].fill = PatternFill(start_color=BLUE_PRIMARY, end_color=BLUE_PRIMARY, fill_type="solid")
    ws1["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[2].height = 24

    # Metadata Info
    meta = [
        ("Target URL", "https://with-bugs.practicesoftwaretesting.com", "Metode Pengujian", "Timeboxed Exploratory Testing (50 Menit)"),
        ("Environment", "Chrome v134.0 / Windows 11 Pro 64-bit", "Waktu Pelaksanaan", "04 Oktober 2026, 12:35 - 13:25 WIB"),
        ("Kandidat Tester", "Ageng QA Automation Engineer", "Total Bug Terverifikasi", "7 Temuan Cacat Aplikasi (1 Critical, 3 Major, 2 Minor, 1 Trivial)")
    ]

    for idx, (lbl1, val1, lbl2, val2) in enumerate(meta, start=4):
        ws1[f"A{idx}"] = lbl1
        ws1[f"A{idx}"].font = bold_font
        ws1[f"A{idx}"].fill = PatternFill(start_color=GRAY_HEADER, fill_type="solid")
        ws1.merge_cells(f"B{idx}:D{idx}")
        ws1[f"B{idx}"] = val1
        ws1[f"B{idx}"].font = cell_font

        ws1[f"E{idx}"] = lbl2
        ws1[f"E{idx}"].font = bold_font
        ws1[f"E{idx}"].fill = PatternFill(start_color=GRAY_HEADER, fill_type="solid")
        ws1.merge_cells(f"F{idx}:H{idx}")
        ws1[f"F{idx}"] = val2
        ws1[f"F{idx}"].font = cell_font
        ws1.row_dimensions[idx].height = 20

    # KPI Metric Boxes (Baris 8 - 10)
    kpi_cards = [
        ("TOTAL BUGS", "7", NAVY_DARK, "A", "B"),
        ("CRITICAL (P1)", "1", COLOR_CRITICAL, "C", "D"),
        ("MAJOR (P2)", "3", COLOR_MAJOR, "E", "F"),
        ("MINOR / TRIVIAL", "3", "4A5568", "G", "H")
    ]

    for title, val, color, col_start, col_end in kpi_cards:
        ws1.merge_cells(f"{col_start}8:{col_end}8")
        ws1[f"{col_start}8"] = title
        ws1[f"{col_start}8"].font = Font(name="Calibri", size=9, bold=True, color="FFFFFF")
        ws1[f"{col_start}8"].fill = PatternFill(start_color=color, fill_type="solid")
        ws1[f"{col_start}8"].alignment = Alignment(horizontal="center", vertical="center")

        ws1.merge_cells(f"{col_start}9:{col_end}9")
        ws1[f"{col_start}9"] = val
        ws1[f"{col_start}9"].font = Font(name="Calibri", size=20, bold=True, color=color)
        ws1[f"{col_start}9"].fill = PatternFill(start_color=BLUE_LIGHT if color == NAVY_DARK else "FFF5F5", fill_type="solid")
        ws1[f"{col_start}9"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws1.row_dimensions[8].height = 18
    ws1.row_dimensions[9].height = 36

    # Section 1. Definisi Severity & Priority
    ws1.merge_cells("A11:H11")
    ws1["A11"] = "1. STANDAR DEFINISI SEVERITY & PRIORITY PENGUJIAN"
    ws1["A11"].font = header_font_dark
    ws1.row_dimensions[11].height = 24

    sev_headers = ["Tingkat", "Severity (Tingkat Dampak)", "Priority (Urgensi Perbaikan)", "Kriteria & Dampak Operasional"]
    ws1.merge_cells("A12:B12")
    ws1["A12"] = sev_headers[0]
    ws1.merge_cells("C12:D12")
    ws1["C12"] = sev_headers[1]
    ws1["E12"] = sev_headers[2]
    ws1.merge_cells("F12:H12")
    ws1["F12"] = sev_headers[3]

    for col in ["A12", "C12", "E12", "F12"]:
        ws1[col].font = header_font_white
        ws1[col].fill = PatternFill(start_color=NAVY_DARK, fill_type="solid")
        ws1[col].alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[12].height = 22

    sev_matrix = [
        ("Critical", "Fitur utama rusak / transaksi finansial gagal / tidak ada workaround", "P1 (Showstopper)", "Wajib segera diperbaiki sebelum rilis berikutnya.", COLOR_CRITICAL, BG_CRITICAL),
        ("Major", "Fungsi penting keliru / salah kalkulasi, namun ada alternatif workaround", "P2 (High)", "Diselesaikan dalam siklus sprint berjalan saat ini.", COLOR_MAJOR, BG_MAJOR),
        ("Minor", "Fungsi sekunder/opsional tidak konsisten, tidak memblokir user", "P3 (Medium)", "Masuk ke backlog release berikutnya.", COLOR_MINOR, BG_MINOR),
        ("Trivial", "Masalah kosmetik, salah ketik (typo), alignment ringan", "P4 (Low)", "Diperbaiki saat code polish / waktu luang.", COLOR_TRIVIAL, BG_TRIVIAL),
    ]

    for idx, (sev, desc, prio, action, c_text, c_bg) in enumerate(sev_matrix, start=13):
        ws1.merge_cells(f"A{idx}:B{idx}")
        ws1[f"A{idx}"] = sev
        ws1[f"A{idx}"].font = Font(name="Calibri", size=10, bold=True, color=c_text)
        ws1[f"A{idx}"].fill = PatternFill(start_color=c_bg, fill_type="solid")
        ws1[f"A{idx}"].alignment = Alignment(horizontal="center", vertical="center")

        ws1.merge_cells(f"C{idx}:D{idx}")
        ws1[f"C{idx}"] = desc
        ws1[f"C{idx}"].font = cell_font
        ws1[f"C{idx}"].alignment = Alignment(vertical="center")

        ws1[f"E{idx}"] = prio
        ws1[f"E{idx}"].font = Font(name="Calibri", size=10, bold=True, color=c_text)
        ws1[f"E{idx}"].alignment = Alignment(horizontal="center", vertical="center")

        ws1.merge_cells(f"F{idx}:H{idx}")
        ws1[f"F{idx}"] = action
        ws1[f"F{idx}"].font = cell_font
        ws1[f"F{idx}"].alignment = Alignment(vertical="center")
        ws1.row_dimensions[idx].height = 22

    # Section 2. Tabel Ringkasan Bug
    ws1.merge_cells("A18:H18")
    ws1["A18"] = "2. TABEL RINGKASAN TEMUAN CACAT APLIKASI (BUG SUMMARY)"
    ws1["A18"].font = header_font_dark
    ws1.row_dimensions[18].height = 24

    sum_cols = ["ID", "Area / Modul", "Judul Temuan Bug", "Severity", "Priority", "Status", "Bukti Screenshot"]
    ws1["A19"] = sum_cols[0]
    ws1["B19"] = sum_cols[1]
    ws1.merge_cells("C19:D19")
    ws1["C19"] = sum_cols[2]
    ws1["E19"] = sum_cols[3]
    ws1["F19"] = sum_cols[4]
    ws1["G19"] = sum_cols[5]
    ws1["H19"] = sum_cols[6]

    for c in ["A19", "B19", "C19", "E19", "F19", "G19", "H19"]:
        ws1[c].font = header_font_white
        ws1[c].fill = PatternFill(start_color=NAVY_DARK, fill_type="solid")
        ws1[c].alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[19].height = 24

    for idx, b in enumerate(bugs_data, start=20):
        ws1[f"A{idx}"] = b["id"]
        ws1[f"A{idx}"].font = bold_font
        ws1[f"A{idx}"].alignment = Alignment(horizontal="center", vertical="center")

        ws1[f"B{idx}"] = b["area"]
        ws1[f"B{idx}"].font = cell_font
        ws1[f"B{idx}"].alignment = Alignment(vertical="center")

        ws1.merge_cells(f"C{idx}:D{idx}")
        ws1[f"C{idx}"] = b["title"]
        ws1[f"C{idx}"].font = cell_font
        ws1[f"C{idx}"].alignment = Alignment(vertical="center")

        ws1[f"E{idx}"] = b["severity"]
        ws1[f"E{idx}"].font = Font(name="Calibri", size=10, bold=True, color=b["sev_color"])
        ws1[f"E{idx}"].fill = PatternFill(start_color=b["sev_bg"], fill_type="solid")
        ws1[f"E{idx}"].alignment = Alignment(horizontal="center", vertical="center")

        ws1[f"F{idx}"] = b["priority"]
        ws1[f"F{idx}"].font = Font(name="Calibri", size=10, bold=True, color=b["sev_color"])
        ws1[f"F{idx}"].alignment = Alignment(horizontal="center", vertical="center")

        ws1[f"G{idx}"] = b["status"]
        ws1[f"G{idx}"].font = bold_font
        ws1[f"G{idx}"].alignment = Alignment(horizontal="center", vertical="center")

        ws1[f"H{idx}"] = ", ".join([os.path.basename(p) for p in b["evidence"]])
        ws1[f"H{idx}"].font = Font(name="Calibri", size=9, color="2B6CB0", underline="single")
        ws1[f"H{idx}"].alignment = Alignment(vertical="center")
        ws1.row_dimensions[idx].height = 24

    # Apply borders for Sheet 1
    for r in range(4, 27):
        for c in range(1, 9):
            cell = ws1.cell(row=r, column=c)
            cell.border = thin_border

    # Kolom widths Sheet 1
    ws1.column_dimensions["A"].width = 12
    ws1.column_dimensions["B"].width = 24
    ws1.column_dimensions["C"].width = 28
    ws1.column_dimensions["D"].width = 28
    ws1.column_dimensions["E"].width = 16
    ws1.column_dimensions["F"].width = 16
    ws1.column_dimensions["G"].width = 12
    ws1.column_dimensions["H"].width = 36


    # =============================================================
    # SHEET 2: DETAIL BUG & SCREENSHOT (EMBEDDED IMAGES)
    # =============================================================
    ws2 = wb.create_sheet(title="Detail Bug & Screenshot")
    ws2.views.sheetView[0].showGridLines = True

    # Header Sheet 2
    ws2.merge_cells("A1:G1")
    ws2["A1"] = "DETAIL TEMUAN BUG LENGKAP DENGAN BUKTI SCREENSHOT (BAGIAN 3)"
    ws2["A1"].font = Font(name="Calibri", size=13, bold=True, color="FFFFFF")
    ws2["A1"].fill = PatternFill(start_color=NAVY_DARK, fill_type="solid")
    ws2["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws2.row_dimensions[1].height = 30

    curr_row = 3
    for bug in bugs_data:
        # Title Card Header
        ws2.merge_cells(f"A{curr_row}:G{curr_row}")
        ws2[f"A{curr_row}"] = f"[{bug['id']}] {bug['title']}"
        ws2[f"A{curr_row}"].font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        ws2[f"A{curr_row}"].fill = PatternFill(start_color=bug["sev_color"], fill_type="solid")
        ws2[f"A{curr_row}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws2.row_dimensions[curr_row].height = 24
        curr_row += 1

        # Metadata Row
        ws2[f"A{curr_row}"] = "Area / Modul:"
        ws2[f"A{curr_row}"].font = bold_font
        ws2[f"B{curr_row}"] = bug["area"]
        ws2[f"B{curr_row}"].font = cell_font

        ws2[f"C{curr_row}"] = "Severity:"
        ws2[f"C{curr_row}"].font = bold_font
        ws2[f"D{curr_row}"] = bug["severity"]
        ws2[f"D{curr_row}"].font = Font(name="Calibri", size=10, bold=True, color=bug["sev_color"])
        ws2[f"D{curr_row}"].fill = PatternFill(start_color=bug["sev_bg"], fill_type="solid")
        ws2[f"D{curr_row}"].alignment = Alignment(horizontal="center", vertical="center")

        ws2[f"E{curr_row}"] = "Priority:"
        ws2[f"E{curr_row}"].font = bold_font
        ws2[f"F{curr_row}"] = bug["priority"]
        ws2[f"F{curr_row}"].font = Font(name="Calibri", size=10, bold=True, color=bug["sev_color"])
        ws2[f"F{curr_row}"].alignment = Alignment(horizontal="center", vertical="center")

        ws2[f"G{curr_row}"] = f"Status: {bug['status']}"
        ws2[f"G{curr_row}"].font = bold_font
        ws2[f"G{curr_row}"].alignment = Alignment(horizontal="center", vertical="center")
        ws2.row_dimensions[curr_row].height = 20
        curr_row += 1

        # Environment Row
        ws2[f"A{curr_row}"] = "Environment:"
        ws2[f"A{curr_row}"].font = bold_font
        ws2.merge_cells(f"B{curr_row}:G{curr_row}")
        ws2[f"B{curr_row}"] = bug["environment"]
        ws2[f"B{curr_row}"].font = cell_font
        ws2.row_dimensions[curr_row].height = 20
        curr_row += 1

        # Section Header Steps & Evidence
        ws2.merge_cells(f"A{curr_row}:C{curr_row}")
        ws2[f"A{curr_row}"] = "Langkah Reproduksi (Steps to Reproduce)"
        ws2[f"A{curr_row}"].font = bold_font
        ws2[f"A{curr_row}"].fill = PatternFill(start_color=GRAY_HEADER, fill_type="solid")

        ws2.merge_cells(f"D{curr_row}:G{curr_row}")
        ws2[f"D{curr_row}"] = "Bukti Visual Tangkapan Layar (Screenshot Evidence)"
        ws2[f"D{curr_row}"].font = bold_font
        ws2[f"D{curr_row}"].fill = PatternFill(start_color=GRAY_HEADER, fill_type="solid")
        ws2.row_dimensions[curr_row].height = 20
        curr_row += 1

        # Content Row (Steps in A:C, Image in D:G)
        image_row = curr_row
        ws2.merge_cells(f"A{image_row}:C{image_row}")
        ws2[f"A{image_row}"] = bug["steps"]
        ws2[f"A{image_row}"].font = cell_font
        ws2[f"A{image_row}"].alignment = Alignment(vertical="top", wrap_text=True)

        # Tambahkan Gambar Screenshot menggunakan openpyxl Image
        img_target_h = 160  # pt tinggi row
        ws2.row_dimensions[image_row].height = 165

        # Embed Image
        if bug["evidence"] and os.path.exists(bug["evidence"][0]):
            img_path = bug["evidence"][0]
            img = OpenpyxlImage(img_path)
            # Scale proportionally: 430px lebar, rasio 2.05:1 -> tinggi ~210px
            img.width = 410
            img.height = 200
            ws2.add_image(img, f"D{image_row}")

        curr_row += 1

        # Expected Result Row
        ws2[f"A{curr_row}"] = "Expected Result:"
        ws2[f"A{curr_row}"].font = bold_font
        ws2[f"A{curr_row}"].fill = PatternFill(start_color=GRAY_BG, fill_type="solid")
        ws2.merge_cells(f"B{curr_row}:G{curr_row}")
        ws2[f"B{curr_row}"] = bug["expected"]
        ws2[f"B{curr_row}"].font = cell_font
        ws2[f"B{curr_row}"].alignment = Alignment(vertical="center", wrap_text=True)
        ws2.row_dimensions[curr_row].height = 28
        curr_row += 1

        # Actual Result Row
        ws2[f"A{curr_row}"] = "Actual Result:"
        ws2[f"A{curr_row}"].font = bold_font
        ws2[f"A{curr_row}"].fill = PatternFill(start_color=GRAY_BG, fill_type="solid")
        ws2.merge_cells(f"B{curr_row}:G{curr_row}")
        ws2[f"B{curr_row}"] = bug["actual"]
        ws2[f"B{curr_row}"].font = cell_font
        ws2[f"B{curr_row}"].alignment = Alignment(vertical="center", wrap_text=True)
        ws2.row_dimensions[curr_row].height = 28
        curr_row += 1

        # Impact Row
        ws2[f"A{curr_row}"] = "Dampak & Risiko:"
        ws2[f"A{curr_row}"].font = bold_font
        ws2[f"A{curr_row}"].fill = PatternFill(start_color=GRAY_BG, fill_type="solid")
        ws2.merge_cells(f"B{curr_row}:G{curr_row}")
        ws2[f"B{curr_row}"] = bug["impact"]
        ws2[f"B{curr_row}"].font = cell_font
        ws2[f"B{curr_row}"].alignment = Alignment(vertical="center", wrap_text=True)
        ws2.row_dimensions[curr_row].height = 28
        curr_row += 1

        # Jika ada gambar evidence kedua (misal pada BUG-007)
        if len(bug["evidence"]) > 1 and os.path.exists(bug["evidence"][1]):
            ws2.merge_cells(f"A{curr_row}:G{curr_row}")
            ws2[f"A{curr_row}"] = f"Bukti Tambahan BUG-007: {os.path.basename(bug['evidence'][1])}"
            ws2[f"A{curr_row}"].font = small_font
            ws2[f"A{curr_row}"].fill = PatternFill(start_color=GRAY_HEADER, fill_type="solid")
            curr_row += 1

            img2_row = curr_row
            ws2.row_dimensions[img2_row].height = 165
            img2 = OpenpyxlImage(bug["evidence"][1])
            img2.width = 410
            img2.height = 200
            ws2.add_image(img2, f"B{img2_row}")
            curr_row += 1

        # Spacer row
        ws2.row_dimensions[curr_row].height = 16
        curr_row += 1

    # Widths Sheet 2
    ws2.column_dimensions["A"].width = 18
    ws2.column_dimensions["B"].width = 24
    ws2.column_dimensions["C"].width = 16
    ws2.column_dimensions["D"].width = 20
    ws2.column_dimensions["E"].width = 16
    ws2.column_dimensions["F"].width = 16
    ws2.column_dimensions["G"].width = 20


    # =============================================================
    # SHEET 3: TABEL DATABASE LENGKAP (GRID EXPORT)
    # =============================================================
    ws3 = wb.create_sheet(title="Tabel Database Lengkap")
    ws3.views.sheetView[0].showGridLines = True

    grid_headers = [
        "Bug ID", "Area / Modul", "Judul Temuan Bug", "Severity", "Priority", 
        "Status", "Langkah Reproduksi", "Expected Result", "Actual Result", "Dampak Bisnis", "File Screenshot"
    ]
    for col_idx, text in enumerate(grid_headers, start=1):
        cell = ws3.cell(row=1, column=col_idx, value=text)
        cell.font = header_font_white
        cell.fill = PatternFill(start_color=NAVY_DARK, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws3.row_dimensions[1].height = 26

    for row_idx, b in enumerate(bugs_data, start=2):
        ws3.cell(row=row_idx, column=1, value=b["id"]).font = bold_font
        ws3.cell(row=row_idx, column=1).alignment = Alignment(horizontal="center", vertical="top")

        ws3.cell(row=row_idx, column=2, value=b["area"]).font = cell_font
        ws3.cell(row=row_idx, column=2).alignment = Alignment(vertical="top")

        ws3.cell(row=row_idx, column=3, value=b["title"]).font = bold_font
        ws3.cell(row=row_idx, column=3).alignment = Alignment(vertical="top", wrap_text=True)

        c_sev = ws3.cell(row=row_idx, column=4, value=b["severity"])
        c_sev.font = Font(name="Calibri", size=10, bold=True, color=b["sev_color"])
        c_sev.fill = PatternFill(start_color=b["sev_bg"], fill_type="solid")
        c_sev.alignment = Alignment(horizontal="center", vertical="top")

        c_prio = ws3.cell(row=row_idx, column=5, value=b["priority"])
        c_prio.font = Font(name="Calibri", size=10, bold=True, color=b["sev_color"])
        c_prio.alignment = Alignment(horizontal="center", vertical="top")

        ws3.cell(row=row_idx, column=6, value=b["status"]).font = cell_font
        ws3.cell(row=row_idx, column=6).alignment = Alignment(horizontal="center", vertical="top")

        ws3.cell(row=row_idx, column=7, value=b["steps"]).font = cell_font
        ws3.cell(row=row_idx, column=7).alignment = Alignment(vertical="top", wrap_text=True)

        ws3.cell(row=row_idx, column=8, value=b["expected"]).font = cell_font
        ws3.cell(row=row_idx, column=8).alignment = Alignment(vertical="top", wrap_text=True)

        ws3.cell(row=row_idx, column=9, value=b["actual"]).font = cell_font
        ws3.cell(row=row_idx, column=9).alignment = Alignment(vertical="top", wrap_text=True)

        ws3.cell(row=row_idx, column=10, value=b["impact"]).font = cell_font
        ws3.cell(row=row_idx, column=10).alignment = Alignment(vertical="top", wrap_text=True)

        ws3.cell(row=row_idx, column=11, value="; ".join([os.path.basename(p) for p in b["evidence"]])).font = small_font
        ws3.cell(row=row_idx, column=11).alignment = Alignment(vertical="top", wrap_text=True)

        ws3.row_dimensions[row_idx].height = 110

        for col_idx in range(1, 12):
            ws3.cell(row=row_idx, column=col_idx).border = thin_border

    # Widths Sheet 3
    col_widths = [12, 18, 28, 12, 10, 10, 36, 28, 30, 28, 25]
    for idx, w in enumerate(col_widths, start=1):
        ws3.column_dimensions[get_column_letter(idx)].width = w

    # Simpan File
    output_path = "docs/03-bug-report.xlsx"
    wb.save(output_path)
    print(f"Laporan Excel berhasil dibuat di: {output_path}")

if __name__ == "__main__":
    create_bug_report_excel()
