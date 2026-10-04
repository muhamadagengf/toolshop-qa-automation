*** Settings ***
Documentation       Page Object for Account Profile Management
Resource            BasePage.robot

*** Variables ***
${PROFILE_PHONE}            id=phone
${PROFILE_STREET}           id=street
${PROFILE_CITY}             id=city
${PROFILE_SUBMIT_BTN}       css:[data-test="update-profile-submit"]
${PROFILE_SUCCESS_ALERT}    css:.alert-success, div[role="alert"]

*** Keywords ***
Navigate To Profile Page
    Go To    ${BASE_URL}/account/profile
    Wait Until Element Is Visible    ${PROFILE_PHONE}    timeout=${TIMEOUT}
    Wait Until Keyword Succeeds      ${TIMEOUT}    500ms    Element Value Should Not Be Empty    ${PROFILE_PHONE}

Update Phone Number
    [Arguments]    ${new_phone}
    Wait And Input Text    ${PROFILE_PHONE}    ${new_phone}

Update Street Address
    [Arguments]    ${new_street}
    Wait And Input Text    ${PROFILE_STREET}    ${new_street}

Submit Profile Changes
    Wait And Click    ${PROFILE_SUBMIT_BTN}
    Wait Until Page Contains    Your profile is successfully updated    timeout=${TIMEOUT}

Reload Profile Page
    Reload Page
    Wait Until Element Is Visible    ${PROFILE_PHONE}    timeout=${TIMEOUT}

Verify Phone Value
    [Arguments]    ${expected_phone}
    Wait Until Keyword Succeeds    ${TIMEOUT}    500ms    Element Value Should Be Equal    ${PROFILE_PHONE}    ${expected_phone}

Verify Street Value
    [Arguments]    ${expected_street}
    Wait Until Keyword Succeeds    ${TIMEOUT}    500ms    Element Value Should Be Equal    ${PROFILE_STREET}    ${expected_street}

Element Value Should Be Equal
    [Arguments]    ${locator}    ${expected_value}
    ${actual_value}=    Get Value    ${locator}
    Should Be Equal As Strings       ${actual_value}    ${expected_value}

Element Value Should Not Be Empty
    [Arguments]    ${locator}
    ${val}=    Get Value    ${locator}
    Should Not Be Empty    ${val}
