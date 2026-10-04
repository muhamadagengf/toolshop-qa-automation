*** Settings ***
Documentation       Page Object for Product Detail and Add to Cart
Resource            BasePage.robot

*** Variables ***
${PRODUCT_NAME_HEADING}     css:[data-test="product-name"]
${PRODUCT_UNIT_PRICE}       css:[data-test="unit-price"]
${PRODUCT_QUANTITY_INPUT}   css:[data-test="quantity"]
${ADD_TO_CART_BTN}          css:[data-test="add-to-cart"]
${NAV_CART_BADGE}           css:[data-test="cart-quantity"]
${CART_LINK}                css:[data-test="nav-cart"]

*** Keywords ***
Verify Product Detail Loaded
    Wait Until Element Is Visible    ${PRODUCT_NAME_HEADING}    timeout=${TIMEOUT}
    Wait Until Element Is Visible    ${ADD_TO_CART_BTN}         timeout=${TIMEOUT}

Get Current Product Name
    ${name}=    Get Text    ${PRODUCT_NAME_HEADING}
    RETURN      ${name}

Get Current Unit Price
    ${price}=    Get Text    ${PRODUCT_UNIT_PRICE}
    RETURN       ${price}

Click Add To Cart
    Wait And Click Via JS    ${ADD_TO_CART_BTN}
    # Wait until cart badge or notification appears
    Wait Until Page Contains Element    ${NAV_CART_BADGE}    timeout=${TIMEOUT}

Proceed To Cart Via Navigation
    Go To    ${BASE_URL}/checkout
    Wait Until Location Contains    /checkout    timeout=${TIMEOUT}
