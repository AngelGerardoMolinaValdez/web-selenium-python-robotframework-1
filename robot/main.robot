*** Settings ***
Documentation
...    Demo de casos de prueba automatizados con fines demostrativos
...    el sitio probado es una demo web que permite practicar la automatizacion
...    web. Este sitio web no almacena datos, esto significa que al cerrar el navegador
...    donde se pruebe se borraran los movimientos.

Metadata    robot     6.0.1
Metadata    python    3.9.0
Metadata    chrome    108

Test Tags
...    demo
...    parabank

Resource    ../loader/import_components.resource

Suite Setup    Set Selenium Timeout    2 minutes
Test Setup    Set Selenium Speed    0.5

*** Test Cases ***
Abrir Nueva Cuenta Tipo SAVINGS
    [Documentation]
	...    Inicia sesion en parabank y crea una nueva cuenta con los datos
	...    proporcionados y guarda la informacion de la nueva cuenta.
	[Tags]
	...    nueva_cuenta
	[Setup]    Iniciar Sesion En ParaBank

	Crear Nueva Cuenta En ParaBank    SAVINGS    13344

	[Teardown]    Close Browser


Abrir Nueva Cuenta Tipo CHECKING
    [Documentation]
	...    Inicia sesion en parabank y crea una nueva cuenta con los datos
	...    proporcionados y guarda la informacion de la nueva cuenta.
	[Tags]
	...    nueva_cuenta
	[Setup]    Iniciar Sesion En ParaBank

	Crear Nueva Cuenta En ParaBank    CHECKING    13344

	[Teardown]    Close Browser


Obtener Resumen De Cuentas
    [Documentation]
	...    Obtiene todas las cuentas en Parabank
	[Tags]
	...    obtener_cuentas
	[Setup]    Iniciar Sesion En ParaBank

    Obtener Resumen De Cuentas En Parabank

	[Teardown]    Close Browser