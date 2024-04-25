*** Settings ***
Documentation     A representation of a open new account page

Keyword Tags    open-new-account-page

Resource    ${EXECDIR}/config/global/dependencies/pages.resource


*** Keywords ***
Select Account Type
    [Arguments]    ${account_type}
    [Tags]    STEP:Se selecciona el tipo de cuenta '${account_type}'
    Highlight Element Persistent    id\=type
    Select From List By Label    id=type    ${account_type}

Select Account Owner
    [Arguments]    ${account_owner}
    [Tags]    STEP:Se selecciona el propietario de la cuenta '${account_owner}'
    Highlight Element Persistent    id\=fromAccountId
    Select From List By Label    id=fromAccountId    ${account_owner}

Click Open Account
    Highlight Element Persistent    css:input[value\="Open New Account"]
    Add Step Capture    Datos de la cuenta    INFO
    Click Element    css:input[value="Open New Account"]

Verify Account Opened And Get Account Id
    Page Should Contain    Congratulations, your account is now open.
    ${account_id}=    Get Text    id=newAccountId
    Highlight Element Persistent    id\=newAccountId
    Add Step Capture    Se obtiene el id de la cuenta '${account_id}'    PASS
    Remove All Highlights
    RETURN    ${account_id}
