*** Settings ***
Documentation     A test suite with a workflows for the application.

Metadata    Author    Angel Gerardo Molina Valdez
Metadata    Application    ParaBank
Metadata    Version    1.0
Metadata    Test Level    Regression

Test Tags    Regression

Resource    ../keywords/login_keywords.resource
Resource    ../workflows/open_account_and_transfer_fund_workflow.resource
Resource    ../workflows/open_account_and_get_overview_workflow.resource

Suite Setup    Login In To The Application

Suite Teardown    Logout From The Application


*** Test Cases ***
Open New Account And Transfer Funds
    [Documentation]    Open a new account for the user
    [Tags]    OpenAccount
    Create New Account And Transfer Money

Open New Account And Verify The Account Overview
    [Documentation]    Open a new account for the user and verify the account overview
    [Tags]    OpenAccount    AccountOverview    transferFunds
    Create New Account And Get Account Overview
