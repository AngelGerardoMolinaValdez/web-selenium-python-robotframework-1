*** Settings ***
Keyword Tags    bill_payment-keywords

Resource    ../pages/bill_payment_page.resource
Resource    ../keywords/common_keywords.resource


*** Keywords ***
Bill Payment
    [Arguments]    ${dt}
    Select Account Service    Bill Pay
    Wait Until Payee Name Is Visible

    Input Payee Name    ${dt.payee_name}
    Input Address    ${dt.address}
    Input City    ${dt.city}
    Input State    ${dt.state}
    Input Zip Code    ${dt.zip_code}
    Input Phone    ${dt.phone}
    Input Account    ${dt.account_payable}
    Input Verify Account    ${dt.account_payable}
    Input Amount    ${dt.amount}
    Select Account    ${dt.account_id}
    Send Payment
    Verify Payment    Bill Payment Complete
    
    RETURN    ${dt}
