*** Settings ***
Documentation    A keywords from open new account page

Keyword Tags    open-new-account-keywords

Library    ../libraries/FileDataReader.py
Library    Collections

Resource    ../keywords/common_keywords.resource
Resource    ../pages/create_new_account_page.resource


*** Keywords ***
Open New Account In The Application
    [Tags]    REPORT:LOG
    [Arguments]    ${data_table}
    Select Account Service    Open New Account

    Select Account Type    ${data_table.account_type}
    Select Account Owner    ${data_table.account_reference}
    Click Open Account

    ${account_id}    Verify Account Opened And Get Account Id
    RETURN    ${account_id}
