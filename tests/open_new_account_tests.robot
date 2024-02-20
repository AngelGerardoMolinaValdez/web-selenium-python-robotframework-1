*** Settings ***
Documentation     A test suite with a test cases that uses data driven testing.

Metadata    type    data driven
Metadata    Author    Angel Gerardo Molina Valdez
Metadata    Application    ParaBank
Metadata    Version    1.0
Metadata    Test Level    regression

Test Tags    regression    data_driven

Library    DataDriver    file=${EXECDIR}/data/data.csv    encoding=utf_8

Resource    ../keywords/login_keywords.resource
Resource    ../keywords/create_new_account_keywords.resource
Resource    ../workflows/open_account_and_transfer_fund_workflow.resource
Resource    ../workflows/open_account_and_get_overview_workflow.resource


Suite Setup    Login In To The Application

Suite Teardown    Logout From The Application

Test Template    Account Workflows


*** Test Cases ***
Account Service Workflows    ${type_account}    ${account_reference}    # robotcode: ignore


*** Keywords ***
Account Workflows
    [Documentation]    Execute specific workflow to open a new account with the given data.
    [Arguments]    ${keyword_name}    ${type_account}    ${account_reference}
    Run Keyword    ${keyword_name}    ${type_account}    ${account_reference}
