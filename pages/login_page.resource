*** Settings ***
Documentation     A representation of a login page

Keyword Tags    login-page

Resource    ${EXECDIR}/config/global/dependencies/pages.resource


*** Variables ***
${BROWSER}    Chrome
${URL}    https://parabank.parasoft.com/parabank/index.htm
${USERNAME}    john
${PASSWORD}    demo


*** Keywords ***
Open Browser To Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0.1
    Login Page Should Be Open

Login Page Should Be Open
    [Tags]    robot:private    STEP:La página de login se ha abierto
    Title Should Be    ParaBank | Welcome | Online Banking
    Add Step Capture    Pagina abierta correctamente    PASS    is_keyword_setup=True

Input Username
    [Tags]    STEP:He introducido el usuario
    Highlight Element Persistent    name:username
    Input Text    name:username    ${USERNAME}

Input Password
    [Tags]    STEP:He introducido la contraseña
    Highlight Element Persistent    name:password
    Input Text    name:password    ${PASSWORD}

Submit Credentials
    Highlight Element Persistent    css:input[value\="Log In"]
    Add Step Capture    Envio de credenciales    INFO    is_keyword_setup=True
    Click Element    css:input[value="Log In"]
    Credentials Should Be Accepted

Credentials Should Be Accepted
    Page Should Contain    Account Services
    Add Step Capture    Credenciales correctas    PASS    is_keyword_setup=True

Logout Application
    [Tags]    STEP:He cerrado la sesión
    Click Link    Log Out
    Title Should Be    ParaBank | Welcome | Online Banking
    Close Browser
