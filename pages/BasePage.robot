*** Settings ***
Documentation       Base Page containing reusable setup, teardown, and explicit wait utilities
Library             SeleniumLibrary
Library             Collections
Library             OperatingSystem
Library             String
Resource            ../config/env.robot

*** Variables ***
${NAV_HOME}             css:[data-test="nav-home"]
${NAV_SIGN_IN}          css:[data-test="nav-sign-in"]
${NAV_CART}             css:[data-test="nav-cart"]
${NAV_USER_MENU}        css:[data-test="nav-menu"]
${NAV_PROFILE}          css:[data-test="nav-profile"]

*** Keywords ***
Open Application Browser
    [Arguments]    ${mode}=default    ${url}=${BASE_URL}
    ${chrome_options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys
    Call Method    ${chrome_options}    add_argument    --window-size\=1920,1080
    Call Method    ${chrome_options}    add_argument    --disable-gpu
    Call Method    ${chrome_options}    add_argument    --no-sandbox
    Call Method    ${chrome_options}    add_argument    --disable-dev-shm-usage
    ${mode_upper}=    Convert To Upper Case    ${mode}
    IF    '${mode_upper}' == 'CHROME' or '${mode_upper}' == 'HEADED'
        Log    Running browser in HEADED mode
    ELSE IF    '${HEADLESS}' == 'true'
        Call Method    ${chrome_options}    add_argument    --headless\=new
    END
    Open Browser    ${url}    browser=chrome    options=${chrome_options}
    Set Selenium Timeout    ${TIMEOUT}
    Set Selenium Implicit Wait    ${IMPLICIT_WAIT}

CHROME
    [Documentation]    Shorthand keyword to directly run test in headed Chrome
    [Arguments]    ${url}=${BASE_URL}
    Open Application Browser    mode=CHROME    url=${url}

Close Application Browser
    Close Browser

Wait And Click
    [Arguments]    ${locator}
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Wait Until Element Is Enabled    ${locator}    timeout=${TIMEOUT}
    Scroll Element Into View         ${locator}
    Click Element                    ${locator}

Wait And Click Via JS
    [Arguments]    ${locator}
    Wait Until Page Contains Element    ${locator}    timeout=${TIMEOUT}
    ${element}=    Get WebElement       ${locator}
    Execute Javascript    arguments[0].scrollIntoView(true); arguments[0].click();    ARGUMENTS    ${element}

Wait And Input Text
    [Arguments]    ${locator}    ${text}
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Wait Until Element Is Enabled    ${locator}    timeout=${TIMEOUT}
    Scroll Element Into View         ${locator}
    Clear Element Text               ${locator}
    Input Text                       ${locator}    ${text}

Wait And Input Password
    [Arguments]    ${locator}    ${password}
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Wait Until Element Is Enabled    ${locator}    timeout=${TIMEOUT}
    Scroll Element Into View         ${locator}
    Clear Element Text               ${locator}
    Input Password                   ${locator}    ${password}

Wait And Select From List By Value
    [Arguments]    ${locator}    ${value}
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Scroll Element Into View         ${locator}
    Select From List By Value        ${locator}    ${value}

Wait And Verify Text Contains
    [Arguments]    ${locator}    ${expected_text}
    Wait Until Element Is Visible    ${locator}    timeout=${TIMEOUT}
    Element Should Contain           ${locator}    ${expected_text}

Wait And Verify Location Contains
    [Arguments]    ${expected_url_part}
    Wait Until Location Contains    ${expected_url_part}    timeout=${TIMEOUT}

Element Value Should Not Be Empty
    [Arguments]    ${locator}
    ${val}=    Get Value    ${locator}
    Should Not Be Empty    ${val}
