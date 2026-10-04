*** Settings ***
Documentation       Page Object for Checkout Steps, Payment, and Order Confirmation
Resource            BasePage.robot

*** Variables ***
${CART_PRODUCT_TITLE}       css:[data-test="product-title"]
${CART_TOTAL_PRICE}         css:[data-test="cart-total"]
${PROCEED_STEP_1}           css:[data-test="proceed-1"]
${PROCEED_STEP_2}           css:[data-test="proceed-2"]
${PROCEED_STEP_3}           css:[data-test="proceed-3"]
${PAYMENT_METHOD_SELECT}    css:[data-test="payment-method"]
${FINISH_ORDER_BTN}         css:[data-test="finish"]
${ORDER_CONFIRMATION_ALERT}    css:#order-confirmation, [data-test="order-confirmation"], .alert-success

*** Keywords ***
Verify Cart Item And Total
    Wait Until Element Is Visible    ${CART_PRODUCT_TITLE}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${CART_TOTAL_PRICE}      timeout=${TIMEOUT}
    ${title}=    Get Text            ${CART_PRODUCT_TITLE}
    ${total}=    Get Text            ${CART_TOTAL_PRICE}
    Should Not Be Empty              ${title}
    Should Not Be Empty              ${total}

Click Proceed Step 1
    Wait And Click Via JS    ${PROCEED_STEP_1}

Click Proceed Step 2
    Wait Until Page Contains Element    ${PROCEED_STEP_2}    timeout=${TIMEOUT}
    Wait And Click Via JS               ${PROCEED_STEP_2}

Click Proceed Step 3
    Wait Until Page Contains Element    ${PROCEED_STEP_3}    timeout=${TIMEOUT}
    Wait Until Keyword Succeeds         ${TIMEOUT}    500ms    Element Value Should Not Be Empty    id=street
    Wait And Input Text                 id=house_number    42
    Press Keys                          id=house_number    TAB
    Wait And Click Via JS               ${PROCEED_STEP_3}

Select Payment Method And Submit
    [Arguments]    ${payment_method_value}=cash-on-delivery
    Wait Until Element Is Visible    ${PAYMENT_METHOD_SELECT}    timeout=${TIMEOUT}
    Scroll Element Into View         ${PAYMENT_METHOD_SELECT}
    Select From List By Value        ${PAYMENT_METHOD_SELECT}    ${payment_method_value}
    Wait Until Element Is Enabled    ${FINISH_ORDER_BTN}         timeout=${TIMEOUT}
    Wait And Click Via JS            ${FINISH_ORDER_BTN}

Verify Order Confirmation Success
    Wait Until Page Contains         Payment was successful         timeout=${TIMEOUT}
    Wait Until Page Contains Element    ${ORDER_CONFIRMATION_ALERT}    timeout=${TIMEOUT}
    ${confirm_text}=    Get Text        ${ORDER_CONFIRMATION_ALERT}
    Should Not Be Empty                 ${confirm_text}
