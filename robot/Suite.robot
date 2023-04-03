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

Resource    ../loader/libraries.resource
Resource    ../loader/util.resource
Resource    ../loader/entry_points.resource


*** Variables ***
${URL}    https://parabank.parasoft.com/parabank/index.htm
${USERNAME}    john
${PASSWORD}    demo


*** Test Cases ***
Test Abrir Nueva Cuenta Tipo SAVINGS
    [Documentation]
	...    Inicia sesion en parabank y crea una nueva cuenta con los datos
	...    proporcionados y guarda la informacion de la nueva cuenta.
	[Tags]
	...    nueva_cuenta
	[Setup]    Iniciar Sesion    ${URL}    ${USERNAME}    ${PASSWORD}
	Crear Nueva Cuenta En ParaBank    SAVINGS    13344
	[Teardown]    Terminar Sesion

Test Abrir Nueva Cuenta Tipo CHECKING
    [Documentation]
	...    Inicia sesion en parabank y crea una nueva cuenta con los datos
	...    proporcionados y guarda la informacion de la nueva cuenta.
	[Tags]
	...    nueva_cuenta
	[Setup]    Iniciar Sesion    ${URL}    ${USERNAME}    ${PASSWORD}
	Crear Nueva Cuenta En ParaBank    CHECKING    13233
	[Teardown]    Terminar Sesion

Abrir Cuentas De Todo Tipo
    [Documentation]
	...    Inicia sesion en parabank y crea una nueva cuenta con los datos
	...    proporcionados y guarda la informacion de la nueva cuenta.
	...    En este caso de prueba se dan de alta 2 cuentas con diferentes Tipos
	...    de apertura
	[Tags]
	...    nueva_cuenta
	[Setup]    Iniciar Sesion    ${URL}    ${USERNAME}    ${PASSWORD}
	[Template]    Crear Nueva Cuenta En ParaBank
	CHECKING    13344
	SAVINGS    13344
	[Teardown]    Terminar Sesion

Test Obtener Resumen De Cuentas
    [Documentation]
	...    Obtiene todas las cuentas en Parabank
	[Tags]
	...    obtener_cuentas
	[Setup]    Iniciar Sesion    ${URL}    ${USERNAME}    ${PASSWORD}
    Obtener Resumen De Cuentas En Parabank
	[Teardown]    Terminar Sesion
