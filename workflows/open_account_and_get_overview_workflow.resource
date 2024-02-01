*** Settings ***
Documentation     Workflow for the user to create a new account and transfer money

Keyword Tags     workflow

Resource    ../keywords/create_new_account_keywords.resource
Resource    ../keywords/account_overview_keywords.resource


*** Keywords ***
Create New Account And Get Account Overview
    @{accounts}    Open New Account In The Application

    FOR  ${account}  IN  @{accounts}
        Get Account Overview    ${account}
    END
