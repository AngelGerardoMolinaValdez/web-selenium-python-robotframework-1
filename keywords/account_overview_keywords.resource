*** Settings ***
Documentation    A keywords from account overview

Keyword Tags    account-overview-keywords

Library    ../libraries/DataTableLibrary.py

Resource    ../keywords/common_keywords.resource
Resource    ../pages/account_overview_page.resource


*** Keywords ***
Get Account Overview
    [Arguments]    ${data_table}
    Select Account Service    Accounts Overview

    Click In Account In The Account Table    ${data_table.account_id}
    Verify Account Overview Page Is Open

    ${balance}=    Get Balance
    ${available}=    Get Available Balance

    ${dt}    Update Data Table    ${data_table}    balance=${balance}    available=${available}
    RETURN    ${dt}
