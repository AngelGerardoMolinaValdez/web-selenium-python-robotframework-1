*** Settings ***
Documentation     A representation of a open new account page

Keyword Tags    open-new-account-page

Library    SeleniumLibrary


*** Keywords ***
Select Account Type
    [Arguments]    ${account_type}
    Select From List By Label    id=type    ${account_type}

Select Account Owner
    [Arguments]    ${account_owner}
    Select From List By Label    id=fromAccountId    ${account_owner}

Click Open Account
    Click Element    css:input[value="Open New Account"]

Verify Account Opened And Get Account Id
    Page Should Contain    Congratulations, your account is now open.
    ${account_id}=    Get Text    id=newAccountId
    RETURN    ${account_id}
