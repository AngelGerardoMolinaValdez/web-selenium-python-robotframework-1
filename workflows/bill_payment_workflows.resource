*** Settings ***
Keyword Tags     workflow

Library    ${EXECDIR}/libraries/DataTableLibrary.py

Resource    ${EXECDIR}/keywords/create_new_account_keywords.resource
Resource    ${EXECDIR}/keywords/bill_payment_keywords.resource


*** Keywords ***
Create New Account And Make Bill Payment    # robotcode: ignore
    [Arguments]    ${dt}
    ${new_account_dt}    Open New Account In The Application    ${dt}
    ${bill_payment_dt}    Bill Payment    ${new_account_dt}
    RETURN    ${bill_payment_dt}
