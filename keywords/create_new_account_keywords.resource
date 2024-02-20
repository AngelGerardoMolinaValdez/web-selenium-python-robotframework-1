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
    [Arguments]    ${account_type}    ${account_owner}
    Select Account Service    Open New Account

    Select Account Type    ${account_type}
    Select Account Owner    ${account_owner}
    Click Open Account

    ${account_id}    Verify Account Opened And Get Account Id
    RETURN    ${account_id}
