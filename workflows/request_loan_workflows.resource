*** Settings ***
Keyword Tags     workflow

Library    ${EXECDIR}/libraries/DataTableLibrary.py

Resource    ../keywords/create_new_account_keywords.resource
Resource    ${EXECDIR}/keywords/request_loan_keywords.resource


*** Keywords ***
Get Request Loan Of A New Account    # robotcode: ignore
    [Arguments]    ${dt}
    ${account_dt}    Open New Account In The Application    ${dt}
    ${loan_dt}    Request Loan    ${account_dt}
    RETURN    ${loan_dt}
