*** Settings ***
Documentation    A keywords from transfer funds page object

Keyword Tags    transfer-funds-keywords

Resource    ../pages/transfer_funds_page.resource


*** Keywords ***
Transfer Funds In The Application
    [Arguments]    ${from_account}    ${to_account}    ${amount}
    Input Amount    ${amount}
    Select From Account   ${from_account}
    Select To Account    ${to_account}
    Click Transfer Button
    Verify Transfer Success
