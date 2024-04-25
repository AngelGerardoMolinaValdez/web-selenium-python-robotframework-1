*** Settings ***
Keyword Tags    steps

Resource    ${EXECDIR}/config/global/dependencies/pages.resource


*** Keywords ***
Wait Until Input Loan Amount Is Visible
    Wait Until Element Is Visible    id:amount

Input Loan Amount
    [Arguments]    ${amount}
    Highlight Element Persistent    id:amount
    Input Text    id:amount    ${amount}

Input Down Payment
    [Arguments]    ${payment}
    Highlight Element Persistent    id:downPayment
    Input Text    id:downPayment    ${payment}

Select From Account
    [Arguments]    ${account}
    Highlight Element Persistent    id:fromAccountId
    Select From List By Label    id:fromAccountId    ${account}

Click Into Apply Now
    Highlight Element Persistent    css:input[value\="Apply Now"]
    Add Step Capture    Solicitud de préstamo    INFO
    Click Element    css:input[value="Apply Now"]

Wait Until Loan Application Is Submitted
    Wait Until Page Contains Element    xpath://h1[contains(text(), "Loan Request Processed")]

New Account With Loan Is Created
    Element Should Be Visible    id:newAccountId
    Highlight Element Persistent    id:newAccountId
    ${new_account_id}=    Get Text    id:newAccountId
    Add Step Capture   Cuenta creada con préstamo exitosamente: ${new_account_id}    PASS
    RETURN    ${new_account_id}
