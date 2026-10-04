*** Settings ***
Documentation       Page Object for Customer Login and Authentication Validations
Resource            BasePage.robot

*** Variables ***
${LOGIN_EMAIL}          id=email
${LOGIN_PASSWORD}       id=password
${LOGIN_SUBMIT_BTN}     css:[data-test="login-submit"]
${LOGIN_ERROR_ALERT}    css:[data-test="login-error"], .alert-danger
${NAV_USER_MENU}        css:[data-test="nav-menu"]

*** Keywords ***
Navigate To Login Page
    Go To    ${BASE_URL}/auth/login
    Wait Until Element Is Visible    ${LOGIN_EMAIL}    timeout=${TIMEOUT}

Input Credentials
    [Arguments]    ${email}    ${password}
    IF    '${email}' != ''
        Wait And Input Text    ${LOGIN_EMAIL}    ${email}
    ELSE
        Clear Element Text     ${LOGIN_EMAIL}
    END
    IF    '${password}' != ''
        Wait And Input Password    ${LOGIN_PASSWORD}    ${password}
    ELSE
        Clear Element Text         ${LOGIN_PASSWORD}
    END

Submit Login Form
    Wait And Click    ${LOGIN_SUBMIT_BTN}

Perform Login
    [Arguments]    ${email}    ${password}
    Navigate To Login Page
    Input Credentials    ${email}    ${password}
    Submit Login Form

Verify Login Successful
    Wait Until Page Contains Element    ${NAV_USER_MENU}    timeout=${TIMEOUT}
    Wait And Verify Location Contains   /account

Verify Login Error Message
    [Arguments]    ${expected_message}
    Wait Until Page Contains            ${expected_message}    timeout=${TIMEOUT}

Verify Validation Error Visible
    [Arguments]    ${expected_validation}
    Wait Until Page Contains            ${expected_validation}    timeout=${TIMEOUT}
