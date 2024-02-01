*** Settings ***
Documentation     Workflow for the user to create a new account and transfer money

Keyword Tags     workflow

Resource    ../keywords/create_new_account_keywords.resource
Resource    ../keywords/transfer_funds_keywords.resource


*** Keywords ***
Create New Account And Transfer Money
    @{accounts}    Open New Account In The Application
    Transfer Funds In The Application    ${accounts}[0]    ${accounts}[1]    1000

