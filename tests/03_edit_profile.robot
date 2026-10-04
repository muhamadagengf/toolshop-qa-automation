*** Settings ***
Documentation       Scenario 3: Edit and Update User Profile with Data Persistence Verification
Resource            ../pages/BasePage.robot
Resource            ../pages/RegisterPage.robot
Resource            ../pages/LoginPage.robot
Resource            ../pages/ProfilePage.robot
Library             ../resources/DataHelper.py

Test Setup          Open Application Browser
Test Teardown       Close Application Browser

*** Test Cases ***
TC_PROF_001_Update_Profile_Information_And_Verify_Persistence
    [Documentation]    Memverifikasi proses update data profil (nomor telepon & alamat jalan) berhasil disimpan,
    ...                menampilkan pesan sukses, dan data yang diperbarui tetap tersimpan setelah reload halaman (F5).
    [Tags]             smoke    regression    profile    positive

    # 1. Setup Akun Baru & Login
    ${user}=    Generate Unique User
    Navigate To Register Page
    Fill Registration Form    ${user}
    Submit Registration
    Verify Successful Registration Redirect

    Navigate To Login Page
    Input Credentials    ${user}[email]    ${user}[password]
    Submit Login Form
    Verify Login Successful

    # 2. Akses Halaman Profil
    Navigate To Profile Page

    # 3. Ubah Nomor Telepon dan Alamat Jalan
    ${updated_phone}=     Set Variable    081299998888
    ${updated_street}=    Set Variable    Jalan Gatot Subroto No. 88

    Update Phone Number       ${updated_phone}
    Update Street Address     ${updated_street}

    # 4. Simpan Perubahan dan Verifikasi Alert Sukses
    Submit Profile Changes

    # 5. Reload Halaman (F5) untuk Verifikasi Data Persistence
    Reload Profile Page

    # 6. Assertions: Pastikan nilai yang baru disimpan tidak kembali ke data lama
    Verify Phone Value     ${updated_phone}
    Verify Street Value    ${updated_street}
