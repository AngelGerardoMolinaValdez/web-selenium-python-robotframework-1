*** Settings ***
Documentation     A test suite with a test cases that uses data driven testing.

Metadata    type    data driven
Metadata    Author    Angel Gerardo Molina Valdez
Metadata    Application    ParaBank
Metadata    Version    1.0
Metadata    Test Level    regression

Test Tags    regression    data_driven

Library    DataDriver    file=${EXECDIR}/data/tests/find_transaction.csv    encoding=utf_8
Library    ../libraries/standard/DataTableLibrary.py
Library    ../libraries/standard/TestsExecutionResults.py

Resource    ../keywords/login_keywords.resource
Resource    ${EXECDIR}/workflows/find_transaction_workflows.resource
Resource    ${EXECDIR}/keywords/find_transaction_keywords.resource

Suite Setup    Login In To The Application

Suite Teardown    Logout From The Application

Test Template    Find Transaction Workflows


*** Test Cases ***
Find Transaction Workflows    keyword_name    index


*** Keywords ***
Find Transaction Workflows
    [Documentation]    Execute specific workflow to find transaction with the given data.
    [Arguments]    ${keyword_name}    ${data_row_index}
    ${data_table}    Create Data Table    ${EXECDIR}/data/tables/find_transaction.csv    ${data_row_index}
    ${dt_updated}    Run Keyword    ${keyword_name}    ${data_table}
    Save Test Execution Results    ${dt_updated}
