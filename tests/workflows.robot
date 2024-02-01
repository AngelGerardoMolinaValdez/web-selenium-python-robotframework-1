*** Settings ***
Documentation     A test suite with a workflows for the application.

Metadata    Author    Angel Gerardo Molina Valdez
Metadata    Application    ParaBank
Metadata    Version    1.0
Metadata    Test Level    Regression

Test Tags    Regression

Resource    ../keywords/login_keywords.resource

Suite Setup    Login In To The Application

Suite Teardown    Logout From The Application


*** Test Cases ***
Open New Account And Transfer Funds
    [Documentation]    Open a new account for the user
    [Tags]    OpenAccount
    No Operation

Open New Account And Transfer Funds And Verify The Account Overview
    [Documentation]    Open a new account for the user and verify the account overview
    [Tags]    OpenAccount    AccountOverview    transferFunds
    No Operation

Transfer Funds And Verify The Account Overview
    [Documentation]    Transfer funds and verify the account overview
    [Tags]    AccountOverview    transferFunds
    No Operation
