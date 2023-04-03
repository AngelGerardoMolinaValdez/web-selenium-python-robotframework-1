*** Settings ***
Documentation
...    Keywords enfocadas en los flujos acerca de cuentas de banco

Keyword Tags
...    consulta

Resource    ../../loader/libraries.resource
Resource    ../../loader/util.resource

Variables    ../../data/variables/cuentas.yml


*** Keywords ***
Obtener Resumen De Cuentas En Parabank
    [Arguments]    ${CONDICION}=${None}

    Click Link    ${link_resumen_de_cuenta}

    Wait Until Element Is Visible    ${tabla_resumen_de_cuentas}
    Wait Until Element Is Enabled    ${tabla_resumen_de_cuentas}

    ${total_filas_disponibles}=    Get Element Count    ${filas_resumen_de_cuentas}

    FOR  ${indice_fila_cuenta}  IN RANGE    ${1}    ${total_filas_disponibles}
        ${fila_informacion_cuenta}    Set Variable    (//table[@id="accountTable"]//tbody//tr)[${indice_fila_cuenta}]
        ${numero_cuenta}    Get Text    ${fila_informacion_cuenta}//a
        ${balance_cuenta}    Get Text    (${fila_informacion_cuenta}//td)[2]
        ${monto_disponible_cuenta}    Get Text    (${fila_informacion_cuenta}//td)[3]
        Log To Console    ${numero_cuenta} ::: ${balance_cuenta} ::: ${monto_disponible_cuenta}
    END
