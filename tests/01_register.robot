*** Settings ***
Documentation       Scenario 1: User Registration with Dynamic Generated Unique Data
Resource            ../pages/BasePage.robot
Resource            ../pages/RegisterPage.robot
Library             ../resources/DataHelper.py

Test Setup          Open Application Browser
Test Teardown       Close Application Browser

*** Test Cases ***
TC_REG_001_Register_New_User_With_Dynamic_Unique_Data
    [Documentation]    Memverifikasi registrasi user baru dengan data unik dinamis (bukan hardcode)
    ...                dan memastikan redirect otomatis ke halaman login (/auth/login).
    [Tags]             smoke    regression    auth    register

    # 1. Generate Data Unik Dinamis
    ${unique_user}=    Generate Unique User
    Log                Mendaftarkan pengguna unik: ${unique_user}[email]

    # 2. Akses Formulir Registrasi
    Navigate To Register Page

    # 3. Isi Formulir dengan Data Lengkap
    Fill Registration Form    ${unique_user}

    # 4. Submit Pendaftaran
    Submit Registration

    # 5. Assertions: Verifikasi Redirect ke /auth/login dan Elemen Login Ditampilkan
    Verify Successful Registration Redirect
    Location Should Contain    /auth/login
    Page Should Contain Element    id=email
