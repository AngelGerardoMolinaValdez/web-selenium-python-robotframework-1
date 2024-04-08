*** Settings ***
Documentation     A reusable keywords that can be used to login to the application

Keyword Tags      common

Resource    ${EXECDIR}/config/Libraries.resource


*** Keywords ***
Select Account Service
    [Arguments]    ${service_name}
    Highlight Element Async    link:${service_name}
    Log    STEP:IMAGE:Seleccione el servicio "${service_name}":PASS
    Click Link    ${service_name}
    Wait Until Page Contains Element   css:h1.title    10s
