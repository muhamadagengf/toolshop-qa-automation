*** Settings ***
Documentation       Page Object for Customer Registration
Resource            BasePage.robot

*** Variables ***
${REG_FIRST_NAME}       id=first_name
${REG_LAST_NAME}        id=last_name
${REG_DOB}              id=dob
${REG_STREET}           id=street
${REG_HOUSE_NUMBER}     id=house_number
${REG_POSTAL_CODE}      id=postal_code
${REG_CITY}             id=city
${REG_STATE}            id=state
${REG_COUNTRY}          id=country
${REG_PHONE}            id=phone
${REG_EMAIL}            id=email
${REG_PASSWORD}         id=password
${REG_SUBMIT_BTN}       css:[data-test="register-submit"]
${REG_ALERT_ERROR}      css:.alert-danger, .invalid-feedback

*** Keywords ***
Navigate To Register Page
    Go To    ${BASE_URL}/auth/register
    Wait Until Element Is Visible    ${REG_FIRST_NAME}    timeout=${TIMEOUT}

Fill Registration Form
    [Arguments]    ${user}
    Wait And Input Text    ${REG_FIRST_NAME}       ${user}[first_name]
    Wait And Input Text    ${REG_LAST_NAME}        ${user}[last_name]
    Wait And Input Text    ${REG_DOB}              ${user}[dob]
    Wait And Input Text    ${REG_STREET}           ${user}[street]
    Wait And Input Text    ${REG_HOUSE_NUMBER}     ${user}[house_number]
    Wait And Input Text    ${REG_POSTAL_CODE}      ${user}[postal_code]
    Wait And Input Text    ${REG_CITY}             ${user}[city]
    Wait And Input Text    ${REG_STATE}            ${user}[state]
    Wait And Select From List By Value    ${REG_COUNTRY}    ${user}[country]
    Wait And Input Text    ${REG_PHONE}            ${user}[phone]
    Wait And Input Text        ${REG_EMAIL}            ${user}[email]
    Wait And Input Password    ${REG_PASSWORD}         ${user}[password]
    Press Keys                 ${REG_PASSWORD}         TAB

Submit Registration
    Scroll Element Into View         ${REG_SUBMIT_BTN}
    Wait Until Element Is Visible    ${REG_SUBMIT_BTN}    timeout=${TIMEOUT}
    Wait And Click Via JS            ${REG_SUBMIT_BTN}

Verify Successful Registration Redirect
    Wait And Verify Location Contains    /auth/login
    Wait Until Element Is Visible        id=email    timeout=${TIMEOUT}

Verify Validation Error Displayed
    [Arguments]    ${expected_error_text}
    Wait Until Page Contains             ${expected_error_text}    timeout=${TIMEOUT}
