*** Settings ***
Documentation    A keywords from transfer funds page object

Keyword Tags    transfer-funds-keywords

Resource    ../keywords/common_keywords.resource
Resource    ../pages/transfer_funds_page.resource


*** Keywords ***
Transfer Funds
    [Arguments]    ${data_table}
    Select Account Service    Transfer Funds

    Input Amount    ${data_table.amount}
    Select From Account   ${data_table.from_account}
    Select To Account    ${data_table.to_account}
    Click Transfer Button
    
    ${amount_is_numeric}    Run Keyword And Return Status    
    ...    Should Match Regexp    ${data_table.amount}    ^-?\\d+$    flags=MULTILINE

    IF    ${amount_is_numeric}
        Verify Transfer Success
    ELSE
        Verify Transfer Failure
    END

    RETURN    ${data_table}