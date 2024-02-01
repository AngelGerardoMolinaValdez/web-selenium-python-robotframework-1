*** Settings ***
Documentation    A keywords from open new account page

Keyword Tags    open-new-account-keywords

Library    ../libraries/FileDataReader.py
Library    Collections

Resource    ../keywords/common_keywords.resource
Resource    ../pages/create_new_account_page.resource


*** Keywords ***
Open New Account In The Application
    VAR    @{accounts}
    @{test_data}    Read Csv    ${CURDIR}/../data/account.csv

    FOR  ${data}  IN  @{test_data}
        Select Account Service    Open New Account

        Select Account Type    ${data["type"]}
        Select Account Owner    ${data["account_reference"]}
        Click Open Account

        ${account_id}    Verify Account Opened And Get Account Id
        Append To List    ${accounts}    ${account_id}
    END

    RETURN    ${accounts}
