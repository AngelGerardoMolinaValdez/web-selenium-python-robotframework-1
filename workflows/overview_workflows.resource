*** Settings ***
Documentation     Workflow for the user to get overview of the account

Keyword Tags     workflow

Library    ${EXECDIR}/libraries/DataTableLibrary.py

Resource    ${EXECDIR}/keywords/create_new_account_keywords.resource
Resource    ${EXECDIR}/keywords/transfer_keywords.resource
Resource    ${EXECDIR}/keywords/overview_keywords.resource
Resource    ./transfer_workflows.resource


*** Keywords ***
Create New Account And Get Overview    # robotcode: ignore
    [Arguments]    ${dt}
    ${new_account_dt}    Open New Account In The Application    ${dt}
    ${overview_dt}    Account Overview    ${new_account_dt}
    RETURN    ${overview_dt}

Create New Account Then Transfer Funds From Existing Account And Get Overview    # robotcode: ignore
    [Arguments]    ${dt}
    ${new_account_transfer_dt}    Create New Account And Transfer Funds From Existing Account    ${dt}
    ${overview_dt}    Account Overview    ${new_account_transfer_dt}
    RETURN    ${overview_dt}

Create New Account Then Transfer Funds To Existing Account And Get Overview    # robotcode: ignore
    [Arguments]    ${dt}
    ${new_account_transfer_dt}    Create New Account And Transfer Funds To Existing Account    ${dt}
    ${overview_dt}    Account Overview    ${new_account_transfer_dt}
    RETURN    ${overview_dt}
