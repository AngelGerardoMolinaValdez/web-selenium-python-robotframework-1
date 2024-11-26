*** Settings ***
Resource    ${EXECDIR}/components/login/usecases/login.resource
Variables    ${EXECDIR}/infraestructure/config/vars/auth.py
Library    ${EXECDIR}/support/reporters/PdfReporterManager.py

Suite Setup    Login Setup
Suite Teardown    Execution TearDown


*** Keywords ***
Login Setup
    ${reporter}    Create Reporter    report_name=Login    tags=["login"]
    VAR    ${LOGIN_REPORTER}    ${reporter}    scope=GLOBAL
    Login    ${USER_AUTH}    ${LOGIN_REPORTER}

Execution TearDown
    Clear Images Folder
