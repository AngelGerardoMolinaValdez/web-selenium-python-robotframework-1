*** Settings ***
Library           SeleniumLibrary    run_on_failure=${None}    timeout=60


*** Keywords ***
Open The Browser
    [Tags]    wrapper
    [Arguments]    ${browser}    &{options}
    Open Browser    browser=${browser}    &{options}

Maximize The Browser Window
    [Tags]    wrapper
    Maximize Browser Window

Go To Page
    [Tags]    wrapper
    [Arguments]    ${url}
    Go To    ${url}

Go Back To Previous Page
    [Tags]    wrapper
    Go Back

Click On
    [Tags]    wrapper
    [Arguments]    ${element}
    Click Element    ${element}

Enter Text
    [Tags]    wrapper
    [Arguments]    ${element}    ${text}
    Input Text    ${element}    ${text}

Enter Password
    [Tags]    wrapper
    [Arguments]    ${element}    ${text}
    Input Password    ${element}    ${text}

Get Text From
    [Tags]    wrapper
    [Arguments]    ${element}
    ${text}=    Get Text    ${element}
    RETURN    ${text}

Select By Visible Text
    [Tags]    wrapper
    [Arguments]    ${element}    ${text}
    Select From List By Label    ${element}    ${text}

Wait For Element To Be Visible
    [Tags]    wrapper
    [Arguments]    ${element}    ${timeout}=${None}
    Wait Until Element Is Visible    ${element}    ${timeout}

Page Should Include
    [Tags]    wrapper
    [Arguments]    ${text}
    Page Should Contain    ${text}

Wait For Text To Be Visible
    [Tags]    wrapper
    [Arguments]    ${text}    ${timeout}=${None}
    Wait Until Page Contains    ${text}    ${timeout}
