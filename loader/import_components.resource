*** Settings ***
Documentation
...    Se colocan las librerias y archivos que seran utilizados en el proyecto.

Library    SeleniumLibrary    run_on_failure=${None}
Library    Collections	
Library    DateTime	
Library    Dialogs	
Library    OperatingSystem	
Library    Process	
Library    String

Resource    ../resources/login.resource
Resource    ../resources/cuentas.resource
Resource    ../resources/util.resource
