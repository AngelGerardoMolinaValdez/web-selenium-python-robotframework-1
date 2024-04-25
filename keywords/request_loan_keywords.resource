*** Settings ***
Keyword Tags    keywords

Library    ${EXECDIR}/libraries/standard/DataTableLibrary.py

Resource    ${EXECDIR}/pages/request_loan_page.resource
Resource    ../keywords/common_keywords.resource


*** Keywords ***
Request Loan
    [Arguments]    ${dt}
    Select Account Service    Request Loan

    Wait Until Input Loan Amount Is Visible

    Input Loan Amount    ${dt.loan_amount}
    Input Down Payment    ${dt.down_amount}
    Select From Account    ${dt.account_id}
    Click Into Apply Now

    Wait Until Loan Application Is Submitted
    ${new_account}    New Account With Loan Is Created

    ${new_account_dt}    Update Data Table    ${dt}    request_loan_account=${new_account}
    RETURN    ${new_account_dt}
