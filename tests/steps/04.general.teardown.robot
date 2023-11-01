*** Settings ***
Documentation
...    realiza un teardown despues de ejecutar todos los steps

Library    ../../libraries/DataTableLibrary.py

Suite Teardown    Guardar Datos De Ejecucion    ${ITERATION}


*** Test Cases ***
Teardown general
    [Tags]    general
    No Operation
