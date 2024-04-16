*** Settings ***
Documentation     A representation of a find transaction page

Keyword Tags    find-transaction-page

Resource    ${EXECDIR}/config/global/dependencies/pages.resource


*** Keywords ***
Wait Until Select Account To Search Transaction Is Enabled
    Wait Until Element Is Visible    id:accountId

Select Account To Search Transaction
    [Arguments]    ${account}
    Highlight Element Async    id:accountId
    Select From List By Label    id:accountId    ${account}

Input Transaction Id
    [Arguments]    ${transaction_id}
    Highlight Element Async    id:criteria.transactionId
    Input Text    id:criteria.transactionId    ${transaction_id}

Click In To Search Transaction By Id
    Highlight Element Async    css:button[ng-click="criteria.searchType = 'ID'"]
    Capture Page Screenshot
    Log    STEP:CAPTURE:Busqueda por ID
    Click Button    css:button[ng-click="criteria.searchType = 'ID'"]

Input Transaction Date
    [Arguments]    ${transaction_date}
    Highlight Element Async    id:criteria.onDate
    Input Text    id:criteria.onDate    ${transaction_date}

Click In To Search Transaction By Date
    Highlight Element Async    css:button[ng-click="criteria.searchType = 'DATE'"]
    Capture Page Screenshot
    Log    STEP:CAPTURE:Busqueda por Fecha
    Click Button    css:button[ng-click="criteria.searchType = 'DATE'"]

Input Transaction From Date
    [Arguments]    ${from_date}
    Highlight Element Async    id:criteria.fromDate
    Input Text    id:criteria.fromDate    ${from_date}

Input Transaction To Date
    [Arguments]    ${to_date}
    Highlight Element Async    id:criteria.toDate
    Input Text    id:criteria.toDate    ${to_date}

Click In To Search Transaction By Date Range
    Highlight Element Async    css:button[ng-click="criteria.searchType = 'DATE_RANGE'"]
    Capture Page Screenshot
    Log    STEP:CAPTURE:Busqueda por Rango de Fecha
    Click Button    css:button[ng-click="criteria.searchType = 'DATE_RANGE'"]

Input Transaction Amount
    [Arguments]    ${amount}
    Highlight Element Async    id:criteria.amount
    Input Text    id:criteria.amount    ${amount}

Click In To Search Transaction By Amount
    Highlight Element Async    css:button[ng-click="criteria.searchType = 'AMOUNT'"]
    Capture Page Screenshot
    Log    STEP:CAPTURE:Busqueda por Monto
    Click Button    css:button[ng-click="criteria.searchType = 'AMOUNT'"]

Wait Until Transaction Table Is Visible
    Wait Until Element Is Visible    id:transactionTable
    Highlight Element Async    id:transactionTable
    Capture Page Screenshot
    Log    STEP:CAPTURE:Tabla de Transacciones

Transaction Table Should Have Transactions
    ${total_trs}    Get Element Count    id:transactionTable >> tag:tbody >> tag:tr
    Should Be True    ${total_trs} > 0    No transactions found
