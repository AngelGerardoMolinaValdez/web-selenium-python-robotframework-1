*** Settings ***
Documentation    A keywords from open new account page

Keyword Tags    open-new-account-keywords

Resource    ../pages/create_new_account_page.resource


*** Keywords ***
Open New Account In The Application
    [Arguments]    ${account_type}    ${account_owner}
    Select Account Type    ${account_type}
    Select Account Owner    ${account_owner}
    Click Open Account
    ${account_id}    Verify Account Opened And Get Account Id
    RETURN    ${account_id}
