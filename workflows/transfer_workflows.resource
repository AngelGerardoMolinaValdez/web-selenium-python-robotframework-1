*** Settings ***
Documentation     Workflow for the user to create a new account and transfer money

Keyword Tags     workflow

Library    ${EXECDIR}/libraries/DataTableLibrary.py

Resource    ../keywords/create_new_account_keywords.resource
Resource    ../keywords/transfer_keywords.resource


*** Keywords ***
Create New Account And Transfer Funds From Existing Account    # robotcode: ignore
    [Arguments]    ${dt}
    ${new_account_dt}    Open New Account In The Application    ${dt}
    VAR    ${new_accound_id}    ${new_account_dt.account_id}
    ${transfer_dt}    Update Data Table    ${new_account_dt}    to_account=${new_accound_id}
    Transfer Funds    ${transfer_dt}
    RETURN    ${transfer_dt}

Create New Account And Transfer Funds To Existing Account    # robotcode: ignore
    [Arguments]    ${dt}
    ${new_account_dt}    Open New Account In The Application    ${dt}
    VAR    ${new_accound_id}    ${new_account_dt.account_id}
    ${transfer_dt}    Update Data Table    ${dt}    from_account=${new_accound_id}
    Transfer Funds    ${transfer_dt}
    RETURN    ${transfer_dt}
