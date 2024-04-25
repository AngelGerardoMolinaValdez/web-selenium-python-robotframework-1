*** Settings ***
Documentation     A representation of a transfer fund workflows in the application

Keyword Tags    transfer_fund-page

Resource    ${EXECDIR}/config/global/dependencies/pages.resource


*** Keywords ***
Input Amount
    [Tags]    STEP:Se ingreso el monto
    [Arguments]    ${amount}
    Highlight Element Persistent    id:amount
    Input Text    id:amount    ${amount}

Select From Account
    [Tags]    STEP:Se selecciona la cuenta de origen
    [Arguments]    ${from_account}
    Highlight Element Persistent    id:fromAccountId
    Select From List By Value    id:fromAccountId    ${from_account}

Select To Account
    [Tags]    STEP:Se selecciona la cuenta de destino
    [Arguments]    ${to_account}
    Highlight Element Persistent    id:toAccountId
    Select From List By Value    id:toAccountId    ${to_account}

Click Transfer Button
    Highlight Element Persistent    css:input[value\="Transfer"]
    Add Step Capture   Datos de la transferencia y se hace click en el botón de transferir.    INFO
    Click Element    css:input[value="Transfer"]
    Sleep    2s

Verify Transfer Success
    Page Should Contain    Transfer Complete!
    Capture Page Screenshot
    Add Step Capture   Transferencia completada con éxito.    PASS

Verify Transfer Failure
    Page Should Contain    Please enter a valid amount.
    Capture Page Screenshot
    Add Step Capture   Transferencia fallida por cantidad alfanumerica    PASS
