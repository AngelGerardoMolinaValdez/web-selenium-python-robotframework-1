*** Settings ***
Documentation    A test suite with a single test for e2e testing of the app functionality.

Metadata    Author    Angel Gerardo Molina Valdez
Metadata    Application    ParaBank
Metadata    Version    1.0
Metadata    Test Level    Regression

Test Tags    Regression

Resource    ../keywords/login_keywords.resource

Suite Setup    Login In To The Application

Suite Teardown    Login In To The Application


*** Test Cases ***
Open New Account
    [Tags]    Smoke
    No Operation

Account Summary
    [Tags]    Smoke
    No Operation

Transfer Funds
    [Tags]    Smoke
    No Operation
