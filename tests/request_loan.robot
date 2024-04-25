*** Settings ***
Test Tags    regression    data_driven

Library    DataDriver    file=${EXECDIR}/data/tests/request_loan.csv    encoding=utf_8
Library    ../libraries/standard/DataTableLibrary.py
Library    ../libraries/standard/TestsExecutionResults.py

Resource    ../keywords/login_keywords.resource
Resource    ${EXECDIR}/keywords/request_loan_keywords.resource
Resource    ${EXECDIR}/workflows/request_loan_workflows.resource

Suite Setup    Login In To The Application

Suite Teardown    Logout From The Application

Test Template    Request Loan Workflows


*** Test Cases ***
Request Loan Service Workflows    keyword_name    index


*** Keywords ***
Request Loan Workflows
    [Documentation]    Execute specific workflow to request loan with the given data.
    [Arguments]    ${keyword_name}    ${data_row_index}
    ${data_table}    Create Data Table    ${EXECDIR}/data/tables/request_loan.csv    ${data_row_index}
    ${dt_updated}    Run Keyword    ${keyword_name}    ${data_table}
    Save Test Execution Results    ${dt_updated}
