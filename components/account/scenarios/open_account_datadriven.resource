*** Settings ***
Resource    ../usecases/open_new_account.resource
Library    ${EXECDIR}/support/datasets/reader/CSVDataSetReader.py
Variables    ../shared/paths.py


*** Keywords ***
Open Account
    [Arguments]    ${config}    ${reporters}
    ${data_set}    Read Data Set    ${OPEN_NEW_ACCOUNT_DATA_PATH}    ${config}[ACCOUNT_DATA_SET_INDEX]

    Open New Account    ${data_set}    ${reporters}

    ReporterWriter.Set Reporter Status
    ReporterWriter.Set Reporter Message