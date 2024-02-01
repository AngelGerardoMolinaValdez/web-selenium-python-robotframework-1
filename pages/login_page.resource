*** Settings ***
Documentation     A representation of a login page

Keyword Tags    login-page

Library    SeleniumLibrary


*** Variables ***
${BROWSER}    Chrome
${URL}    https://parabank.parasoft.com/parabank/index.htm
${USERNAME}    john
${PASSWORD}    demo


*** Keywords ***
Open Browser To Login Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    0
    Login Page Should Be Open

Login Page Should Be Open
    [Tags]    robot:private
    Title Should Be    ParaBank | Welcome | Online Banking

Input Username
    Input Text    name:username    ${USERNAME}

Input Password
    Input Text    name:password    ${PASSWORD}

Submit Credentials
    Click Element    css:input[value="Log In"]
    Credentials Should Be Accepted

Credentials Should Be Accepted
    [Tags]    robot:private
    Page Should Contain    Account Services

Logout From The Application
    Click Link    Log Out
    Title Should Be    ParaBank | Welcome | Online Banking
    Close Browser
