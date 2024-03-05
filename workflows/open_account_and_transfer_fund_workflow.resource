*** Settings ***
Documentation     Workflow for the user to create a new account and transfer money

Keyword Tags     workflow

Resource    ../keywords/create_new_account_keywords.resource
Resource    ../keywords/transfer_funds_keywords.resource


*** Keywords ***
Create Two New Accounts And Transfer Money    # robotcode: ignore
    [Tags]    REPORT:LOG    STEP:Se crearan dos cuentas y se transferira dinero entre ellas
    [Arguments]    ${data_table}
    ${new_account_1}    Open New Account In The Application    ${data_table}
    ${new_account_2}    Open New Account In The Application    ${data_table}

    Transfer Funds In The Application    ${new_account_1}    ${new_account_2}    1

