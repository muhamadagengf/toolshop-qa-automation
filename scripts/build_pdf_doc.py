import subprocess
import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>01 - Analytical & Test Design (QA Technical Test)</title>
  <style>
    @page {
      size: A4;
      margin: 18mm 14mm 18mm 14mm;
      @bottom-right {
        content: counter(page);
      }
    }
    body {
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
      font-size: 10pt;
      line-height: 1.45;
      color: #2D3748;
      background-color: #FFFFFF;
      margin: 0;
      padding: 0;
    }
    .header-banner {
      border-bottom: 3px solid #1F4E79;
      padding-bottom: 12px;
      margin-bottom: 20px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    .company-title {
      font-size: 18pt;
      font-weight: 800;
      color: #1F4E79;
      letter-spacing: -0.5px;
      margin: 0;
    }
    .doc-subtitle {
      font-size: 12pt;
      font-weight: 600;
      color: #4A5568;
      margin-top: 4px;
      margin-bottom: 0;
    }
    .meta-box {
      background: #F7FAFC;
      border: 1px solid #E2E8F0;
      border-left: 4px solid #1F4E79;
      padding: 10px 14px;
      border-radius: 4px;
      margin-bottom: 22px;
      font-size: 9pt;
    }
    .meta-grid {
      display: grid;
      grid-template-columns: 140px 1fr 140px 1fr;
      gap: 6px 12px;
    }
    .meta-label {
      font-weight: 700;
      color: #2D3748;
    }
    h2 {
      font-size: 13pt;
      color: #1F4E79;
      border-bottom: 1.5px solid #CBD5E0;
      padding-bottom: 4px;
      margin-top: 24px;
      margin-bottom: 12px;
      page-break-after: avoid;
    }
    h3 {
      font-size: 11pt;
      color: #2B6CB0;
      margin-top: 16px;
      margin-bottom: 8px;
      page-break-after: avoid;
    }
    p {
      margin: 0 0 10px 0;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 18px;
      font-size: 8.5pt;
      page-break-inside: auto;
    }
    tr {
      page-break-inside: avoid;
      page-break-after: auto;
    }
    th {
      background-color: #1F4E79;
      color: #FFFFFF;
      font-weight: 700;
      text-align: left;
      padding: 7px 8px;
      border: 1px solid #1A365D;
    }
    td {
      padding: 6px 8px;
      border: 1px solid #CBD5E0;
      vertical-align: top;
    }
    tr:nth-child(even) td {
      background-color: #F8FAFC;
    }
    .badge {
      display: inline-block;
      padding: 2px 7px;
      font-size: 7.5pt;
      font-weight: 700;
      border-radius: 3px;
      text-align: center;
    }
    .badge-high {
      background-color: #FED7D7;
      color: #C53030;
      border: 1px solid #FEB2B2;
    }
    .badge-med {
      background-color: #FEFCBF;
      color: #B7791F;
      border: 1px solid #F6E05E;
    }
    .badge-valid {
      background-color: #C6F6D5;
      color: #22543D;
      border: 1px solid #9AE6B4;
    }
    .badge-invalid {
      background-color: #FED7D7;
      color: #9B2C2C;
      border: 1px solid #FEB2B2;
    }
    .text-center { text-align: center; }
    .text-bold { font-weight: 700; }
    .code-block {
      background-color: #1A202C;
      color: #E2E8F0;
      font-family: 'Consolas', 'Courier New', monospace;
      font-size: 8pt;
      padding: 12px;
      border-radius: 4px;
      margin-bottom: 16px;
      white-space: pre-wrap;
      line-height: 1.4;
      page-break-inside: avoid;
    }
    .feature-kw { color: #F6AD55; font-weight: bold; }
    .scenario-kw { color: #63B3ED; font-weight: bold; }
    .step-kw { color: #68D391; font-weight: bold; }
    .tag-kw { color: #FAF089; }
    .page-break {
      page-break-before: always;
    }
    ul, ol {
      margin-top: 0;
      margin-bottom: 10px;
      padding-left: 20px;
    }
    li {
      margin-bottom: 4px;
    }
  </style>
</head>
<body>

  <div class="header-banner">
    <div>
      <h1 class="company-title">TECHNICAL TEST - QA</h1>
      <div class="doc-subtitle">PT Logika Sarana Teknologi (Logique) — Bagian 1: Analytical & Test Design (35%)</div>
    </div>
  </div>

  <div class="meta-box">
    <div class="meta-grid">
      <div class="meta-label">Aplikasi Target:</div>
      <div>Practice Software Testing (Toolshop)</div>
      <div class="meta-label">Target URL:</div>
      <div>https://practicesoftwaretesting.com</div>
      <div class="meta-label">Lingkup Pengujian:</div>
      <div>Register, Login, Edit Profile, Navigasi Menu</div>
      <div class="meta-label">Tanggal Pengujian:</div>
      <div>Oktober 2026</div>
      <div class="meta-label">Kandidat QA:</div>
      <div>QA Automation Engineering Candidate</div>
      <div class="meta-label">File Pendukung:</div>
      <div>01-test-design.xlsx, features/*.feature</div>
    </div>
  </div>

  <h2>1. Risk Analysis & Mitigation Matrix</h2>
  <p>Analisis risiko mengidentifikasi 7 area rentan dengan pembobotan <strong>Likelihood (1–3) &times; Impact (1–3)</strong>. Diurutkan dari skor tertinggi:</p>

  <table>
    <thead>
      <tr>
        <th style="width: 7%;" class="text-center">ID</th>
        <th style="width: 25%;">Area Risiko</th>
        <th style="width: 7%;" class="text-center">L (1-3)</th>
        <th style="width: 7%;" class="text-center">I (1-3)</th>
        <th style="width: 8%;" class="text-center">Skor</th>
        <th style="width: 9%;" class="text-center">Level</th>
        <th style="width: 37%;">Alasan Risiko & Strategi Mitigasi</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="text-center text-bold">R-01</td>
        <td class="text-bold">Autentikasi & Penyimpanan Sesi (Broken Auth / Session Hijacking)</td>
        <td class="text-center">2</td>
        <td class="text-center">3</td>
        <td class="text-center text-bold">6</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Jika token sesi tidak diamankan atau tidak di-invalidate saat logout/ganti password, akun rentan dibajak.<br><strong>Mitigasi:</strong> Verifikasi invalidasi token pasca logout dan proteksi private route.</td>
      </tr>
      <tr>
        <td class="text-center text-bold">R-02</td>
        <td class="text-bold">Validasi Batasan Usia Pendaftar (DOB Validation Bypass)</td>
        <td class="text-center">3</td>
        <td class="text-center">2</td>
        <td class="text-center text-bold">6</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Syarat usia 18–75 thn seringkali hanya dicek di browser sehingga rentan dibypass via direct API.<br><strong>Mitigasi:</strong> Terapkan Boundary Value Analysis (BVA) pada field tanggal lahir baik di UI maupun API.</td>
      </tr>
      <tr>
        <td class="text-center text-bold">R-03</td>
        <td class="text-bold">Persistensi Data Pembaruan Profil (Data Loss on Reload)</td>
        <td class="text-center">2</td>
        <td class="text-center">3</td>
        <td class="text-center text-bold">6</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Perubahan alamat/telepon gagal tersimpan permanen di database, memicu salah pengiriman pesanan.<br><strong>Mitigasi:</strong> Uji skenario update profil, reload browser (F5), dan verifikasi sinkronisasi payload backend.</td>
      </tr>
      <tr>
        <td class="text-center text-bold">R-04</td>
        <td class="text-bold">Ganti Password Tanpa Verifikasi Password Lama</td>
        <td class="text-center">2</td>
        <td class="text-center">3</td>
        <td class="text-center text-bold">6</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Jika sistem mengizinkan password baru tanpa verifikasi password lama yang cocok, akun mudah diambil alih.<br><strong>Mitigasi:</strong> Uji penolakan saat password lama salah dan uji kompleksitas password baru.</td>
      </tr>
      <tr>
        <td class="text-center text-bold">R-05</td>
        <td class="text-bold">Duplikasi Email saat Registrasi (Race Condition / Conflict)</td>
        <td class="text-center">3</td>
        <td class="text-center">2</td>
        <td class="text-center text-bold">6</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Registrasi dengan email yang sudah ada berisiko corrupt jika backend tidak memiliki unique constraint.<br><strong>Mitigasi:</strong> Uji registrasi dengan email terdaftar, validasi kode HTTP 422 dan pesan error UI.</td>
      </tr>
      <tr>
        <td class="text-center text-bold">R-06</td>
        <td class="text-bold">Keamanan Input Form (Stored XSS / SQL Injection)</td>
        <td class="text-center">2</td>
        <td class="text-center">3</td>
        <td class="text-center text-bold">6</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Field nama atau alamat yang tidak disanitasi dapat mengeksekusi script jahat di profil atau invoice PDF.<br><strong>Mitigasi:</strong> Uji karakter HTML (&lt;script&gt;), petik, serta verifikasi output encoding di UI.</td>
      </tr>
      <tr>
        <td class="text-center text-bold">R-07</td>
        <td class="text-bold">Inkonsistensi Filter & Navigasi Kategori Produk</td>
        <td class="text-center">2</td>
        <td class="text-center">2</td>
        <td class="text-center text-bold">4</td>
        <td class="text-center"><span class="badge badge-med">Medium</span></td>
        <td>Jika query slug navigasi putus atau state kategori corrupt, katalog gagal menampilkan daftar produk.<br><strong>Mitigasi:</strong> Uji routing navigasi, sinkronisasi URL slug, dan verifikasi relevansi produk.</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <h2>2. Test Scenarios (Gherkin / BDD)</h2>
  <p>Skenario BDD disusun secara <strong>declarative</strong> (orientasi nilai bisnis, bukan teknis klik elemen). Tersimpan pada <code>features/auth_profile_navigation.feature</code>:</p>

  <div class="code-block"><span class="feature-kw">Feature:</span> User Authentication, Profile Management, and Navigation
  As a customer of Toolshop
  I want to register, authenticate, manage my personal profile, and browse product categories
  So that I can securely manage my account and find tools easily

  <span class="step-kw">Background:</span>
    <span class="step-kw">Given</span> the customer is on the Toolshop application home page

  <span class="tag-kw">@auth @register @smoke @positive</span>
  <span class="scenario-kw">Scenario:</span> Successful customer registration with valid personal details
    <span class="step-kw">Given</span> the customer navigates to the registration page
    <span class="step-kw">When</span> the customer submits the registration form with valid and complete personal information
    <span class="step-kw">Then</span> the system should register the new account successfully
    <span class="step-kw">And</span> the customer should be redirected to the login page with a success confirmation

  <span class="tag-kw">@auth @register @negative</span>
  <span class="scenario-kw">Scenario:</span> Registration rejected when applicant is under legal age (under 18 years old)
    <span class="step-kw">Given</span> the customer navigates to the registration page
    <span class="step-kw">When</span> the customer attempts to register with a date of birth indicating age younger than 18 years
    <span class="step-kw">Then</span> the system should reject the registration submission
    <span class="step-kw">And</span> an age validation error stating that the customer must be at least 18 years old should be displayed

  <span class="tag-kw">@auth @login @data-driven</span>
  <span class="scenario-kw">Scenario Outline:</span> Customer login attempts with various credential states
    <span class="step-kw">Given</span> the customer navigates to the login page
    <span class="step-kw">When</span> the customer attempts to sign in with email "&lt;email&gt;" and password "&lt;password&gt;"
    <span class="step-kw">Then</span> the authentication outcome should be "&lt;status&gt;"
    <span class="step-kw">And</span> the customer should receive the expected message "&lt;expected_message&gt;"

    <span class="scenario-kw">Examples:</span>
      | email                                | password         | status  | expected_message             |
      | customer@practicesoftwaretesting.com | welcome01        | SUCCESS | User dashboard displayed     |
      | customer@practicesoftwaretesting.com | WrongPassword99! | FAILED  | Invalid email or password    |
      | unregistered.user.2026@test.com      | ValidPass#2026   | FAILED  | Invalid email or password    |
      |                                      | ValidPass#2026   | FAILED  | E-mail is required           |
      | customer@practicesoftwaretesting.com |                  | FAILED  | Password is required         |

  <span class="tag-kw">@profile @positive</span>
  <span class="scenario-kw">Scenario:</span> Successful update of customer profile details
    <span class="step-kw">Given</span> the customer is authenticated with an active account
    <span class="step-kw">And</span> the customer accesses the account profile settings
    <span class="step-kw">When</span> the customer updates the phone number and residential address with new details
    <span class="step-kw">Then</span> the updated profile should be saved successfully
    <span class="step-kw">And</span> the new information should persist upon reloading the profile page

  <span class="tag-kw">@profile @password @negative</span>
  <span class="scenario-kw">Scenario:</span> Password change rejected when new password does not satisfy security complexity
    <span class="step-kw">Given</span> the customer is authenticated with an active account
    <span class="step-kw">And</span> the customer accesses the change password page
    <span class="step-kw">When</span> the customer attempts to set a weak new password lacking numbers or special characters
    <span class="step-kw">Then</span> the system should reject the password update request
    <span class="step-kw">And</span> a password complexity warning should prompt the customer to fulfill security requirements

  <span class="tag-kw">@navigation @catalog @positive</span>
  <span class="scenario-kw">Scenario:</span> Targeted product catalog filtering through header category menu
    <span class="step-kw">When</span> the customer navigates to "Power Tools" via the top categories navigation menu
    <span class="step-kw">Then</span> the product catalog view should display only products classified under "Power Tools"
    <span class="step-kw">And</span> the page header and breadcrumb should display "Power Tools"</div>

  <div class="page-break"></div>

  <h2>3. Detailed Test Cases Specification</h2>
  <p>Daftar 9 test case komprehensif (positif dan negatif) lengkap dengan precondition, test data, langkah uji, priority, dan teknik test design:</p>

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
      <tr>
        <td class="text-center text-bold">TC-REG-01</td>
        <td class="text-bold">Registrasi user baru dengan data lengkap & valid</td>
        <td><strong>Pre:</strong> Halaman home, guest.<br><strong>Data:</strong> John Doe, DOB: 1995-05-20, Email dinamis, Password@123</td>
        <td>1. Klik Sign in -> Register.<br>2. Isi seluruh field dengan data valid.<br>3. Klik tombol Register.</td>
        <td>Pendaftaran berhasil, otomatis redirect ke /auth/login, muncul pesan sukses.</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Equivalence Partitioning</td>
      </tr>
      <tr>
        <td class="text-center text-bold">TC-REG-02</td>
        <td class="text-bold">Registrasi ditolak saat usia pendaftar &lt; 18 tahun</td>
        <td><strong>Pre:</strong> Form /auth/register.<br><strong>Data:</strong> DOB = 2008-10-05 (17 thn 364 hr), data lain valid</td>
        <td>1. Isi form pendaftaran.<br>2. Masukkan DOB usia 17 thn.<br>3. Klik Register.</td>
        <td>Pendaftaran ditolak, muncul error: pendaftar minimal harus berusia 18 tahun.</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Boundary Value Analysis</td>
      </tr>
      <tr>
        <td class="text-center text-bold">TC-REG-03</td>
        <td class="text-bold">Registrasi ditolak saat email sudah terdaftar</td>
        <td><strong>Pre:</strong> Email sudah aktif di DB.<br><strong>Data:</strong> customer@practicesoftwaretesting.com</td>
        <td>1. Buka form registrasi.<br>2. Isi field email yang sudah terdaftar.<br>3. Submit form.</td>
        <td>Sistem menolak registrasi, menampilkan feedback error: email sudah digunakan.</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Error Guessing</td>
      </tr>
      <tr>
        <td class="text-center text-bold">TC-LOG-01</td>
        <td class="text-bold">Login berhasil dengan kredensial valid</td>
        <td><strong>Pre:</strong> Akun aktif terdaftar.<br><strong>Data:</strong> customer@practicesoftwaretesting.com / welcome01</td>
        <td>1. Buka /auth/login.<br>2. Masukkan email & password valid.<br>3. Klik tombol Login.</td>
        <td>Otentikasi sukses, redirect ke /account, nama user tampil pada menu navigasi.</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Decision Table</td>
      </tr>
      <tr>
        <td class="text-center text-bold">TC-LOG-02</td>
        <td class="text-bold">Login ditolak ketika password salah</td>
        <td><strong>Pre:</strong> User terdaftar.<br><strong>Data:</strong> Email valid, Password: SalahPassword#99</td>
        <td>1. Buka /auth/login.<br>2. Masukkan email valid & password salah.<br>3. Klik Login.</td>
        <td>Login gagal, tetap di login page, muncul alert: 'Invalid email or password'.</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Decision Table</td>
      </tr>
      <tr>
        <td class="text-center text-bold">TC-LOG-03</td>
        <td class="text-bold">Validasi field email & password dikosongkan</td>
        <td><strong>Pre:</strong> Form login.<br><strong>Data:</strong> Email: "", Password: ""</td>
        <td>1. Klik field email & password lalu biarkan kosong.<br>2. Klik Login.</td>
        <td>Muncul pesan error: 'E-mail is required' & 'Password is required'. Form tidak terkirim.</td>
        <td class="text-center"><span class="badge badge-med">Med</span></td>
        <td>Equivalence Partitioning</td>
      </tr>
      <tr>
        <td class="text-center text-bold">TC-PRF-01</td>
        <td class="text-bold">Update profil & verifikasi persistensi reload</td>
        <td><strong>Pre:</strong> Login di /account/profile.<br><strong>Data:</strong> Phone baru, Alamat baru</td>
        <td>1. Ubah nilai Phone & Address.<br>2. Klik Update Profile.<br>3. Reload browser page (F5).</td>
        <td>Muncul notifikasi sukses update, data baru tetap tampil setelah halaman di-reload.</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>State Transition</td>
      </tr>
      <tr>
        <td class="text-center text-bold">TC-PWD-01</td>
        <td class="text-bold">Ganti password ditolak jika tidak memenuhi syarat</td>
        <td><strong>Pre:</strong> Login di Change Password.<br><strong>Data:</strong> Current: welcome01, New: simplepass</td>
        <td>1. Masukkan current pass valid.<br>2. Masukkan new pass tanpa angka/simbol.<br>3. Klik Save.</td>
        <td>Sistem menolak update password, muncul peringatan syarat kompleksitas password.</td>
        <td class="text-center"><span class="badge badge-high">High</span></td>
        <td>Boundary & Decision</td>
      </tr>
      <tr>
        <td class="text-center text-bold">TC-NAV-01</td>
        <td class="text-bold">Navigasi menu kategori produk (Power Tools)</td>
        <td><strong>Pre:</strong> Berada di beranda.<br><strong>Data:</strong> Kategori 'Power Tools' (/category/power-tools)</td>
        <td>1. Klik dropdown Categories.<br>2. Pilih 'Power Tools'.<br>3. Verifikasi halaman katalog.</td>
        <td>URL berubah ke /category/power-tools, judul 'Power Tools', hanya produk kategori tersebut tampil.</td>
        <td class="text-center"><span class="badge badge-med">Med</span></td>
        <td>State Transition</td>
      </tr>
    </tbody>
  </table>

  <div class="page-break"></div>

  <h2>4. Penerapan Teknik Test Design Formal Secara Konkret</h2>

  <h3>4.1. Teknik 1: Equivalence Partitioning (EP) & Boundary Value Analysis (BVA)</h3>
  <p>Diterapkan pada aturan bisnis field <strong>Tanggal Lahir (Date of Birth)</strong>: Batasan usia pendaftar wajib antara <strong>18 s.d. 75 tahun</strong> (Asumsi tanggal sistem pengujian: <code>04-10-2026</code>).</p>

  <p><strong>A. Tabel Partisi (Equivalence Partitioning):</strong></p>
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
      <tr>
        <td class="text-center text-bold">P1</td>
        <td>Usia &lt; 18 tahun (Minor)</td>
        <td>2012-05-10 (14 thn)</td>
        <td class="text-center"><span class="badge badge-invalid">Invalid</span></td>
        <td>Ditolak: usia minimal pendaftar 18 tahun</td>
      </tr>
      <tr>
        <td class="text-center text-bold">P2</td>
        <td>18 tahun &le; Usia &le; 75 tahun (Legal)</td>
        <td>1990-08-15 (36 thn)</td>
        <td class="text-center"><span class="badge badge-valid">Valid</span></td>
        <td>Diterima: registrasi dapat dilanjutkan</td>
      </tr>
      <tr>
        <td class="text-center text-bold">P3</td>
        <td>Usia &gt; 75 tahun (Senior di atas batas)</td>
        <td>1945-01-01 (81 thn)</td>
        <td class="text-center"><span class="badge badge-invalid">Invalid</span></td>
        <td>Ditolak: usia maksimal pendaftar 75 tahun</td>
      </tr>
      <tr>
        <td class="text-center text-bold">P4</td>
        <td>Tanggal di masa depan (Future Date)</td>
        <td>2028-01-01 (-2 thn)</td>
        <td class="text-center"><span class="badge badge-invalid">Invalid</span></td>
        <td>Ditolak: tanggal lahir tidak boleh di masa depan</td>
      </tr>
      <tr>
        <td class="text-center text-bold">P5</td>
        <td>Format non-tanggal / string acak</td>
        <td>abc-def-ghij</td>
        <td class="text-center"><span class="badge badge-invalid">Invalid</span></td>
        <td>Ditolak: format tanggal wajib YYYY-MM-DD</td>
      </tr>
    </tbody>
  </table>

  <p><strong>B. Nilai Batas (Boundary Value Analysis):</strong></p>
  <table>
    <thead>
      <tr>
        <th style="width: 12%;" class="text-center">Titik Uji</th>
        <th style="width: 26%;">Nilai Uji (DOB)</th>
        <th style="width: 32%;">Representasi Batas</th>
        <th style="width: 10%;" class="text-center">Status</th>
        <th style="width: 20%;">Expected Result</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="text-center text-bold">BVA-01</td>
        <td>2008-10-05 (17 thn 364 hr)</td>
        <td>Just below min boundary (18 thn - 1 hr)</td>
        <td class="text-center"><span class="badge badge-invalid">Invalid</span></td>
        <td>Ditolak (Error: usia &lt; 18 thn)</td>
      </tr>
      <tr>
        <td class="text-center text-bold">BVA-02</td>
        <td>2008-10-04 (Tepat 18 thn)</td>
        <td>Exact minimum valid boundary</td>
        <td class="text-center"><span class="badge badge-valid">Valid</span></td>
        <td>Diterima</td>
      </tr>
      <tr>
        <td class="text-center text-bold">BVA-03</td>
        <td>2008-10-03 (18 thn 1 hr)</td>
        <td>Just above min boundary (18 thn + 1 hr)</td>
        <td class="text-center"><span class="badge badge-valid">Valid</span></td>
        <td>Diterima</td>
      </tr>
      <tr>
        <td class="text-center text-bold">BVA-04</td>
        <td>1951-10-05 (74 thn 364 hr)</td>
        <td>Just below max boundary (75 thn - 1 hr)</td>
        <td class="text-center"><span class="badge badge-valid">Valid</span></td>
        <td>Diterima</td>
      </tr>
      <tr>
        <td class="text-center text-bold">BVA-05</td>
        <td>1951-10-04 (Tepat 75 thn)</td>
        <td>Exact maximum valid boundary</td>
        <td class="text-center"><span class="badge badge-valid">Valid</span></td>
        <td>Diterima</td>
      </tr>
      <tr>
        <td class="text-center text-bold">BVA-06</td>
        <td>1951-10-03 (75 thn 1 hr)</td>
        <td>Just above max boundary (75 thn + 1 hr)</td>
        <td class="text-center"><span class="badge badge-invalid">Invalid</span></td>
        <td>Ditolak (Error: usia &gt; 75 thn)</td>
      </tr>
    </tbody>
  </table>

  <h3>4.2. Teknik 2: Decision Table Testing (Logika Autentikasi Pengguna)</h3>
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
      <tr>
        <td class="text-bold">C1: Format Email Valid</td>
        <td class="text-center">Y</td>
        <td class="text-center">Y</td>
        <td class="text-center">Y</td>
        <td class="text-center">T</td>
        <td class="text-center">Y</td>
        <td class="text-center">T</td>
      </tr>
      <tr>
        <td class="text-bold">C2: Email Terdaftar di Database</td>
        <td class="text-center">Y</td>
        <td class="text-center">Y</td>
        <td class="text-center">T</td>
        <td class="text-center">-</td>
        <td class="text-center">Y</td>
        <td class="text-center">-</td>
      </tr>
      <tr>
        <td class="text-bold">C3: Password Sesuai Hash DB</td>
        <td class="text-center">Y</td>
        <td class="text-center">T</td>
        <td class="text-center">-</td>
        <td class="text-center">-</td>
        <td class="text-center">-</td>
        <td class="text-center">-</td>
      </tr>
      <tr>
        <td class="text-bold">C4: Field Password Terisi</td>
        <td class="text-center">Y</td>
        <td class="text-center">Y</td>
        <td class="text-center">Y</td>
        <td class="text-center">Y</td>
        <td class="text-center">T</td>
        <td class="text-center">T</td>
      </tr>
      <tr style="background-color: #E2E8F0;">
        <td colspan="7" class="text-bold" style="padding: 4px 8px; color: #1F4E79;">AKSI SISTEM (ACTIONS)</td>
      </tr>
      <tr>
        <td>A1: Login Sukses & Buat Token Sesi</td>
        <td class="text-center text-bold" style="background: #C6F6D5;">X</td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
      </tr>
      <tr>
        <td>A2: Redirect ke Dashboard (/account)</td>
        <td class="text-center text-bold" style="background: #C6F6D5;">X</td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
      </tr>
      <tr>
        <td>A3: Tampilkan Pesan 'Invalid email or password'</td>
        <td class="text-center"></td>
        <td class="text-center text-bold" style="background: #FED7D7;">X</td>
        <td class="text-center text-bold" style="background: #FED7D7;">X</td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
      </tr>
      <tr>
        <td>A4: Tampilkan Validasi 'Format e-mail tidak valid'</td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center text-bold" style="background: #FEFCBF;">X</td>
        <td class="text-center"></td>
        <td class="text-center"></td>
      </tr>
      <tr>
        <td>A5: Tampilkan Validasi 'Password is required'</td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center"></td>
        <td class="text-center text-bold" style="background: #FEFCBF;">X</td>
        <td class="text-center text-bold" style="background: #FEFCBF;">X</td>
      </tr>
    </tbody>
  </table>

  <h3>4.3. Teknik 3: State Transition Testing (Siklus Akun Pengguna)</h3>
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
      <tr>
        <td class="text-bold">S0: Guest</td>
        <td>Submit Form Registrasi Valid</td>
        <td>POST /users/register, simpan akun</td>
        <td class="text-bold">S1: Registered</td>
      </tr>
      <tr>
        <td class="text-bold">S0: Guest</td>
        <td>Submit Kredensial Login Valid</td>
        <td>POST /users/login, terbitkan token JWT</td>
        <td class="text-bold">S2: Authenticated</td>
      </tr>
      <tr>
        <td class="text-bold">S2: Authenticated</td>
        <td>Ubah Nilai Profil & Klik Update</td>
        <td>PUT /users/me, update database</td>
        <td class="text-bold">S3: Profile Updated</td>
      </tr>
      <tr>
        <td class="text-bold">S3: Profile Updated</td>
        <td>Reload Browser (F5)</td>
        <td>GET /users/me, populate form</td>
        <td class="text-bold">S3: Profile Updated (Persisted)</td>
      </tr>
      <tr>
        <td class="text-bold">S2: Authenticated</td>
        <td>Klik Tombol 'Sign Out'</td>
        <td>Hapus JWT session storage</td>
        <td class="text-bold">S0: Guest</td>
      </tr>
    </tbody>
  </table>

  <h2>5. Out of Scope & Asumsi Pengujian</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
    <div>
      <h3 style="margin-top: 0;">Out of Scope (Sengaja Tidak Dites)</h3>
      <ul>
        <li><strong>Verifikasi Email SMTP Real Server:</strong> Aplikasi demo langsung mengaktifkan akun tanpa tautan email nyata.</li>
        <li><strong>Payment Gateway Real Kartu Kredit:</strong> Transaksi diuji dalam mode demo/dummy belanja e-commerce.</li>
        <li><strong>Social Login (OAuth Google / FB):</strong> Arsitektur Toolshop belum menyediakan integrasi pihak ketiga.</li>
        <li><strong>Deep Penetration Testing (DAST):</strong> Fokus pengujian adalah QA fungsional & test design sesuai brief.</li>
      </ul>
    </div>
    <div>
      <h3 style="margin-top: 0;">Asumsi Pengujian</h3>
      <ul>
        <li><strong>Environment Stabil:</strong> Server demo publik <code>practicesoftwaretesting.com</code> beroperasi normal.</li>
        <li><strong>Isolasi Data Uji:</strong> Registrasi otomatis menggunakan email unik berbasis timestamp agar bebas konflik duplikasi.</li>
        <li><strong>Basis Perhitungan Usia:</strong> Pengecekan usia 18–75 thn berpedoman pada tanggal pengujian dijalankan.</li>
        <li><strong>Browser Standar:</strong> Pengujian dioptimasi untuk browser modern berbasis Chromium (Chrome / Edge).</li>
      </ul>
    </div>
  </div>

</body>
</html>
"""

html_path = "c:/genesis-sage-automation/logique-qa-assessment/docs/01-test-design-print.html"
pdf_path = "c:/genesis-sage-automation/logique-qa-assessment/docs/01-test-design.pdf"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]
chrome_bin = next((p for p in chrome_paths if os.path.exists(p)), None)

if chrome_bin:
    cmd = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]
    subprocess.run(cmd, check=True)
    print(f"PDF successfully generated at: {pdf_path}")
else:
    print("Chrome binary not found!")
