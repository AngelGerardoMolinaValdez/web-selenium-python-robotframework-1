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
    Log    STEP:IMAGE:Datos de la transferencia y se hace click en el botón de transferir.
    Click Element    css:input[value="Transfer"]

Verify Transfer Success
    Page Should Contain    Transfer Complete!
    Log    STEP:IMAGE:Transferencia completada con éxito.:PASS
