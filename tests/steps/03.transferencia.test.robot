*** Settings ***
Documentation    Se encarga de transferir cierta cantidad a la cuenta que se le indique

Test Tags    transferencia

Library    SeleniumLibrary    timeout=1 minutes    run_on_failure=No Operation
Library    ../../libraries/DataTableLibrary.py

Suite Setup    Set Selenium Speed    0.1


*** Test Cases ***
Transferir fondos
    [Tags]    creacion-transferencias
    Click Link    link:Transfer Funds

    Wait Until Page Contains Element    css:h1.title

    Input Text    id:amount    ${DATATABLE.monto_transferencia}
    Select From List By Label    id:fromAccountId    ${DATATABLE.cuenta_de_referencia}
    Select From List By Label    id:toAccountId    ${NUMERO_DE_CUENTA}

    Click Element    css:input[type="submit"]

    Wait Until Page Contains    Transfer Complete!

    ${mensaje_transferencia}    Get Text    xpath:(//h1[@class="title"]//..//p)[1]
    ${pattern}    Catenate    SEPARATOR=
    ...    \\$${DATATABLE.monto_transferencia}.*
    ...    has been transferred.*
    ...    from.*${DATATABLE.cuenta_de_referencia}.*
    ...    to.*${NUMERO_DE_CUENTA}.*

    Should Match Regexp
    ...    ${mensaje_transferencia}
    ...    ${pattern}