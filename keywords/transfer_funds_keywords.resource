*** Settings ***
Documentation    A keywords from transfer funds page object

Keyword Tags    transfer-funds-keywords

Resource    ../keywords/common_keywords.resource
Resource    ../pages/transfer_funds_page.resource


*** Keywords ***
Transfer Funds In The Application
    [Arguments]    ${data_table}
    Select Account Service    Transfer Funds

    Input Amount    ${data_table.amount}
    Select From Account   ${data_table.from_account}
    Select To Account    ${data_table.to_account}
    Click Transfer Button
    Verify Transfer Success
