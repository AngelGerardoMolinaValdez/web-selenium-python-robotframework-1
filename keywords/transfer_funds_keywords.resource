*** Settings ***
Documentation    A keywords from transfer funds page object

Keyword Tags    transfer-funds-keywords

Resource    ../keywords/common_keywords.resource
Resource    ../pages/transfer_funds_page.resource


*** Keywords ***
Transfer Funds In The Application
    [Tags]    REPORT:LOG
    [Arguments]    ${from_account}    ${to_account}    ${amount}
    Select Account Service    Transfer Funds

    Input Amount    ${amount}
    Select From Account   ${from_account}
    Select To Account    ${to_account}
    Click Transfer Button
    Verify Transfer Success
