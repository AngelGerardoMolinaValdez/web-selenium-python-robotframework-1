*** Settings ***
Documentation     A representation of a account overview in the application

Keyword Tags    account-overview-page

Resource    ${EXECDIR}/config/Libraries.resource


*** Keywords ***
Click In Account In The Account Table
    [Arguments]    ${account}
    Log    STEP:IMAGE:Seleccione la cuenta en la tabla de cuentas "${account}"
    Click Link    ${account}

Verify Account Overview Page Is Open
    Wait Until Page Contains Element    css:h1.title
    Page Should Contain Element    css:td#accountId

Get Balance
    ${balance}    Get Text    css:td#balance
    Log    ${balance}
    RETURN    ${balance}

Get Available Balance
    ${availableBalance}    Get Text    css:td#availableBalance
    Log    ${availableBalance}
    RETURN    ${availableBalance}
