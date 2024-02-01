*** Settings ***
Documentation    A keywords from account overview

Keyword Tags    account-overview-keywords

Resource    ../pages/account_overview_page.resource


*** Keywords ***
Get Account Overview
    [Arguments]    ${account}
    Click In Account In The Account Table    ${account}
    Verify Account Overview Page Is Open