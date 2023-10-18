*** Settings ***
Documentation    inicio de sesion

Test Tags    login

Library    SeleniumLibrary    timeout=1 minutes    run_on_failure=No Operation

Suite Setup    Set Selenium Speed    0.1


*** Test Cases ***
Iniciar sesion
    [Tags]    creacion-transferencias
    Open Browser    ${URL}    ${BROWSER}
    Wait Until Element Is Visible    link:Register

    Maximize Browser Window

    Input Text    name:username    ${USERNAME}
    Input Password    name:password    ${PASSWORD}
    Click Element    css:input[value="Log In"]

    Wait Until Page Contains    Welcome

    Element Should Be Visible    link:Log Out