*** Settings ***
Documentation       Page Object for Product Catalog and Search
Resource            BasePage.robot

*** Variables ***
${SEARCH_QUERY_INPUT}       css:[data-test="search-query"]
${SEARCH_SUBMIT_BTN}        css:[data-test="search-submit"]
${PRODUCT_CARD}             css:a.card
${PRODUCT_CARD_TITLE}       css:.card-title, [data-test="product-name"], h5

*** Keywords ***
Navigate To Catalog Home
    Go To    ${BASE_URL}
    Wait Until Element Is Visible    ${PRODUCT_CARD}    timeout=${TIMEOUT}

Search Product
    [Arguments]    ${search_term}
    Wait And Input Text      ${SEARCH_QUERY_INPUT}    ${search_term}
    Wait And Click Via JS    ${SEARCH_SUBMIT_BTN}
    Wait Until Page Contains Element    ${PRODUCT_CARD}    timeout=${TIMEOUT}

Select First Product
    Wait Until Element Is Visible    ${PRODUCT_CARD}    timeout=${TIMEOUT}
    Wait And Click Via JS            ${PRODUCT_CARD}
