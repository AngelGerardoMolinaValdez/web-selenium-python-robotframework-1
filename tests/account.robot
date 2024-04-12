*** Settings ***
Documentation     A test suite with a test cases that uses data driven testing.

Metadata    type    data driven
Metadata    Author    Angel Gerardo Molina Valdez
Metadata    Application    ParaBank
Metadata    Version    1.0
Metadata    Test Level    regression

Test Tags    regression    data_driven

Library    DataDriver    file=${EXECDIR}/data/tests/${SUITE_NAME}.csv    encoding=utf_8
Library    ../libraries/DataTableLibrary.py
Library    ../libraries/TestsExecutionResults.py

Resource    ../keywords/login_keywords.resource
Resource    ../keywords/create_new_account_keywords.resource

Suite Setup    Login In To The Application

Suite Teardown    Logout From The Application

Test Template    Account Workflows


*** Test Cases ***
Account Service Workflows    keyword_name    index


*** Keywords ***
Account Workflows
    [Documentation]    Execute specific workflow to open a new account with the given data.
    [Arguments]    ${keyword_name}    ${data_row_index}
    ${data_table}    Create Data Table    ${EXECDIR}/data/tables/${SUITE_NAME}.csv    ${data_row_index}
    ${dt_updated}    Run Keyword    ${keyword_name}    ${data_table}
    Save Test Execution Results    ${dt_updated}
