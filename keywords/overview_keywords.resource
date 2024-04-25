*** Settings ***
Documentation    A keywords from account overview

Keyword Tags    account-overview-keywords

Library    ../libraries/standard/DataTableLibrary.py

Resource    ../keywords/common_keywords.resource
Resource    ../pages/account_overview_page.resource


*** Keywords ***
Account Overview
    [Arguments]    ${data_table}
    Select Account Service    Accounts Overview

    Click In Account In The Account Table    ${data_table.account_id}
    Verify Account Overview Page Is Open

    ${balance}=    Get Balance
    ${available}=    Get Available Balance

    ${dt}    Update Data Table    ${data_table}    balance=${balance}    available=${available}
    RETURN    ${dt}

Save Last Account Transaction Overview
    [Arguments]    ${dt}
    Select Account Service    Accounts Overview

    Click In Account In The Account Table    ${dt.account_id}
    Verify Account Overview Page Is Open

    @{last_transaction}=    Get WebElements    //table[@id="transactionTable"]/tbody/tr[last()]//*[text()]

    ${date}    Get Text    ${last_transaction[0]}
    ${description}    Get Text    ${last_transaction[1]}
    ${href_description}    Get Element Attribute    ${last_transaction[1]}    href
    ${match}    Evaluate    re.search(r'(transaction.htm\\?id=)(\\d+)', '${href_description}')    modules=re
    VAR    ${id}    ${match.group(2)}
    ${ng_if_amount}    Get Element Attribute    ${last_transaction[2]}    ng-if
    ${type}    Evaluate    re.search(r"==\\s*'(\\w*)'", """${ng_if_amount}""").group(1)    modules=re
    ${amount_text}    Get Text    ${last_transaction[2]}
    ${amount_number}    Evaluate    re.search(r'\\$([0-9]+)\\.\\d+', '${amount_text}')    modules=re
    VAR    ${amount}    ${amount_number.group(1)}

    ${last_transaction_details}    Update Data Table    ${dt}
    ...    transaction_date=${date}    transaction_desc=${description}
    ...    transaction_id=${id}    transaction_type=${type}    transaction_amount=${amount}

    RETURN    ${last_transaction_details}
