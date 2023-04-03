*** Settings ***
Documentation
...    Keywords utilizadas para el login de la aplicacion del proyecto

Keyword Tags
...    login

Resource    ../../loader/libraries.resource

Variables    ../../data/variables/login.yml


*** Keywords ***
Iniciar Sesion
    [Arguments]    ${url}    ${username}    ${password}
    Open Browser    ${url}    gc

    Wait Until Element Is Visible    ${input_username}
    Wait Until Element Is Enabled    ${input_username}

    Maximize Browser Window
    Input Text    ${input_username}    ${username}
    Input Password    ${input_password}    ${password}

    Click Element    ${boton_login}

    Wait Until Element Is Visible    ${panel_inicio}
    Wait Until Element Is Enabled    ${panel_inicio}

Terminar Sesion
    [Documentation]
    ...    Si el caso de prueba falla entonces se mantendra
    ...    abierto el navegador para poder validar el error
    ...    caso contrario se cerrara el navegador y continuara.

    IF  "${TEST STATUS}" != "PASS"    RETURN
    Close All Browsers
