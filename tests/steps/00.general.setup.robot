*** Settings ***
Library    ../../libraries/DataTableLibrary.py

Suite Setup    Crear configuracion de inicio


*** Keywords ***
Crear configuracion de inicio
    ${DATATABLE}    Crear DataTable    test_data.csv    ${ITERATION}
    Set Global Variable    ${DATATABLE}


*** Test Cases ***
Setup general
    [Tags]    general
    No Operation
