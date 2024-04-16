*** Settings ***
Documentation    A resource file with reusable keywords from find transaction

Keyword Tags    find_transaction-keywords

Library    DateTime
Library    ${EXECDIR}/libraries/DataTableLibrary.py

Resource    ./common_keywords.resource
Resource    ${EXECDIR}/pages/find_transaction_page.resource


*** Keywords ***
Find Transaction
    [Arguments]    ${dt}
    Select Account Service    Find Transactions
    Wait Until Select Account To Search Transaction Is Enabled

    Select Account To Search Transaction    ${dt.account_id}
    ${find_transaction_dt}    Run Keyword    Find Transaction By ${dt.type_search}    ${dt}

    Wait Until Transaction Table Is Visible
    Transaction Table Should Have Transactions
    RETURN    ${find_transaction_dt}

Find Transaction By Id    # robotcode: ignore
    [Tags]    robot:private
    [Arguments]    ${dt}
    Input Transaction Id    ${dt.transaction_id}
    Click In To Search Transaction By Id
    RETURN    ${dt}

Find Transaction By Date    # robotcode: ignore
    [Tags]    robot:private
    [Arguments]    ${dt}
    Input Transaction Date    ${dt.transaction_date}
    Click In To Search Transaction By Date
    RETURN    ${dt}

Find Transaction By Date Range    # robotcode: ignore
    [Tags]    robot:private
    [Arguments]    ${dt}
    ${start_date}=    Convert Date    ${dt.transaction_date}    date_format=%m-%d-%Y    result_format=%Y-%m-%d
    ${end_date}=    Add Time To Date    ${start_date}    1 day    result_format=%m-%d-%Y
    ${dt_with_dates}    Update Data Table    ${dt}    start_date=${dt.transaction_date}    end_date=${end_date}

    Input Transaction From Date    ${dt_with_dates.start_date}
    Input Transaction To Date    ${dt_with_dates.end_date}
    Click In To Search Transaction By Date Range
    RETURN    ${dt_with_dates}

Find Transaction By Amount    # robotcode: ignore
    [Tags]    robot:private
    [Arguments]    ${dt}
    Input Transaction Amount    ${dt.transaction_amount}
    Click In To Search Transaction By Amount
    RETURN    ${dt}
