*** Settings ***
Keyword Tags    workflow

Resource    ./overview_workflows.resource
Resource    ${EXECDIR}/keywords/find_transaction_keywords.resource


*** Keywords ***
Find Transaction Of A Transfer Funds From New Account    # robotcode: ignore
    [Arguments]    ${dt}
    ${overview_dt}    Create New Account Then Transfer Funds From Existing Account And Save Overview    ${dt}
    Find Transaction    ${overview_dt}
    RETURN    ${overview_dt}
