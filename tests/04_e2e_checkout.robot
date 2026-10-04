*** Settings ***
Documentation       Scenario 4: End-to-End Product Purchase and Checkout Flow
Resource            ../pages/BasePage.robot
Resource            ../pages/RegisterPage.robot
Resource            ../pages/LoginPage.robot
Resource            ../pages/ProductCatalogPage.robot
Resource            ../pages/ProductDetailPage.robot
Resource            ../pages/CheckoutPage.robot
Library             ../resources/DataHelper.py

Test Setup          Open Application Browser
Test Teardown       Close Application Browser

*** Test Cases ***
TC_E2E_001_Complete_Product_Purchase_With_Cash_On_Delivery
    [Documentation]    Memverifikasi seluruh alur End-to-End e-commerce Toolshop:
    ...                Registrasi akun -> Login -> Pencarian Produk -> Detail Produk -> Tambah ke Keranjang ->
    ...                Multi-step Checkout (Keranjang, Konfirmasi Akun, Alamat Pengiriman, Metode Pembayaran COD) ->
    ...                Selesaikan Pesanan -> Verifikasi Konfirmasi Pembayaran Berhasil.
    [Tags]             smoke    regression    e2e    checkout    positive

    # 1. Setup Akun Baru & Login (Agar flow 100% mandiri dan tidak terdampak demo account lockout)
    ${user}=    Generate Unique User
    Navigate To Register Page
    Fill Registration Form    ${user}
    Submit Registration
    Verify Successful Registration Redirect

    Navigate To Login Page
    Input Credentials    ${user}[email]    ${user}[password]
    Submit Login Form
    Verify Login Successful

    # 2. Cari Produk pada Katalog
    Navigate To Catalog Home
    Search Product            Pliers
    Select First Product

    # 3. Verifikasi Halaman Detail & Tambah ke Keranjang
    Verify Product Detail Loaded
    ${product_name}=          Get Current Product Name
    ${product_price}=         Get Current Unit Price
    Log                       Memilih produk: ${product_name} dengan harga: ${product_price}
    Click Add To Cart

    # 4. Akses Halaman Keranjang / Checkout
    Proceed To Cart Via Navigation

    # 5. Multi-step Checkout
    # Step 1: Ringkasan Keranjang
    Verify Cart Item And Total
    Click Proceed Step 1

    # Step 2: Konfirmasi Akun Login
    Click Proceed Step 2

    # Step 3: Konfirmasi Alamat & Nomor Rumah
    Click Proceed Step 3

    # Step 4: Pilih Metode Pembayaran (Cash on Delivery) & Submit Order
    Select Payment Method And Submit    cash-on-delivery

    # 6. Assertions: Verifikasi Konfirmasi Pesanan dan Pembayaran Sukses
    Verify Order Confirmation Success
