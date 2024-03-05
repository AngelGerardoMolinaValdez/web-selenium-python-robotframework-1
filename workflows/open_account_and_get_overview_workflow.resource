*** Settings ***
Documentation     Workflow for the user to create a new account and transfer money

Keyword Tags     workflow

Resource    ../keywords/create_new_account_keywords.resource
Resource    ../keywords/account_overview_keywords.resource


*** Keywords ***
Create New Account And Get Account Overview    # robotcode: ignore
    [Tags]    REPORT:LOG    STEP:Se creara una nueva cuenta y se obtendra una vista general de la cuenta
    [Arguments]    ${data_table}
    ${account}    Open New Account In The Application    ${data_table}

    Get Account Overview    ${account}
