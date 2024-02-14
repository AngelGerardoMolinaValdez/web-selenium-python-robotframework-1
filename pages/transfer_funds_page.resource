*** Settings ***
Documentation     A representation of a transfer fund workflows in the application

Keyword Tags    transfer_fund-page

Library    SeleniumLibrary


*** Keywords ***
Input Amount
    [Tags]    STEP:Se ingreso el monto
    [Arguments]    ${amount}
    Input Text    id:amount    ${amount}

Select From Account
    [Tags]    STEP:Se selecciona la cuenta de origen
    [Arguments]    ${from_account}
    Select From List By Value    id:fromAccountId    ${from_account}

Select To Account
    [Tags]    STEP:Se selecciona la cuenta de destino
    [Arguments]    ${to_account}
    Select From List By Value    id:fromAccountId    ${to_account}

Click Transfer Button
    [Tags]    STEP:Se hace clic en el botón de transferencia
    Click Element    css:input[value="Transfer"]

Verify Transfer Success
    [Tags]    STEP:Se verifica que la transferencia se realizó con éxito
    Page Should Contain    Transfer Complete!
