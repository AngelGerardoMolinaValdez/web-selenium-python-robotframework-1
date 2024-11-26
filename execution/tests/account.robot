*** Settings ***
Library    ${EXECDIR}/support/reporters/PdfReporterManager.py
Variables    ${EXECDIR}/infraestructure/config/tests/account.py
Resource    ${EXECDIR}/components/account/scenarios/open_account.resource

Test Template    Account Scenario Setup


*** Variables ***
${LOGIN_REPORTER}    ${None}


*** Test Cases ***
Test 001 New Account Checking    ${ACCOUNT_CHECKING_CFG}
Test 002 New Account Savings    ${ACCOUNT_SAVINGS_CFG}


*** Keywords ***
Account Scenario Setup
    [Arguments]    ${config}
    ${reporter}    Create Reporter    report_name=${TEST_NAME}

    Open Account    ${config}    ${reporter}

    Generate Report    ${EXECDIR}/output/reports    ${TEST_NAME}    PASS    OK    [${LOGIN_REPORTER}, ${reporter}]
