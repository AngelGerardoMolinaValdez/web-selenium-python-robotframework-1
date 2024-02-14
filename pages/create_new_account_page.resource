*** Settings ***
Documentation     A representation of a open new account page

Keyword Tags    open-new-account-page

Library    SeleniumLibrary


*** Keywords ***
Select Account Type
    [Arguments]    ${account_type}
    [Tags]    STEP:Se selecciona el tipo de cuenta '${account_type}'
    Select From List By Label    id=type    ${account_type}

Select Account Owner
    [Arguments]    ${account_owner}
    [Tags]    STEP:Se selecciona el propietario de la cuenta '${account_owner}'
    Select From List By Label    id=fromAccountId    ${account_owner}

Click Open Account
    [Tags]    STEP:Se hace clic en el botón 'Open New Account'
    Click Element    css:input[value="Open New Account"]

Verify Account Opened And Get Account Id
    [Tags]    STEP:Se verifica que la cuenta se abrió y se obtiene el id de la cuenta
    Page Should Contain    Congratulations, your account is now open.
    ${account_id}=    Get Text    id=newAccountId
    RETURN    ${account_id}
