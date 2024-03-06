*** Settings ***
Documentation     A reusable keywords that can be used to login to the application

Keyword Tags      common

Library           SeleniumLibrary


*** Keywords ***
Select Account Service
    [Arguments]    ${service_name}
    Click Link    ${service_name}
    Wait Until Page Contains Element   css:h1.title    10s
    Log    STEP:IMAGE:Seleccione el servicio "${service_name}":PASS
