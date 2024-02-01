*** Settings ***
Documentation    A test suite with a tests for e2e testing of the app functionality.

Metadata    Author    Angel Gerardo Molina Valdez
Metadata    Application    ParaBank
Metadata    Version    1.0
Metadata    Test Level    Regression

Test Tags    Regression

Library    ../libraries/FileDataReader.py

Resource    ../keywords/login_keywords.resource
Resource    ../keywords/common_keywords.resource
Resource    ../keywords/transfer_funds_keywords.resource
Resource    ../keywords/account_overview_keywords.resource
Resource    ../keywords/create_new_account_keywords.resource

Suite Setup    Login In To The Application

Suite Teardown    Logout Application


*** Test Cases ***
Open New Account
    [Tags]    Smoke
    @{test_data}    Read Csv    ${CURDIR}/../data/account.csv
    FOR  ${data}  IN  @{test_data}
        Select Account Service    Open New Account
        Open New Account In The Application    ${data["type"]}    ${data["account_reference"]}
    END

Account Overview
    [Tags]    Smoke
    Select Account Service    Accounts Overview
    Get Account Overview    12345

Transfer Funds
    [Tags]    Smoke
    Select Account Service    Transfer Funds
    Transfer Funds In The Application    1000    12345    12345