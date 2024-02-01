*** Settings ***
Documentation     A representation of a account overview in the application

Keyword Tags    account-overview-page

Library    SeleniumLibrary


*** Keywords ***
Click In Account In The Account Table
    [Arguments]    ${account}
    Click Link    ${account}

Verify Account Overview Page Is Open
    Wait Until Page Contains Element    css:h1.title
    Page Should Contain Element    css:td#accountId
