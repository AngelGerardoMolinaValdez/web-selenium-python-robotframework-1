*** Settings ***
Documentation     A test suite with a test cases that uses data driven testing.

Metadata    type    data driven
Metadata    Author    Angel Gerardo Molina Valdez
Metadata    Application    ParaBank
Metadata    Version    1.0
Metadata    Test Level    regression

Test Tags    regression    data_driven

Library    DataDriver    file=${EXECDIR}/data/tests/bill_payment.csv    encoding=utf_8
Library    ../libraries/standard/DataTableLibrary.py
Library    ../libraries/standard/TestsExecutionResults.py

Resource    ../keywords/login_keywords.resource
Resource    ${EXECDIR}/keywords/bill_payment_keywords.resource
Resource    ${EXECDIR}/workflows/bill_payment_workflows.resource

Suite Setup    Login In To The Application

Suite Teardown    Logout From The Application

Test Template    Bill Payment Workflows


*** Test Cases ***
Overview Service Workflows    keyword_name    index


*** Keywords ***
Bill Payment Workflows
    [Documentation]    Execute specific workflow to Overview funds with the given data.
    [Arguments]    ${keyword_name}    ${data_row_index}
    ${data_table}    Create Data Table    ${EXECDIR}/data/tables/bill_payment.csv    ${data_row_index}
    ${dt_updated}    Run Keyword    ${keyword_name}    ${data_table}
    Save Test Execution Results    ${dt_updated}
