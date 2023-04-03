*** Settings ***
Documentation
...    Keywords de utilidad

Keyword Tags
...    util
...    reusable

Resource    ../loader/libraries.resource


*** Keywords ***
Wait Until Select Has Number Options
    [Arguments]    ${select}    ${num_opciones}    ${intentos_maximos}=${60}
    
    ${select_opciones}=    Set Variable    ${select}//option
    ${contador}=    Set Variable    ${0}
    
    WHILE  ${True}
        Sleep    ${1} secondS
        ${contador}=    Evaluate    ${contador}+${1}
        ${total_opciones}=    Get Element Count    ${select_opciones}
        IF    ${total_opciones} >= ${num_opciones}    BREAK
        IF    ${contador} == ${intentos_maximos}    BREAK
    END
