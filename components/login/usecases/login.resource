*** Settings ***
Variables       ../pages/LoginPage.py
Variables       ${EXECDIR}/shared/pages/HomePage.py
Variables       ${EXECDIR}/support/reporters/entry_status.py
Resource        ${EXECDIR}/shared/actions/BrowserActions.resource
Library         ${EXECDIR}/support/reporters/ReporterWriter.py


*** Keywords ***
Login
    [Arguments]    ${data_set}    ${reporters}
    Open The Browser    ${data_set}[BROWSER]
    Maximize The Browser Window
    Go To Page    ${data_set}[URL]

    Wait For Element To Be Visible    ${LoginPage.USERNAME}
    Enter Text    ${LoginPage.USERNAME}    ${data_set}[USERNAME]
    Enter Password    ${LoginPage.PASSWORD}    ${data_set}[PASSWORD]
    Add Entry To Report    Credentials    ${EntryStatus.INFO}    ${reporters}

    Click On    ${LoginPage.LOGIN_BUTTON}
    Wait For Element To Be Visible    ${HomePage.LEFT_MENU}    timeout=10s

    ${is_home_page_visible}    Run Keyword And Return Status
    ...    Page Should Include    Welcome John Smith

    IF  ${is_home_page_visible}
        Add Entry To Report    Login has been completed successfully    ${EntryStatus.PASS}    ${reporters}
    ELSE
        Add Entry To Report    Login has been failed    ${EntryStatus.FAIL}    ${reporters}
        Fatal Error    Login has been failed
    END
