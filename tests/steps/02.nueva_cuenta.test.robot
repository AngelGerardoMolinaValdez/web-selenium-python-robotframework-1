*** Settings ***
Documentation    creacion de cuentas

Test Tags    creacion

Library    SeleniumLibrary    timeout=1 minutes    run_on_failure=No Operation
Library    ../../libraries/DataTableLibrary.py

Suite Setup    Set Selenium Speed    0.1


*** Test Cases ***
Crear una cuenta
    [Tags]    creacion-transferencias
    Click Link    link:Open New Account

    Wait Until Element Is Visible    css:h1[class="title"]

    Select From List By Label    id:type    ${DATATABLE.tipo_de_cuenta}
    Select From List By Label    id:fromAccountId    ${DATATABLE.cuenta_de_referencia}
    Click Element    css:input[value="Open New Account"]

    Sleep    2 seconds
    Wait Until Element Is Visible    css:h1[class="title"]

    Page Should Contain    Congratulations, your account is now open.
    Element Should Be Visible    id:newAccountId

    ${cuenta_creada}    Get Text    id:newAccountId
    ${NUMERO_DE_CUENTA}    Set Variable    ${cuenta_creada}
    Guardar En DataTable
    ...    ${DATATABLE}    ${ITERATION}
    ...    cuenta_generada    ${NUMERO_DE_CUENTA}
    Set Global Variable    ${NUMERO_DE_CUENTA}
