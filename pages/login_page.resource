*** Settings ***
Documentation     A representation of a login page

Keyword Tags    login-page

Resource    ${EXECDIR}/config/Libraries.resource


*** Variables ***
${BROWSER}    Chrome
${URL}    https://parabank.parasoft.com/parabank/index.htm
${USERNAME}    john
${PASSWORD}    demo


*** Keywords ***
Open Browser To Login Page
    [Tags]    STEP: He abierto el navegador
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.1
    Login Page Should Be Open

Login Page Should Be Open
    [Tags]    robot:private    STEP:La página de login se ha abierto
    Title Should Be    ParaBank | Welcome | Online Banking

Input Username
    [Tags]    STEP:He introducido el usuario
    Highlight Element Async    name:username
    Input Text    name:username    ${USERNAME}

Input Password
    [Tags]    STEP:He introducido la contraseña
    Highlight Element Async    name:password
    Input Text    name:password    ${PASSWORD}

Submit Credentials
    Highlight Element Async    css:input[value="Log In"]
    Log    STEP:IMAGE:He enviado las credenciales
    Click Element    css:input[value="Log In"]
    Credentials Should Be Accepted

Credentials Should Be Accepted
    Page Should Contain    Account Services
    Log    STEP:Las credenciales han sido aceptadas:PASS

Logout Application
    [Tags]    STEP:He cerrado la sesión
    Click Link    Log Out
    Title Should Be    ParaBank | Welcome | Online Banking
    Close Browser
