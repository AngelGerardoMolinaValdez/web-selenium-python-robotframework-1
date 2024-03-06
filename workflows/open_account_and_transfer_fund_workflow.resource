*** Settings ***
Documentation     Workflow for the user to create a new account and transfer money

Keyword Tags     workflow

Resource    ../keywords/create_new_account_keywords.resource
Resource    ../keywords/transfer_funds_keywords.resource


*** Keywords ***
Create Two New Accounts And Transfer Money    # robotcode: ignore
    [Tags]    REPORT:LOG    STEP:Se crearan dos cuentas y se transferira dinero entre ellas
    [Arguments]    ${data_table}
    ${new_account_1_dt}    Open New Account In The Application    ${data_table}
    ${new_account_2_dt}    Open New Account In The Application    ${data_table}
    
    ${dt}    Update Data Table
    ...    ${data_table}
    ...    from_account=${new_account_1_dt.account_id}
    ...    to_account=${new_account_2_dt.account_id}
    ...    amount=100
    Transfer Funds In The Application    ${dt}

    RETURN    ${dt}
