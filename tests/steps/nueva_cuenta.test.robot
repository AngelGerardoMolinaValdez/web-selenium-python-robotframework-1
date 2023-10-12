*** Settings ***
Documentation    creacion de cuentas

Test Tags    creacion

Library    SeleniumLibrary    timeout=1 minutes    run_on_failure=No Operation

Suite Setup    Set Selenium Speed    0.1


*** Variables ***
${tipo_de_cuenta}    CHECKING
${cuenta_de_referencia}    13344


*** Test Cases ***
Crear una cuenta
    [Tags]    creacion-transferencias
    Click Link    link:Open New Account

    Wait Until Element Is Visible    css:h1[class="title"]

    Select From List By Label    id:type    ${tipo_de_cuenta}
    Select From List By Label    id:fromAccountId    ${cuenta_de_referencia}
    Click Element    css:input[value="Open New Account"]

    Wait Until Element Is Visible    css:h1[class="title"]

    Page Should Contain    Congratulations, your account is now open.
    Element Should Be Visible    id:newAccountId

    ${cuenta_creada}    Get Text    id:newAccountId
    ${NUMERO_DE_CUENTA}    Set Global Variable    ${cuenta_creada}
