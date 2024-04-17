*** Settings ***
Keyword Tags    steps

Resource    ${EXECDIR}/config/global/dependencies/pages.resource


*** Keywords ***
Wait Until Input Loan Amount Is Visible
    Wait Until Element Is Visible    id:amount

Input Loan Amount
    [Arguments]    ${amount}
    Highlight Element Async    id:amount
    Input Text    id:amount    ${amount}

Input Down Payment
    [Arguments]    ${payment}
    Highlight Element Async    id:downPayment
    Input Text    id:downPayment    ${payment}

Select From Account
    [Arguments]    ${account}
    Highlight Element Async    id:fromAccountId
    Select From List By Label    id:fromAccountId    ${account}

Click Into Apply Now
    Highlight Element Async    css:input[value\="Apply Now"]
    Capture Page Screenshot
    Log    STEP:CAPTURE:Solicitud de préstamo
    Click Element    css:input[value="Apply Now"]

Wait Until Loan Application Is Submitted
    Wait Until Page Contains Element    xpath://h1[contains(text(), "Loan Request Processed")]

New Account With Loan Is Created
    Element Should Be Visible    id:newAccountId
    Highlight Element Async    id:newAccountId
    ${new_account_id}=    Get Text    id:newAccountId
    Capture Page Screenshot
    Log    STEP:CAPTURE:Cuenta creada con préstamo exitosamente: ${new_account_id}
    RETURN    ${new_account_id}
