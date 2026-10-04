*** Settings ***
Documentation       Scenario 2: Customer Authentication Flow (Positive Login & Data-Driven Negative Validations)
Resource            ../pages/BasePage.robot
Resource            ../pages/RegisterPage.robot
Resource            ../pages/LoginPage.robot
Library             ../resources/DataHelper.py

Test Setup          Open Application Browser
Test Teardown       Close Application Browser

*** Test Cases ***
TC_LOG_001_Positive_Login_With_Registered_User
    [Documentation]    Memverifikasi proses login berhasil menggunakan kredensial akun yang baru didaftarkan secara dinamis.
    ...                Memastikan user diarahkan ke halaman akun (/account) dan menu pengguna aktif.
    [Tags]             smoke    regression    auth    login    positive

    # 1. Daftarkan akun baru secara dinamis agar independen dari demo account
    ${user}=    Generate Unique User
    Navigate To Register Page
    Fill Registration Form    ${user}
    Submit Registration
    Verify Successful Registration Redirect

    # 2. Lakukan login dengan kredensial yang baru didaftarkan
    Navigate To Login Page
    Input Credentials    ${user}[email]    ${user}[password]
    Submit Login Form

    # 3. Verifikasi keberhasilan login
    Verify Login Successful
    Location Should Contain    /account
    Page Should Contain Element    ${NAV_USER_MENU}

TC_LOG_002_Data_Driven_Negative_Login_Combinations
    [Documentation]    Memverifikasi skenario negatif login menggunakan data-driven testing dari file JSON.
    ...                Mencakup: password salah, email belum terdaftar, email kosong, dan password kosong.
    [Tags]             regression    auth    login    negative    data-driven

    ${test_cases}=    Load Json Data    data/login_test_data.json

    FOR    ${tc}    IN    @{test_cases}
        Log    Menjalankan Test Case: ${tc}[test_id] - ${tc}[description]
        Navigate To Login Page
        Input Credentials    ${tc}[email]    ${tc}[password]
        Submit Login Form
        Verify Login Error Message    ${tc}[expected_message]
        Location Should Contain    /auth/login
    END
