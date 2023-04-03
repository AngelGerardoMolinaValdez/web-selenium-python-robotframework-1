*** Settings ***
Documentation
...    Creacion de cuentas.

Keyword Tags
...    create

Resource    ../../loader/libraries.resource
Resource    ../../loader/util.resource

Variables    ../../data/variables/cuentas.yml


*** Keywords ***
Crear Nueva Cuenta En ParaBank
    [Arguments]    ${TIPO_DE_CUENTA}    ${CUENTA_EXISTENTE}

    Click Link    ${link_nueva_cuenta}
    
    Wait Until Element Is Visible    ${select_tipo_cuenta}
    Wait Until Element Is Enabled    ${select_tipo_cuenta}    

    Select From List By Label    ${select_tipo_cuenta}    ${TIPO_DE_CUENTA}
    Sleep    ${2} seconds
    Select From List By Label    ${select_cuenta_existente}    ${CUENTA_EXISTENTE}

    Click Element    ${boton_abrir_nueva_cuenta}

    Wait Until Page Contains    Congratulations, your account is now open.

    ${NUMERO_NUEVA_CUENTA}=    Get Text    ${link_numero_nueva_cuenta}

    Log To Console    La cuenta obtenida es: ${NUMERO_NUEVA_CUENTA}