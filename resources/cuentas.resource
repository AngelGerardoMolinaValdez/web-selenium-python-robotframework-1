*** Settings ***
Documentation
...    Keywords enfocadas en los flujos acerca de cuentas de banco

Keyword Tags
...    cuenta

Variables    ../data/variables/cuentas.yml
Resource    ../loader/import_components.resource

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


Obtener Resumen De Cuentas En Parabank
    [Arguments]    ${CONDICION}=${None}

    Click Link    ${link_resumen_de_cuenta}
    
    Wait Until Element Is Visible    ${tabla_resumen_de_cuentas}
    Wait Until Element Is Enabled    ${tabla_resumen_de_cuentas}

    ${total_filas_disponibles}=    Get Element Count    ${filas_resumen_de_cuentas}

    FOR  ${indice_fila_cuenta}  IN RANGE  ${1}    ${total_filas_disponibles}
        ${fila_informacion_cuenta}    Set Variable    (//table[@id="accountTable"]//tbody//tr)[${indice_fila_cuenta}]
        ${numero_cuenta}    Get Text    ${fila_informacion_cuenta}//a
        ${balance_cuenta}    Get Text    (${fila_informacion_cuenta}//td)[2]
        ${monto_disponible_cuenta}    Get Text    (${fila_informacion_cuenta}//td)[3]
        Log To Console    ${numero_cuenta} ::: ${balance_cuenta} ::: ${monto_disponible_cuenta}
    END
    