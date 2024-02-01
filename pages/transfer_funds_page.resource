*** Settings ***
Documentation     A representation of a transfer fund workflows in the application

Keyword Tags    transfer_fund-page

Library    SeleniumLibrary


*** Keywords ***
Input Amount
    [Arguments]    ${amount}
    Input Text    id:amount    ${amount}

Select From Account
    [Arguments]    ${from_account}
    Select From List By Value    id:fromAccountId    ${from_account}

Select To Account
    [Arguments]    ${to_account}
    Select From List By Value    id:fromAccountId    ${to_account}

Click Transfer Button
    Click Element    css:input[value="Transfer"]

Verify Transfer Success
    Page Should Contain    Transfer Complete!
