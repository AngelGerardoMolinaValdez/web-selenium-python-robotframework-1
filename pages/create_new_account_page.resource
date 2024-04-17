*** Settings ***
Documentation     A representation of a open new account page

Keyword Tags    open-new-account-page

Resource    ${EXECDIR}/config/global/dependencies/pages.resource


*** Keywords ***
Select Account Type
    [Arguments]    ${account_type}
    [Tags]    STEP:Se selecciona el tipo de cuenta '${account_type}'
    Highlight Element Async    id\=type
    Select From List By Label    id=type    ${account_type}

Select Account Owner
    [Arguments]    ${account_owner}
    [Tags]    STEP:Se selecciona el propietario de la cuenta '${account_owner}'
    Highlight Element Async    id\=fromAccountId
    Select From List By Label    id=fromAccountId    ${account_owner}

Click Open Account
    Highlight Element Async    css:input[value\="Open New Account"]
    Log    STEP:IMAGE:Datos de la cuenta ingresados, se procede a abrir la cuenta.
    Click Element    css:input[value="Open New Account"]

Verify Account Opened And Get Account Id
    Page Should Contain    Congratulations, your account is now open.
    ${account_id}=    Get Text    id=newAccountId
    Highlight Element Async    id\=newAccountId
    Log    STEP:IMAGE:Se obtiene el id de la cuenta '${account_id}':PASS
    RETURN    ${account_id}
