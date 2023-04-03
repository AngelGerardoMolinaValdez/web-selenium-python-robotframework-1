*** Settings ***
Documentation
...    Librerias principales de Robot Framework

Library    SeleniumLibrary    run_on_failure=${None}    timeout=10 minutes
Library    Collections
Library    DateTime
Library    Dialogs
Library    OperatingSystem
Library    Process
Library    String
