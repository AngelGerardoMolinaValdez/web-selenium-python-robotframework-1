*** Settings ***
Documentation     A representation of a account overview in the application

Keyword Tags    account-overview-page

Library    SeleniumLibrary


*** Keywords ***
Click In Account In The Account Table
    [Tags]    STEP:Seleccione la cuenta en la tabla de cuentas
    [Arguments]    ${account}
    Click Link    ${account}

Verify Account Overview Page Is Open
    [Tags]    STEP:Verificar que la página de resumen de cuenta esté abierta
    Wait Until Page Contains Element    css:h1.title
    Page Should Contain Element    css:td#accountId
