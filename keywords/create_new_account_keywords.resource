*** Settings ***
Documentation    A keywords from open new account page

Keyword Tags    open-new-account-keywords

Library    ../libraries/DataTableLibrary.py

Resource    ../keywords/common_keywords.resource
Resource    ../pages/create_new_account_page.resource


*** Keywords ***
Open New Account In The Application
    [Arguments]    ${data_table}
    Select Account Service    Open New Account

    Select Account Type    ${data_table.type_account}
    Select Account Owner    ${data_table.account_reference}
    Click Open Account

    ${account_id}    Verify Account Opened And Get Account Id
    ${dt}    Update Data Table    ${data_table}    account_id=${account_id}
    RETURN    ${dt}
