*** Settings ***
Documentation    A test suite with a tests for e2e testing of the app functionality.

Metadata    Author    Angel Gerardo Molina Valdez
Metadata    Application    ParaBank
Metadata    Version    1.0
Metadata    Test Level    Regression

Test Tags    Regression

Library    ../libraries/DataTableLibrary.py

Resource    ../keywords/login_keywords.resource
Resource    ../keywords/common_keywords.resource
Resource    ../keywords/transfer_funds_keywords.resource
Resource    ../keywords/account_overview_keywords.resource
Resource    ../keywords/create_new_account_keywords.resource

Suite Setup    Login In To The Application

Suite Teardown    Logout From The Application


*** Test Cases ***
Account Overview
    [Tags]    Smoke
    ${dt}    Create Data Table    ${EXECDIR}/data/data.csv    0
    Get Account Overview    ${dt}

Transfer Funds
    [Tags]    Smoke
    ${dt}    Create Data Table    ${EXECDIR}/data/data.csv    0
    Transfer Funds In The Application    ${dt}
