*** Settings ***
Variables       ../pages/OpenNewAccountPage.py
Variables       ../pages/AccountOpenedPage.py
Variables       ${EXECDIR}/shared/pages/HomePage.py
Variables       ${EXECDIR}/support/reporters/entry_status.py
Resource        ${EXECDIR}/shared/actions/BrowserActions.resource
Library         ${EXECDIR}/support/reporters/ReporterWriter.py


*** Keywords ***
Open New Account
    [Arguments]    ${data_set}    ${reporters}
    Add Entry To Report    Option "Open New Account" has been selected    ${EntryStatus.INFO}    ${reporters}
    Click On    ${HomePage.OPEN_NEW_ACCOUNT}

    Wait For Element To Be Visible    ${OpenNewAccountPage.ACCOUNT_TYPE}
    BrowserActions.Select By Visible Text    ${OpenNewAccountPage.ACCOUNT_TYPE}    ${data_set.ACCOUNT_TYPE}
    BrowserActions.Select By Visible Text    ${OpenNewAccountPage.ACCOUNT_REFERENCE}    ${data_set.ACCOUNT_REFERENCE}
    Add Entry To Report    Account type and reference have been selected    ${EntryStatus.INFO}    ${reporters}
    Click On    ${OpenNewAccountPage.OPEN_NEW_ACCOUNT}

    BrowserActions.Wait For Text To Be Visible    ${AccountOpenedPage.OPEN_ACCOUNT_RESULT}

    ${did_confirmation_account_open_message_appear}    Run Keyword And Return Status
    ...    Page Should Include    Congratulations, your account is now open.

    IF  ${did_confirmation_account_open_message_appear}
        ${account_number}    Get Text From    ${AccountOpenedPage.ACCOUNT_NUMBER}
        Add Entry To Report    Account ${account_number} has been opened    ${EntryStatus.PASS}    ${reporters}
        RETURN    ${account_number}
    ELSE
        Add Entry To Report    Account has not been opened    ${EntryStatus.FAIL}    ${reporters}
        Fail    Account has not been opened
    END
