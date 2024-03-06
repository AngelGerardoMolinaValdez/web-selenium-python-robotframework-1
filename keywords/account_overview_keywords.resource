*** Settings ***
Documentation    A keywords from account overview

Keyword Tags    account-overview-keywords

Resource    ../keywords/common_keywords.resource
Resource    ../pages/account_overview_page.resource


*** Keywords ***
Get Account Overview
    [Arguments]    ${account}
    Select Account Service    Accounts Overview

    Click In Account In The Account Table    ${account}
    Verify Account Overview Page Is Open
