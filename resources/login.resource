*** Settings ***
Documentation
...    Keywords utilizadas para el login de la aplicacion del proyecto

Keyword Tags
...    login

Variables    ../data/variables/login.yml
Resource    ../loader/import_components.resource

*** Keywords ***
Iniciar Sesion En ParaBank    
    Open Browser    ${url_parabank}    gc

    Wait Until Element Is Visible    ${input_username}
    Wait Until Element Is Enabled    ${input_username}

    Maximize Browser Window
    
    Input Text    ${input_username}    ${user_parabank}
    Input Password    ${input_password}    ${password_parabank}

    Click Element    ${boton_login}

    Wait Until Element Is Visible    ${panel_inicio}
    Wait Until Element Is Enabled    ${panel_inicio}
