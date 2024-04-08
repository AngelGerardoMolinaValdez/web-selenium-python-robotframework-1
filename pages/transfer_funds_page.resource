*** Settings ***
Documentation     A representation of a transfer fund workflows in the application

Keyword Tags    transfer_fund-page

Resource    ${EXECDIR}/config/Libraries.resource


*** Keywords ***
Input Amount
    [Tags]    STEP:Se ingreso el monto
    [Arguments]    ${amount}
    Highlight Element Async    id:amount
    Input Text    id:amount    ${amount}

Select From Account
    [Tags]    STEP:Se selecciona la cuenta de origen
    [Arguments]    ${from_account}
    Highlight Element Async    id:fromAccountId
    Select From List By Value    id:fromAccountId    ${from_account}

Select To Account
    [Tags]    STEP:Se selecciona la cuenta de destino
    [Arguments]    ${to_account}
    Highlight Element Async    id:toAccountId
    Select From List By Value    id:toAccountId    ${to_account}

Click Transfer Button
    Highlight Element Async    css:input[value="Transfer"]
    Log    STEP:IMAGE:Datos de la transferencia y se hace click en el botón de transferir.
    Click Element    css:input[value="Transfer"]
    Sleep    2s

Verify Transfer Success
    Page Should Contain    Transfer Complete!
    Log    STEP:IMAGE:Transferencia completada con éxito.:PASS
